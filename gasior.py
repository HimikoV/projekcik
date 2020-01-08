import numpy as np
import random


# średnia ilość klientów na minute = .15
klientow=0.05
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
        list[deep_index(list,'kolejkaA')[0][0]][1] -= 1
    except:
        pass
    try:
        list[deep_index(list,'kolejkaB')[0][0]][1] -=1
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
        if list[i][3] == 'kolejkaA':
            listA += 1
        else:
            listB += 1
    return listA, listB

def simulation(klientow):
    list = []
    queueA = 0
    queueB = 0
    time = 0
    profit = 0
    utracony=0
    while time < 720:
        minute_check = random.random()
        list, profit = skracanie_czasu(list, profit)
        if minute_check > 1-klientow:
            los = random.random()
            if queueB-queueA>6 and los<.66 and queueA<8:
                list.append([Client(los), random.randint(5,15),'normalny','kolejkaA'])
            elif queueA>=10 and los>.66:
                if kolejka(queueA):
                    list.append([Client(los), random.randint(15, 35),'biznes','kolejkaA'])
                else:
                    utracony+=1
            elif queueB>=10 and los <=.66:
                if kolejka(queueB):
                    list.append([Client(los), random.randint(5, 15),'normalny','kolejkaB'])
                else:
                    utracony+=1
            else:
                if los > .66:
                    list.append([Client(los), random.randint(15, 35),'biznes','kolejkaA'])
                else:
                    list.append([Client(los), random.randint(5, 15),'normalny','kolejkaB'])
            queueA, queueB = counter(list)
        if time % 60 == 0:
            profit -= (Client.normal_employee_cost + Client.qualified_employee_cost)
        time += 1

    # print(f"profit: {profit}, kolejka biznesowa: {queueA} kolejka normalna: {queueB} klientów utraconych przez rozmyslenie się: {utracony}"  )
    return {'profit':profit,'kolejka1':queueA,'kolejka2':queueB,'utraceni':utracony}

dane={}
dane2={}
import time
poczatek= time.time()
for j in range(50):
    for i in range(1,1001):
        dane[f"dzien{i}"]=simulation(klientow)
    dane2[f"scenariusz{j}"]=dane
    klientow+=0.01
print(dane)
print("czas: ", time.time()-poczatek)