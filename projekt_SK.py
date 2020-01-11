import numpy as np
import random

"""
# średnia ilość klientów na minute = .15, założenie że 1 na 3 klientów jest biznesowy 
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
dodać możlwiość modyfikacji średnich zarobków
w sprawku opisać problem, postawić pytanie badania
opisac przebieg symulacji, ilość powtórzeń zmieniane parametry itd
wykresy omega od czasu dla dwóch wariantów śrendich czasów obsługi, pamiętać o wskaźniku jakości(co to wgl jest?XD)
test statystyczny dla średniej 100k wskaźników, gdzie każdy wskąźnik jest liczony dla każdego dnia każdej symulacji,
zrobić to dla obydwóch przypadków porównać te 2 wskaźniki i zdecydować czy jest to znaczne
TEST Z będzie pasować
"""
#klasa stworzona do tworzenia obiektu klienta
class Client():
    def __init__(self, category):
        self.category = category
    #zarobki pracowników
    normal_employee_cost = 2000 / 160
    qualified_employee_cost = 5000 / 160
    #zwraca True jeśli klient biznesowe, False dla normalnego
    def queue_check(self):
        if self.category > .66:
            return 1
        return 0

#do wyszukiwania indexów
def deep_index(lst, w):
    return [(i, sub.index(w)) for (i, sub) in enumerate(lst) if w in sub]

#funckja skraca czas obslugiwannych aktualnie klientów oraz
#usuwa już obsłużonych a za nich nalicza odpowiedni profit
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
        list[deep_index(list, 'kolejkaA')[0][0]][1] -= 1
    except:
        pass
    try:
        list[deep_index(list, 'kolejkaB')[0][0]][1] -= 1
    except:
        pass
    return list, actual_profit

#zwraca czy osoba się rozmyśliła po zobaczeniu zbyt długiej kolejki
def kolejka(kolejka):
    los = random.randint(1, 100)
    if los > 50 + 5 * (kolejka - 10):
        return True
    return False

#zlicza aktualny stan kolejki biznesowej i kolejki normalnej
def counter(list):
    listA = 0
    listB = 0
    for i in range(len(list)):
        if list[i][3] == 'kolejkaA':
            listA += 1
        else:
            listB += 1
    return listA, listB

#symulacja całego obiektu
def simulation(klientow, srednia):
    list = []
    queueA = 0
    queueB = 0
    time = 0
    profit = 0
    utracony = 0
    klient=0
    while time < 720: #czas symulacji - 12h pracy
        minute_check = random.random()
        list, profit = skracanie_czasu(list, profit)
        if minute_check > 1 - klientow: #co minute czasu symulacji czy zjawił się nowy klient w zależności od średniej klientów na minute
            los = random.random()
            klient+=1
            if queueB - queueA > 6 and los < .66 and queueA < 8:
                list.append([Client(los), random.randint(srednia[0]-5, srednia[0]+5), 'normalny', 'kolejkaA'])
            elif queueA >= 10 and los > .66:
                if kolejka(queueA):
                    list.append([Client(los), random.randint(srednia[1]-10, srednia[1]+10), 'biznes', 'kolejkaA'])
                else:
                    utracony += 1
            elif queueB >= 10 and los <= .66:
                if kolejka(queueB):
                    list.append([Client(los), random.randint(srednia[0]-5, srednia[0]+5), 'normalny', 'kolejkaB'])
                else:
                    utracony += 1
            else:
                if los > .66:
                    list.append([Client(los), random.randint(srednia[1]-10, srednia[1]+10), 'biznes', 'kolejkaA'])
                else:
                    list.append([Client(los), random.randint(srednia[0]-5, srednia[0]+5), 'normalny', 'kolejkaB'])
            queueA, queueB = counter(list)
        if time % 60 == 0:
            profit -= (Client.normal_employee_cost + Client.qualified_employee_cost)
        time += 1

    # print(f"profit: {profit}, kolejka biznesowa: {queueA} kolejka normalna: {queueB}
    # klientów utraconych przez rozmyslenie się: {utracony}"  )
    return {'profit': profit, 'kolejka1': queueA, 'kolejka2': queueB, 'utraceni': utracony, 'iloscKlientow': klient}


dane = {}
dane2 = {}
import time
dane3={}
klientow = 0.05
poczatek = time.time()
srednia = [[10,25],[15,30]]
for k in range(2):
    for j in range(50): #ilosc wariantów (srednia czestotliwosc klientow)
        for i in range(1, 1001):
            dane[f"dzien{i}"] = simulation(klientow,srednia[k]) #ilosc prob sprawdzania danej symulacji
        dane2[f"scenariusz{j}"] = dane
        klientow += 0.01
    dane3[f"srednia{k}"]=dane2
print("czas: ", time.time() - poczatek) #zwraca czas pracy symulacji
import pickle
#zapisywanie zebranych danych nt profit, ilosci kolejek pod koniec dnia, utraconych klientow danego dnia oraz sredniej ilosc klientow danego dnia
with open("dane_do_sk.pkl","wb") as file:
    pickle.dump(dane3,file)