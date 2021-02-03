FROM ubuntu:20.04

RUN apt-get update && apt-get upgrade -y && \
apt-get install iperf -y && \
apt-get install ssh openssh-client -y && \
apt-get install sshfs -y && \
apt-get install -f -y

COPY entrypoint.sh /
COPY id_rsa /root/.ssh/
COPY id_rsa.pub /root/.ssh/

ENTRYPOINT ["/entrypoint.sh"]
