from content.db import redis_db as rdb


ARTICLE_KEYS = 'tg:article_keys'
IMAGE_KEYS = 'tg:image_keys'
AI_PHASE ='tg:ai_phase'


r = rdb.Redis()

KEY_MAP = {
    'article':ARTICLE_KEYS,
    'imgprt':IMAGE_KEYS}

def save_keys(con_id,keys,type='article'):
    keys = ','.join(keys)
    r.r.hset(KEY_MAP[type],con_id,keys)

def get_keys(con_id,type='article'):
    keys=r.r.hget(KEY_MAP[type],con_id)
    if keys:
        return keys.split(',')

def get_phase(con_id):
    phase = r.r.hget(AI_PHASE, con_id)
    return int(phase) if phase else 0

def save_phase(con_id,phase):
    r.r.hset(AI_PHASE,con_id,phase)


if __name__ == '__main__':
    #save_phase('aaa',1)
    get_phase('11')



