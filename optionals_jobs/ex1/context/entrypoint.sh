#! /bin/sh

mkdir /media/lab
#ssh -o StrictHostKeyChecking=no fernando@212.128.254.4
sshfs fernando@212.128.254.4:/home/alumnos/fernando /media/lab
iperf -s -p 9999 &
bash
