import requests, os, json
from pyroute2 import IPDB


if 'API_HOST' in os.environ:
    API_HOST = os.environ['API_HOST']
else:
    ip = IPDB()
    API_HOST = ip.routes['default']['gateway']

API_SCHEMA = os.environ['API_SCHEMA']
API_PORT = os.environ['API_PORT']
API_PATH = os.environ['API_PATH']

API_URL = '%s%s:%s%s' % (API_SCHEMA, API_HOST, API_PORT, API_PATH)

data = dict()
for i in [ 'SERVER_NAME', 'DOCKER_IP' ]:
    if i in os.environ: data[i] = os.environ[i]


data['data'] = [
{{range $key, $value := .}}
	{{ $addrLen := len $value.Addresses }}
	{{ if eq $addrLen 1 }}
		{{ with $address := index $value.Addresses 0 }}
		{{ if $address.HostPort}}
		{{ if $value.Env.VIRTUAL_HOST}}
			{ 'VIRTUAL_HOST' : '{{ $value.Env.VIRTUAL_HOST }}', 'PORT' : {{ $address.HostPort }} },
		{{ end }}
		{{ end }}
		{{ end }}
	{{end}}
{{end}}
]

try:
    requests.post(API_URL, json = data)
except:
    pass
