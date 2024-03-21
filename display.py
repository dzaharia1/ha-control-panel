import board
import neopixel
import digitalio
from statuscolors import statusColors

dayBrightness = 30
nightBrightness = 10
brightness = nightBrightness
offBrightness = 2
sunState = "below_horizon"
temperatureSetting = 70
temperatureReading = 66
thermostatMode = statusColors["state/thermostat-mode-command"]["heat"]
displayActive = False

temperatureDisplay = neopixel.NeoPixel(board.SDA, 16, pixel_order=neopixel.RGB)
statusRowOne = neopixel.NeoPixel(board.A5, 4, pixel_order=neopixel.RGB)
statusRowTwo = neopixel.NeoPixel(board.A4, 5, pixel_order=neopixel.RGB)
for light in statusRowOne:
    light = (0, 0, 0)
for light in statusRowTwo:
    light = (0, 0, 0)
statusRowOne.show()
statusRowTwo.show()

deviceStatuses = {
    "state/vacuum": "cleaning",
    "sensor/air-quality": "30",
    "subway-sign/switch": "ON",
    "state/media": "playing",
    "state/fan-on": "1",
    "state/humidifier": "on",
    "state/humidifier-empty": "off",
    "state/video-call": "on",
    "state/tv": "on",
}


statusLightsDictionaryOne = {
    "state/vacuum": 0,
    "sensor/air-quality": 1,
    "subway-sign/switch": 2,
    "state/media": 3
}

statusLightsDictionaryTwo = {
    "state/fan-on": 0,
    "state/humidifier": 1,
    "state/humidifier-empty": 1,
    "state/video-call": 2,
    "state/tv": 3,
    "battery": 4
}

def setThermostatMode(mode):
    global thermostatMode
    thermostatMode = statusColors["state/thermostat-mode-command"][mode]

def setBrightness(state):
    global brightness
    global sunState
    sunState = state
    if sunState == "above_horizon":
        brightness = dayBrightness
    elif sunState == "below_horizon":
        brightness = nightBrightness
    elif sunState == "off":
        brightness = offBrightness

    showTempIndicator()
    for thisDevice in deviceStatuses:
        setStatus(thisDevice, deviceStatuses[thisDevice])

def setStatus(device, status):
    statusColor = (0, 0, 0)
    deviceStatuses[device] = status
    # if displayActive == True or brightness == dayBrightness:
    if status in statusColors[device]:
        statusColor = tuple(value * brightness for value in statusColors[device][status])

    if device == "sensor/air-quality":
        status = int(status)
        if status >= 0 and status <= 50:
            statusColor = tuple(value * brightness for value in statusColors[device]["good"])
        elif status > 50 and status <= 100:
            statusColor = tuple(value * brightness for value in statusColors[device]["medium"])
        elif status > 100 and status <= 150:
            statusColor = tuple(value * brightness for value in statusColors[device]["bad"])
        elif status > 150:
            statusColor = tuple(value * brightness for value in statusColors[device]["terrible"])
    elif device == "state/fan-on":
        statusColor = tuple((value * int(status) * brightness) for value in thermostatMode)
    elif device == "state/humidifier-empty":
        global humidifierEmpty
        humidifierEmpty = status
    elif device == "state/humidifier":
        global humidifierRunning
        humidifierRunning = status
        if humidifierEmpty == "on":
            statusColor = tuple(value * brightness for value in statusColors["state/humidifier-empty"]["on"])

    if device in statusLightsDictionaryOne:
        statusRowOne[statusLightsDictionaryOne[device]] = statusColor
    else:
        statusRowTwo[statusLightsDictionaryTwo[device]] = statusColor
    # else:
    #     deActivateDisplay()

def showTempIndicator():
    # if displayActive == True or brightness == dayBrightness:
    tempSettingIndex = 77 - temperatureSetting
    tempSettingIndex = max(0, tempSettingIndex)
    tempSettingIndex = min(14, tempSettingIndex)

    tempReadingIndex = 77 - temperatureReading
    tempReadingIndex = max(0, tempReadingIndex)
    tempReadingIndex = min(14, tempReadingIndex)

    for i in range(len(temperatureDisplay)):
        temperatureDisplay[i] = (0, 0, 0)
        if i >= min(tempSettingIndex, tempReadingIndex) and i <= max(tempSettingIndex, tempReadingIndex):
            temperatureDisplay[i] = tuple(value * brightness for value in thermostatMode)
        if i == tempSettingIndex:
            temperatureDisplay[i] = (brightness, brightness, brightness)

def activateDisplay():
    global displayActive
    if not displayActive:
        displayActive = True
        print("Activating")
        setBrightness(sunState)
        # showTempIndicator()
        # for thisDevice in deviceStatuses:
        #     setStatus(thisDevice, deviceStatuses[thisDevice])

def deActivateDisplay():
    global displayActive
    global brightness
    if displayActive:
        print("Deactivating")
        displayActive = False
        brightness = offBrightness
        showTempIndicator()
        for thisDevice in deviceStatuses:
            setStatus(thisDevice, deviceStatuses[thisDevice])
        # temperatureDisplay.fill((0, 0, 0))
        # statusRowOne.fill((0, 0, 0))
        # statusRowTwo.fill((0, 0, 0))