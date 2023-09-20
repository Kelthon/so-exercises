#!/usr/bin/python3

from time import sleep
from random import randint
from typing import List, Any
from threading import Thread, Semaphore

class BankCashier():
    def __init__(self, id: str) -> None:
        self.__id = id
        self.__isfree = True
        self.__current_ticket = None

    @property
    def id(self) -> str:
        return self.__id

    @property
    def isfree(self) -> bool:
        return self.__isfree

    def update(self, ticket) -> None:
        self.__current_ticket = ticket
        self.__isfree = False

    def resolve(self) -> None:
        if not self.__isfree:
            sleep(randint(3, 10))
            self.__isfree = True
            self.__current_ticket = None

    def __repr__(self) -> str:
        return f'[{self.__id} | {self.__current_ticket}]'


class Bank():
    def __init__(self) -> None:
        self.__queue: List[str] = []
        self.__cashierlist: List[BankCashier] = [
            BankCashier('01'), BankCashier('02'), BankCashier('03')
        ]

    def add(self, ticket: str) -> None:
        self.__queue.append(ticket)

    def remove(self, ticket: str) -> None:
        return self.__queue.pop(0)

    def semaphore(self):
        semaphore = Semaphore()
        semaphore.acquire()
        thread =  Thread(target=self.update, args=())
        thread.start()
        semaphore.release()

    def update(self):
        for ticket in self.__queue:
            slist = f'['
            for i in self.__queue[0:5]:
                slist = slist + (f', {i}' if i != self.__queue[0] else f'{i}' )
            elist = f' ... {slist[-1]}]' if len(self.__queue) > 5 else ']' 
            print(ticket, f'{slist}{elist}')

            for cashier in self.__cashierlist:
                cashier.update(ticket)
                print(cashier)
                cashier.resolve()
            print()


    def __repr__(self) -> str:
        return f'{self.__queue}'


if __name__ == '__main__':

    myBank = Bank()

    for i in range(30):
        randonStr = chr(randint(65, 71))
        ticket = f'0{i}{randonStr}' if i < 10 else f'{i}{randonStr}'
        myBank.add(ticket)

    myBank.semaphore()

    print(myBank)
