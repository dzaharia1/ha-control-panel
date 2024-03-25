import board
import time
import feeds
import digitalio
import rotaryio
import display
import feeds
from statuscolors import statusColors

knob = rotaryio.IncrementalEncoder(board.A2, board.A1)
knobButton = digitalio.DigitalInOut(board.A0)
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
timeSinceKnobInteract = time.monotonic()
KnobInteract = time.monotonic()
lastTemperaturePublish = time.monotonic()
lastEncoderMove = time.monotonic()
timeSinceLastEncoderMove = time.monotonic()
newTempPublished = True

def checkEncoder():
    global lastEncoderPosition
    global timeSinceKnobInteract
    global KnobInteract
    global lastEncoderMove
    global timeSinceLastEncoderMove
    global newTempPublished

    newPosition = knob.position
    if lastEncoderPosition == None:
        lastEncoderPosition = newPosition

    if newPosition != lastEncoderPosition:
        KnobInteract = time.monotonic()
        timeSinceKnobInteract = time.monotonic()
        lastEncoderMove = time.monotonic()
        timeSinceLastEncoderMove = time.monotonic()
        display.activateDisplay()
        if display.selectMode:
            if newPosition > lastEncoderPosition:
                display.selectItem(1)
            else:
                display.selectItem(-1)
        else:
            if newPosition > lastEncoderPosition:
                display.temperatureSetting = display.temperatureSetting + 1
            if newPosition < lastEncoderPosition:
                display.temperatureSetting = display.temperatureSetting - 1
            newTempPublished = False
            display.showTempIndicator()
        lastEncoderPosition = newPosition
        time.sleep(.1)

def checkKnobButton():
    global timeSinceKnobInteract
    global KnobInteract
    if not knobButton.value:
        KnobInteract = time.monotonic()
        timeSinceKnobInteract = time.monotonic()
        display.activateDisplay()
        if display.selectMode:
            performIconAction(display.selectedItem)
        else:
            display.setSelectMode()
        time.sleep(.2)

def performIconAction(index):
    print("Performing action {}".format(index))
    if index == 0:
        feeds.publish(feeds.commanderFeed, 6)
    if index == 2:
        if display.deviceStatuses[feeds.subwaySignFeed] == "ON":
            feeds.publish("subway-sign/status", "OFF")
        else:
            feeds.publish("subway-sign/status", "ON")
    if index == 3:
        feeds.publish(feeds.commanderFeed, 7)
    if index == 5:
        feeds.publish(feeds.commanderFeed, 8)
    if index == 7:
        feeds.publish(feeds.commanderFeed, 9)
    feeds.loop()
    display.unsetSelectMode()

def checkButtons():
    for i in range(len(buttons)):
        if buttons[i].value == True:
            if i == 5:
                print(5)
                feeds.publish(feeds.commanderFeed, 5)
            elif i == 4: 
                print(7)
                feeds.publish(feeds.commanderFeed, 7)
            else:
                print(i)
                feeds.publish(feeds.commanderFeed, i + 1)
            time.sleep(.1)

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
    checkButtons()
    if (timeSinceLastEncoderMove - lastEncoderMove) > .2 and not newTempPublished and not display.selectMode:
        print("publishing temperature")
        feeds.publish(feeds.temperatureSettingFeedCommand, display.temperatureSetting)
        newTempPublished = True
    timeSinceLastEncoderMove = time.monotonic()
    timeSinceKnobInteract = time.monotonic()
    if timeSinceKnobInteract - KnobInteract > 5:
        display.deActivateDisplay()
    if (not display.selectMode):
        feeds.loop()
    else:
        time.sleep(.1)
