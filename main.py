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
    db=firestore.Client()
    data=[]
    result=''
    for doc in db.collection('sensor1').stream():
        x = doc.to_dict()
        data.append([x['Date'],float(x['Humidity'])])
    return json.dumps(data) #bisogna che ritorni una stringa affichè il broswer lo possa leggere quindi usiamo json

@app.route('/graph', methods =['GET'])
def graph():
    #riconverto di nuovo in lista di liste in modo che funzioni l'"insert"
    data = json.loads(read_all()) #questa funzione chiama la funzione di sopra e si fa passare i dati numerici
    data.insert(0,['Date', 'Humidity'])
    return render_template('graph.html',data=data)

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
        db = firestore.Client()
        #per evitare che se si blocca l'invio dei dati e dopo ricomincia evito che si creino duplicati
        db.collection('sensor1').document(Date).set({'Date': Date, 'MaxT': MaxT, 'MinT':MinT, 'WindSpeed': WindSpeed, 'Humidity': Humidity, 'Precipitation': Precipitation})
        return "ok", 200
    else:
        return "", 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)