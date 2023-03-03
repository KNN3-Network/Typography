# -*- coding: utf-8 -*-
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from flask import Flask,jsonify,request
from content.utils import servier_utils as sf
import traceback
from content.projects.aicreation.main import Play
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(1)

app = Flask(__name__)
P = Play()
@app.route('/hello',methods=['get'])
def index():
    return 'hello'

def chat_job(input,article,phase,uid,traceId,conid):
    try:
        P.chat(input,article,phase,uid,traceId,conid)
    except Exception as e:
        err = traceback.format_exc()
        print(err)

@app.route('/chat',methods=['POST'])
def chat():
    r={}
    try:
        uid = sf.getArgs('user')
        traceId = sf.getArgs('traceId')
        input = sf.getArgs('input')
        article = sf.getArgs('article')
        phase = sf.getArgs('phase')
        phase = int(phase) if phase and phase!='' else 0
        conid = sf.getArgs('conId')
        executor.submit(chat_job,input,article,phase,uid,traceId,conid)
        r['ok'] = 1
    except Exception as e:
        r['ok'] = 0
        r['msg'] = traceback.format_exc()
    return jsonify(r)

@app.route('/image',methods=['POST'])
def image():
    r={}
    try:
        uid = sf.getArgs('user')
        traceId = sf.getArgs('traceId')
        article = sf.getArgs('article')
        conId = sf.getArgs('conId')
        url = P.image(article,uid,conId)
        r['ok'] = 1
        r['image'] = url
    except Exception as e:
        r['ok'] = 0
        r['msg'] = traceback.format_exc()
    return jsonify(r)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000,debug=False)