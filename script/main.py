#!/usr/bin/python
# coding: utf8
"""
Точка входа
"""

import sys
import os
import MySQLdb
from CodeStack import CodeStack
from SemanticAnalyzer import SemanticAnalyzer
from SyntaxAnalyzer import SyntaxAnalyzer
from ErrorHelper import ErrorHelper
from MemoryProvider import MemoryProvider
from ContextProvider import ContextProvider
from TriggerProvider import TriggerProvider
from ConditionProvider import ConditionProvider
from CodeProvider import CodeProvider
from PropositionTree import PropositionTree

reload (sys)

def main (single_run, text):
    exit = False
    db = MySQLdb.connect (host="localhost", user="qslbase", passwd="qslbase", db="qslbase", charset="utf8")
    cursor = db.cursor ()
    result = ""
    sys.setdefaultencoding ("utf8")
    SyntaxAnalyzer (cursor)
    semantic_analyzer = SemanticAnalyzer (cursor)
    CodeProvider (cursor)
    CodeStack ()
    ErrorHelper (cursor)
    MemoryProvider ()
    ContextProvider ()
    TriggerProvider ()
    ConditionProvider ()

    if single_run == False:
        pipein = os.open("/tmp/qlp-tube", os.O_RDONLY | os.O_NONBLOCK)
        pipeout = os.open("/tmp/qlpterm-tube", os.O_WRONLY)

    #print text
    if SyntaxAnalyzer.analize (text):
        #syntax_analyzer.proposition_tree.print_tree ()
        if semantic_analyzer.analize (SyntaxAnalyzer.proposition_tree, None):
            #semantic_analyzer.proposition_tree.print_tree ()
            result += semantic_analyzer.result
        else:
            return semantic_analyzer.get_error_text ()
    else:
        return SyntaxAnalyzer.get_error_text ()

    while (exit != True):
        code_line = CodeStack.pop ()
        while (code_line != None):
            print code_line.text
            analized = True
            if code_line.tree == None:
                analized = SyntaxAnalyzer.analize (code_line.text)
                tree = SyntaxAnalyzer.proposition_tree
            else:
                tree = code_line.tree
            if analized:
                #tree.print_tree ()
                if semantic_analyzer.analize (tree, code_line):
                    #tree.print_tree ()
                    if code_line.tree != None:
                        if code_line.tree.is_totally_parsed == False:
                            code_line.tree = semantic_analyzer.proposition_tree
                            code_line.tree.is_totally_parsed = True
                    result += semantic_analyzer.result
                else:
                    return semantic_analyzer.get_error_text ()
            else:
                return SyntaxAnalyzer.get_error_text ()
            if CodeStack.is_empty () == True:
                if CodeStack.inside_procedure == False:
                    TriggerProvider.dispatch_triggers ()
                    ConditionProvider.dispatch_conditions ()
                    CodeStack.sort ()
            code_line = CodeStack.pop ()

            if result != "" and single_run == False:
                #print result
                os.write (pipeout, result)
                result = ""
                exit = True

        if single_run == True:
            return result

    os.close (pipeout)
    os.close (pipein)

single_run = False
for arg in sys.argv:
    if arg == "-1":
        single_run = True
    else:
        text = arg
if single_run == True:
    print main(single_run, text)
else:
    main(single_run, text)
