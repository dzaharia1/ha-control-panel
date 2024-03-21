import board
import time
import feeds
import digitalio
import rotaryio
import display
import feeds
from statuscolors import statusColors

knob = rotaryio.IncrementalEncoder(board.SCL, board.D5)
knobButton = digitalio.DigitalInOut(board.A2)
knobButton.direction = digitalio.Direction.INPUT
knobButton.pull = digitalio.Pull.UP

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
timeSinceKnobInteract = time.monotonic()
KnobInteract = time.monotonic()

def checkEncoder():
    global lastEncoderPosition
    global lastEncoderTick
    global newTempPublished
    global timeSinceKnobInteract
    global KnobInteract
    lastEncoderTick = time.monotonic()
    newPosition = knob.position
    if lastEncoderPosition == None:
        lastEncoderPosition = newPosition

    if newPosition != lastEncoderPosition:
        KnobInteract = time.monotonic()
        timeSinceKnobInteract = time.monotonic()
        display.activateDisplay()
        if newPosition > lastEncoderPosition:
            display.temperatureSetting = display.temperatureSetting + 1
        if newPosition < lastEncoderPosition:
            display.temperatureSetting = display.temperatureSetting - 1
        display.showTempIndicator()
        newTempPublished = False
        lastEncoderPosition = newPosition

def checkKnobButton():
    global timeSinceKnobInteract
    global KnobInteract
    if not knobButton.value:
        KnobInteract = time.monotonic()
        timeSinceKnobInteract = time.monotonic()
        if display.displayActive:
            display.selectNextPosition()
        else:
            display.activateDisplay()

def checkButtons():
    for i in range(len(buttons)):
        if buttons[i].value == True:
            if i == 5:
                print(5)
                feeds.publish(feeds.commanderFeed, 5)
            elif i == 4: 
                print(6)
                feeds.publish(feeds.commanderFeed, 6)
            else:
                print(i)
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
        display.setThermostatMode(payload)
        display.showTempIndicator()     
    elif feed_id == feeds.sunFeed:
        display.setBrightness(payload)
    else:
        display.setStatus(feed_id, payload)

feeds.mqtt_client.on_message = mqtt_message

while (True):
    checkEncoder()
    checkKnobButton()
    if (lastEncoderTick - lastTemperaturePublish) > 2 and newTempPublished == False:
        print("publishing")
        feeds.publish(feeds.temperatureSettingFeedCommand, display.temperatureSetting)
        lastTemperaturePublish = time.monotonic()
        newTempPublished = True
    timeSinceKnobInteract = time.monotonic()
    if timeSinceKnobInteract - KnobInteract > 5:
        display.deActivateDisplay()
    checkButtons()
    feeds.loop()
