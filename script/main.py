#!/usr/bin/python
# coding: utf8
"""
Точка входа
"""

import MySQLdb
import sys
from SemanticAnalyzer import SemanticAnalyzer
from SyntaxAnalyzer import SyntaxAnalyzer

reload (sys)

def main (text):
    db = MySQLdb.connect (host="localhost", user="qslbase", passwd="1q2w3e", db="qslbase", charset="utf8")
    cursor = db.cursor ()

    sys.setdefaultencoding ("utf8")

    syntax_analyzer = SyntaxAnalyzer (cursor)
    if syntax_analyzer.analize (text):
        syntax_analyzer.proposition_tree.print_tree ()
        semantic_analyzer = SemanticAnalyzer (cursor, syntax_analyzer.proposition_tree)
        if semantic_analyzer.analize ():
            semantic_analyzer.proposition_tree.print_tree ()
            return semantic_analyzer.result
        else:
            return semantic_analyzer.get_error_text ()
    else:
        return syntax_analyzer.get_error_text ()

print main(sys.argv[1])
