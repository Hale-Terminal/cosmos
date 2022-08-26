from cosmos.models import InfluxEvent


class CosmosHeartbeatEvent(InfluxEvent):
    def __init__(self, region, status, event_type=None):
        super(CosmosHeartbeatEvent, self).__init__(event_type=event_type)
        self.region = region
        self.status = status

    def get_influx_event(self):
        event = super().get_influx_event()
        event[0]["fields"]["status"] = self.status
        event[0]["tags"]["region"] = self.region
        return event
        

class ServerCountEvent(InfluxEvent):
    def __init__(self, app, count, event_type=None):
        super(ServerCountEvent, self).__init__(event_type=event_type)
        self.app = app
        self.count = count

    def get_influx_event(self):
        event = super().get_influx_event()
        event[0]["tags"]["app"] = self.app
        event[0]["fields"]["count"] = self.count
        return event