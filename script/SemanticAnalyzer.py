# coding: utf8
"""
Семантический анализатор
"""

from string import uppercase
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
from TriggerProvider import TriggerProvider
from Trigger import Trigger
from TriggerType import TriggerType
from ConditionProvider import ConditionProvider
from CodeProvider import CodeProvider

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
                if code_line.concept_id == CodeProvider.get_initial_procedure ():
                    database_list = DatabaseList.read (self.__cursor, code_line.concept_id, code_line.id)
                    if database_list != None:
                        code_line = CodeLine ()
                        code_line.id = database_list.id
                        code_line.concept_id = database_list.concept_id
                        code_line.prev_line_id = database_list.prev_line_id
                        code_line.text = database_list.text
                        CodeStack.push (code_line)
                        #CodeStack.inside_procedure = True
                    else:
                        CodeStack.inside_procedure = False
                else:
                    CodeProvider.prepare_next_line ()

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
                        child = None
                        if is_new == True:
                            if k == 2:
                                child = self.__replace_subtree (node, side, is_new)
                            else:
                                child = self.__replace_subtree (node, side, False)
                        else:
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

        # Программная инструкция
        if actor.concept.name == LanguageHelper.translate ("you"):
            if self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-create"):
                if actant.concept.name == LanguageHelper.translate ("condition"):
                    node = PropositionTreeNode ()
                    node.type = PropositionTreeNodeType.concept
                    node.side = actant.side
                    node.concept = TreeNodeConcept ()
                    node.concept.id = ConditionProvider.create_condition ()
                    node.concept.type = TreeNodeConceptType.condition
                    node.concept.name = "$" + str (node.concept.id)
                    node.text = node.concept.name
                    ContextProvider.set_condition_node (node)
                elif actant.concept.name == LanguageHelper.translate ("list"):
                    node = PropositionTreeNode ()
                    node.type = PropositionTreeNodeType.concept
                    node.side = actant.side
                    node.concept = TreeNodeConcept ()
                    node.concept.id = MemoryProvider.create_list ("")
                    node.concept.type = TreeNodeConceptType.memlist
                    node.concept.name = "$" + str (node.concept.id)
                    node.text = node.concept.name
                    ContextProvider.set_list_node (node)
                elif actant.concept.name == LanguageHelper.translate ("reference"):
                    list_id = 0
                    ref_list_id = 0
                    element_id = 0
                    i = 0
                    while i < len (actant.children):
                        child = actant.children[i]
                        if child.type == PropositionTreeNodeType.linkage:
                            if child.linkage.name == LanguageHelper.translate ("for-what"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.concept:
                                    if child.concept.name == LanguageHelper.translate ("element"):
                                        j = 0
                                        while j < len (child.children):
                                            child1 = child.children[j]
                                            if child1.type == PropositionTreeNodeType.linkage:
                                                if child1.linkage.name == LanguageHelper.translate ("of-what"):
                                                    child1 = child1.children[0]
                                                    if child1.type == PropositionTreeNodeType.concept:
                                                        if child1.concept.name == LanguageHelper.translate ("list"):
                                                            node = ContextProvider.get_list_node ()
                                                            if node != None:
                                                                list_id = node.concept.id
                                                        else:
                                                            list_id = child1.concept.id
                                                elif child1.linkage.name == LanguageHelper.translate ("which"):
                                                    child1 = child1.children[0]
                                                    if child1.type == PropositionTreeNodeType.number:
                                                        element_id = int (child1.text)
                                            j += 1
                                        if list_id == 0:
                                            node = ContextProvider.get_list_node ()
                                            if node != None:
                                                list_id = node.concept.id
                                        if element_id == 0:
                                            node = ContextProvider.get_element_node ()
                                            if node != None:
                                                element_id = node.concept.id
                            elif child.linkage.name == LanguageHelper.translate ("on-what"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.concept:
                                    if child.concept.name == LanguageHelper.translate ("list"):
                                        node = ContextProvider.get_list_node ()
                                        if node != None:
                                            ref_list_id = node.concept.id
                                    else:
                                        ref_list_id = child.concept.id
                        i += 1
                    if list_id != 0 and element_id != 0 and ref_list_id != 0:
                        MemoryProvider.set_list_element_ref_list (list_id, element_id, ref_list_id)

            elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-execute"):
                if code_line == None:
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
                        if database_concept.type != TreeNodeConceptType.dblist:
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
                    CodeStack.inside_procedure = True
                    CodeProvider.set_initial_procedure (database_list.concept_id)
                else:
                    if CodeProvider.is_procedure_already_loaded (actant.concept.id) == False:
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
                            if database_concept.type != TreeNodeConceptType.dblist:
                                continue
                            list_concept_id = database_concept.id
                        if list_concept_id == 0:
                            self.__error_text = ErrorHelper.get_text (106)
                            return False
                        database_list = DatabaseList.read (self.__cursor, list_concept_id, 0)
                        if database_list == None:
                            self.__error_text = ErrorHelper.get_text (106)
                            return False
                        CodeProvider.load_procedure (actant.concept.id, database_list.concept_id)
                    CodeProvider.execute_procedure (actant.concept.id)

            elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-set"):
                if actant.concept.name == LanguageHelper.translate ("value"):
                    field_id = 0
                    list_id = 0
                    element_id = 0
                    new_value = None
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
                                    elif child.concept.name == LanguageHelper.translate ("element"):
                                        j = 0
                                        while j < len (child.children):
                                            child1 = child.children[j]
                                            if child1.type == PropositionTreeNodeType.linkage:
                                                if child1.linkage.name == LanguageHelper.translate ("of-what"):
                                                    child1 = child1.children[0]
                                                    if child1.type == PropositionTreeNodeType.concept:
                                                        if child1.concept.name == LanguageHelper.translate ("list"):
                                                            node = ContextProvider.get_list_node ()
                                                            if node != None:
                                                                list_id = node.concept.id
                                                        else:
                                                            list_id = child1.concept.id
                                                elif child1.linkage.name == LanguageHelper.translate ("which"):
                                                    child1 = child1.children[0]
                                                    if child1.type == PropositionTreeNodeType.number:
                                                        element_id = int (child1.text)
                                                    elif child1.type == PropositionTreeNodeType.concept:
                                                        element_id = MemoryProvider.get_field_value (MemoryProvider.get_field_id (child1.concept.name))
                                            j += 1
                                        if list_id == 0:
                                            node = ContextProvider.get_list_node ()
                                            if node != None:
                                                list_id = node.concept.id
                                        if element_id == 0:
                                            node = ContextProvider.get_element_node ()
                                            if node != None:
                                                element_id = node.concept.id
                                    else:
                                        field_id = child.concept.id
                            elif child.linkage.name == LanguageHelper.translate ("which"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.number:
                                    new_value = int (child.text)
                                elif child.type == PropositionTreeNodeType.string:
                                    new_value = child.text
                                elif child.type == PropositionTreeNodeType.concept:
                                    if child.concept.name == LanguageHelper.translate ("element"):
                                        list1_id = None
                                        element1_id = None
                                        node = ContextProvider.get_list_node ()
                                        if node != None:
                                            list1_id = node.concept.id
                                        node = ContextProvider.get_element_node ()
                                        if node != None:
                                            element1_id = node.concept.id
                                        if list1_id != None and element1_id != None:
                                            new_value = MemoryProvider.get_list_element_value (list1_id, element1_id)
                                    else:
                                        new_value = MemoryProvider.get_field_value (MemoryProvider.get_field_id (child.concept.name))
                        i += 1
                    if field_id != 0:
                        if new_value != None:
                            old_value = MemoryProvider.get_field_value (field_id)
                            if new_value != old_value:
                                #trigger_key = str (field_id) + "=" + str (old_value)
                                #ConditionProvider.deprocess_object_triggers (TriggerProvider.get_trigger_id (trigger_key))
                                MemoryProvider.set_field_value (field_id, new_value)
                                object_key = str (field_id)
                                TriggerProvider.process_object_triggers (object_key, new_value)
                    elif list_id != 0 and element_id != 0:
                        if new_value != None:
                            old_value = MemoryProvider.get_list_element_value (list_id, element_id)
                            if new_value != old_value:
                            #    trigger_key = str (list_id) + "[" + str (element_id) + "]=" + str (old_value)
                            #    ConditionProvider.deprocess_object_triggers (TriggerProvider.get_trigger_id (trigger_key))
                                MemoryProvider.set_list_element_value (list_id, element_id, new_value)
                            #trigger_key = str (list_id) + "[" + str (element_id) + "]"
                            #TriggerProvider.process_object_triggers (trigger_key)
                            #trigger_key = str (list_id) + "[" + str (element_id) + "]=" + str (new_value)
                            #TriggerProvider.process_object_triggers (trigger_key)

                elif actant.concept.name == LanguageHelper.translate ("handler"):
                    trigger_id = 0
                    condition_id = 0
                    handler_text = None
                    i = 0
                    while i < len (actant.children):
                        child = actant.children[i]
                        if child.type == PropositionTreeNodeType.linkage:
                            if child.linkage.name == LanguageHelper.translate ("of-what"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.concept:
                                    if child.concept.name == LanguageHelper.translate ("trigger"):
                                        node = ContextProvider.get_trigger_node ()
                                        if node != None:
                                            trigger_id = node.concept.id
                                    elif child.concept.name == LanguageHelper.translate ("condition"):
                                        node = ContextProvider.get_condition_node ()
                                        if node != None:
                                            condition_id = node.concept.id
                                    else:
                                        field_id = child.concept.id
                            elif child.linkage.name == LanguageHelper.translate ("which"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.string:
                                    handler_text = child.text
                        i += 1
                    if trigger_id != 0:
                        if handler_text != None:
                            handler_text = handler_text.replace ("\\", "")
                            TriggerProvider.set_handler (trigger_id, handler_text)
                    elif condition_id != 0:
                        if handler_text != None:
                            handler_text = handler_text.replace ("\\", "")
                            ConditionProvider.set_handler (condition_id, handler_text)

            elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-use"):
                if actant.concept.name == LanguageHelper.translate ("element"):
                    list_id = 0
                    element_id = 0
                    is_ref = False
                    i = 0
                    while i < len (actant.children):
                        child = actant.children[i]
                        if child.type == PropositionTreeNodeType.linkage:
                            if child.linkage.name == LanguageHelper.translate ("of-what"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.concept:
                                    if child.concept.name == LanguageHelper.translate ("list"):
                                        node = ContextProvider.get_list_node ()
                                        if node != None:
                                            list_id = node.concept.id
                                    else:
                                        list_id = child.concept.id
                            elif child.linkage.name == LanguageHelper.translate ("which"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.number:
                                    element_id = int (child.text)
                                elif child.type == PropositionTreeNodeType.concept:
                                    element_id = MemoryProvider.get_field_value (MemoryProvider.get_field_id (child.concept.name))
                        i += 1
                    i = 0
                    while i < len (self.proposition_tree.root_node.children):
                        child = self.proposition_tree.root_node.children[i]
                        if child.type == PropositionTreeNodeType.linkage:
                            if child.linkage.name == LanguageHelper.translate ("as-what"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.concept:
                                    if child.concept.name == LanguageHelper.translate ("list"):
                                        is_ref = True
                                        list_id = MemoryProvider.get_list_element_ref_list (list_id, element_id)
                        i += 1
                    if list_id != 0 and element_id != 0:
                        node = PropositionTreeNode ()
                        node.type = PropositionTreeNodeType.concept
                        node.side = actant.side
                        node.concept = TreeNodeConcept ()
                        node.concept.id = list_id
                        node.concept.type = TreeNodeConceptType.memlist
                        node.concept.name = "$" + str (node.concept.id)
                        node.text = node.concept.name
                        ContextProvider.set_list_node (node)

                        if is_ref != True:
                            node = PropositionTreeNode ()
                            node.type = PropositionTreeNodeType.concept
                            node.side = actant.side
                            node.concept = TreeNodeConcept ()
                            node.concept.id = element_id
                            node.concept.type = TreeNodeConceptType.element
                            node.concept.name = "$" + str (node.concept.id)
                            node.text = node.concept.name
                            ContextProvider.set_element_node (node)

            elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-add"):
                if actant.concept.name == LanguageHelper.translate ("element"):
                    child = actant.children[0]
                    if child.type == PropositionTreeNodeType.linkage:
                        if child.linkage.name == LanguageHelper.translate ("of-what"):
                            child = child.children[0]
                            if child.type == PropositionTreeNodeType.concept:
                                if child.concept.name == LanguageHelper.translate ("list"):
                                    node = ContextProvider.get_list_node ()
                                    if node != None:
                                        list_id = node.concept.id
                                        if list_id != 0:
                                            node = PropositionTreeNode ()
                                            node.type = PropositionTreeNodeType.concept
                                            node.side = actant.side
                                            node.concept = TreeNodeConcept ()
                                            node.concept.id = MemoryProvider.add_list_element (list_id)
                                            node.concept.type = TreeNodeConceptType.element
                                            node.concept.name = "$" + str (node.concept.id)
                                            node.text = node.concept.name
                                            ContextProvider.set_element_node (node)

            elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-increase"):
                if actant.concept.name == LanguageHelper.translate ("value"):
                    field_id = 0
                    list_id = 0
                    element_id = 0
                    new_value = None
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
                                    elif child.concept.name == LanguageHelper.translate ("element"):
                                        #j = 0
                                        #while j < len (child.children):
                                        #    child1 = child.children[j]
                                        #    if child1.type == PropositionTreeNodeType.linkage:
                                        #        if child1.linkage.name == LanguageHelper.translate ("of-what"):
                                        #            child1 = child1.children[0]
                                        #            if child1.type == PropositionTreeNodeType.concept:
                                        #                if child1.concept.name == LanguageHelper.translate ("list"):
                                        #                    node = ContextProvider.get_list_node ()
                                        #                    if node != None:
                                        #                        list_id = node.concept.id
                                        #                else:
                                        #                    list_id = child1.concept.id
                                        #        elif child1.linkage.name == LanguageHelper.translate ("which"):
                                        #            child1 = child1.children[0]
                                        #            if child1.type == PropositionTreeNodeType.number:
                                        #                element_id = int (child1.text)
                                        #            elif child1.type == PropositionTreeNodeType.concept:
                                        #                element_id = MemoryProvider.get_field_value (MemoryProvider.get_field_id (child1.concept.name))
                                        #    j += 1
                                        if list_id == 0:
                                            node = ContextProvider.get_list_node ()
                                            if node != None:
                                                list_id = node.concept.id
                                        if element_id == 0:
                                            node = ContextProvider.get_element_node ()
                                            if node != None:
                                                element_id = node.concept.id
                                    else:
                                        field_id = child.concept.id
                            #elif child.linkage.name == LanguageHelper.translate ("which"):
                            #    child = child.children[0]
                            #    if child.type == PropositionTreeNodeType.number:
                            #        field_value = child.text
                        i += 1
                    i = 0
                    while i < len (self.proposition_tree.root_node.children):
                        child = self.proposition_tree.root_node.children[i]
                        if child.type == PropositionTreeNodeType.linkage:
                            if child.linkage.name == LanguageHelper.translate ("on-how-many"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.number:
                                    new_value = int (child.text)
                        i += 1
                    if field_id != 0:
                        if new_value != None:
                            old_value = MemoryProvider.get_field_value (field_id)
                            new_value += old_value
                            MemoryProvider.set_field_value (field_id, new_value)
                            object_key = str (field_id)
                            TriggerProvider.process_object_triggers (object_key, new_value)
                    elif list_id != 0 and element_id != 0:
                        if new_value != None:
                            old_value = MemoryProvider.get_list_element_value (list_id, element_id)
                            new_value += old_value
                            MemoryProvider.set_list_element_value (list_id, element_id, new_value)

            elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-print"):
                if actant.concept.name == LanguageHelper.translate ("value"):
                    field_id = 0
                    list_id = 0
                    element_id = 0
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
                                    elif child.concept.name == LanguageHelper.translate ("element"):
                                        j = 0
                                        while j < len (child.children):
                                            child1 = child.children[j]
                                            if child1.type == PropositionTreeNodeType.linkage:
                                                if child1.linkage.name == LanguageHelper.translate ("of-what"):
                                                    child1 = child1.children[0]
                                                    if child1.type == PropositionTreeNodeType.concept:
                                                        if child1.concept.name == LanguageHelper.translate ("list"):
                                                            node = ContextProvider.get_list_node ()
                                                            if node != None:
                                                                list_id = node.concept.id
                                                elif child1.linkage.name == LanguageHelper.translate ("which"):
                                                    child1 = child1.children[0]
                                                    if child1.type == PropositionTreeNodeType.number:
                                                        element_id = int (child1.text)
                                            j += 1
                                        if list_id == 0:
                                            node = ContextProvider.get_list_node ()
                                            if node != None:
                                                list_id = node.concept.id
                                        if element_id == 0:
                                            node = ContextProvider.get_element_node ()
                                            if node != None:
                                                element_id = node.concept.id
                                    else:
                                        field_id = child.concept.id
                                    if field_id != 0:
                                        self.result += str (MemoryProvider.get_field_value (field_id))
                                    elif list_id != 0 and element_id != 0:
                                        self.result += str (MemoryProvider.get_list_element_value (list_id, element_id))
                            elif child.linkage.name == LanguageHelper.translate ("which"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.string:
                                    self.result += child.text
                        i += 1

            elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-register"):
                if actant.concept.name == LanguageHelper.translate ("trigger"):
                    field_id = 0
                    trigger_type = 0
                    trigger_condition = ""
                    field_value = ""
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
                                        trigger_type = TriggerType.on_change
                                    elif child.concept.name == LanguageHelper.translate ("value"):
                                        trigger_type = TriggerType.on_value
                                        child = child.children[0]
                                        if child.type == PropositionTreeNodeType.linkage:
                                            if child.linkage.name == LanguageHelper.translate ("which"):
                                                child = child.children[0]
                                                if child.type == PropositionTreeNodeType.number:
                                                    field_value = child.text
                            elif child.linkage.name == LanguageHelper.translate ("which"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.string:
                                    trigger_condition = child.text
                        i += 1
                    object_key = None
                    if trigger_type == TriggerType.on_change:
                        trigger_condition = ""
                    object_key = str (field_id)
                    if object_key != None:
                        node = PropositionTreeNode ()
                        node.type = PropositionTreeNodeType.concept
                        node.side = child.side
                        node.concept = TreeNodeConcept ()
                        node.concept.id = TriggerProvider.register_trigger (object_key, trigger_type, trigger_condition, field_value)
                        node.concept.type = TreeNodeConceptType.trigger
                        node.concept.name = "$" + str (node.concept.id)
                        node.text = node.concept.name
                        ContextProvider.set_trigger_node (node)

            elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-delete"):
                if actant.concept.name == LanguageHelper.translate ("trigger"):
                    field_id = 0
                    trigger_type = 0
                    trigger_condition = ""
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
                                        trigger_type = TriggerType.on_change
                                    elif child.concept.name == LanguageHelper.translate ("value"):
                                        trigger_type = TriggerType.on_value
                                        child = child.children[0]
                                        if child.type == PropositionTreeNodeType.linkage:
                                            if child.linkage.name == LanguageHelper.translate ("which"):
                                                child = child.children[0]
                                                if child.type == PropositionTreeNodeType.number:
                                                    field_value = child.text
                            elif child.linkage.name == LanguageHelper.translate ("which"):
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.string:
                                    trigger_condition = child.text
                        i += 1
                    object_key = None
                    if trigger_type == TriggerType.on_change:
                        trigger_condition = ""
                    object_key = str (field_id)
                    if object_key != None:
                        TriggerProvider.delete_trigger (object_key, trigger_condition, field_value)

            elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-attach"):
                if actant.concept.name == LanguageHelper.translate ("trigger"):
                    trigger_id = 0
                    condition_id = 0
                    node = ContextProvider.get_trigger_node ()
                    if node != None:
                        trigger_id = node.concept.id
                    if trigger_id != 0:
                        i = 0
                        while i < len (self.proposition_tree.root_node.children):
                            child = self.proposition_tree.root_node.children[i]
                            if child.type == PropositionTreeNodeType.linkage:
                                if child.linkage.name == LanguageHelper.translate ("towards-what"):
                                    child = child.children[0]
                                    if child.type == PropositionTreeNodeType.concept:
                                        if child.concept.name == LanguageHelper.translate ("condition"):
                                            node = ContextProvider.get_condition_node ()
                                            if node != None:
                                                condition_id = node.concept.id
                            i += 1
                    if condition_id != 0:
                        ConditionProvider.attach_trigger (condition_id, trigger_id)

            elif self.proposition_tree.root_node.concept.name == LanguageHelper.translate ("to-convert"):
                from_value = None
                from_type = None
                into_value = None
                into_type = None
                list_id = 0
                element_id = 0
                i = 0
                while i < len (self.proposition_tree.root_node.children):
                    child = self.proposition_tree.root_node.children[i]
                    if child.type == PropositionTreeNodeType.linkage:
                        if child.linkage.name == LanguageHelper.translate ("what"):
                            child = child.children[0]
                            if child.type == PropositionTreeNodeType.concept:
                                if child.concept.name == LanguageHelper.translate ("field"):
                                    pass
                                elif child.concept.name == LanguageHelper.translate ("element"):
                                    if list_id == 0:
                                        node = ContextProvider.get_list_node ()
                                        if node != None:
                                            list_id = node.concept.id
                                    if element_id == 0:
                                        node = ContextProvider.get_element_node ()
                                        if node != None:
                                            element_id = node.concept.id
                                    if list_id != 0 and element_id != 0:
                                        from_value = MemoryProvider.get_list_element_value (list_id, element_id)
                                else:
                                    pass
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.linkage:
                                    if child.linkage.name == LanguageHelper.translate ("as-what"):
                                        child = child.children[0]
                                        if child.type == PropositionTreeNodeType.concept:
                                            if child.concept.name == LanguageHelper.translate ("number"):
                                                from_type = 1
                        elif child.linkage.name == LanguageHelper.translate ("into-what"):
                            child = child.children[0]
                            if child.type == PropositionTreeNodeType.concept:
                                if child.concept.name == LanguageHelper.translate ("field"):
                                    pass
                                elif child.concept.name == LanguageHelper.translate ("element"):
                                    pass
                                else:
                                    into_field_id = MemoryProvider.get_field_id (child.concept.name)
                                child = child.children[0]
                                if child.type == PropositionTreeNodeType.linkage:
                                    if child.linkage.name == LanguageHelper.translate ("as-what"):
                                        child = child.children[0]
                                        if child.type == PropositionTreeNodeType.concept:
                                            if child.concept.name == LanguageHelper.translate ("letter"):
                                                into_type = 2
                    i += 1
                if from_value != None and into_field_id != None:
                    if from_type == 1 and into_type == 2:
                        from_value -= 1
                        new_value = uppercase [from_value]
                        MemoryProvider.set_field_value (into_field_id, new_value)

            else:
                pass
        else:
            # Запрос к базе знаний
            pass

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
        is_memobject = False

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
                                    is_memobject = True
                                    result_node.concept.type = TreeNodeConceptType.field
                                    result_node.concept.name = "$" + str (result_node.concept.id)
                                    result_node.text = result_node.concept.name
                                    ContextProvider.set_field_node (result_node)
                                else:
                                    result_node.concept.id = MemoryProvider.get_field_id (child2.concept.name)
                                    is_memobject = True
                                    result_node.concept.type = TreeNodeConceptType.field
                                    result_node.concept.name = "$" + str (result_node.concept.id)
                                    result_node.text = result_node.concept.name
                elif actor.concept.name == LanguageHelper.translate ("list"):
                    child1 = actant.children[0]
                    if child1.type == PropositionTreeNodeType.linkage:
                        if child1.linkage.name == LanguageHelper.translate ("which"):
                            child2 = child1.children[0]
                            if child2.type == PropositionTreeNodeType.concept:
                                if is_new == True:
                                    result_node.concept.id = MemoryProvider.create_list (child2.concept.name)
                                    is_memobject = True
                                    result_node.concept.type = TreeNodeConceptType.memlist
                                    result_node.concept.name = "$" + str (result_node.concept.id)
                                    result_node.text = result_node.concept.name
                                    ContextProvider.set_list_node (result_node)
                                else:
                                    result_node.concept.id = MemoryProvider.get_list_id (child2.concept.name)
                                    is_memobject = True
                                    result_node.concept.type = TreeNodeConceptType.memlist
                                    result_node.concept.name = "$" + str (result_node.concept.id)
                                    result_node.text = result_node.concept.name
                elif actor.concept.name == LanguageHelper.translate ("procedure"):
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
        if is_memobject != True:
            if result_node.concept.id != 0:
                database_concept = DatabaseConcept.read_by_id (self.__cursor, result_node.concept.id)
                result_node.concept.type = database_concept.type
                result_node.concept.name = database_concept.name
                result_node.text = result_node.concept.name
            else:
                return None

        return result_node