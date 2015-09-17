Frontend server
===============

nginx image
```
docker run --name nginx --restart=always -d -p 80:80 -p 443:443 \
 -v /tmp/nginx:/etc/nginx/conf.d/ nginx
```

Container including API to auto-configure nginx
```
docker run --name nginx-proxy-api-server --restart=always \
 -d -p 5555:5555 --volumes-from nginx \
 -v /var/run/docker.sock:/var/run/docker.sock zunbado/nginx-proxy-api-server
```
Enviroment variables
-------------------
```
DOCKER_SOCKET default: unix://var/run/docker.sock
NGINX_CONF default: /etc/nginx/conf.d/api.conf
NGINX_CONTAINER default: nginx
```


Backend servers
===============
```
docker run --name nginx-proxy-api-client --restart=always \
 -d -v /var/run/docker.sock:/var/run/docker.sock  zunbado/nginx-proxy-api-client
```

Enviroment variables
-------------------
```
DOCKER_SOCKET default: unix://var/run/docker.sock
API_HOST default: container default gateway
API_SCHEMA default: http
API_PORT default: 5555
API_PATH default: /
DOCKER_IP default: Not set
```
