from datetime import datetime

from cosmos.services import RedisHandler
from cosmos import config, log


r = RedisHandler()


class Monitor:
    def __init__(self):
        self.instance_failures = {}
        self.total_instances = 0
        self.ungraceful_disconnects = 0

    def check_instances(self):
        instance_keys = r.get_all()
        self.total_instances = len(instance_keys)
        for instance_key in instance_keys:
            instance = r.get(instance_key)
            timestamp = instance["timestamp"]
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            instance_id = instance["instance_id"]
            if (datetime.utcnow() - timestamp).total_seconds() > config.COSMOS_RENEWAL_THRESHOLD:
                if instance_id in self.instance_failures:
                    failures = self.instance_failures[instance_id]
                    if failures >= config.COSMOS_INSTANCE_FAILURE_THRESHOLD:
                        key = instance["app"] + ":" + instance_id
                        r.update(key, "DOWN")
                    failures += 1
                    self.instance_failures[instance_id] = failures
                else:
                    self.instance_failures[instance_id] = 1

    def preservation(self):
        if (self.ungraceful_disconnects / self.total_instances) > config.COSMOS_SELF_PRESERVATION_THRESHOLD:
            print("Preservation")
