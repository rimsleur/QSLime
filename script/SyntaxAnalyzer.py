#!/usr/bin/python
# coding: utf8

class SyntaxAnalyzer():
    def __init__(self,text,cursor):
        class Concept:
            id = 0
            name = 0
            type = 0
        class Triad:
            linkage_id = 0
            linkage_name = ""
            left_concept = Concept ()
            right_concept = Concept ()
        self.word = []
        self.tokens = []
        self.triads = []
        self.major_linkage_id = 0
        self.text = text
        self.cursor = cursor
        self.after_space = False
        self.after_linkage = False
        self.left_concept = Concept ()
        for letter in self.text:
            if letter == "?" and self.after_space == True:
                token = ''.join (self.word)
                self.tokens.append (token)
                self.word = []
                self.after_linkage = True
            self.after_space = False
            if letter == " ":
                self.after_space = True
                if self.after_linkage == True:
                    token = ''.join (self.word)
                    self.tokens.append (token)
                    self.word = []
                else:
                    self.word.append (letter)
                self.after_linkage = False
            else:
                self.word.append (letter)

        token = ''.join (self.word)
        if token != "":
            token = token.replace ('?', '')
            self.tokens.append (token)
    # Построение списка триад
        self.linkage_filled = False
        self.idx = 1

        for token in self.tokens:
            if token.find ('?') == 0:
                triad = Triad ()
                s = token.replace ('?', '')
                query = "SELECT id FROM qsl_linkage WHERE name = \'" + s + "\';"
                self.cursor.execute (query)
                row = cursor.fetchone ()
                if row != None:
                    triad.linkage_id = row[0]
                triad.linkage_name = token
                triad.left_concept = Concept ()
                triad.right_concept = Concept ()
                triad.left_concept.id = self.left_concept.id
                triad.left_concept.name = self.left_concept.name
                self.linkage_filled = True
            else:
                if self.linkage_filled == True:
                    self.linkage_filled = False
                    if token != "_":
                        query = "SELECT id, type FROM qsl_concept WHERE name = \'" + token + "\';"
                        self.cursor.execute (query)
                        row = cursor.fetchone ()
                        if row != None:
                            triad.right_concept.id = row[0]
                            triad.right_concept.type = row[1]
                        if triad.right_concept.type == 1:
                            self.major_linkage_id = self.idx
                            self.idx += 1
                    triad.right_concept.name = token
                    self.left_concept.id = triad.right_concept.id
                    self.left_concept.name = triad.right_concept.name
                    self.triads.append (triad)
                else:
                    if token != "_":
                        query = "SELECT id, type FROM qsl_concept WHERE name = \'" + token + "\';"
                        self.cursor.execute (query)
                        row = cursor.fetchone ()
                        if row != None:
                            self.left_concept.id = row[0]
                            self.left_concept.type = row[1]
                    self.left_concept.name = token
