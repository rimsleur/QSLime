# coding: utf8
"""
Синтаксический анализатор
"""

from TokenConcept import TokenConcept
from TokenLinkage import TokenLinkage
from Token import Token
from TokenType import TokenType
from TokenConceptType import TokenConceptType
from PropositionTree import PropositionTree
from PropositionTreeNode import PropositionTreeNode
from PropositionTreeNodeType import PropositionTreeNodeType
from PropositionTreeNodeSide import PropositionTreeNodeSide
from TreeNodeConcept import TreeNodeConcept
from TreeNodeLinkage import TreeNodeLinkage
from ErrorHelper import ErrorHelper

class SyntaxAnalyzer ():

    def __init__ (self, cursor):
        self.proposition_tree = None
        self.__cursor = cursor
        self.__error_text = ""

    def analize (self, text):
        word = []
        tokens = []
        prev_letter = ""

        # Разбивка на токены
        i = 0
        while i < len (text):
            letter = text[i]
            if letter == " ":
                if len (word) > 0:
                    token = Token ()
                    token.text = ''.join (word)
                    tokens.append (token)
                    word = []
            elif letter == "(" or \
                 letter == ")" or \
                 letter == "." or \
                 letter == "," or \
                 letter == "=" or \
                 letter == "_":
                if len (word) > 0:
                    token = Token ()
                    token.text = ''.join (word)
                    tokens.append (token)
                    word = []
                token = Token ()
                token.text = letter
                tokens.append (token)
            elif letter == "?":
                if len (word) > 0:
                    token = Token ()
                    token.text = ''.join (word)
                    tokens.append (token)
                    word = []
                if prev_letter not in [" ", "("]:
                    token = Token ()
                    token.text = letter
                    tokens.append (token)
                else:
                    word.append (letter)
            elif letter == "\"":
                i += 1
                while i < len (text):
                    prev_letter = letter
                    letter = text[i]
                    if letter == "\"" and prev_letter != "\\":
                        break
                    else:
                        word.append (letter)
                    i += 1
                token = Token ()
                token.text = ''.join (word)
                token.type = TokenType.string
                tokens.append (token)
                word = []
            else:
                word.append (letter)
            prev_letter = letter
            i += 1

        # Идентификация токенов
        for token in tokens:
            #print token.text
            if token.type == TokenType.string:
                continue
            if token.text.find ('?') == 0 and len (token.text) > 1:
                s = token.text.replace ('?', '')
                query = "SELECT id FROM qsl_linkage WHERE name = \'" + s + "\';"
                self.__cursor.execute (query)
                row = self.__cursor.fetchone ()
                if row != None:
                    token.type = TokenType.linkage
                    token.linkage = TokenLinkage ()
                    token.linkage.id = row[0]
                    token.linkage.name = s
                else:
                    self.__error_text = ErrorHelper.get_text (102, token.text)
                    return False
            elif token.text.find ('*') == 0:
                # Модификатор
                token.type = TokenType.modifier
            elif token.text == "(":
                token.type = TokenType.opening_bracket
            elif token.text == ")":
                token.type = TokenType.closing_bracket
            elif token.text == ",":
                token.type = TokenType.comma
            elif token.text == "_":
                token.type = TokenType.underscore
            elif token.text == ".":
                token.type = TokenType.point
            elif token.text == "?":
                token.type = TokenType.question_mark
            elif token.text == "=":
                token.type = TokenType.equal_sign
            else:
                query = "SELECT id, type FROM qsl_concept WHERE name = \'" + token.text + "\';"
                self.__cursor.execute (query)
                row = self.__cursor.fetchone ()
                if row != None:
                    token.type = TokenType.concept
                    token.concept = TokenConcept ()
                    token.concept.id = row[0]
                    token.concept.type = row[1]
                    token.concept.name = token.text
                else:
                    if token.text.isdigit ():
                        token.type = TokenType.number
                    else:
                        self.__error_text = ErrorHelper.get_text (103, token.text)
                        return False

        node = self.build_tree (tokens)
        if node != None:
            self.proposition_tree = PropositionTree ()
            self.proposition_tree.root_node = node
        else:
            return False

        return True

    def build_tree (self, tokens):
        # Поиск главного понятия действия
        idx = 0
        node = None
        root_node = None
        for token in tokens:
            if token.type == TokenType.concept:
                if token.concept.type == TokenConceptType.action:
                    node = PropositionTreeNode ()
                    node.text = token.text
                    node.type = PropositionTreeNodeType.concept
                    node.side = PropositionTreeNodeSide.center
                    node.concept = TreeNodeConcept ()
                    node.concept.id = token.concept.id
                    node.concept.name = token.concept.name
                    node.concept.type = token.concept.type
                    root_node = node
                    break
            idx += 1

        if node == None:
            self.__error_text = ErrorHelper.get_text (101)
            return None

        # Обработка левой ветки суждения
        i = idx - 1
        while i >= 0:
            if tokens[i].type == TokenType.equal_sign:
                if tokens[i+1].type == TokenType.concept:
                    node.concept.sublink = True
            else:
                parent_node = node
                node = PropositionTreeNode ()
                node.parent = parent_node
                node.text = tokens[i].text
                if tokens[i].type == TokenType.concept:
                    node.type = PropositionTreeNodeType.concept
                    node.side = PropositionTreeNodeSide.left
                    node.concept = TreeNodeConcept ()
                    node.concept.id = tokens[i].concept.id
                    node.concept.name = tokens[i].concept.name
                    node.concept.type = tokens[i].concept.type
                elif tokens[i].type == TokenType.linkage:
                    node.type = PropositionTreeNodeType.linkage
                    node.side = PropositionTreeNodeSide.left
                    node.linkage = TreeNodeLinkage ()
                    node.linkage.id = tokens[i].linkage.id
                    node.linkage.name = tokens[i].linkage.name
                elif tokens[i].type == TokenType.underscore:
                    node.type = PropositionTreeNodeType.underscore
                elif tokens[i].type == TokenType.number:
                    node.type = PropositionTreeNodeType.number
                elif tokens[i].type == TokenType.string:
                    node.type = PropositionTreeNodeType.string
                #print node.text
                parent_node.children.append (node)
            i -= 1

        # Обработка правой ветки суждения
        i = idx + 1
        node = root_node
        inside_brackets = False
        common_parent = None
        while i < len (tokens):
            if tokens[i].type == TokenType.point:
                pass
            elif tokens[i].type == TokenType.question_mark:
                pass
            elif tokens[i].type == TokenType.opening_bracket:
                inside_brackets = True
                if node.type == PropositionTreeNodeType.concept:
                    common_parent = node
                elif node.type == PropositionTreeNodeType.linkage:
                    b = 1
                    subtree_tokens = []
                    j = i + 1
                    while j < len (tokens) and b != 0:
                        if tokens[j].type == TokenType.opening_bracket:
                            b += 1
                        if tokens[j].type == TokenType.closing_bracket:
                            b -= 1
                        if b != 0:
                            subtree_tokens.append (tokens[j])
                        j += 1

                    subtree_rootnode = self.build_tree (subtree_tokens)
                    subtree_rootnode.concept.subroot = True
                    if node != None:
                        node.children.append (subtree_rootnode)
                    else:
                        return None
                    i = j - 1
            elif tokens[i].type == TokenType.closing_bracket:
                inside_brackets = False
            elif tokens[i].type == TokenType.comma:
                if inside_brackets == True:
                    node = common_parent
            elif tokens[i].type == TokenType.equal_sign:
                pass
            else:
                parent_node = node
                node = PropositionTreeNode ()
                node.parent = parent_node
                node.text = tokens[i].text
                if tokens[i].type == TokenType.concept:
                    node.type = PropositionTreeNodeType.concept
                    node.side = PropositionTreeNodeSide.right
                    node.concept = TreeNodeConcept ()
                    node.concept.id = tokens[i].concept.id
                    node.concept.name = tokens[i].concept.name
                    node.concept.type = tokens[i].concept.type
                elif tokens[i].type == TokenType.linkage:
                    node.type = PropositionTreeNodeType.linkage
                    node.side = PropositionTreeNodeSide.right
                    node.linkage = TreeNodeLinkage ()
                    node.linkage.id = tokens[i].linkage.id
                    node.linkage.name = tokens[i].linkage.name
                elif tokens[i].type == TokenType.underscore:
                    node.type = PropositionTreeNodeType.underscore
                elif tokens[i].type == TokenType.number:
                    node.type = PropositionTreeNodeType.number
                elif tokens[i].type == TokenType.string:
                    node.type = PropositionTreeNodeType.string
                #print node.text
                parent_node.children.append (node)
            i += 1

        return root_node

    def get_error_text (self):
        return self.__error_text
