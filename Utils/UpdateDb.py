import os

import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)

from DB.DataBase import SQLDB

db=SQLDB()
inp=raw_input("select option           1- SetPrgid   2- setavilability  avilable  3- setavilability  notavilable")
if(inp=="1"):
    ms=raw_input("PrgNew :- ")
    db.setPrgID(ms)
if(inp=="2"):
    db.setStatus(True)

if(inp=="3"):
    db.setStatus(False)
