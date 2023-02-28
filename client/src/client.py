"""members websocket client"""

import json
import sys
from datetime import datetime
from os import environ
from time import sleep

import rel
import requests
import websocket

WELCOME = """
----------------------------
TUBE ARCHIVIST MEMBER CLIENT
----------------------------
"""

MB_HOST = "members.tubearchivist.com"


def check_expected_env():
    """check all expected environment variables are set"""
    env_vars = ["MB_TOKEN", "TA_URL", "TA_TOKEN"]
    for var in env_vars:
        if not environ.get(var):
            print(f"[startup] missing expected environment variable: {var}")
            raise ValueError

    print("[startup] all expected environment vars are set")


def get_ws_url():
    """return websocket url, local testing and remote production"""
    if environ.get("MB_TESTING"):
        return "ws://members.tubearchivist.local/ws/notification/"

    return f"wss://{MB_HOST}/ws/notification/"


def get_timestamp():
    """return formatted now timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class TubeArchivist:
    """interact with TA"""

    TA_URL = environ.get("TA_URL").rstrip("/")
    HEADERS = {"Authorization": "Token " + environ.get("TA_TOKEN")}
    RETRY = 12

    def ping(self):
        """verify TA connection"""
        url = f"{self.TA_URL}/api/ping/"
        print(f"[startup] connecting to TA on url {url}")

        for i in range(self.RETRY):
            error = f"[startup][error] connection failed, [{i}/{self.RETRY}]"
            try:
                response = requests.get(url, headers=self.HEADERS, timeout=3)
                if response.ok:
                    print("[startup] TA connection established")
                    print(f"[startup] TA answered: {response.json()}")
                    return

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            ):
                print(error)

            sleep(10)

        print("[startup] connection to TA failed.")
        raise ConnectionError

    def add_to_queue(self, video_ids):
        """add list of video ids to queue"""
        to_download = {
            "data": [{"youtube_id": i, "status": "pending"} for i in video_ids]
        }
        url = f"{self.TA_URL}/api/download/"
        response = requests.post(
            url, json=to_download, headers=self.HEADERS, timeout=10
        )
        if not response.ok:
            print("[message] failed to send video ids to TA")
            print(f"[message] TA responded: {response.text}")
            return

        print(f"[message] video ids sent to TA: {response.text}\n")


def on_message(ws_connection, message):
    """message received"""
    # pylint: disable=unused-argument
    content = json.loads(message).get("message")
    print(f"[message][{get_timestamp()}] new message: {content}")

    if "download" in content:
        video_ids = content.get("download")
        TubeArchivist().add_to_queue(video_ids)


def on_error(ws_connection, error):
    """error found"""
    # pylint: disable=unused-argument
    print(f"[error][{get_timestamp()}] {error}")


def on_close(ws_connection, close_status_code, close_msg):
    """connection closed"""
    # pylint: disable=unused-argument
    print(f"[closed][{get_timestamp()}] connection to {MB_HOST} closed")
    print(f"[closed] status code: {close_status_code}")
    print(f"[closed] message: {close_msg}")
    sleep(10)
    sys.exit(1)


def on_open(ws_connection):
    """connection opened"""
    # pylint: disable=unused-argument
    print(f"[connect][{get_timestamp()}] connection to {MB_HOST} established")


if __name__ == "__main__":
    print(WELCOME)
    check_expected_env()
    TubeArchivist().ping()

    if environ.get("MB_TESTING"):
        websocket.enableTrace(True)

    print(f"[connect] opening connection to {MB_HOST}")
    connection = websocket.WebSocketApp(
        get_ws_url(),
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header={"Authorization": "Token " + environ.get("MB_TOKEN")},
    )

    connection.run_forever(dispatcher=rel, reconnect=10)
    rel.signal(2, rel.abort)
    rel.signal(15, rel.abort)
    rel.dispatch()
