
from flask import request

def getArgs(t):
    a = None
    d = request.json
    if d:
        a = d.get(t)
    if not a:
        a = request.args.get(t)
    if not a :
        a = request.form.get(t)
    return a
