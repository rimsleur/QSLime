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

class SyntaxAnalyzer ():

    def __init__ (self, cursor):
        self.proposition_tree = None
        self.__cursor = cursor
        self.__error_text = ""

    def analize (self, text):
        word = []
        tokens = []
        after_space = False
        after_linkage = False

        # Разбивка на токены
        for letter in text:
            if letter == "?" and after_space == True:
                token = Token ()
                token.text = ''.join (word)
                tokens.append (token)
                word = []
                after_linkage = True
            after_space = False
            if letter == " ":
                after_space = True
                if after_linkage == True:
                    token = Token ()
                    token.text = ''.join (word)
                    tokens.append (token)
                    word = []
                else:
                    word.append (letter)
                after_linkage = False
            else:
                word.append (letter)

        token = Token ()
        token.text = ''.join (word)
        if token.text != "":
            token.text = token.text.replace ('?', '')
            tokens.append (token)

        # Идентификация токенов
        for token in tokens:
            if token.text.find ('?') == 0:
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
                    self.__error_text = "#102:Неизвестное имя линката '" + token.text + "'"
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
                    self.__error_text = "#103:Неизвестное имя понятия '" + token.text + "'"
                    return False

        # Поиск главного понятия действия
        idx = 0
        node = None
        for token in tokens:
            if token.type == TokenType.concept:
                if token.concept.type == TokenConceptType.action:
                    self.proposition_tree = PropositionTree ()
                    node = PropositionTreeNode ()
                    #node.type = 
                    node.text = token.text
                    self.proposition_tree.root_node = node
                    break
            idx += 1

        if node == None:
            self.__error_text = "#101:Понятие действия в суждении не найдено"
            return False

        # Обработка левой ветки суждения
        i = idx - 1
        while i >= 0:
            parent_node = node
            node = PropositionTreeNode ()
            node.parent = parent_node
            node.text = tokens[i].text
            #print node.text
            parent_node.children.append (node)
            i -= 1

        # Обработка правой ветки суждения
        i = idx + 1
        node = self.proposition_tree.root_node
        while i < len (tokens):
            parent_node = node
            node = PropositionTreeNode ()
            node.parent = parent_node
            node.text = tokens[i].text
            #print node.text
            parent_node.children.append (node)
            i += 1

        return True

    def get_error_text (self):
        return self.__error_text
