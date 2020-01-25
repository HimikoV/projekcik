import pickle
import matplotlib as plt
import numpy as np
with open("dane_do_sk.pkl","rb") as file:
    dane = pickle.load(file)
lista=[]


for i in dane:
    for j in dane[i]:
        for k in dane[i][j]:
            lista.append(dane[i][j][k]["profit"]*5-dane[i][j][k]["utraceni"]*100)

wskaznik=[]
for i in range(20):
    suma=0
    for j in range(5000):
        suma+=lista[5000*i+j]
    wskaznik.append(suma/5000)
print(wskaznik)
