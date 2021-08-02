import requests
from bs4 import BeautifulSoup
import json

from fastapi import FastAPI
#Variables globales


#Funciones Operativas

def encontrar_todas(cadena, subcadena):
    posiciones = []
    posicion = 0

    while posicion != -1:
        posicion = cadena.find(subcadena,posicion)
        if posicion != -1:
            posiciones.append(posicion)
            posicion += 1
    return posiciones

def extraccion():
    r = requests.get('https://play.google.com/store/apps/details?id=com.clarocolombia.miclaro&hl=es_CO&gl=US&showAllReviews=true')
    soup=BeautifulSoup(r.text, 'lxml')
    data=str(soup) 
    Bloque_Comentarios=data[686000:735000]
    posiciones1 = encontrar_todas(Bloque_Comentarios,'"')
    comentarios=[]
    for i in range(len(posiciones1)):
        if (i!=(len(posiciones1)-1)):
            if ((posiciones1[i+1]-posiciones1[i]>150)):  
                comentarios.append(Bloque_Comentarios[posiciones1[i]:posiciones1[i+1]])    
    return comentarios

def dictionario():
    receptor=extraccion()
    comentarios_dict=dict(enumerate(set(receptor)))
    return comentarios_dict 
perri=[1,2]
app=FastAPI()

@app.get('/')
def rea_root():
    return {"Welcome":"wenas"}

@app.get('/comments')
def visualize_comments():    
    return dictionario()

@app.post('/comments')
def visualize_Ncomments(n):
    number=int(n)
    print(type(number))
    receptor=extraccion()
    comentarios_dict=dict(enumerate(set(receptor[0:number])))  
    return comentarios_dict

#@app.post()