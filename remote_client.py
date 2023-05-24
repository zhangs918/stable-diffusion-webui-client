
import os
import requests
import time
from modules import shared
import threading
import json

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

def sync_files_loop_helper():
    while 1:
        time.sleep(1)
        print("sync_files_loop_helper start")
        # get remote file paths
        file_paths = []
        folder_paths = ["./stable-diffusion-webui/embeddings", "./stable-diffusion-webui/models"]
        for _path in folder_paths:
            try:
                rsp = requests.get(url=shared.cmd_opts.remote_file_server_url + "/get_file_configs?folder_path=" + _path)
                file_paths.extend(json.loads(rsp.text))
            except Exception as e:
                pass
        # download all files
        for _f, _c in file_paths:
            try:
                _url = shared.cmd_opts.remote_file_server_url + "/download_file?file_path=" + _f
                _local = os.path.dirname(_f.replace('stable-diffusion-webui/', ''))
                _local_file = _local + "/" + os.path.basename(_f)
                current_size = 0
                if os.path.exists(_local_file):
                    current_size = os.path.getsize(_local_file)
                if current_size == _c:
                    continue
                os.makedirs(_local, exist_ok=True)
                print("downloading... ", _url, _local, os.path.basename(_f))
                shared.file_download(_url, _local, os.path.basename(_f))
            except Exception as e:
                print("download fail for: ", e)

def active_loop():
    if shared.cmd_opts.remote_server_url:
        threading.Thread(target=active_loop_helper).start()

def sync_files_loop():
    if shared.cmd_opts.remote_file_server_url:
        threading.Thread(target=sync_files_loop_helper).start()

if __name__ == '__main__':
    pass
    # shared.cmd_opts.remote_file_server_url = "http://8.130.94.216:5294"
    # sync_files_loop_helper()