Frontend server
===============

nginx image
```
docker run --restart=always --name nginx -d -p 80:80 -p 443:443 -v /tmp/nginx:/etc/nginx/conf.d/ nginx
```

api to configure nginx
```
docker run --name nginx-proxy-api-server --restart=always -d -p 5555:5555 --volumes-from nginx -v /var/run/docker.sock:/var/run/docker.sock zunbado/nginx-proxy-api-server
```


Backend servers
===============
```
    docker run --name nginx-proxy-api-client --restart=always -d -v /var/run/docker.sock:/var/run/docker.sock  zunbado/nginx-proxy-api-client
```
