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

class SemanticAnalyzer ():

    def __init__ (self, cursor, code_stack):
        self.result = ""
        self.__cursor = cursor
        self.__error_text = ""
        self.__code_stack = code_stack

    def analize (self, tree):
        self.result = ""
        self.__error_text = ""
        self.proposition_tree = tree
        print "<SemanticAnalyzer>"
        actor, actant = self.__get_actor_and_actant (self.proposition_tree.root_node)
        if actor == None:
            return False
        if self.proposition_tree.root_node.concept.name == "выполнять":
            if actor.concept.name == "ты":
                database_concept = DatabaseConcept.read_by_name (self.__cursor, "быть")
                if database_concept == None:
                    self.__error_text = "#106:Процедура не содержит программного кода"
                    return False
                database_triad = DatabaseTriad.read (self.__cursor, actant.concept.id, 0, database_concept.id)
                if database_triad == None:
                    self.__error_text = "#106:Процедура не содержит программного кода"
                    return None
                query = "SELECT right_triad_id FROM qsl_sequence WHERE left_triad_id = " + str (database_triad.id) + ";"
                self.__cursor.execute (query)
                row = self.__cursor.fetchone ()
                rows = []
                list_id = 0
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
                    list_id = database_concept.id
                if list_id == 0:
                    self.__error_text = "#106:Процедура не содержит программного кода"
                    return False
                database_list = DatabaseList.read (self.__cursor, list_id, 0)
                if database_list == None:
                    self.__error_text = "#106:Процедура не содержит программного кода"
                    return False
                self.__code_stack.push (database_list)
                print database_list.text

        print "</SemanticAnalyzer>"
        return True

    def get_error_text (self):
        return self.__error_text

    def __get_actor_and_actant (self, root_node):
        idx = 0
        actor = None
        actant = None
        while idx < len (root_node.children) or actor == None or actant == None:
            child = root_node.children[idx]
            if child.type == PropositionTreeNodeType.linkage:
                if child.linkage.name == "кто" or child.linkage.name == "что":
                    parent = child
                    child = child.children[0]
                    if child.type == PropositionTreeNodeType.concept:
                        if child.side == PropositionTreeNodeSide.left:
                            actor = child
                        elif child.side == PropositionTreeNodeSide.right:
                            actant = child
                        elif child.side == PropositionTreeNodeSide.center:
                            if child.concept.subroot == True:
                                actant = self.__replace_subtree (child)
                                if actant != None:
                                    parent.children[0] = actant
                                else:
                                    return None, None
            idx += 1
        return actor, actant

    def __replace_subtree (self, root_node):
        actor, actant = self.__get_actor_and_actant (root_node)
        result_node = PropositionTreeNode ()
        result_node.type = PropositionTreeNodeType.concept
        result_node.concept = TreeNodeConcept ()

        if root_node.concept.name == "иметь":
            if actant.concept.name == "имя":
                child1 = actant.children[0]
                if child1.type == PropositionTreeNodeType.linkage:
                    if child1.linkage.name == "какое":
                        child2 = child1.children[0]
                        if child2.type == PropositionTreeNodeType.concept:
                            database_triad = DatabaseTriad.read (self.__cursor, actant.concept.id, child1.linkage.id, child2.concept.id)
                            if database_triad == None:
                                self.__error_text = "#105:Понятие с таким именем не найдено"
                                return None
                            database_sequense1 = DatabaseSequence.read (self.__cursor, 0, 0, database_triad.id)
                            if database_sequense1 == None:
                                self.__error_text = "#105:Понятие с таким именем не найдено"
                                return None
                            database_triad = DatabaseTriad.read_by_id (self.__cursor, database_sequense1.left_triad_id)
                            if database_triad == None:
                                self.__error_text = "#105:Понятие с таким именем не найдено"
                                return None
                            if database_triad.left_concept_id == root_node.concept.id:
                                database_sequense2 = DatabaseSequence.read (self.__cursor, database_sequense1.proposition_id, 0, database_triad.id)
                                if database_sequense2 == None:
                                    self.__error_text = "#105:Понятие с таким именем не найдено"
                                    return None
                                database_triad = DatabaseTriad.read_by_id (self.__cursor, database_sequense2.left_triad_id)
                                if database_triad == None:
                                    self.__error_text = "#105:Понятие с таким именем не найдено"
                                    return None
                                result_node.concept.id = database_triad.left_concept_id
                                database_concept = DatabaseConcept.read_by_name (self.__cursor, "быть")
                                if database_concept == None:
                                    self.__error_text = "#104:Понятие не является процедурой"
                                    return None
                                database_triad1 = DatabaseTriad.read (self.__cursor, result_node.concept.id, 0, database_concept.id)
                                if database_triad1 == None:
                                    self.__error_text = "#104:Понятие не является процедурой"
                                    return None
                                database_triad2 = DatabaseTriad.read (self.__cursor, database_concept.id, 0, actor.concept.id)
                                if database_triad2 == None:
                                    self.__error_text = "#104:Понятие не является процедурой"
                                    return None
                                database_sequense3 = DatabaseSequence.read (self.__cursor, 0, database_triad1.id, database_triad2.id)
                                if database_sequense3 == None:
                                    self.__error_text = "#104:Понятие не является процедурой"
                                    return None
                            else:
                                self.__error_text = "#105:Понятие с таким именем не найдено"
                                return None

        if result_node.concept.id != 0:
            database_concept = DatabaseConcept.read_by_id (self.__cursor, result_node.concept.id)
            result_node.concept.type = database_concept.type
            result_node.concept.name = database_concept.name
            result_node.text = result_node.concept.name
        else:
            return None

        return result_node