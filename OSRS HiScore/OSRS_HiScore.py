# TODO: Validate that this Positions array only contains items from apiReponseOrder

from pathlib import Path

# Utilities
from utilities.common import *
from utilities.runescape import *
from utilities.osrsHiscore import *

# Globals
from config import *

# After config is located calculate grid based positions
calculatePositions()

# Make sure in and output directories use absolute path
absoluteInputDir = toAbsolutePath(appConfig.get("inputDir"))
appConfig.update({"inputDir": absoluteInputDir})

absoluteOutputDir = toAbsolutePath(appConfig.get("outputDir"))
appConfig.update({"outputDir": absoluteOutputDir})

font = ImageFont.truetype(buildPath("fonts/Reckoner.ttf"), 18, encoding="unic")

while True:
    # TODO: add update interval/delay
    loopthroughAccounts()
