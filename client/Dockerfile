FROM python:2-onbuild

ENV VERSION 0.4.0
ENV DOWNLOAD_URL https://github.com/jwilder/docker-gen/releases/download/$VERSION/docker-gen-linux-amd64-$VERSION.tar.gz
ENV DOCKER_HOST unix:///tmp/docker.sock

RUN wget -O docker-gen.tar.gz $DOWNLOAD_URL && tar -C /usr/local/bin -xvzf docker-gen.tar.gz

CMD docker-gen -watch -notify "python /tmp/client.py" client.py /tmp/client.py

