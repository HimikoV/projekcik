import pickle
import matplotlib as plt
with open("dane_do_sk.pkl","rb") as file:
    dane = pickle.load(file)
lista=[]
for i in dane:
    for j in dane[i]:
        for k in dane[i][j]:
            lista.append(dane[i][j][k]['profit']*10 - dane[i][j][k]['utraceni']*5)

print(len(lista))