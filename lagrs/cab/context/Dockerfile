FROM ubuntu:20.04
RUN apt-get update && apt-get upgrade -y && \
apt-get install net-tools -y && \
apt-get install iputils-ping -y && \
apt-get install dnsutils -y && \
apt-get install ssh openssh-client -y && \
apt-get install locales -y && \
localedef -i es_ES -c -f UTF-8 \
-A /usr/share/locale/locale.alias es_ES.UTF-8
ENV LANG es_ES.UTF-8
COPY entrypoint.sh /
COPY delta_hosts /
ENTRYPOINT ["/entrypoint.sh"]
