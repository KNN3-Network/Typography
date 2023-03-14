
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from content.configs.global_configs import RedisConfigs as rc

if rc.cluster:
    from rediscluster import RedisCluster
else:
    from redis import Redis as redis

class Redis():

    def __init__(self):
        if rc.cluster:
            startup_nodes = [{"host":rc.host, "port": rc.port}]
            self.r = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, ssl=True, ssl_cert_reqs=None,
                              skip_full_coverage_check=True)
            #self.r = RedisCluster(host= rc.host, port= rc.port,decode_responses = True,ssl=True,ssl_cert_reqs=None,skip_full_coverage_check=True)
        else:
            if rc.pwd:
                self.r = redis(host=rc.host, port=rc.port, decode_responses=True,password=rc.pwd)
            else:
                self.r = redis(host=rc.host, port=rc.port, decode_responses=True)

    def __del__(self):
        self.r.close()


if __name__ == '__main__':
    a = Redis().r.ping()
    print(a)
