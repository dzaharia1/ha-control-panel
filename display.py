import board
import neopixel
from statuscolors import statusColors

dayBrightness = 30
nightBrightness = 10
brightness = dayBrightness
temperatureSetting = 70
temperatureReading = 66
thermostatHeating = (1, .5, .1)
thermostatCooling = (.1, .1, 1)
thermostatOff = (.5, .5, .5)
thermostatMode = thermostatHeating

temperatureDisplay = neopixel.NeoPixel(board.SDA, 16, pixel_order=neopixel.RGB)
statusRowOne = neopixel.NeoPixel(board.A5, 4, pixel_order=neopixel.RGB)
statusRowTwo = neopixel.NeoPixel(board.A4, 5, pixel_order=neopixel.RGB)
for light in statusRowOne:
    light = (0, 0, 0)
for light in statusRowTwo:
    light = (0, 0, 0)
statusRowOne.show()
statusRowTwo.show()


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

def setBrightness(sunState):
    global brightness
    if sunState == "above_horizon":
        brightness = dayBrightness
    else:
        brightness = nightBrightness
    showTempIndicator()

def setStatus(device, status):
    statusColor = (0, 0, 0)
            
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

def showTempIndicator():
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