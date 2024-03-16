import board
import time
import feeds
import digitalio
import rotaryio
import display
import feeds
from statuscolors import statusColors

knob = rotaryio.IncrementalEncoder(board.D5, board.SCL)

buttons = [
    digitalio.DigitalInOut(board.D10),
    digitalio.DigitalInOut(board.D12),
    digitalio.DigitalInOut(board.D6),
    digitalio.DigitalInOut(board.D11),
    digitalio.DigitalInOut(board.D13),
    digitalio.DigitalInOut(board.D9)
]
for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.DOWN

lastEncoderPosition = None
lastTemperaturePublish = time.monotonic()
lastEncoderTick = time.monotonic()
newTempPublished = True
def checkEncoder():
    global lastEncoderPosition
    global lastEncoderTick
    global newTempPublished
    lastEncoderTick = time.monotonic()
    newPosition = knob.position
    if lastEncoderPosition == None:
        lastEncoderPosition = newPosition

    if newPosition != lastEncoderPosition:
        if newPosition > lastEncoderPosition:
            display.temperatureSetting = display.temperatureSetting + 1
        if newPosition < lastEncoderPosition:
            display.temperatureSetting = display.temperatureSetting - 1
        display.showTempIndicator()
        newTempPublished = False
        lastEncoderPosition = newPosition

def checkButtons():
    for i in range(len(buttons)):
        if buttons[i].value == True:
            feeds.publish(feeds.commanderFeed, i + 1)

def mqtt_message(client, feed_id, payload):
    print("Got {} from {}".format(payload, feed_id))

    if feed_id == feeds.temperatureSensorFeed:
        display.temperatureReading = round(float(payload))
        display.showTempIndicator()
    elif feed_id == feeds.temperatureSettingFeed:
        display.temperatureSetting = float(payload)
        display.showTempIndicator()
    elif feed_id == feeds.thermostatMode:
        if payload == "heat":
            display.thermostatMode = display.thermostatHeating
        if payload == "cool":
            display.thermostatMode = display.thermostatCooling
        if payload == "off":
            display.thermostatMode = display.thermostatOff
        display.showTempIndicator()     
    elif feed_id == feeds.sunFeed:
        display.setBrightness(payload)
    else:
        display.setStatus(feed_id, payload)

feeds.mqtt_client.on_message = mqtt_message

while (True):
    checkEncoder()
    if (lastEncoderTick - lastTemperaturePublish) > 2 and newTempPublished == False:
        print("publishing")
        feeds.publish(feeds.temperatureSettingFeedCommand, display.temperatureSetting)
        lastTemperaturePublish = time.monotonic()
        newTempPublished = True
    checkButtons()
    feeds.loop()
    time.sleep(.1)
