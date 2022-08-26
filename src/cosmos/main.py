from time import sleep

import uvicorn
import click

from cosmos import config

from cosmos.api import api
from cosmos.monitor import Monitor

from cosmos.services.eventlogging import EventLogging
from cosmos.models import CosmosHeartbeatEvent, ServerCountEvent


eventlogger = EventLogging()


@click.group()
def cosmos_cli():
    pass

@cosmos_cli.command("api")
def api_s():
    uvicorn.run("cosmos.api:api", host="0.0.0.0")


@cosmos_cli.command("monitor")
def monitor_s():
    monitor = Monitor()
    while True:
        monitor.check_instances()
        sleep(config.COSMOS_MONITOR_SLEEP_TIME)


@click.group("start")
def server_group():
    pass


@server_group.command("api")
def start_api():
    uvicorn.run("cosmos.api:api", host="0.0.0.0")


@server_group.command("monitor")
def start_monitor():
    monitor = Monitor()
    while True:
        monitor.check_instances()
        sleep(config.COSMOS_MONITOR_SLEEP_TIME)


def entrypoint():
    cosmos_cli()


def send_heartbeat():
    eventlogger.save_event(
        CosmosHeartbeatEvent(
            region="us-east-1",
            status="UP",
            event_type="cosmos_heartbeat"
        )
    )


def send_server_count():
    eventlogger.save_event(
        ServerCountEvent(
            app="Kangaroo",
            count=20,
            event_type="cosmos_servers"
        )
    )

def run():
    #send_heartbeat()
    #send_server_count()
    #run_api()
    #run_monitor()
    pass