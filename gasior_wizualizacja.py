import pickle
import matplotlib as plt
with open("dane_do_gasiora","rb") as file:
    dane2 = pickle.load(file)

for i in dane2:
    for j in dane2[i]:
        iterator=0
        for k in dane2[i][j]:
            print(dane2[i][j][k])