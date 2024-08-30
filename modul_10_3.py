from threading import Thread, Lock
from time import sleep
from random import randint


class Bank:
    balans = 0
    lock = Lock()

    def deposit(self):
        for i in range(100):
            cash_d = randint(50, 500)
            self.balans = self.balans + cash_d
            print(f"Пополнение: {cash_d}. Баланс: {self.balans}")
            if self.balans >= 500 and self.lock.locked():
                self.lock.release()
            sleep(0.001)

    def take(self):
        for i in range(100):
            while True:
                if not self.lock.locked():
                    cash_t = randint(50, 500)
                    break
            print(f"Запрос на {cash_t}")
            if cash_t <= self.balans:
                self.balans = self.balans - cash_t
                print(f"Снятие: {cash_t}. Баланс: {self.balans}")
            else:
                print('Запрос отклонён, недостаточно средств')
                self.lock.acquire()
            sleep(0.001)


bk = Bank()

th1 = Thread(target=Bank.deposit, args=(bk,))
th2 = Thread(target=Bank.take, args=(bk,))
th1.start()
th2.start()
th1.join()
th2.join()
print(f'Итоговый баланс: {bk.balans}')
