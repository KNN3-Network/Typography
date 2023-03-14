import random
import traceback
import time
import openai
from content.configs.global_configs import OpenAiConfigs as cfg
from content.utils.log_utils import logger

def sub(m,**kwargs):
    logger.info(kwargs)
    for _ in range(2):
        try:
            #openai.api_key = random.choice(cfg.keys)
            openai.api_key = cfg.keys[0]
            r = m(**kwargs)
            return r
        except:
            logger.error(traceback.format_exc())
            time.sleep(0.1)
            continue

def submit_easy(prompt, temperature=0.7, max_tokens=512, stop=None, n=1):
    openai.api_key = cfg.keys[0]
    response = openai.Completion.create(
      model = "text-davinci-003",
      prompt = prompt,
      temperature = temperature,
      max_tokens = max_tokens,
      stop = stop,
      top_p = 1,
      n = n,
      frequency_penalty = 0,
      presence_penalty = 0
    )
    return response
    #return response.get('choices')[0].get('text')

def submit_easy_chat(messages, temperature=0.7, max_tokens=512, stop=None, n=1):
    openai.api_key = cfg.keys[0]
    response = openai.ChatCompletion.create(
      model = "gpt-3.5-turbo-0301",
      messages = messages,
      temperature = temperature,
      max_tokens = max_tokens,
      stop = stop,
      top_p = 1,
      n = n,
      stream = False,
      frequency_penalty = 0,
      presence_penalty = 0
    )
    return response

def submit(**kwargs):
    response = sub(openai.Completion.create,**kwargs)
    return [t.get('text') for t in response.get('choices')]

def submit_chat(**kwargs):
    response = sub(openai.ChatCompletion.create,**kwargs)
    return [t.get('message').get('content') for t in response.get('choices')]

def submit_chat_stream(**kwargs):
    response = sub(openai.ChatCompletion.create, **kwargs)
    return response

def submit_stream(**kwargs):
    response = sub(openai.Completion.create, **kwargs)
    return response

def submit_image(**kwargs):
    response = sub(openai.Image.create, **kwargs)
    return response

def submit_image_variation(**kwargs):
    response = sub(openai.Image.create_variation, **kwargs)
    return response


if __name__ == '__main__':




    create = '用户命令: 创建关于狗的文章 \n 请根据用户的命令生成一句用以给chatgpt生成文章的prompt,若无法生成则返回false.' \
             '以json格式返回,key是 prompt, can_or_not.'
    messages = [{'role':'system','content':'你是一个创造用以给chatgpt生成文章prompt的助手。'},{'role': 'user', 'content': create}]

    messages = [{'role': 'system', 'content': '你是一个创建文章的助手，每次生成的文章都很简短。'},
                {'role': 'user', 'content': "写一篇关于狗的文章。"}]

    s = '狗是人类最忠诚的朋友之一。这些可爱的动物在我们的生活中扮演着重要的角色，不仅能够给人们带来欢乐，还能作为伴侣、看门狗以及服务动物。' \
        '\n狗是一种非常聪明的动物，有很强的学习能力。他们可以通过训练学会一些基本的技能，例如：坐下、待命、握手等。在军队和警察部门中，狗也被广泛应用，可以用来追踪嫌疑人、查找炸弹等。' \
        '\n狗也是一种非常友好和亲密的动物。他们可以成为人类的朋友，陪伴我们度过孤独的时刻。许多人把狗当做家庭的一员，他们会为狗提供舒适的床铺、美味的食物、以及充足的运动时间。' \
        '\n除此之外，狗还可以作为服务动物，为那些有残疾的人提供帮助。例如：导盲犬可以帮助视力障碍者行走，助听犬可以帮助听力障碍者听到声音。' \
        '\n总之，狗是一种非常重要的动物，在我们的生活中扮演着不可替代的角色。我们应该珍惜和爱护他们，与他们建立深厚的友谊。'

    messages = [{'role': 'system', 'content': '你是一个创造用以给chatgpt修改文章prompt的助手。例如: “用户命令:加个猫”，返回：“请给文章加个猫的内容”。以json格式返回,key是 prompt, can_or_not.'},
                #{'role':'assistant','content':s},
                {'role': 'user', 'content': "用户命令: 加个猫 \n 请根据用户的命令生成一句用以给chatgpt修改文章的prompt,若无法生成则返回false.' \
             '以json格式返回,key是 prompt, can_or_not."}]
    from tqdm import tqdm
    for i in tqdm(range(50)):
        r = submit_easy_chat(messages)
        #print(r['choices'][0]['message']['content'])