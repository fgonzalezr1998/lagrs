#! /usr/bin/env python3

import sys, subprocess

DESIRED_PORT = 53

def get_port(line):
    for l in line:
        try:
            pos = l.index(':')
        except ValueError:
            continue

        port = l[pos + 1:]
        if (port == str(DESIRED_PORT)):
            return port
        # print(port)

    return None


def main(args=None):
    command = "netstat -tupan"

    try:

        stdout = subprocess.run(command.split(),
            check=True, stdout=subprocess.PIPE)

    except subprocess.CalledProcessError as err:
        print("[ERROR] " + err)
        sys.exit(1)

    output = stdout.stdout.decode('utf-8').split('\n')
    
    for line in output:
        port = get_port(line.split(' '))
        if (port != None):
            print(port + ' found!')

    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)