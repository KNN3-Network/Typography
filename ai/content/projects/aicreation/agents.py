import json
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from content.utils import openai_utils as ai
from content.db import mysql_db as mdb
from content.utils import string_utils as su
import random
class BaseAgent():

    def __init__(self):
        self.nlp_sql_template = 'select prompt,temperature,model,n,stop,max_tokens,top_p,presence_penalty,frequency_penalty from openai_nlp_request_parameters where `key`="{}"'
        self.image_sql_template = 'select prompt, n, response_format from openai_image_request_parameters where `key`="{}"'
        self.chat_sql_template = 'select messages,temperature,model,n,stop,max_tokens,top_p,presence_penalty,frequency_penalty from openai_chat_request_parameters where `key`="{}"'
        self.size_map ={1:'256x256',2:'512x512',3:'1024x1024'}

    def read_default_chat_params(self,key='default'):
        params = mdb.PandasDB().read_sql(self.chat_sql_template.format(key))
        d = params.to_dict()
        d = {k: d[k][0] for k in d}
        d['messages'] = json.loads(d['messages'])
        return d
    def get_chat_params(self,key='default',*formats):
        params = self.read_default_chat_params(key)
        params['messages'][0]['content'] = params['messages'][0]['content'].format(*formats)
        return params

    def read_default_nlp_params(self,key='default'):
        params = mdb.PandasDB().read_sql(self.nlp_sql_template.format(key))
        d = params.to_dict()
        return {k: d[k][0] for k in d}

    def read_default_image_params(self,key='default'):
        params = mdb.PandasDB().read_sql(self.image_sql_template.format(key))
        d = params.to_dict()
        return {k: d[k][0] for k in d}
#openai.error.RateLimitError: Rate limit reached for default-gpt-3.5-turbo in organization org-8WfCx8Ph6iLsz0B1BGrYtfVS on requests per min. Limit: 20 / min. Current: 30 / min. Contact support@openai.com if you continue to have issues. Please add a payment method to your account to increase your rate limit. Visit https://platform.openai.com/account/billing to add a payment method.

class ArticleGenerationAgent(BaseAgent):

    def __init__(self):
        super().__init__()
        self.system_role = {"role": "system",
                            "content": "You are an article generation assistant, "
                                       "if you can't generate article according to user comments, "
                                       "you just generate randomly. What you give to user is only the article, "
                                       "do not say anything else!"}

    def first_generation(self, uimport):
        params = self.get_chat_params('first_article_generate',uimport)
        params['messages'].insert(0,self.system_role)
        params['stream'] = True
        r = ai.submit_chat_stream(**params)
        return r

    def generation(self, uimport, post):
        params = self.get_chat_params('article_generate', uimport)
        params['messages'].insert(0,{"role": "assistant", "content": post})
        params['messages'].insert(0, self.system_role)
        params['stream'] = True
        r = ai.submit_chat_stream(**params)
        return r

class ContextAnalysisAgent(BaseAgent):

    def __init__(self):
        super().__init__()

    def analysis(self, s,context, keys):
        params = self.get_chat_params('analyze',s,','.join(keys), ','.join(keys))
        context = context[:-1]
        context.append(params['messages'][0])
        params['messages'] = context
        r = ai.submit_chat(**params)[0].strip()
        try:
            r = su.get_braces_as_json(r)
        except:
            r = {k: round(random.random(),2) for k in keys}
        return r

class PhaseControlAgent():
    def __init__(self):
        super().__init__()

    def control(self,phase,keys,hf,k,times):
        print('{},type:{}'.format(phase,type(phase)))
        flag = False
        if phase==0 and times>0:
            if times>=3:
                return True
            if len(keys)>0 and hf and k:
                if k not in keys or su.sum_dict(hf)>0.9*len(hf):
                    flag = True
                else:
                    flag = False
            else:
                flag = True

        return flag

class ReplyGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def reply(self, k, post,context):
        params = self.get_chat_params('reply', post, k)
        context = context[:-1]
        context.append(params['messages'][0])
        params['messages'] = context
        r = ai.submit_chat(**params)[0].strip()
        return r

    def random_reply(self, post,context):
        params = self.get_chat_params('random_reply', post)
        context = context[:-1]
        context.append(params['messages'][0])
        params['messages'] = context
        r = ai.submit_chat(**params)[0].strip()
        return r

class ImagePromptGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def first_generation(self, post):
        params = self.get_chat_params('first_imgprt', post)
        r = ai.submit_chat(**params)[0].strip()
        return r

    def generation(self, uimport, image_prompt):
        params = self.get_chat_params('imgprt', image_prompt,uimport)
        r = ai.submit_chat(**params)[0].strip()
        return r

class ImageGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def generate_image(self, prompt, n=1, size_type=1):
        params = self.read_default_image_params()
        params['prompt'] = prompt
        params['size'] = self.size_map[size_type]
        params['n'] = n
        r = ai.submit_image(**params)
        return [i['b64_json'] for i in r['data']]
class ImageVariationAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def generate_image_variation(self, image, n=3, size_type=1):
        params = self.read_default_image_params()
        params['image'] = image
        params['size'] = self.size_map[size_type]
        params['n'] = n
        del params['prompt']
        r = ai.submit_image_variation(**params)
        return r

