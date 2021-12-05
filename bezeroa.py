import paho.mqtt.client as mqtt
import threading

konektatuta = False


def on_connect(client, userdata, flags, rc):
    print("Emaitza-kode honekin konektatuta: " + str(rc))
    client.subscribe("$SYS/#")
    print()
    print("\"$SYS\" gaiari buruzko mezuak irakurtzen...")
    print()


# "$SYS" gaiko mezu bat jasotzen den bakoitzean, horren edukia pantailaratu
def on_message(client, userdata, msg):
    print("   " + msg.topic + " " + str(msg.payload))


# bezeroa remote broker batera konektatu
def bezeroa_martxan_jarri():
    bezeroa.connect("mqtt.eclipseprojects.io", 1883, 60)
    bezeroa.loop_forever()


def konektatu_arte_itxaron():
    global konektatuta

    while not konektatuta:
        if bezeroa.is_connected():
            konektatuta = True


# bezeroa konfiguratu
bezeroa = mqtt.Client()
bezeroa.on_connect = on_connect  # bezeroarekin connect() metodoari deitu ostean ze metodori deitu behar zaion adierazten du
bezeroa.on_message = on_message  # mezu bat jasotzen den bakoitzean ze metodori deitu behar zaion adierazten du

# bezeroa martxan jarri hari batean
bMJHaria = threading.Thread(target=bezeroa_martxan_jarri)
bMJHaria.start()

# mezuak bidali baino lehen bezeroa remote broker-era konektatu arte itxaron
konektatu_arte_itxaron()
