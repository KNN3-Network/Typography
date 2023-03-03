import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from content.projects.aicreation.agents import *
from content.projects.aicreation import s3manager as s3m
from content.utils import string_utils as su
import random
import base64
from uuid import uuid4
from content.db import kafka_mq as kmq
from content.projects.aicreation import configs as cfg

# https://github.com/KNN3-Network/Typography


class BaseChat():

    def __init__(self,mq_flag=True):
        self.first_GQ = "I'm an AI-assisted author, can you tell me what kind of article you want to create? You can also tell me the key elements to be included in the article, the personal perspective, the target audience, the type of subject matter, the style of the article, etc"
        self.move_str = 'And also you can click the button below to move next phase if your want.'
        self.reply_begin_template = 'The article has been {} by your {}.'
        self.requirements = ['requirement','comment','command','demand']
        self.mq_flag = mq_flag
        if self.mq_flag:
            self.producer = kmq.Producer()
        self.times = 0


    def get_min_hf(self, hf, keys):
        try:
            k = min(hf, key=lambda x: float(hf[x]))
        except:
            k = random.choice(keys)
        if k in keys:
            keys.remove(k)
        return k

    def get_gc(self,s,reply_begin,control_str,times):
        ls = s.strip().split('\n')
        ai = ls[0].strip()[3:].strip()
        if ai.startswith(':'): ai = ai[1:].strip()
        if times<2 and control_str=='':
            ai = reply_begin+ ' '+ ai
        else:
            ai = ai + ' ' + control_str

        demos = []
        for l in ls[1:]:
            if l.strip()=='':continue
            demo = l.strip()[6:].strip()
            if demo.startswith(':'): demo = demo[1:].strip()
            demos.append(demo)

        return ai,demos


    def iter_gen(self,gen,trace_id):
        begin = False
        find_ = False
        post = ''
        for g in gen:
            t = g['choices'][0]['delta'].get('content')
            if t==None:continue
            if find_ and t!=':':
                continue
            else:
                find_ = False

            if begin == False and t in ['Here','Randomly']:
                find_ = True
                continue
            else:
                begin = True

            print(t,end='')
            d = {'token':t,'traceId':trace_id}
            if self.mq_flag:
                self.producer.send(cfg.TOPIC_ARTICLE,d)
            post+=t
        if self.mq_flag:
            d = {'token': '<end>', 'traceId': trace_id}
            self.producer.send(cfg.TOPIC_ARTICLE, d)
        print()
        return post


class ArticleChat(BaseChat):

    def __init__(self,mq_flag=True):
        super().__init__(mq_flag)
        self.aga = ArticleGenerationAgent()
        self.rga = ReplyGenerationAgent()
        self.pca = PhaseControlAgent()
        self.caa = ContextAnalysisAgent()

    def chat(self,s,post,phase,uid,traceid,con_id,keys,context,is_cold):
        context.append({'role': 'user', 'content':  s})
        print('phase control...')
        hf,k = None,None
        if len(keys)>0:
            hf = self.caa.analysis(s,context,keys)
            print(hf)
            if hf!=None and hf!={} and hf!='':
                k = self.get_min_hf(hf,keys)
        move_flag = self.pca.control(phase,keys, hf, k,self.times)
        print(move_flag)
        control_str = self.move_str if move_flag else ''

        print('Generating article...')
        if is_cold:
            gen = self.aga.first_generation(s)
            post = self.iter_gen(gen,traceid)
            reply_begin = self.reply_begin_template.format('created',random.choice(self.requirements))
            is_cold = False
        else:
            gen = self.aga.generation(s, post)
            post = self.iter_gen(gen,traceid)
            reply_begin = self.reply_begin_template.format('modified',random.choice(self.requirements))

        print('Generating ai reply...')
        if len(keys)>0:
            gc = self.rga.reply(k,post,context)
        else:
            gc = self.rga.random_reply(post,context)
        ai,demos = self.get_gc(gc,reply_begin,control_str,self.times)
        d = {'reply':ai,'examples':demos[:3],'traceId':traceid,'movePhase':1 if move_flag else 0}
        context.append({'role': 'assistant', 'content': ai})
        if len(context)>6:
            context = context[2:]
        print(d)
        if self.mq_flag:
            self.producer.send(cfg.TOPIC_REPLY, d)
        self.times +=1


        return context,keys,is_cold,post

class Image():

    def __init__(self):
        super().__init__()
        self.ipga = ImagePromptGenerationAgent()
        self.iga = ImageGenerationAgent()

    def chat(self,post,uid,con_id):
        print('generate image prompt')
        imp = self.ipga.first_generation(post)
        print('generate image')
        image = self.iga.generate_image(imp,1)[0]
        image = base64.b64decode(image)
        print('image update')
        url = s3m.update_one_img(image,uid,con_id)
        return url



class ImageChat(BaseChat):

    def __init__(self):
        super().__init__()
        self.ipga = ImagePromptGenerationAgent()
        self.iga  = ImageGenerationAgent()
        self.rga = ReplyGenerationAgent()
        self.caa = ContextAnalysisAgent()
        self.is_cold_start = True
        self.keys = ['key elements', 'artistic mood', 'image style']

    def chat(self,s,post,imp,uid=None,traceid=None):
        pass


class Chat():

    def __init__(self,conId,mq_flag=True):
        self.con_id = conId
        self.artchat = ArticleChat(mq_flag)
        self.imgchat = Image()
        self.is_cold_start = True
        self.keys = ['key elements', 'artistic mood', 'article style']
        #self.context = [{"role": "system", "content": "You are a helpful assistant."}]
        self.context = []

    def chat(self,input,post,phase,uid,traceid):
        self.context,self.keys,self.is_cold_start,post = self.artchat.chat(input,post,phase,uid=uid,traceid=traceid,con_id=self.con_id,keys=self.keys,context=self.context,is_cold=self.is_cold_start)
        return post

    def image(self,post,uid):
        url = self.imgchat.chat(post,uid,self.con_id)
        return url

class Play():

    def __init__(self,mq_flag=True):
        self.mq_flag = mq_flag
        self.conId = None
        self.C = None

    def chat(self,input,post,phase,uid,traceid,conid):
        if conid!=self.conId:
            self.C = Chat(conid,self.mq_flag)
            self.conId = conid
        return self.C.chat(input,post,phase,uid,traceid)

    def image(self,post,uid,conid):
        if conid != self.conId: self.C = Chat(conid,self.mq_flag)
        return self.C.image(post,uid)



def play():
    p = Play(False)
    conid = 3
    post = None
    phase = 0
    uid = 1
    traceid = 2
    while True:
        print('Please input...')
        s = input()
        post = p.chat(s,post,phase,uid,traceid,conid)

def TryImg(p):
    c=Chat(str(uuid4()))
    url = c.image(p,'')
    print(url)

if __name__ == '__main__':
    play()
