import paho.mqtt.client as mqtt
import threading
import time

konektatuta = False
denbora = 1


def on_connect(client, userdata, flags, rc):
    global konektatuta

    print("Emaitza-kode honekin konektatuta: " + str(rc))
    client.subscribe("timer/#")
    print()
    print("\"timer\" gaiari buruzko mezuak irakurtzen 10 segundoz...")
    print()

    konektatuta = True


# "timer" gaiko mezu bat jasotzen den bakoitzean, horren edukia pantailaratu
def on_message(client, userdata, msg):
    print("   " + msg.topic + " " + str(msg.payload))


# bezeroa remote broker batera konektatu
def bezeroa_martxan_jarri():
    bezeroa.connect("eclipse-mosquitto", 1883, 60)
    bezeroa.loop_start()


def konektatu_arte_itxaron():
    while not konektatuta:
        pass


# 10 segundo itxaron remote broker-etik deskonektatu eta programaren exekuzioa bukatu baino lehen
def konexioa_itxi():
    time.sleep(10)

    bezeroa.disconnect()
    bezeroa.loop_stop()

    print()
    print("Agur!")
    exit(0)


# "timer/segundoak" gaiari bidali mezu bat segundo bat pasatzen den bakoitzean
def mezuak_bidali():
    global denbora

    if bezeroa.is_connected():
        bezeroa.publish("timer/segundoak", denbora)

        denbora += 1
        time.sleep(1)
        mezuak_bidali()


# bezeroa konfiguratu
bezeroa = mqtt.Client()
bezeroa.on_connect = on_connect  # bezeroarekin connect() metodoari deitu ostean ze metodori deitu behar zaion adierazten du
bezeroa.on_message = on_message  # mezu bat jasotzen den bakoitzean ze metodori deitu behar zaion adierazten du

# bezeroa martxan jarri hari batean
bMJHaria = threading.Thread(target=bezeroa_martxan_jarri)
bMJHaria.start()

# mezuak bidali baino lehen bezeroa remote broker-era konektatu arte itxaron
konektatu_arte_itxaron()

# deskonexio-prozesua martxan jarri hari batean
kIHaria = threading.Thread(target=konexioa_itxi)
kIHaria.start()

# mezuak bidali hari batean (bezeroa entzuten egonda modu paralelo batean mezuak bidali ahal izateko)
mezuak_bidali()