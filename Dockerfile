# Python irudia
FROM python:3.7-alpine

# lan-direktorioa zehaztu
WORKDIR /fitxategiak

# paho.mqtt.client liburutegia erabili ahal izateko
RUN pip install paho-mqtt

# beharrezko fitxategia container-ean bezeroa egikaritu ahal izateko
COPY bezeroa.py /fitxategiak/

# hasiera-komandoa
CMD ["python","bezeroa.py"]