#! /usr/bin/env python3

##################################
# author: Fernando González Ramos#
# login: fernando                #
##################################

# WARNING! This program is potentially DANGEROUS!

import sys
import time
import telepot
import threading
import subprocess
from telepot.loop import MessageLoop

class TelegramShell():
    def __init__(self):
        self.token = self.__get_token()
        self.bot = telepot.Bot(self.token)
        self.chat_id = None
        self.msg_received = False
        self.cmd_received = None

        self.cmds_timeout = 0.5

        # Read/Write Locks:

        self.r_lock = threading.RLock()
        self.w_lock = threading.Lock()

        MessageLoop(self.bot, self.__callback).run_as_thread()

    def step(self):
        self.r_lock.acquire()
        received = self.msg_received
        self.r_lock.release()

        if (received):
            self.w_lock.acquire()
            self.msg_received = False
            self.w_lock.release()

            self.r_lock.acquire()
            id = self.chat_id
            self.r_lock.release()

            self.__reply(id)

    # Private Methods:

    def __reply(self, target_id):
        # Get the command:

        self.r_lock.acquire()
        cmd = self.cmd_received
        print("cmd: " + cmd)
        self.r_lock.release()

        # Run command:

        output = self.__run_cmd(cmd)

        print("output: " + output)

        self.__send_msg(target_id, output)

    def __run_cmd(self, cmd):
        output = ''
        try:
            stdout = subprocess.run(cmd.split(), check=True,
                stdout=subprocess.PIPE, timeout=self.cmds_timeout)
            stdout = stdout.stdout.decode('utf-8').split('\n')
            for i in stdout:
                output = output + i + '\n'

        except FileNotFoundError as err:
            print('[ERROR] ', err)
            output = "[BOT] The command does not exist or you can not run this command remotelly"
        except subprocess.CalledProcessError as err:
            print('[ERROR] ', err)
            output = "[BOT] The command returned a failure status or Something wrong happened"
        except subprocess.TimeoutExpired:
            output = "[BOT] Blocking commands are not allowed!"

        return output

    def __send_msg(self, target_id, msg):
        try:
            self.bot.sendMessage(target_id, msg)
        except telepot.exception.UnauthorizedError:
            sys.stderr.write("[ERROR] Invalid Token!\n")
            sys.exit(1)

        except telepot.exception.TelegramError as err:
            warning = "[WARNING] " + err.description
            print(warning)
            self.bot.sendMessage(target_id, warning)

    def __print_request_log(self, msg, st):
        for key in msg:
            if (isinstance(msg[key], dict)):
                print(key)
                self.__print_request_log(msg[key], st + '\t')
            else:
                print(st + key + ": ", msg[key])

    def __callback(self, msg):
        chat_id = msg["chat"]["id"]

        self.w_lock.acquire()
        self.chat_id = chat_id
        self.cmd_received = msg["text"]
        self.msg_received = True
        self.w_lock.release()

        self.__print_request_log(msg, '')
        print("-------------------")

    def __get_token(self):
        '''
        The first written line is the token
        '''

        try:
            file = open('token.txt', 'r')
        except FileNotFoundError:
            sys.stderr.write("[ERROR] token.txt file not found!\n")
            sys.exit(1)

        for line in file.readlines():
            if (line != '\n'):
                file.close()
                return line
        file.close()

        sys.stderr.write("[ERROR] No token found!\n")
        sys.exit(1)

def main(args=None):
    telegram_sh = TelegramShell()

    try:
        while (True):
            telegram_sh.step()
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main(sys.argv)
    sys.exit(0)