statusColors = {
    "state/vacuum": {
        "cleaning": (0, 1, 0),
        "returning": (0, 1, 0),
        "paused": (1, 1, 0),
        "docked": (0, 0, 0),
        "idle": (0, 0, 0),
        "error": (1, 0, 0)
    },
    "sensor/air-quality": {
        "good": (0, 1, 0),
        "medium": (1, 1, 0),
        "bad": (1, .5, 0),
        "terrible": (1, 0 ,0)
    },
    "state/fan-on": {
        "0": (0, 0, 0),
        "1": (1, 1, 1)
    },
    "state/thermostat-mode-command": {
        "cool": (.1, .3, 1),
        "heat": (1, .5, .1),
        "off": (0, 0, 0)
    },
    "state/subway-sign": {
        "ON": (1, 1, 1),
        "OFF": (0, 0, 0)
    },
    "state/media": {
        "idle": (0, 0, 0),
        "buffering": (1, 1, 0),
        "playing": (0, 1, 0),
        "paused": (1, 1, 0),
        "off": (0, 0, 0)
    },
    "thermostat": {
        "heating": (1, .5, 0),
        "cooling": (.2, .2, 1),
        "off": (0, 0, 0)
    },
    "state/humidifier": {
        "on": (1, 1, 1),
        "off": (0, 0, 0),
        "true": (1, 0, 0)
    },
    "state/humidifier-empty": {
        "on": (1, 0, 0)
    },
    "state/video-call": {
        "on": (0, 1, 0),
        "ending": (1, 0, 0),
        "off": (0, 0, 0)
    },
    "state/tv": {
        "on": (1, 1, 1),
        "off": (0, 0, 0)
    },
    "battery": {
        "good": (0, 0, 0),
        "low": (1, .5, 0),
        "dying": (1, 0, 0)
    }
}