import numpy as np
import random


# średnia ilość klientów na minute = 0.1 normalny (10% szans że w danej minucie przyjdzie klient normalny)
# srednia ilość klientów na minutę = 0.04 biznesowy (5% szans że w danej minucie przyjdzie klient biznesowy)
# sredni czas obslugi 10 - normalny, losujemy między 5 a 15
# sredni czas obslugi 30 - biznesowy losujemy miedzy 20 a 40
# sredni zarobek za klienta normalnego - 65 (losujemy pomiędzy 40 a 90)
# sredni zarobek na klienta biznesowego - 200 (losujemy miedzy 100 a 300)
# wyplata pracowników narzucona z góry, normalny - 2000/160 za godzine, nie liczymy podatków
# wyplata pracowników narzucona z góry, wyszkolony - 5000/160 za godzine, nie liczymy podatków
# jak kolejka dojdzie do 10 czekających, następna osoba która podejdzie ma 50% szans że zrezgynuje,
# każda dodatkowa osoba w kolejce zwiększa ryzyko odejscia następnego klienta
# jak dojdzie do 10 straconych klientów, koniec symulacji, wynikiem jest uzyskany profit na godzine
# dodatkowy warunek stopu to osiągniecie 300% zysku


class Client():
    def __init__(self, category):
        self.category = category

    normal_employee_cost = 2000 / 160
    qualified_employee_cost = 5000 / 160

    def zwroc(self):
        return self.category

    def queue_check(self):
        if self.category > .66:
            return 1
        return 0

def deep_index(lst, w):
    return [(i, sub.index(w)) for (i, sub) in enumerate(lst) if w in sub]


def skracanie_czasu(list, actual_profit):
    lista = []
    for i in range(len(list)):
        if list[i][1] == 0:
            lista.append(i)
            if list[i][0].queue_check():
                actual_profit += random.randint(100, 300)
            else:
                actual_profit += random.randint(40, 90)
    j = 0
    for i in lista:
        del list[i - j]
        j += 1
    try:
        list[deep_index(list,'biznes')[0][0]][1] -= 1
    except:
        pass
    try:
        list[deep_index(list,'normalny')[0][0]][1] -=1
    except:
        pass
    return list, actual_profit

def kolejka(kolejka):
   los = random.randint(1,100)
   if los > 50+5*(kolejka-10):
       return True
   return False

def counter(list):
    listA = 0
    listB = 0
    for i in range(len(list)):
        if list[i][0].zwroc() > .66:
            listA += 1
        else:
            listB += 1
    return listA, listB


list = []
queueA = 0
queueB = 0
iterator = 0
time = 0
profit = 0
utracony=0
while time < 720:
    minute_check = random.random()
    list, profit = skracanie_czasu(list, profit)
    if minute_check > .8:
        los = random.random()
        if queueA>=10:
            if kolejka(queueA):
                if los > .66:
                    list.append([Client(los), random.randint(20, 40),'biznes'])
        elif queueB>=10:
            if kolejka(queueB):
                if los < .66:
                    list.append([Client(los), random.randint(5, 15),'normalny'])
            else:
                utracony+=1
                print(utracony)
        else:
            if los > .66:
                list.append([Client(los), random.randint(20, 40),'biznes'])
            else:
                list.append([Client(los), random.randint(5, 15),'normalny'])
        queueA, queueB = counter(list)
    if time % 60 == 0:
        profit -= (Client.normal_employee_cost + Client.qualified_employee_cost)
    if utracony>10:
        time=721
    time += 1

print(f"profit: {profit}, kolejki {queueA, queueB}")
