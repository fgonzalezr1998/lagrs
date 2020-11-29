#! /usr/bin/env python3

##################################
# author: Fernando González Ramos#
# login: fernando                #
##################################

import subprocess
import sys
import math

# Consts:
MinCPU = 0.0
PIDField = 1
USERField = 2
CPUField = 9
CMDField = 12
EndHeaderTop = 6

def print_processes(procs):
    '''
    Prints the info of the process that consume more than 'MinCPU' cpu amount
    '''

    nprocs = 0
    cpu_per = 0.0
    for line in procs[1:len(procs) - 1]:
        l = line.split()
        if (float(l[CPUField]) > MinCPU):
            nprocs = nprocs + 1
            cpu_per = cpu_per + float(l[CPUField])
            print('{:>20s}{:>10}{:>10}{:>15}'.format(
                l[CMDField], l[PIDField], l[USERField], l[CPUField]))
    pi = 3.1416
    print("\n\tMostrando " + str(nprocs), "procesos que consumen el " +
        f"{cpu_per:.2f}" + "% de la CPU")

def main(args=None):
    command = "top -n 1"
    try:
        stdout = subprocess.run(command.split(), check=True,
            stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as err:
        print('ERROR:', err)
        sys.exit(14)

    output = stdout.stdout.decode('utf-8').split('\n')

    print_processes(output[EndHeaderTop:])

    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)
