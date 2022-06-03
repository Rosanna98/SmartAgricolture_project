from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from google.cloud import firestore
from secret import secret, secret_key, usersdb
import json #consente di convertire oggetti in stringhe in formato json

#creazione oggetto utente
class User(UserMixin):
    def __init__(self, username):
        super().__init__()
        self.id = username
        self.username = username
        self.par = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
login = LoginManager(app)
login.login_view = '/static/login-form/index.html'


@login.user_loader
def load_user(username):
    if username in usersdb:
        return User(username)
    return None

@app.route('/',methods=['GET'])
def main():
    return render_template("home.html")

@app.route('/pers',methods=['GET'])
def pers():
    return render_template("personal_page.html")

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
@login_required #questa funzione diventa accessibile solo quando l'utente fa il login
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

@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/pers'))
    username = request.values['u']
    password = request.values['p']
    if username in usersdb and password == usersdb[username]:
        login_user(User(username), remember=True)
        next_page = request.args.get('next')
        if not next_page:
            next_page = '/'
        return redirect(next_page)
    return redirect('/static/login-form/index.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)