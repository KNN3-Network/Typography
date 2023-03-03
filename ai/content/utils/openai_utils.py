import random
import openai
from content.configs.global_configs import OpenAiConfigs as cfg

def sub(m,**kwargs):
    for _ in range(3):
        try:
            openai.api_key = random.choice(cfg.keys)
            r = m(**kwargs)
            return r
        except:
            continue

def submit_easy(prompt, temperature=0.7, max_tokens=4000, stop=None, n=1):
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

def submit_easy_chat(messages, temperature=0.7, max_tokens=4000, stop=None, n=1):
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
    pass