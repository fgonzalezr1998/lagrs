FROM ubuntu:20.04
RUN apt-get update && apt-get upgrade -y && \
apt-get install net-tools -y && \
apt-get install iputils-ping -y && \
apt-get install dnsutils -y && \
apt-get install ssh openssh-client -y
COPY entrypoint.sh /
COPY delta_hosts /
ENTRYPOINT ["/entrypoint.sh"]
