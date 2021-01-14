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

        self.random_replies = [
            "Hola, me llamo Iñigo Montoya, tú mataste a mi padre, \
            prepárate a morir",
            "Yo soy tu padre",
            "Mi nombre es Bond, James Bond",
            "Ayúdame, Obi-Wan Kenobi… eres mi única esperanza",
            "Mi mamá siempre me decía que la vida era como una caja de bombones: nunca sabes lo que te va a tocar",
            "Un mago nunca llega tarde, ni pronto: llega exactamente cuando se lo propone",
            "Me llamo Máximo Décimo Meridio, general de los ejércitos del \
            norte, capitán de las legiones medias, leal servidor del verdadero \
            emperador Marco Aurelio… marido de una mujer asesinada… padre de un hijo asesinado… y tomaré mi venganza en esta vida o en la otra"
            ]

        # Read/Write Locks:

        self.r_lock = threading.RLock()
        self.w_lock = threading.Lock()

        self.__send_hello()
        MessageLoop(self.bot, self.__callback).run_as_thread()

    def step(self):
        self.r_lock.acquire()
        received = self.msg_received
        self.r_lock.acquire()

        if (received):
            self.w_lock.acquire()
            self.msg_received = False
            self.w_lock.release()

            self.r_lock.acquire()
            id = self.chat_id
            self.r_lock.acquire()

            self.bot.sendMessage(id, self.__random_msg())

    # Private Methods:

    def __random_msg(self):
        return random.choice(self.random_replies)

    def __send_hello(self):
        self.bot.sendMessage(self.client_id, "Hola Mundo :)")

    def __callback(self, msg):
        self.w_lock.acquire()
        self.msg_received = True
        self.w_lock.release()

        chat_id = msg["chat"]["id"]

        self.w_lock.acquire()
        self.chat_id = chat_id
        self.w_lock.release()

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