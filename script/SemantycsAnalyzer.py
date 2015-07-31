# coding: utf8
"""
Семантический анализатор
"""

class SemantycsAnalyzer ():

    def __init__ (self, triads, cursor, major_linkage_id, idx):
        self.triads = triads
        self.cursor = cursor
        self.major_linkage_id = major_linkage_id
        self.idx = idx
        self.triad_count = len (triads)  
        self.idx = self.major_linkage_id
        self.triad1_id = 0
        self.triad2_id = 0
        self.proposition_id = 0

        while self.idx <= self.triad_count:
            query = "SELECT id FROM qsl_triad WHERE left_concept_id = " + str (self.triads[self.idx-1].left_concept.id)
            query += " AND linkage_id = " + str (self.triads[self.idx-1].linkage_id)
            query += " AND right_concept_id = " + str (self.triads[self.idx-1].right_concept.id) + ";"
            self.cursor.execute (query)
            row = cursor.fetchone ()
            if row != None:
                if self.triad1_id == 0:
                    self.triad1_id = row[0]
                else:
                    if self.triad2_id != 0:
                        self.triad1_id = self.triad2_id
                    self.triad2_id = row[0]
            else:
                if self.idx == self.major_linkage_id:
                    break

            if self.triad1_id != 0 and self.triad2_id != 0:
                query = "SELECT proposition_id FROM qsl_sequence WHERE"
                query += " left_triad_id = " + str (self.triad1_id)
                query += " AND right_triad_id = " + str (self.triad2_id)
                if self.proposition_id != 0:
                    query += " AND proposition_id = " + str (self.proposition_id)
                query += ";"
                self.cursor.execute (query)
                row = self.cursor.fetchone ()
                if row != None:
                    self.proposition_id = row[0]

            self.idx += 1

        self.res = ""

        if self.proposition_id != 0:
            query = "SELECT text FROM qsl_proposition WHERE id = " + str (self.proposition_id) + ";"
            self.cursor.execute (query)
            row = self.cursor.fetchone ()
            if row != None:
                self.res = row[0]

        if self.res == "":
            self.res = "Информация отсутствует"
