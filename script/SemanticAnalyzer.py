# coding: utf8
"""
Семантический анализатор
"""

from PropositionTreeNode import PropositionTreeNode
from PropositionTreeNodeType import PropositionTreeNodeType
from PropositionTreeNodeSide import PropositionTreeNodeSide
from TreeNodeConcept import TreeNodeConcept
from DatabaseConcept import DatabaseConcept
from DatabaseTriad import DatabaseTriad
from DatabaseSequence import DatabaseSequence
from DatabaseList import DatabaseList
from TreeNodeConceptType import TreeNodeConceptType
from CodeStack import CodeStack
from CodeLine import CodeLine
from ErrorHelper import ErrorHelper
from LanguageHelper import LanguageHelper
from MemoryProvider import MemoryProvider
from ContextProvider import ContextProvider
from EventProvider import EventProvider
from Event import Event
from EventType import EventType

class SemanticAnalyzer ():

    def __init__ (self, cursor):
        self.result = ""
        self.__cursor = cursor
        self.__error_text = ""
        LanguageHelper (self.__cursor, "RU")

    def analize (self, tree, code_line):
        self.result = ""
        self.__error_text = ""
        self.proposition_tree = tree
        is_new = False
        #print "<SemanticAnalyzer>"
        if code_line != None:
            if code_line.concept_id != 0:
                database_list = DatabaseList.read (self.__cursor, code_line.concept_id, code_line.id)
                if database_list != None:
                    code_line = CodeLine ()
                    code_line.id = database_list.id
                    code_line.concept_id = database_list.concept_id
                    code_line.prev_line_id = database_list.prev_line_id
                    code_line.text = database_list.text
                    CodeStack.push (code_line)
                    #print database_list.text

        if self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-create"):
            is_new = True
        # Раскрытие вложенных суждений
        node = self.proposition_tree.root_node
        node.child_index = 0
        side = None
        k = 0
        while node != None:
            if node.child_index == 0:
                if node.type == PropositionTreeNodeType.concept:
                    if node.concept.subroot == True:
                        child = self.__replace_subtree (node, side, is_new)
                        if child != None:
                            parent.children[0] = child
                else:
                    side = node.side
            if node.child_index < len (node.children):
                idx = node.child_index
                node.child_index += 1
                self.proposition_tree.push_node (node)
                parent = node
                node = node.children[idx]
                node.child_index = 0
                k += 1
            else:
                node = self.proposition_tree.pop_node ()
                k -= 1

        actor, actant = self.__get_actor_and_actant (self.proposition_tree.root_node)
        if actor == None:
            return False

        if self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-execute"):
            if actor.concept.name == LanguageHelper.translate ("you"):
                database_concept = DatabaseConcept.read_by_name (self.__cursor, LanguageHelper.translate ("to-be"))
                if database_concept == None:
                    self.__error_text = ErrorHelper.get_text (106)
                    return False
                database_triad = DatabaseTriad.read (self.__cursor, actant.concept.id, 0, database_concept.id)
                if database_triad == None:
                    self.__error_text = ErrorHelper.get_text (106)
                    return None
                query = "SELECT right_triad_id FROM qsl_sequence WHERE left_triad_id = " + str (database_triad.id) + ";"
                self.__cursor.execute (query)
                row = self.__cursor.fetchone ()
                rows = []
                list_concept_id = 0
                while (row != None):
                    rows.append (row[0])
                    row = self.__cursor.fetchone ()
                for row in rows:
                    database_triad = DatabaseTriad.read_by_id (self.__cursor, row)
                    if database_triad == None:
                        continue
                    database_concept = DatabaseConcept.read_by_id (self.__cursor, database_triad.right_concept_id)
                    if database_concept == None:
                        continue
                    if database_concept.type != TreeNodeConceptType.list:
                        continue
                    list_concept_id = database_concept.id
                if list_concept_id == 0:
                    self.__error_text = ErrorHelper.get_text (106)
                    return False
                database_list = DatabaseList.read (self.__cursor, list_concept_id, 0)
                if database_list == None:
                    self.__error_text = ErrorHelper.get_text (106)
                    return False
                code_line = CodeLine ()
                code_line.id = database_list.id
                code_line.concept_id = database_list.concept_id
                code_line.prev_line_id = database_list.prev_line_id
                code_line.text = database_list.text
                CodeStack.push (code_line)
                #print database_list.text
        elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-set"):
            if actor.concept.name == LanguageHelper.translate ("you"):
                if actant.concept.name == LanguageHelper.translate ("value"):
                    field_id = 0
                    field_value = None
                    i = 0
                    while i < len (actant.children):
                        child = actant.children[i]
                        if child.type == PropositionTreeNodeType.linkage:
                            if child.linkage.name == LanguageHelper.translate ("of-what"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.concept:
                                    if child.concept.name == LanguageHelper.translate ("field"):
                                        node = ContextProvider.get_field_node ()
                                        if node != None:
                                            field_id = node.concept.id
                                    else:
                                        field_id = child.concept.id
                            elif child.linkage.name == LanguageHelper.translate ("which"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.number:
                                    field_value = int (child.text)
                        i += 1
                    if field_id != 0 and field_value != None:
                        MemoryProvider.set_field_value (field_id, field_value)
                        event_key = str (field_id)
                        EventProvider.fire_event (event_key)
                elif actant.concept.name == LanguageHelper.translate ("handler"):
                    event_id = 0
                    event_handler = None
                    i = 0
                    while i < len (actant.children):
                        child = actant.children[i]
                        if child.type == PropositionTreeNodeType.linkage:
                            if child.linkage.name == LanguageHelper.translate ("of-what"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.concept:
                                    if child.concept.name == LanguageHelper.translate ("event"):
                                        node = ContextProvider.get_event_node ()
                                        if node != None:
                                            event_id = node.concept.id
                                    else:
                                        field_id = child.concept.id
                            elif child.linkage.name == LanguageHelper.translate ("which"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.string:
                                    event_handler = child.text
                        i += 1
                    if event_id != 0:
                        if event_handler != None:
                            EventProvider.set_event_handler (event_id, event_handler)
        elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-increase"):
            if actor.concept.name == LanguageHelper.translate ("you"):
                if actant.concept.name == LanguageHelper.translate ("value"):
                    field_id = 0
                    i = 0
                    while i < len (actant.children):
                        child = actant.children[i]
                        if child.type == PropositionTreeNodeType.linkage:
                            if child.linkage.name == LanguageHelper.translate ("of-what"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.concept:
                                    if child.concept.name == LanguageHelper.translate ("field"):
                                        node = ContextProvider.get_field_node ()
                                        if node != None:
                                            field_id = node.concept.id
                                    else:
                                        field_id = child.concept.id
                            elif child.linkage.name == LanguageHelper.translate ("which"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.number:
                                    field_value = child.text
                        i += 1
                    field_value = None
                    if field_id != 0:
                        field_value = MemoryProvider.get_field_value (field_id)
                        i = 0
                        while i < len (self.proposition_tree.root_node.children):
                            child = self.proposition_tree.root_node.children[i]
                            if child.type == PropositionTreeNodeType.linkage:
                                if child.linkage.name == LanguageHelper.translate ("on-how-many"):
                                    child = child.children[0]
                                    if child.type == PropositionTreeNodeType.number:
                                        field_value += int (child.text)
                                        MemoryProvider.set_field_value (field_id, field_value)
                            i += 1
        elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-print"):
            if actor.concept.name == LanguageHelper.translate ("you"):
                if actant.concept.name == LanguageHelper.translate ("value"):
                    field_id = 0
                    i = 0
                    while i < len (actant.children):
                        child = actant.children[i]
                        if child.type == PropositionTreeNodeType.linkage:
                            if child.linkage.name == LanguageHelper.translate ("of-what"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.concept:
                                    if child.concept.name == LanguageHelper.translate ("field"):
                                        node = ContextProvider.get_field_node ()
                                        if node != None:
                                            field_id = node.concept.id
                                    else:
                                        field_id = child.concept.id
                                    self.result += str (MemoryProvider.get_field_value (field_id))
                        i += 1
        elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-register"):
            if actor.concept.name == LanguageHelper.translate ("you"):
                if actant.concept.name == LanguageHelper.translate ("event"):
                    field_id = 0
                    event_type = 0
                    i = 0
                    while i < len (actant.children):
                        child = actant.children[i]
                        if child.type == PropositionTreeNodeType.linkage:
                            if child.linkage.name == LanguageHelper.translate ("for-what"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.concept:
                                    if child.concept.name == LanguageHelper.translate ("field"):
                                        node = ContextProvider.get_field_node ()
                                        if node != None:
                                            field_id = node.concept.id
                                    else:
                                        field_id = child.concept.id
                            elif child.linkage.name == LanguageHelper.translate ("on-what"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.concept:
                                    if child.concept.name == LanguageHelper.translate ("change"):
                                        event_type = EventType.on_change
                                    elif child.concept.name == LanguageHelper.translate ("value"):
                                        event_type = EventType.on_value
                        i += 1
                    event_key = None
                    if event_type == EventType.on_change:
                        if field_id != 0:
                            event_key = str (field_id)
                    if event_key != None:
                        node = PropositionTreeNode ()
                        node.type = PropositionTreeNodeType.concept
                        node.side = child.side
                        node.concept = TreeNodeConcept ()
                        node.concept.id = EventProvider.register_event (field_id, event_key)
                        node.concept.type = TreeNodeConceptType.event
                        node.concept.name = "$" + str (node.concept.id)
                        node.text = node.concept.name
                        ContextProvider.set_event_node (node)

        #print "</SemanticAnalyzer>"
        return True

    def get_error_text (self):
        return self.__error_text

    def __get_actor_and_actant (self, root_node):
        idx = 0
        actor = None
        actant = None
        while idx < len (root_node.children):
            child = root_node.children[idx]
            if child.type == PropositionTreeNodeType.linkage:
                if child.linkage.name == LanguageHelper.translate ("who") or child.linkage.name == LanguageHelper.translate ("what"):
                    parent = child
                    child = child.children[0]
                    if child.type == PropositionTreeNodeType.concept:
                        if child.side == PropositionTreeNodeSide.left:
                            actor = child
                            if root_node.concept.subroot != True:
                                ContextProvider.set_actor_node (actor)
                        elif child.side == PropositionTreeNodeSide.right:
                            actant = child
            if actor != None and actant != None:
                break
            idx += 1
        if actor == None:
            actor = ContextProvider.get_actor_node ()
        return actor, actant

    def __replace_subtree (self, root_node, side, is_new):
        actor, actant = self.__get_actor_and_actant (root_node)
        result_node = PropositionTreeNode ()
        result_node.type = PropositionTreeNodeType.concept
        result_node.side = side
        result_node.concept = TreeNodeConcept ()
        is_field = False

        if root_node.concept.name == LanguageHelper.translate ("to-have"):
            if actant.concept.name == LanguageHelper.translate ("name"):
                if actor.concept.name == LanguageHelper.translate ("field"):
                    child1 = actant.children[0]
                    if child1.type == PropositionTreeNodeType.linkage:
                        if child1.linkage.name == LanguageHelper.translate ("which"):
                            child2 = child1.children[0]
                            if child2.type == PropositionTreeNodeType.concept:
                                if is_new == True:
                                    result_node.concept.id = MemoryProvider.create_field (child2.concept.name)
                                    is_field = True
                                    result_node.concept.type = TreeNodeConceptType.field
                                    result_node.concept.name = "$" + str (result_node.concept.id)
                                    result_node.text = result_node.concept.name
                                    ContextProvider.set_field_node (result_node)
                                else:
                                    result_node.concept.id = MemoryProvider.get_field_id (child2.concept.name)
                                    is_field = True
                                    result_node.concept.type = TreeNodeConceptType.field
                                    result_node.concept.name = "$" + str (result_node.concept.id)
                                    result_node.text = result_node.concept.name
                else:
                    child1 = actant.children[0]
                    if child1.type == PropositionTreeNodeType.linkage:
                        if child1.linkage.name == LanguageHelper.translate ("which"):
                            child2 = child1.children[0]
                            if child2.type == PropositionTreeNodeType.concept:
                                database_triad = DatabaseTriad.read (self.__cursor, actant.concept.id, child1.linkage.id, child2.concept.id)
                                if database_triad == None:
                                    self.__error_text = ErrorHelper.get_text (105)
                                    return None
                                database_sequense1 = DatabaseSequence.read (self.__cursor, 0, 0, database_triad.id)
                                if database_sequense1 == None:
                                    self.__error_text = ErrorHelper.get_text (105)
                                    return None
                                database_triad = DatabaseTriad.read_by_id (self.__cursor, database_sequense1.left_triad_id)
                                if database_triad == None:
                                    self.__error_text = ErrorHelper.get_text (105)
                                    return None
                                if database_triad.left_concept_id == root_node.concept.id:
                                    database_sequense2 = DatabaseSequence.read (self.__cursor, database_sequense1.proposition_id, 0, database_triad.id)
                                    if database_sequense2 == None:
                                        self.__error_text = ErrorHelper.get_text (105)
                                        return None
                                    database_triad = DatabaseTriad.read_by_id (self.__cursor, database_sequense2.left_triad_id)
                                    if database_triad == None:
                                        self.__error_text = ErrorHelper.get_text (105)
                                        return None
                                    result_node.concept.id = database_triad.left_concept_id
                                    database_concept = DatabaseConcept.read_by_name (self.__cursor, LanguageHelper.translate ("to-be"))
                                    if database_concept == None:
                                        self.__error_text = ErrorHelper.get_text (104)
                                        return None
                                    database_triad1 = DatabaseTriad.read (self.__cursor, result_node.concept.id, 0, database_concept.id)
                                    if database_triad1 == None:
                                        self.__error_text = ErrorHelper.get_text (104)
                                        return None
                                    database_triad2 = DatabaseTriad.read (self.__cursor, database_concept.id, 0, actor.concept.id)
                                    if database_triad2 == None:
                                        self.__error_text = ErrorHelper.get_text (104)
                                        return None
                                    database_sequense3 = DatabaseSequence.read (self.__cursor, 0, database_triad1.id, database_triad2.id)
                                    if database_sequense3 == None:
                                        self.__error_text = ErrorHelper.get_text (104)
                                        return None
                                else:
                                    self.__error_text = ErrorHelper.get_text (105)
                                    return None
        if is_field != True:
            if result_node.concept.id != 0:
                database_concept = DatabaseConcept.read_by_id (self.__cursor, result_node.concept.id)
                result_node.concept.type = database_concept.type
                result_node.concept.name = database_concept.name
                result_node.text = result_node.concept.name
            else:
                return None

        return result_node