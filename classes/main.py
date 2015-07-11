#!/usr/bin/python
# coding: utf8
import MySQLdb
import sys
from semantycs import SemantycsAnalyzer
from syntax import SyntaxAnalyzer

reload(sys)

def main (text):
    db = MySQLdb.connect (host="localhost", user="qslbase", passwd="1q2w3e", db="qslbase", charset="utf8")
    cursor = db.cursor()

    sys.setdefaultencoding("utf8")

    synObj = SyntaxAnalyzer(text, cursor)
    triads = synObj.triads
    major_linkage_id = synObj.major_linkage_id
    idx = synObj.idx

    semObj = SemantycsAnalyzer(triads, cursor, major_linkage_id, idx)

    return  semObj.res


print main(sys.argv[1])
