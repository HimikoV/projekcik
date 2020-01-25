import pickle
import matplotlib as plt
import numpy as np
with open("dane_do_sk2.pkl","rb") as file:
    dane = pickle.load(file)

with open("dane_do_sk.pkl", "rb") as file:
    dane1 = pickle.load(file)

def zbieranina(dane):
    lista=[]
    for i in dane:
        for j in dane[i]:
            for k in dane[i][j]:
                lista.append(dane[i][j][k]["profit"]*5-dane[i][j][k]["utraceni"]*100)
    return lista

def liczenie_wskaznika(lista):
    wskaznik=[]
    for i in range(20):
        suma=0
        for j in range(5000):
            suma+=lista[5000*i+j]
        wskaznik.append(suma/5000)
    return wskaznik

print(liczenie_wskaznika(zbieranina(dane))) #dane dla SK2
print(liczenie_wskaznika(zbieranina(dane1))) #dane dla SK

