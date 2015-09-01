from flask import Flask, request
from docker import Client
import jinja2, os, json

templateLoader = jinja2.FileSystemLoader( searchpath=os.path.dirname(os.path.abspath(__file__)) )
templateEnv = jinja2.Environment( loader=templateLoader )

DOCKER_SOCKET = os.environ['DOCKER_SOCKET'] if 'DOCKER_SOCKET' in os.environ else 'unix://tmp/docker.sock'
NGINX_DIR = os.environ['NGINX_DIR'] if 'NGINX_DIR' in os.environ else '/etc/nginx/conf.d'
NGINX_CONTAINER = os.environ['NGINX_CONTAINER'] if 'NGINX_CONTAINER' in os.environ else 'nginx'

app = Flask(__name__)

def make_template(hosts, DOCKER_IP):
    template = templateEnv.get_template( 'nginx.conf.j2' )
    return template.render( hosts = hosts, DOCKER_IP = DOCKER_IP )

def write_file(filename, data, path = NGINX_DIR):
    if os.path.exists(path):
        with open(os.path.join(path, filename), 'w') as conffile:
            conffile.write(data)
            conffile.close()
            return True
    return False

def read_file(filename):
    if os.path.isfile(filename):
        with open(filename, 'r') as data:
            return json.loads(data.read())
    return dict()

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
        
        vhosts = read_file('/tmp/vhosts.json')
        if 'data' in request.json:
            data = request.json['data']

            for d in data:
                if d['VIRTUAL_HOST'] not in vhosts: vhosts[d['VIRTUAL_HOST']] = []
                vhosts[d['VIRTUAL_HOST']].append(d['PORT'])
            
            write_file('vhosts.json', json.dumps(vhosts), '/tmp')
            data = make_template(vhosts, DOCKER_IP)
            print data
            write_file('%s.conf' % SERVER_NAME, data)

    print vars(request)
    return 'No valid data'


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)
