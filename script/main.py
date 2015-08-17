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
from ContextProvider import ContextProvider
from EventProvider import EventProvider
from ConditionProvider import ConditionProvider

reload (sys)

def main (text):
    db = MySQLdb.connect (host="localhost", user="qslbase", passwd="1q2w3e", db="qslbase", charset="utf8")
    cursor = db.cursor ()
    result = ""
    sys.setdefaultencoding ("utf8")
    syntax_analyzer = SyntaxAnalyzer (cursor)
    semantic_analyzer = SemanticAnalyzer (cursor)
    CodeStack ()
    ErrorHelper (cursor)
    MemoryProvider ()
    ContextProvider ()
    EventProvider ()
    ConditionProvider ()

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

    code_line = CodeStack.pop ()
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
        ConditionProvider.dispatch_conditions ()
        EventProvider.dispatch_events ()
        code_line = CodeStack.pop ()
    return result

print main(sys.argv[1])
