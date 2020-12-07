import paho.mqtt.client as mqtt
import pandas as pd
import datetime
import matplotlib.pyplot as plt


# Qui viene definito il nome del client
client = mqtt.Client(client_id = "imac_subscriber_1")
# Definizione della connessione al broker, qui va inserito l'indirizzo del broker
client.connect("localhost")
topic = "home/distanza/dati_secchi"

colonne = ['data','valore']
df = pd.DataFrame(columns=colonne)
plot_timer = 0
print("primo plot timer "+str(plot_timer))
def plot_data(df):
    df.plot(kind='line', x='data', y='valore')
    plt.show()

def on_message(client, userdata, message):
    now = datetime.datetime.now()
    df.loc[len(df)] = [now,float(message.payload.decode())]
    print(message.payload.decode())
    global plot_timer
    plot_timer +=1
    if plot_timer%20 == 0:
        plot_data(df)
   



client.on_message = on_message
client.subscribe(topic)
client.loop_forever()