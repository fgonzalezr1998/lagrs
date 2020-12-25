#! /bin/sh

docker run -it --rm -h optional1 --name optional1 --cap-add SYS_ADMIN --device /dev/fuse --security-opt apparmor:unconfined fgonzalezr1998/optional1
