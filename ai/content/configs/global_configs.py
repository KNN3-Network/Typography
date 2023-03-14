import os
import yaml

class FilePath():
    SERVICE_YAML = os.path.join(os.path.split(os.path.realpath(__file__))[0],'services.yaml')
    PROMPTS_YAML = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'prompts.yaml')
    IMAGE_PROMPTS_YAML = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'image_prompts.yaml')
    CHAT_PROMPTS_YAML = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'chat_prompts.yaml')
    ASSISTANT_YAML = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'assistant_set.yaml')
    AI_CONFIGS = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'typography_ai_configs.yaml')
    DATA_FOLDER = os.path.join(os.path.split(os.path.realpath(__file__))[0], '../../data')
    MODELS_FOLDER = os.path.join(os.path.split(os.path.realpath(__file__))[0], '../../models')
    MODEL_FOLDER = os.path.join(DATA_FOLDER,'model')

with open(FilePath.SERVICE_YAML,'r') as f:
    CONS = yaml.safe_load(f.read())
#print(CONS)
ENV = os.getenv('ENV','dev_out')

HOST = 'host'
PORT = 'port'
USER = 'user'
PWD = 'pwd'


class MysqlConfigs():
    name = 'mysql'
    host = CONS[name][ENV].get(HOST,)
    port = CONS[name][ENV].get(PORT,)
    user = CONS[name][ENV].get(USER,)
    pwd = CONS[name][ENV].get(PWD,)
    db_a = CONS[name][ENV].get('db_a',)
    db_tg = CONS[name][ENV].get('db_tg')

class S3Configs():
    name = 's3'
    host = CONS[name][ENV].get(HOST,)
    user = CONS[name][ENV].get(USER,)
    pwd = CONS[name][ENV].get(PWD,)
    region_name = CONS[name][ENV].get('region_name',)
    bucket = CONS[name][ENV].get('bucket',)

class KafkaConfigs():
    name = 'kafka'
    urls = CONS[name][ENV].get('urls',)

class OpenAiConfigs():
    name = 'openai'
    keys = CONS[name][ENV].get('keys',)


class RedisConfigs():
    name = 'redis'
    host = CONS[name][ENV].get(HOST, )
    port = CONS[name][ENV].get(PORT, )
    user = CONS[name][ENV].get(USER,)
    pwd = CONS[name][ENV].get(PWD,)
    cluster = CONS[name][ENV].get('cluster')
    print(cluster)
class Queue():
    TRY = 'algo_try'
    WORD_CLOUD = 'algo_word_cloud'


if __name__ == '__main__':
    print(RedisConfigs.cluster)