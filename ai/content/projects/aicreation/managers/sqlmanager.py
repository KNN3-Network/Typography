from content.db import mysql_db as mdb
from content.configs.global_configs import MysqlConfigs as mc

nlp_sql_template = 'select prompt,temperature,model,n,stop,max_tokens,top_p,presence_penalty,frequency_penalty from openai_nlp_request_parameters where `key`="{}"'
image_sql_template = 'select prompt, n, response_format from openai_image_request_parameters where `key`="{}"'
chat_sql_template = 'select messages,temperature,model,n,stop,max_tokens,top_p,presence_penalty,frequency_penalty from openai_chat_request_parameters where `key`="{}"'
assistant_sql_template = 'select `set` from openai_assistant_set where `key` = "{}"'
config_sql_template = 'select `value` from typography_ai_configs where `key` = "{}"'
configs_sql_template = 'select `key`,`value` from typography_ai_configs'
TABLE_TRACE = 'typography_trace'
TABLE_CONTEXT = 'typography_context'
TABLE_REPLY_DEMOS = 'typography_trace_reply_demos'

def read_config(key):
    db = mdb.MYSQL(mc.db_tg)
    sql_template = config_sql_template.format(key)
    ds = db.search(sql_template.format(key))
    db.close()
    return ds[0][0]

def read_configs():
    db = mdb.MYSQL(mc.db_tg)
    ds = db.search(configs_sql_template)
    return {d[0]:d[1] for d in ds}

def read_assistant_set(key):
    db = mdb.MYSQL(mc.db_a)
    sql_template = assistant_sql_template.format(key)
    ds = db.search(sql_template.format(key))
    db.close()
    return ds[0][0]

def read_params(sql_template,key):
    pdb = mdb.PandasDB(mc.db_a)
    params = pdb.read_sql(sql_template.format(key))
    pdb.close()
    return params

def read_context(con_id,type,limit=4):
    db = mdb.MYSQL(mc.db_tg)
    sql = "select human_input, ai_reply from {} where con_id = '{}' and type = '{}' order by timestamp DESC limit {} ".format(TABLE_TRACE,con_id,type,limit)
    ds = db.search(sql)
    db.close()
    return ds

def apply_user_context(con_id,address):
    db = mdb.MYSQL(mc.db_tg)
    sql = "select address from {} where con_id = '{}'".format(TABLE_CONTEXT,con_id)
    ds = db.search(sql)
    if len(ds)==0:
        params = {'con_id':con_id,'address':address}
        sql,data = db.generate_insert_sql_and_data(TABLE_CONTEXT, params)
        db.insert(sql,data)
    db.close()
def insert_context(context,trace_id,con_id,type):
    db = mdb.MYSQL(mc.db_tg)
    params = {
        'human_input':context[0] if context else None,
        'ai_reply':context[1] if context else None,
        'trace_id':trace_id,
        'con_id':con_id,
        'type':type
    }
    sql, data = db.generate_insert_sql_and_data(TABLE_TRACE,params)
    db.insert(sql, data)
    db.close()

def insert_demos(trace_id,demos):
    db = mdb.MYSQL(mc.db_tg)
    if demos and demos!=[]:
        params = [{
            'trace_id':trace_id,
            'reply_demo':demo,
        } for demo in demos]
        sql, datas = db.generate_insert_sql_and_data_batch(TABLE_REPLY_DEMOS,params)
        db.insert_batch(sql, datas)
    db.close()

def get_image_request_count(address):
    image_times_sql = 'select count(tt.`trace_id`) from ' \
                      '`typography_trace` as tt JOIN `typography_context` as tc ' \
                      'on tt.`con_id` = tc.`con_id` where `address`="{}"' \
                      ' and tt.`type` in ("imgprt","variation") and `mistake`=0 ' \
                      'and UNIX_TIMESTAMP(tt.`timestamp`) > UNIX_TIMESTAMP(DATE(NOW()))'.format(address)
    db = mdb.MYSQL(mc.db_tg)
    r = db.search(image_times_sql)[0][0]
    db.close()
    return r

if __name__ == '__main__':

    configs = read_configs()
    print(configs)

