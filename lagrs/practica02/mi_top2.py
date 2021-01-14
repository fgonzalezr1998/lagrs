#! /usr/bin/env python3

##################################
# author: Fernando González Ramos#
# login: fernando                #
##################################

import subprocess
from optparse import OptionParser
import sys

# Consts:
MinCPU = 0.0
PIDField = 1
USERField = 2
CPUField = 9
CMDField = 12
EndHeaderTop = 6

def add_options(parser):
    parser.add_option("-u", "--user",
        help="User whose processes you have to list. By default, all are taken",
        default="all")

    parser.add_option("-U", "--User",
        help="Display only processes with users not matching the one provided",
        default="none")

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

    print("\n\tMostrando " + str(nprocs), "procesos que consumen el " +
        f"{cpu_per:.2f}" + "% de la CPU")

def get_command(opts):
    cmd = ['top', '-n', '1']

    if (opts.user != "all"):
        cmd.append('-u')
        cmd.append(opts.user)
    elif (opts.User != "none"):
        cmd.append('-u')
        cmd.append("!" + opts.User)
    print(cmd)
    return cmd

def run_command(opts):
    command = get_command(opts)

    try:
        stdout = subprocess.run(command, check=True,
            stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as err:
        print('ERROR:', err)
        sys.exit(1)

    output = stdout.stdout.decode('utf-8').split('\n')

    print_processes(output[EndHeaderTop:])

    sys.exit(0)

def main(args=None):
    parser = OptionParser()

    add_options(parser)

    (options, args) = parser.parse_args(args)

    run_command(options)

if __name__ == "__main__":
    main(sys.argv)
