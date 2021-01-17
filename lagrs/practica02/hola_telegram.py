#! /usr/bin/env python3

##################################
# author: Fernando González Ramos#
# login: fernando                #
##################################

import sys
import time
import telepot
import threading
import random
from telepot.loop import MessageLoop

class MyTelegramBot():
    def __init__(self):
        self.token = self.__get_token()
        self.bot = telepot.Bot(self.token)
        self.client_id = '736350606'
        self.chat_id = None
        self.msg_received = False

        self.random_replies = []
        self.__set_tandom_replies()

        # Read/Write Locks:

        self.r_lock = threading.RLock()
        self.w_lock = threading.Lock()

        self.__send_hello()
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

            self.__send_msg(id, self.__random_msg())

    # Private Methods:

    def __set_tandom_replies(self):
        self.random_replies = [
            "Hola, me llamo Iñigo Montoya, tú mataste a mi padre, \
            prepárate a morir",
            "Yo soy tu padre",
            "Eres el kernel de mi linux",
            "Mi nombre es Bond, James Bond",
            "Ayúdame, Obi-Wan Kenobi… eres mi única esperanza",
            "Mi mamá siempre me decía que la vida era como una caja de bombones: nunca sabes lo que te va a tocar",
            "Un mago nunca llega tarde, ni pronto: llega exactamente cuando se lo propone",
            "Los programas deben ser escritos para que la gente los lea y sólo accidentalmente, para que las máquinas los ejecuten",
            "Me llamo Máximo Décimo Meridio, general de los ejércitos del \
            norte, capitán de las legiones medias, leal servidor del verdadero \
            emperador Marco Aurelio… marido de una mujer asesinada… padre de un hijo asesinado… y tomaré mi venganza en esta vida o en la otra",
            "Que la Fuerza te acompañe"
            ]

    def __random_msg(self):
        return random.choice(self.random_replies)

    def __send_hello(self):
        self.__send_msg(self.client_id, "Hola Mundo :)")

    def __send_msg(self, target_id, msg):
        try:
            self.bot.sendMessage(target_id, msg)
        except telepot.exception.UnauthorizedError:
            print('yes')
            sys.stderr.write("[ERROR] Invalid Token!\n")
            sys.exit(1)

    def __callback(self, msg):
        self.w_lock.acquire()
        self.msg_received = True
        self.w_lock.release()

        chat_id = msg["chat"]["id"]

        self.w_lock.acquire()
        self.chat_id = chat_id
        self.w_lock.release()

        self.__print_log(msg, '')
        print("-------------------")

    def __print_log(self, msg, st):
        for key in msg:
            if (isinstance(msg[key], dict)):
                print(key)
                self.__print_log(msg[key], st + '\t')
            else:
                print(st + key + ": ", msg[key])

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
    telegram_bot = MyTelegramBot()

    try:
        while (True):
            telegram_bot.step()
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main(sys.argv)
    sys.exit(0)