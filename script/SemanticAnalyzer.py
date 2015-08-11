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

class SemanticAnalyzer ():

    def __init__ (self, cursor, tree):
        self.proposition_tree = tree
        self.result = ""
        self.__cursor = cursor
        self.__error_text = ""

    def analize (self):
        print "-------- SemanticAnalyzer --------"
        actor, actant = self.__get_actor_and_actant (self.proposition_tree.root_node)
        if actor != None:
            #print actor.name
            pass
        if actant != None:
            #print actant.name
            pass
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
                                parent.children[0] = actant
            idx += 1
        return actor, actant

    def __replace_subtree (self, root_node):
        actor, actant = self.__get_actor_and_actant (root_node)
        if actor != None:
            print actor.concept.name
        if actant != None:
            print actant.concept.name
        result_node = PropositionTreeNode ()
        result_node.type = PropositionTreeNodeType.concept
        result_node.text = "qqq"
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
                                return None
                            database_sequense1 = DatabaseSequence.read (self.__cursor, 0, 0, database_triad.id)
                            if database_sequense1 == None:
                                return None
                            database_triad = DatabaseTriad.read_by_id (self.__cursor, database_sequense1.left_triad_id)
                            if database_triad == None:
                                return None
                            if database_triad.left_concept_id == root_node.concept.id:
                                database_sequense2 = DatabaseSequence.read (self.__cursor, database_sequense1.proposition_id, 0, database_triad.id)
                                if database_sequense2 == None:
                                    return None
                                #result_node.concept.id = database_triad.left_concept_id
                                result_node.concept.id = 8
                            else:
                                return None

        if result_node.concept.id != 0:
            database_concept = DatabaseConcept.read_by_id (self.__cursor, result_node.concept.id)
            result_node.concept.type = database_concept.type
            result_node.concept.name = database_concept.name
        else:
            return None

        return result_node