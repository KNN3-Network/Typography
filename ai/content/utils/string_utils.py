import json
import re

def isNone(d):
    return d==None or d=='' or d==[] or d=={} or d==set() or d==()

def get_int(s,defalt):
    return int(s) if s is not None and s!='' else defalt

def get_braces_as_json(s):
    print(s)
    s=s.replace('\n','')
    result = re.findall(r"\{(.+?)\}",s.strip())
    if len(result)>0:
        return json.loads("{"+result[0]+"}")
    else:
        return {}


def sum_dict(d):
    return sum([float(i) for i in d.values()])

if __name__ == '__main__':
    d={'a':'1','b':2}
    print(d.values())
    print(sum_dict(d))