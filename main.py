from flask import Flask, request
from google.cloud import firestore
#from secret import secret

app = Flask(__name__)
@app.route('/',methods=['GET'])
def main():
    return 'ok'

@app.route('/sensors/sensor1', methods =['GET']) #metodo che permette di visualizzare tutti i dati
def read_all():
    db=firestore.Client()
    result=''
    for doc in db.collection('sensor1').stream():
        result += (f'{doc.id} --> {doc.to_dict()} <br>')
    return result

@app.route('/sensors/sensor1', methods =['POST']) #questo metodo salva nella tabelal 'sensor1' il timestamp e i dati
def save_data():
    #s =request.values['secret']
    #if s == secret:
    db=firestore.Client()

    Date = request.values['Date']
    MaxT = request.values['MaxT']
    MinT = request.values['MinT']
    WindSpeed = request.values['WindSpeed']
    Humidity = request.values['Humidity']
    Precipitation = request.values['Precipitation']
    db = firestore.Client()
    #per evitare che se si blocca l'invio dei dati e dopo ricomincia evito che si creino duplicati
    db.collection('sensor1').document(Date).set({'Date': Date, 'MaxT': MaxT, 'MinT':MinT, 'WindSpeed': WindSpeed, 'Humidity': Humidity, 'Precipitation': Precipitation})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)