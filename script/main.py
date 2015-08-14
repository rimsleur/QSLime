#!/usr/bin/python
# coding: utf8
"""
Точка входа
"""

import MySQLdb
import sys
from CodeStack import CodeStack
from SemanticAnalyzer import SemanticAnalyzer
from SyntaxAnalyzer import SyntaxAnalyzer
from ErrorHelper import ErrorHelper
from MemoryProvider import MemoryProvider

reload (sys)

def main (text):
    db = MySQLdb.connect (host="localhost", user="qslbase", passwd="1q2w3e", db="qslbase", charset="utf8")
    cursor = db.cursor ()
    sys.setdefaultencoding ("utf8")
    code_stack = CodeStack ()
    syntax_analyzer = SyntaxAnalyzer (cursor)
    semantic_analyzer = SemanticAnalyzer (cursor, code_stack)
    result = ""
        
    ErrorHelper (cursor)
    MemoryProvider ()

    #print text
    if syntax_analyzer.analize (text):
        #syntax_analyzer.proposition_tree.print_tree ()
        if semantic_analyzer.analize (syntax_analyzer.proposition_tree, None):
            #semantic_analyzer.proposition_tree.print_tree ()
            result += semantic_analyzer.result
        else:
            return semantic_analyzer.get_error_text ()
    else:
        return syntax_analyzer.get_error_text ()

    code_line = code_stack.pop ()
    while (code_line != None):
        #print code_line.text
        if syntax_analyzer.analize (code_line.text):
            #syntax_analyzer.proposition_tree.print_tree ()
            if semantic_analyzer.analize (syntax_analyzer.proposition_tree, code_line):
                #semantic_analyzer.proposition_tree.print_tree ()
                result += semantic_analyzer.result
            else:
                return semantic_analyzer.get_error_text ()
        else:
            return syntax_analyzer.get_error_text ()
        code_line = code_stack.pop ()
    return result

print main(sys.argv[1])
