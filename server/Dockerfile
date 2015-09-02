FROM python:2-onbuild
EXPOSE 5000
ENV DOCKER_SOCKET unix://tmp/docker.sock
ENV NGINX_CONF /etc/nginx/conf.d/proxy-docker.conf
ENV NGINX_CONTAINER nginx
CMD [ "python", "app.py" ]
