from content.db.s3_connect import S3Conn
from uuid import uuid4
bucket_name = 'tg'

def update_one_img(img,uid,con_id):
    s3 = S3Conn()
    if uid==None or uid =='':
        uid = 'unuid'
    filename = str(uid)+'/'+str(con_id)+'/'+str(uuid4()) +'.jpg'
    url = s3.put_data_return_url(bucket_name,filename,img,content_type='image/jpg')
    s3.close()
    return url

if __name__ == '__main__':
    print(uuid4())


