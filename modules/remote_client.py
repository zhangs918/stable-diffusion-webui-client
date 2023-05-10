
import requests
import time
from modules import shared
import threading

def activate_client():
    try:
        data = {"req": {"port": str(shared.cmd_opts.port), "user_level": shared.cmd_opts.client_user_level, "model_id": shared.opts.sd_model_checkpoint}}
        requests.post(url=shared.cmd_opts.remote_server_url, json=data)
    except Exception as e:
        pass

def active_loop_helper():
    while 1:
        time.sleep(5)
        activate_client()

def active_loop():
    if shared.cmd_opts.remote_server_url:
        threading.Thread(target=active_loop_helper).start()

if __name__ == '__main__':
    pass