import requests, os, json
from pyroute2 import IPDB


if 'PROXY_API' in os.environ:
    PROXY_API = os.environ['PROXY_API']
else:
    ip = IPDB()
    PROXY_API = ip.routes['default']['gateway']

API_SCHEMA = 'http'
API_PORT = '5000'
API_PATH = ''

API_URL = '%s://%s:%s/%s' % (API_SCHEMA, API_HOST, API_PORT, API_PATH)

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

requests.post(API_URL, json = data)
