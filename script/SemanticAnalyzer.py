# coding: utf8
"""
Семантический анализатор
"""

from string import uppercase
from PropositionTree import PropositionTree
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
from SyntaxAnalyzer import SyntaxAnalyzer
from HandlerVariables import HandlerVariables

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
                    if CodeProvider.is_priorities_assigned () == False:
                        CodeProvider.assign_priorities ()
                    CodeProvider.prepare_next_line ()
            else:
                if CodeProvider.is_priorities_assigned () == False:
                    CodeProvider.assign_priorities ()

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
                                child, self.__error_text = PropositionTree.replace_subtree (node, side, is_new, self.__cursor)
                            else:
                                child, self.__error_text = PropositionTree.replace_subtree (node, side, False, self.__cursor)
                        else:
                            child, self.__error_text = PropositionTree.replace_subtree (node, side, is_new, self.__cursor)
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

        actor, actant = PropositionTree.get_actor_and_actant (self.proposition_tree.root_node)
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
                                                            if child1.concept.type == TreeNodeConceptType.definition:
                                                                list_id = MemoryProvider.get_list_id (child1.concept.name)
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
                                        if child.concept.type == TreeNodeConceptType.definition:
                                            field_id = MemoryProvider.get_field_id (child.concept.name)
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
                    handler_variables = HandlerVariables ()
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
                    #Предварительная загрузка процедур в память
                    if handler_text != None:
                        handler_text = handler_text.replace ("\\", "")
                    actor = None
                    actant = None
                    analized = SyntaxAnalyzer.analize (handler_text)
                    if analized == True:
                        tree = SyntaxAnalyzer.proposition_tree
                        # Раскрытие вложенных суждений
                        node = tree.root_node
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
                                                child, self.__error_text = PropositionTree.replace_subtree (node, side, is_new, self.__cursor)
                                            else:
                                                child, self.__error_text = PropositionTree.replace_subtree (node, side, False, self.__cursor)
                                        else:
                                            child, self.__error_text = PropositionTree.replace_subtree (node, side, is_new, self.__cursor)
                                        if child != None:
                                            parent.children[0] = child
                                else:
                                    side = node.side
                            if node.child_index < len (node.children):
                                idx = node.child_index
                                node.child_index += 1
                                tree.push_node (node)
                                parent = node
                                node = node.children[idx]
                                node.child_index = 0
                                k += 1
                            else:
                                node = tree.pop_node ()
                                k -= 1
                        actor, actant = PropositionTree.get_actor_and_actant (tree.root_node)
                        #tree.print_tree ()
                    if actor == None:
                        return False
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

                        if trigger_id != 0:
                            if handler_text != None:
                                TriggerProvider.set_handler (trigger_id, handler_text)
                                handler_variables.type = 'T'
                                handler_variables.id = trigger_id
                                CodeProvider.load_procedure (actant.concept.id, database_list.concept_id, handler_variables)
                        elif condition_id != 0:
                            if handler_text != None:
                                ConditionProvider.set_handler (condition_id, handler_text)
                                handler_variables.type = 'C'
                                handler_variables.id = condition_id
                                CodeProvider.load_procedure (actant.concept.id, database_list.concept_id, handler_variables)
                        else:
                            CodeProvider.load_procedure (actant.concept.id, database_list.concept_id, None)

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
                                        if child.concept.type == TreeNodeConceptType.definition:
                                            list_id = MemoryProvider.get_list_id (child.concept.name)
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
                                        if child.concept.type == TreeNodeConceptType.definition:
                                            field_id = MemoryProvider.get_field_id (child.concept.name)
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
                                elif child.type == PropositionTreeNodeType.concept:
                                    if child.concept.name == LanguageHelper.translate ("field"):
                                        node = ContextProvider.get_field_node ()
                                        if node != None:
                                            field_id = node.concept.id
                                    else:
                                        if child.concept.type == TreeNodeConceptType.definition:
                                            new_value = MemoryProvider.get_field_value (MemoryProvider.get_field_id (child.concept.name))
                                        else:
                                            new_value = MemoryProvider.get_field_value (child.concept.id)
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
                                        if child.concept.type == TreeNodeConceptType.definition:
                                            field_id = MemoryProvider.get_field_id (child.concept.name)
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