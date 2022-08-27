from datetime import datetime

from redis import Redis

from cosmos import config
from cosmos.logging import log


class RedisHandler:
    def __init__(self):
        self.r = Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DATABASE,
            password=config.REDIS_PASSWORD
        )

    def add(self, key, app, ip_address, status, port, ami_id, instance_id, availability_zone, instance_type, cpu_usage, ram_usage, ami_launch_index):
        now = datetime.utcnow()
        d = {
            "app": app,
            "ip_address": ip_address,
            "status": status,
            "port": port,
            "ami_id": ami_id,
            "instance_id": instance_id,
            "availability_zone": availability_zone,
            "instance_type": instance_type,
            "ami_launch_index": ami_launch_index,
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage,
            "timestamp": f"{now}"
        }
        try:
            self.r.hmset(key, d)
        except Exception:
            log.error("failed to add ", exc_info=True)

    def get(self, key):
        result = self.r.hgetall(key)
        y = {}
        for x in result:
            a = x.decode('utf-8')
            b = result[x].decode('utf-8')
            y[a] = b
        return y

    def get_all(self):
        result = self.r.keys()
        y = []
        for x in result:
            y.append(x.decode('utf-8'))
        return y

    def delete(self, key):
        self.r.delete(key)

    def heartbeat(self, key):
        d = {
            "timestamp": f"{datetime.utcnow()}"
        }
        self.r.hmset(key, d)

    def update(self, key, status):
        d = {
            "status": status
        }
        self.r.hmset(key, d)

    def update_metadata(self, appkey, key, value):
        self.r.hset(appkey, {key: value})

    def flush(self):
        self.r.flushdb()