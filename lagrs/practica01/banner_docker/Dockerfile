FROM ubuntu:20.04
RUN apt-get update && apt-get upgrade -y && apt-get install -y sysvbanner
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
