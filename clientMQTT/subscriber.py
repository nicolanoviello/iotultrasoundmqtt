
# Importo le librerie necessarie
import paho.mqtt.client as mqtt
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# Istanzio l'oggetto e definisco il nome del client MQTT
client = mqtt.Client(client_id = "imac_subscriber_1")
# Definisco la connessione al broker, qui va inserito l'indirizzo del broker
client.connect("localhost")
# Setto il topic di interesse
topic = "home/distanza/dati_secchi"

# Creo un DataFrame per raccogliere e trattare un subset di dati acquisiti
colonne = ['data','valore']
df = pd.DataFrame(columns=colonne)

# Definisco un metodo che, quando chiamata
# mostra con un grafico le informazioni raccolte
plot_timer = 0
print("primo plot timer "+str(plot_timer))
def plot_data(df):
    df.plot(kind='line', x='data', y='valore')
    plt.show()
# Definisco un metodo che aggiunge la lettura del messaggio con la relativa data
# ad un dataframe ogni qualvolta viene chiamato
def on_message(client, userdata, message):
    now = datetime.datetime.now()
    # Creo una struttura con la data di lettura ed il payload
    df.loc[len(df)] = [now,float(message.payload.decode())]
    print(message.payload.decode())
    global plot_timer
    plot_timer +=1
    # Aggiorno il grafico con le letture ogni due minuti
    if plot_timer%60 == 0:
        plot_data(df)
   


# Chiamo il metodo on_message quando ricevo un messaggio
client.on_message = on_message
# Creao una subscription ad un topic
client.subscribe(topic)
# Resto in ascolto in maniera indefinita
client.loop_forever()