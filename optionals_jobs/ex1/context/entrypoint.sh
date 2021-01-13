#! /bin/sh

mkdir /media/lab
sshfs fernando@f-l2108-pc02.aulas.etsit.urjc.es:/home/alumnos/fernando /media/lab
iperf -s -p 9999 &
bash
