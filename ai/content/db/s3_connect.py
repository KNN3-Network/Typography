
import boto3
from content.configs.global_configs import S3Configs as cfg
class S3Conn():
    def __init__(self):
        self.end_point = cfg.host
        access_key = cfg.user
        secret_key = cfg.pwd
        region_name = cfg.region_name
        self.conn = self._init_s3(self.end_point, access_key, secret_key,region_name)
        self.expiration = 7200

    def close(self):
        self.conn.close()

    def _init_s3(self, end_point, access_key, secret_key,region_name):

        return boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            use_ssl=True,
            region_name=region_name,
            endpoint_url=end_point)

    def get_file(self, bucket_name, filename):

        return self.conn.get_object(
            Bucket=bucket_name,
            Key=filename,
        )

    def put_data_return_url(self, bucket_name, filename, data,content_type):
        self.put_data(bucket_name, filename, data, content_type)
        url = self.end_point + '/' + bucket_name +'/' + filename
        return url

    def put_data(self, bucket_name, filename, data, content_type):
        return self.conn.put_object(
            Bucket=bucket_name,
            Body=data,
            Key=filename,
            ContentType=content_type,
        )

    def put_file(self, bucket_name, filename, file):
        return self.conn.put_object(
            Bucket=bucket_name,
            Body=open(file, 'rb'),
            Key=filename,
        )

    def generate_url(self,bucket_name,filename):
        url = self.conn.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': filename
            },
            ExpiresIn=self.expiration
        )
        return url


if __name__ == '__main__':

    s3 = S3Conn()
    url = s3.generate_url('test','test.jpg')
    print(url)




