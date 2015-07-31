#!/usr/bin/python
# coding: utf8
"""
Точка входа
"""

import MySQLdb
import sys
from SemantycsAnalyzer import SemantycsAnalyzer
from SyntaxAnalyzer import SyntaxAnalyzer

reload (sys)

def main (text):
    db = MySQLdb.connect (host="localhost", user="qslbase", passwd="1q2w3e", db="qslbase", charset="utf8")
    cursor = db.cursor ()

    sys.setdefaultencoding ("utf8")

    syntax_analyzer = SyntaxAnalyzer (cursor)
    if syntax_analyzer.analize (text):
        syntax_analyzer.proposition_tree.print_tree ()
    else:
        print syntax_analyzer.get_error_text ()

    #triads = synObj.triads
    #major_linkage_id = synObj.major_linkage_id
    #idx = synObj.idx

    #semObj = SemantycsAnalyzer(triads, cursor, major_linkage_id, idx)

    #return  semObj.res


print main(sys.argv[1])
