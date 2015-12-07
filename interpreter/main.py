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
from DebuggerProvider import DebuggerProvider

reload (sys)

def main (single_run, use_ctl, use_dbg, text):
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
    DebuggerProvider ()

    if single_run == False:
        stdin = os.open ("/tmp/qslime-std-in", os.O_RDONLY | os.O_NONBLOCK)
        stdout = os.open ("/tmp/qslime-std-out", os.O_WRONLY)
    if use_ctl == True:
        ctlout = os.open ("/tmp/qslime-ctl-out", os.O_WRONLY)
        ctlin = open ("/tmp/qslime-ctl-in", "r")
    if use_dbg == True:
        dbgout = os.open ("/tmp/qslime-dbg-out", os.O_WRONLY)
        dbgin = open ("/tmp/qslime-dbg-in", "r")
        DebuggerProvider.dbgin = dbgin
        DebuggerProvider.dbgout = dbgout
    if use_ctl == True:
        text = ctlin.readline ()
        if text != "":
            if SyntaxAnalyzer.analize (text):
                #PropositionTree.print_tree (SyntaxAnalyzer.proposition_tree)
                if semantic_analyzer.analize (SyntaxAnalyzer.proposition_tree, None):
                    #semantic_analyzer.proposition_tree.print_tree ()
                    result += semantic_analyzer.result
                    os.write (ctlout, 'OK.\n')
                else:
                    os.write (ctlout, semantic_analyzer.get_error_text () + '\n')
            else:
                os.write (ctlout, semantic_analyzer.get_error_text () + '\n')
    else:
        if text != "":
            DebuggerProvider.reset ()
            DebuggerProvider.append_code_line (text)
            data = DebuggerProvider.build_debug_data ()
            os.write (dbgout, (data + u'\n').encode ("utf-8"))
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
            #print code_line.text
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
                    if CodeProvider.is_priorities_assigned () == False:
                        CodeProvider.assign_priorities ()
                    TriggerProvider.dispatch_triggers ()
                    ConditionProvider.dispatch_conditions ()
                    CodeStack.sort ()
            code_line = CodeStack.pop ()

            if result != "" and single_run == False:
                #print result
                os.write (stdout, result)
                result = ""
                exit = True

        if single_run == True:
            return result

    os.close (stdin)
    os.close (stdout)
    os.close (ctlin)
    os.close (ctlout)
    os.close (dbgin)
    os.close (dbgout)

single_run = False
use_ctl = False
use_dbg = False
text = ""
argi = 0
for arg in sys.argv:
    argi += 1
    if arg == "-1":
        single_run = True
    elif arg == "-c":
        use_ctl = True
    elif arg == "-d":
        use_dbg = True
    elif argi > 1:
        text = arg
if single_run == True:
    print main (single_run, use_ctl, use_dbg, text)
else:
    main (single_run, use_ctl, use_dbg, text)