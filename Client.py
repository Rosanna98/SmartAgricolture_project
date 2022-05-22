#https://smartagricolture-project.appspot.com/

from requests import get, post
import csv
import time
from secret import secret
base_url = 'https://smartagricolture-project.appspot.com/' #url a cui vogliamo inviare i dati

#funzione che mi serve per convertire string in float. Altrimenti mi da errore
def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False

with open('Farm_Weather_Data.csv') as fileInput: #lettura del file
    csv_r = csv.reader(fileInput, delimiter=';')
    next(csv_r) #salto la riga di intestazione
    for csv_r in fileInput:
        csv_r=csv_r.strip() #elimino gli spazi tra le righe
        print(csv_r)
        Date,MaxT,MinT,WindSpeed,Humidity,Precipitation = csv_r.split(';')

        # converto variabili in float
        MaxT=MaxT.replace(',','.') #sostituisco la virgola con il punto per far funzionare i comandi successivi
        if isfloat(MaxT):
            MaxT=float(MaxT)
        MinT = MinT.replace(',', '.')
        if isfloat(MinT):
            MinT=float(MinT)
        WindSpeed= WindSpeed.replace(',', '.')
        if isfloat(WindSpeed):
            WindSpeed=float(WindSpeed)
        Humidity = Humidity.replace(',', '.')
        if isfloat(Humidity):
            Humidity=float(Humidity)
        Precipitation = Precipitation.replace(',', '.')
        if isfloat(Precipitation):
            Precipitation=float(Precipitation)

        #invio i dati:
        csv_r = post(f'{base_url}/sensors/sensor1', data={'Date': Date, 'MaxT': MaxT, 'MinT':MinT, 'WindSpeed': WindSpeed, 'Humidity': Humidity, 'Precipitation': Precipitation, 'secret': secret})
        print('sending',Date,MaxT,MinT,WindSpeed,Humidity,Precipitation)
        time.sleep(30)#funzione di sleep per bloccare il processo di invio dati ogni 30 sec '''