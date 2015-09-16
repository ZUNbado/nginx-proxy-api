import os, json, requests
from docker import Client
from pyroute2 import IPDB

DOCKER_SOCKET = os.environ.get('DOCKER_SOCKET', 'unix://var/run/docker.sock')
API_HOST = os.environ.get('API_HOST', IPDB().routes['default']['gateway'])
API_SCHEMA = os.environ.get('API_SCHEMA', 'http')
API_PORT = os.environ.get('API_PORT', '5555')
API_PATH = os.environ.get('API_PATH', '/')
API_URL = '%s://%s:%s%s' % (API_SCHEMA, API_HOST, API_PORT, API_PATH)

data = dict()
for i in [ 'DOCKER_IP' ]:
    if i in os.environ: data[i] = os.environ[i]

def get_vhosts():
    vhosts = dict()
    for container in c.containers():
        inspect = c.inspect_container(container['Id'])
        for env in inspect['Config']['Env']:
            if '=' in env:
                item, value = env.split('=', 2)
                if item == 'VIRTUAL_HOST':
                    if value not in vhosts: vhosts[value] = []
                    port = container['Ports'][0]['PublicPort']
                    vhosts[value].append(port)
    return vhosts

if __name__ == "__main__":
    c = Client(base_url=DOCKER_SOCKET)
    for e in c.events():
        event = json.loads(e)
        if event['status'] in [ 'start', 'stop' ]:
            data['vhosts'] = get_vhosts()
            requests.post(API_URL, json = data)
