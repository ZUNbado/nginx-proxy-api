from flask import Flask, request
from docker import Client
import jinja2, os, json

templateLoader = jinja2.FileSystemLoader( searchpath=os.path.dirname(os.path.abspath(__file__)) )
templateEnv = jinja2.Environment( loader=templateLoader )

DOCKER_SOCKET = os.environ['DOCKER_SOCKET']
NGINX_CONF = os.environ['NGINX_CONF']
NGINX_CONTAINER = os.environ['NGINX_CONTAINER']
TEMP_FILE = '/tmp/vhosts.json'

app = Flask(__name__)

def make_template(hosts):
    template = templateEnv.get_template( 'nginx.conf.j2' )
    return template.render( hosts = hosts )

def write_file(filename, data):
    if os.path.exists(os.path.dirname(filename)):
        with open(filename, 'w') as conffile:
            conffile.write(data)
            conffile.close()
            return True
    return False

def read_file(filename):
    if os.path.isfile(filename):
        with open(filename, 'r') as data:
            return data.read()
    return ''

def kill():
    c = Client(base_url=DOCKER_SOCKET)
    for container in c.containers():
        if "/%s" % NGINX_CONTAINER in container['Names']:
            c.kill(container['Id'], 'SIGHUP')

@app.route('/', methods = [ 'POST', 'GET' ])
def index():
    if request.method == 'POST':
        if 'DOCKER_IP' in request.json:
            DOCKER_IP = request.json['DOCKER_IP']
        else:
            DOCKER_IP = request.remote_addr

        if 'SERVER_NAME' in request.json: 
            SERVER_NAME = request.json['SERVER_NAME']
        else:
            return 'No SERVER_NAME especified'
        
        if 'data' in request.json:
            vhosts = json.loads(read_file( TEMP_FILE ))
            data = request.json['data']

            vhosts_server = dict()
            for d in data:
                if d['VIRTUAL_HOST'] not in vhosts_server: vhosts_server[d['VIRTUAL_HOST']] = []
                vhosts_server[d['VIRTUAL_HOST']].append(d['PORT'])

            for vhost, ports in vhosts_server.items():
                if vhost not in vhosts: vhosts[vhost] = {}
                vhosts[vhost][SERVER_NAME] = { 'IP' : DOCKER_IP, 'PORTS' : ports }
            
            write_file(TEMP_FILE, json.dumps(vhosts))
            data = make_template(vhosts)
            write_file(NGINX_CONF, data)
            kill()

    return 'No valid data'


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)
