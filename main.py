from flask import Flask, request, render_template
from google.cloud import firestore
from secret import secret
import json #consente di convertire oggetti in stringhe in formato json

app = Flask(__name__)
@app.route('/',methods=['GET'])
def main():
    return 'ok'

@app.route('/sensors/sensor1', methods =['GET']) #metodo che permette di visualizzare tutti i dati
def read_all():
    db = firestore.Client.from_service_account_json('credentials.json')
    #db=firestore.Client()
    data=[]
    for doc in db.collection('sensor1').stream(): #questo for scorre tutti i dati presenti nel datastore
        x = doc.to_dict()
        data.append([x['Date'].split(' ')[0],float(x['Humidity'])])
    return json.dumps(data) #trasformo data in una stringa json

@app.route('/graph', methods =['GET'])
def graph():
    #riconverto di nuovo in lista di liste in modo che funzioni l'"insert"
    data = json.loads(read_all()) #loads riconverte la stringa in variabili
    data.insert(0,['Date', 'Humidity']) #inserisco la lista con i titoli
    return render_template('graph.html',data=data) #passo il paramentro data al graph

@app.route('/sensors/sensor1', methods =['POST']) #questo metodo salva nella tabelal 'sensor1' il timestamp e i dati
def save_data():
    s = request.values['secret']
    if s == secret:
        Date = request.values['Date']
        MaxT = request.values['MaxT']
        MinT = request.values['MinT']
        WindSpeed = request.values['WindSpeed']
        Humidity = request.values['Humidity']
        Precipitation = request.values['Precipitation']
        db = firestore.Client.from_service_account_json('credentials.json')
        #db = firestore.Client()
        #per evitare che se si blocca l'invio dei dati e dopo ricomincia evito che si creino duplicati
        db.collection('sensor1').document(Date).set({'Date': Date, 'MaxT': MaxT, 'MinT':MinT, 'WindSpeed': WindSpeed, 'Humidity': Humidity, 'Precipitation': Precipitation})
        return "ok", 200
    else:
        return "", 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)