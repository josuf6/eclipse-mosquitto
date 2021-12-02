import paho.mqtt.client as mqtt
import threading

denbora = 0  # denbora kontrolatzeko erabiltzen den aldagai globala


def on_connect(client, userdata, flags, rc):
    print("Emaitza-kode honekin konektatuta: " + str(rc))
    client.subscribe("timer/#")
    print()
    print("\"timer\" gaiari buruzko mezuak irakurtzen...")
    print()


# "timer" gaiko mezu bat jasotzen den bakoitzean, horren edukia pantailaratu
def on_message(client, userdata, msg):
    print("   " + msg.topic + " " + str(msg.payload))


# bezeroa remote broker batera konektatu
def bezeroaMartxanJarri():
    bezeroa.connect("mqtt.eclipseprojects.io", 1883, 60)
    bezeroa.loop_forever()


def konektatuArteItxaron():
    konektatuta = False

    while not konektatuta:
        if bezeroa.is_connected():
            konektatuta = True


# "timer/segundoak" gaiari bidali mezu bat segundo bat pasatzen den bakoitzean
# minutu bakoitzero mezu bat bidaltzen da "timer/minutuak" gaiari ere
def mezuakBidali():
    global denbora

    if bezeroa.is_connected():
        bezeroa.publish("timer/segundoak", denbora)

        if denbora > 0 and denbora % 60 == 0:
            if denbora == 60:
                bezeroa.publish("timer/minutuak", "minutu bat")
            else:
                bezeroa.publish("timer/minutuak", str(int(denbora/60)) + " minutu")

        denbora += 1
        threading.Timer(1.0, mezuakBidali).start()


# bezeroa konfiguratu
bezeroa = mqtt.Client()
bezeroa.on_connect = on_connect  # bezeroarekin connect() metodoari deitu ostean ze metodori deitu behar zaion adierazten du
bezeroa.on_message = on_message  # mezu bat jasotzen den bakoitzean ze metodori deitu behar zaion adierazten du

# bezeroa martxan jarri hari batean
bMJHaria = threading.Thread(target=bezeroaMartxanJarri)
bMJHaria.start()

# mezuak bidali baino lehen bezeroa remote broker-era konektatu arte itxaron
konektatuArteItxaron()

# mezuak bidali hari batean (bezeroa entzuten egonda modu paralelo batean mezuak bidali ahal izateko)
mBHaria = threading.Thread(target=mezuakBidali)
mBHaria.start()