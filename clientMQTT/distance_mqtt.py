# Importo le librerie necessarie
from gpiozero import DistanceSensor
from time import sleep
import paho.mqtt.client as mqtt

# Definisco il nome del client MQTT
client = mqtt.Client(client_id = "raspberry_1")
# Definizione della connessione al broker, qui va inserito l'indirizzo del broker
client.connect("192.168.1.62")
# Creo due topic, uno per i dati verbosi e uno per quelli secchi
topic_def = "home/distanza/dati_verbosi"
topic_alt = "home/distanza/dati_secchi"

# Istanzio l'oggetto DistanceSensor specificando i pin GPIO utilizzati
sensor = DistanceSensor(echo=24, trigger=23)
# Creo un ciclo infinito dal quale leggo la distanza acquisita dal sensore e la converto in cm
# Stampo il risultato in console
while True:
    distanza = sensor.distance*100
    # Definisco due variabili
    # La prima con una lettura dotata di descrizion
    lettura_verbosa = str('Distanza rilevata: '+str(distanza)+' cm')
    # La seconda con una lettura dei dati secca
    lettura_secca = distanza

    # Creo un file data.json - Se esiste lo sovrascrivo
    f = open("/var/www/html/data.json", "w")
    # Serializzo all'interno di un file un oggetto di tipo {"level":"xx"}
    f.write('data = \'[{"level":"'+str(int(round(distanza)))+'\"}]\';')
    f .close()
    # Scrivo le informazioni salvate nelle due variabili all'interno di due code distinte
    client.publish(topic = topic_def, payload = lettura_verbosa)
    client.publish(topic = topic_alt, payload = lettura_secca)  

	
# Inserisco un timer per ridurre le letture ad una, ogni due secondi
#   sleep(2)
