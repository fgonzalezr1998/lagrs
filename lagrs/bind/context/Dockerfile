FROM ubuntu:20.04
RUN apt-get update && apt-get upgrade -y
COPY entrypoint.sh /
RUN useradd -d /home/fernando -s /bin/bash -rm -u 1001 fernando
WORKDIR /home/fernando
ENTRYPOINT ["/entrypoint.sh"]
