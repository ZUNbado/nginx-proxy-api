from flask import Flask, request, render_template
from docker import Client
import os, json

DOCKER_SOCKET = os.environ.get('DOCKER_SOCKET', 'unix://var/run/docker.sock')
NGINX_CONF = os.environ.get('NGINX_CONF', '/etc/nginx/conf.d/api.conf')
NGINX_CONTAINER = os.environ.get('NGINX_CONTAINER', 'nginx' )
API_PORT = os.environ.get('API_PORT', 5555)
VHOSTS = '/tmp/vhosts.json'

app = Flask(__name__)

def write_file(filename, data):
    with open(filename, 'w') as wfile:
        wfile.write(data)
        wfile.close()
        return True
    return False

def read_file(filename):
    if os.path.isfile(filename):
        with open(filename, 'r') as data:
            return data.read()
    return None

def reload_nginx():
    c = Client(base_url=DOCKER_SOCKET)
    for container in c.containers():
        if "/%s" % NGINX_CONTAINER in container['Names']:
            c.kill(container['Id'], 'SIGHUP')

@app.route('/', methods = [ 'POST', 'GET' ])
def index():
    if request.method == 'POST':
        if 'DOCKER_IP' in request.json:
            SERVER = request.json['DOCKER_IP']
        else:
            SERVER = request.remote_addr

        data = read_file(VHOSTS)
        vhosts = json.loads(data) if data else dict()
        post = request.json['vhosts']
        for vhost, backends in vhosts.items():
            if vhost in post:
                for backend, ports in backends.items():
                    if backend in post[vhost]:
                        vhosts[vhost][backend] = post.pop(vhost)
            else:
                if SERVER in backends:
                    vhosts[vhost].pop(SERVER)

            if len(vhosts[vhost]) == 0:
                vhosts.pop(vhost)

        for vhost, ports in post.items():
            if vhost not in vhosts: vhosts[vhost] = dict()
            vhosts[vhost][SERVER] = ports
        
        template = render_template('nginx.conf.j2', vhosts = vhosts)
        write_file(NGINX_CONF, template)
        write_file(VHOSTS, json.dumps(vhosts))
        reload_nginx()
        return ''
    return 'No valid data'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True, port = API_PORT)
