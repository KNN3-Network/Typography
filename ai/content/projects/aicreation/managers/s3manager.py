import os.path
from content.configs.global_configs import S3Configs as s3cfg
from content.db.s3_connect import S3Conn
from uuid import uuid4
import requests
from content.projects.aicreation.configs import TEMP_DIR

BUCKET_NAME = s3cfg.bucket

TYPE_MAP = {
    'article':'articles',
    'imgprt':'imgprts',
    'image':'images',
}


def update_one_img(img,uid,con_id):
    s3 = S3Conn()
    if uid==None or uid =='':
        uid = 'unuid'
    filename = str(uid)+'/'+str(con_id)+'/'+str(uuid4()) +'.jpeg'
    url = s3.put_data_return_url(BUCKET_NAME,filename,img,content_type='image/jpeg')
    s3.close()
    return url


def _get_file_name(address,con_id,trace_id,type,i):
    pef = '.jpeg' if type=='image' else '.txt'
    filename = TYPE_MAP[type] + '/' +str(address) + '/' + str(con_id) + '/' + str(trace_id) + '/' +str(i) + pef
    return filename

def _get_file_names(address,con_id,trace_id,type,n):
    return [_get_file_name(address,con_id,trace_id,type,i) for i in range(n)]

def update_datas(datas,uid,con_id,trace_id,type):
    names = _get_file_names(uid, con_id, trace_id, type, len(datas))
    s3 = S3Conn()
    urls = []
    for data,name in zip(datas,names):
        url = s3.put_data_return_url(BUCKET_NAME, name, data, content_type='image/jpeg' if type=='image' else 'text/plain')
        urls.append(url)
    s3.close()
    return urls

def download(image,trace_id):
    response = requests.get(image)
    img_path = os.path.join(TEMP_DIR,trace_id+'.png')
    with open(img_path, "wb") as f:
        f.write(response.content)
    return img_path

if __name__ == '__main__':
    pass
