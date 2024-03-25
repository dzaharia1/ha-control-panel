import board
import microcontroller
import time
import wifi
import ssl
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from secrets import secrets

temperatureSettingFeed = "state/temp-setting"
temperatureSettingFeedCommand = "state/temp-setting-command"
temperatureSensorFeed = "state/temp-sensor"
thermostatMode = "state/thermostat-mode-command"
fanToggleFeed = "state/fan-on"
fanSpeedFeed = "state/fan-speed"
subwaySignFeed = "state/subway-sign"
vacuumFeed = "state/vacuum"
airQualityFeed = "sensor/air-quality"
mediaFeed = "state/media"
TVFeed = "state/tv"
humidifierFeed = "state/humidifier"
humidifierEmptyFeed = "state/humidifier-empty"
videoCallFeed = "state/video-call"
commanderFeed = "commander/command"
sunFeed = "state/sun"

subscriptions = [
    (temperatureSettingFeed, 1),
    (thermostatMode, 1),
    (fanToggleFeed, 1),
    (temperatureSensorFeed, 1),
    (subwaySignFeed, 1),
    (vacuumFeed, 1),
    (airQualityFeed, 1),
    (mediaFeed, 1),
    (TVFeed, 1),
    (humidifierFeed, 1),
    (humidifierEmptyFeed, 1),
    (videoCallFeed, 1),
    (sunFeed, 1)
]

def connected(client, userdata, flags, rc):
    print("Connected to HA!")

def disconnected(client):
    print("Disconnected from HA")

def subscribed(a, b, c, d):
    print("Subscribed")

def connect():
    try:
        wifi.radio.connect(secrets["ssid"], secrets["password"])
    except:
        print("Failed to connect to wifi")
        time.sleep(3)
        connect()
    print("Connected to wifi")

connect()

pool = socketpool.SocketPool(wifi.radio)
socket_timeout = .1
mqtt_client = MQTT.MQTT(
    broker=secrets["mqtt_broker"],
    port=secrets["mqtt_port"],
    username=secrets["mqtt_username"],
    password=secrets["mqtt_password"],
    socket_pool=pool,
    socket_timeout=socket_timeout
)

def publish(feed, data):
    try:
        mqtt_client.publish(feed, data, retain=True)
    except:
        try:
            mqtt_client.reconnect(resub_topics=False)
            mqtt_client.subscribe(subscriptions)
        except:
            wifi.radio.connect(secrets["ssid"], secrets["password"])

        publish(feed, data)

def loop():
    try:
        mqtt_client.loop(timeout=socket_timeout)
    except:
        print("Couldn't loop")
        try:
            mqtt_client.reconnect(resub_topics=True)
        except:
            wifi.radio.connect(secrets["ssid"], secrets["password"])
            loop()

mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_subscribe = subscribed

mqtt_client.connect()

mqtt_client.subscribe(subscriptions)
