import imp
from fastapi import FastAPI
from pydantic import BaseModel

from cosmos.services import RedisHandler


class App(BaseModel):
    app: str
    ip_address: str
    status: str
    port: int | None = None
    ami_id: str | None = ""
    instance_id: str | None = ""
    availability_zone: str | None = ""
    instance_type: str | None = ""
    

api = FastAPI()
r = RedisHandler()


@api.post("/cosmos/v1/flush")
async def flush():
    r.flush()


@api.get("/cosmos/v1/healthcheck")
async def healthcheck():
    return "ok"


@api.post("/cosmos/v1/apps/{app_id}")
async def register(app_id, app: App):
    """Register new application instance."""

    key = app_id + ":" + app.instance_id
    try:
        r.add(
            key=key,
            app=app.app, 
            ip_address=app.ip_address,
            status=app.status, 
            port=app.port,
            ami_id=app.ami_id, 
            instance_id=app.instance_id, 
            availability_zone=app.availability_zone, 
            instance_type=app.instance_type)
    except Exception as e:
        print(e)


@api.delete("/cosmosv1/apps/{app_id}/{instance_id}")
async def deregister_app(app_id, instance_id):
    """De-register application instance"""

    key = app_id + ":" + instance_id
    try:
        r.delete(key)
    except Exception as e:
        print(e)


@api.get("/cosmos/v1/apps")
async def get_all_instances():
    try:
        result = []
        raw_result = r.get_all()
        for x in raw_result:
            result.append(x.split(':')[1])
        return result
    except Exception as e:
        print(e)


@api.get("/cosmos/v1/apps/{app_id}")
async def get_all_by_appid(app_id):
    """Query for all app_id instances."""

    try:
        result = []
        raw_result = r.get_all()
        for x in raw_result:
            if x.split(':')[0] == app_id:
                result.append(x.split(':')[1])
        return result
    except Exception as e:
        print(e)


@api.get("/cosmos/v1/apps/{app_id}/{instance_id}")
async def get_app_instance(app_id, instance_id):
    """Query for a specific app_id/instance_id"""

    key = app_id + ":" + instance_id
    try:
        return r.get(key)
    except Exception as e:
        print(e)


@api.get("/cosmos/v1/instances/{instance_id}")
async def get_by_instance(instance_id):
    """Query for specific instance_id"""

    try:
        raw_results = r.get_all()
        for x in raw_results:
            if x.split(':')[1] == instance_id:
                return r.get(x)
    except Exception as e:
        print(e)


@api.put("/cosmos/v1/apps/{app_id}/{instance_id}")
async def update_instance_status(app_id, instance_id, status=None):
    """Update instance status"""

    key = app_id + ":" + instance_id
    try:
        if status:
            r.update(key, status)
        else:
            r.heartbeat(key)
    except Exception as e:
        print(e)


@api.put("/cosmos/v1/apps/{app_id}/{instance_id}/metadata")
async def update_instance_metadata(app_id, instance_id, key, value):
    """Update instances metadata"""
    appkey = app_id + ":" + instance_id
    try:
        r.update_metadata(appkey, key, value)
    except Exception as e:
        print(e)


@api.get("/cosmosv1/latest/metadata")
async def get_cosmos_metadata():
    """Get Cosmos latest metadata"""
    instances = []
    keys = r.get_all()
    for key in keys:
        instances.append(r.get(key))
    response = {
        "instances": instances
    }
    return response


