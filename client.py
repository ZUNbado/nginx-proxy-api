import requests, os, json

data = dict()
for i in [ 'SERVER_NAME', 'DOCKER_IP' ]:
    if i in os.environ: data[i] = os.environ[i]


data['data'] = [
{{range $key, $value := .}}
	{{ $addrLen := len $value.Addresses }}
	{{ if eq $addrLen 1 }}
		{{ with $address := index $value.Addresses 0 }}
		{{ if $address.HostPort}}
			{ 'VIRTUAL_HOST' : '{{ $value.Env.VIRTUAL_HOST }}', 'PORT' : {{ $address.HostPort }} },
		{{ end }}
		{{ end }}
	{{end}}
{{end}}
]
print data


requests.post('http://localhost:5000', json = data)
