#! /bin/bash

print_usage() {
    echo "Usage:"
    echo -e "\t./monta_tmp.sh [Option] [user]"
    echo -e "\tuser: user of remote machine"
    echo "Option:"
    echo -e "\t -h: Print help"
}

make_sshfs() {
    # $1: remote machine address
    # $2: remote user
    # $3: number of mounting folder

    if [ -d "tmp0$3" ]
    then
        umount -f tmp0$3 2> /dev/null && rm -rf tmp0$3
    fi

    mkdir tmp0$3

    sshfs $2@$1:/tmp ./tmp0$3 2> /dev/null
    if [ $? -ne 0 ]
    then
        rm -rf tmp0$3
        echo -e "\e[31m[ERROR] sshfs failed!\e[39m"
        echo "[$1] machine failed"
    fi
}

main() {
    # $1: remote user

    # Declare Remote machines:

    rm1=f-l2108-pc02.aulas.etsit.urjc.es
    rm2=f-l2108-pc03.aulas.etsit.urjc.es
    rm3=f-l2108-pc04.aulas.etsit.urjc.es

    j=1
    for i in $rm1 $rm2 $rm3
    do
        make_sshfs $i $1 $j
        j=$(($j + 1))
    done
}

# If not root, do nothing

if [ "$EUID" -ne 0 ]
then
    echo "Execute with sudo!"
    exit 1
fi

# Parse options and arguments:

if [ $# -eq 2 ]
then
    if [ "$1" = "-h" ] || [ "$2" = "-h" ]
    then
        print_usage
        exit 0
    else
        echo -e "\e[31m[ERROR] Usage Error!\e[39m"
        print_usage
        exit 1
    fi
elif [ $# -eq 1 ]
then
    if [ "$1" = "-h" ]
    then
        print_usage
        exit 0
    else
        main $1    # Execute the main program
    fi
else
    echo -e "\e[31m[ERROR] Usage Error!\e[39m"
    print_usage
    exit 1
fi
