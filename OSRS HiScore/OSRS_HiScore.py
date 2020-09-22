import requests
from pathlib import Path
import lxml.html
import os
from PIL import Image, ImageFont, ImageDraw
import math
import json

# Classes
from classes.position import Position
from classes.bossData import BossData
from classes.levelData import LevelData

# Utilities
from utilities.main import *
from utilities.runescape import *

# TODO: move positions to config
# TODO: Validate that this array only contains items from apiReponseOrder


# TODO: Move to helper file
def getFileContents(path):
    file = open(path, "r")
    contents = file.read()
    file.close()
    return contents

def processHiscoreItem(itemData, itemCount):
    itemData = itemData.split(',')
    for i in range(0, len(itemData)):
        # print(itemData[i])
        if itemData[i] == "-1":
            itemData[i] = "-"

    itemName = apiResponseOrder[itemCount]

    if itemName in positions:
        position = getPosition(itemName)

        if len(itemData) == 2:
            # Hiscore entry is boss
            bossScore = BossData(itemData, itemName, position)
            # print(repr(bossScore))
            bossScores.append(bossScore)
        elif len(itemData) == 3:
            # Hiscore entry is level
            levelScore = LevelData(itemData, itemName, position)
            # print(repr(levelScore))
            levelScores.append(levelScore)

# Define config paths
accountsConfigPath = Path("./config/accounts.json").absolute()
apiConfigPath = Path("./config/api.json").absolute()
appConfigPath = Path("./config/app.json").absolute()
positionsConfigPath = Path("./config/positions.json").absolute()

# load config
accountConfig = json.loads(getFileContents(accountsConfigPath))
accounts = accountConfig.get("accounts")
accountTypes = accountConfig.get("accountTypes")
apiResponseOrder = json.loads(getFileContents(apiConfigPath)).get("apiResponseOrder")
appConfig = json.loads(getFileContents(appConfigPath))

positionConfig = json.loads(getFileContents(positionsConfigPath))
positions = positionConfig.get("positions")
gridOffset = positionConfig.get("gridOffset")
gridAxis = positionConfig.get("gridAxis")

# Configure grid
xGridOffset = gridOffset.get("x")
yGridOffset = gridOffset.get("y")
xGridAxis = gridAxis.get("x")
yGridAxis = gridAxis.get("y")

# Declare score lists
levelScores = []
bossScores = []

def calculatePositions(positions):
    for position in positions:
        positionData = positions.get(position)
        x = positionData[0]
        y = positionData[1]
        usesGrid = positionData[2]
        
        if usesGrid:
            print(f"Using grid position for {position}")

            x = xGridAxis[x] + xGridOffset
            y = yGridAxis[y] + yGridOffset

            positions.update({position: [x, y, True]})

            print(f"Calculated grid positions at x={x} y={y}")
            print("")

calculatePositions(positions)

def processPlayerHiscore(response):
    # Empty previous data
    LevelScores = []
    BossScores = []
    itemCount = 0

    # Process individual highscore entries
    highscoreData = response.splitlines()
    for itemData in highscoreData:
        processHiscoreItem(itemData, itemCount)
        itemCount += 1


def getPosition(name):
    x = positions.get(name)[0]
    y = positions.get(name)[1]
    return Position(x, y)


def absolutePath(__file__):
    "This function returns the directory path of the file being ran, the __file__ variable accepts __file__ inputs"
    return os.path.join(os.path.dirname(__file__))

absolutePath = absolutePath(__file__)

# TODO: dir separtors do not match / and \ both used
outputPath = Path(Path(__file__).parent.absolute() / "output")

# sample text and font
unicode_text = u"Hello World!"
font = ImageFont.truetype("{}\\Reckoner.ttf".format(
    absolutePath), 18, encoding="unic")
# font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 28, encoding="unic")

# get the line size
text_width, text_height = font.getsize(unicode_text)

def loopthroughAccounts():

    for account in accounts:

        # TODO: What does this do
        HiScoreDictionary = True
        temp_list = True
        LeaguesList = True
        Leaguestext = True
        Leaguesbody = True
        Leagueshtml_string = True
        LeaguesURL = True
        # Comment end

        accountType = accounts.get(account)
        accountTypeParameter = accountTypes.get(accountType)
        apiUrl = f"https://secure.runescape.com/m={accountTypeParameter}/index_lite.ws?player={account}"
        baseImagePath = Path(f"./Images/{accountType}.png").absolute()
        baseImage = Image.open(baseImagePath)

        # TODO: Error handling
        html_string = requests.get(apiUrl).content
        body = lxml.html.document_fromstring(html_string).find('body')
        text = body.text_content()

        # Old code starts here

        temp_list = text.splitlines()
        processPlayerHiscore(text)

        # TODO: Leagues - unsure what old code function was. See line 103 in base repo

        # TODO: Combat level calculation

        font = ImageFont.truetype("{}\\Reckoner.ttf".format(
            absolutePath), 14, encoding="unic")
        drawImg = ImageDraw.Draw(baseImage)
        text_color = (255, 255, 255)

        for levelScore in levelScores:
            text = levelScore.level
            x = levelScore.position.x
            y = levelScore.position.y
            # print(drawImg.textsize(text, font=font))
            width, height = drawImg.textsize(text, font=font)

            print(f"Drew skill: {levelScore.name} at X={levelScore.position.x} and Y={levelScore.position.y}")

            drawImg.text((x, y), text, font=font, fill=text_color)

        for bossScore in bossScores:
            text = bossScore.kills
            x = bossScore.position.x
            y = bossScore.position.y
            # print(drawImg.textsize(text, font=font))
            width, height = drawImg.textsize(text, font=font)

            # print(f"Drew boss: {bossScore.name} at X={bossScore.position.x} and Y={bossScore.position.y}")

            drawImg.text((x, y), text, font=font, fill=text_color)

        print(f"{outputPath}/{account}_hiscore.png")
        baseImage.save(f"{outputPath}/{account}_hiscore.png")

        # print("{}{}_hiscore.png".format(outputPath, account))
        # TODO: remove exit()
        print("The end")
        exit()


while True:
    # TODO: add update interval/delay
    loopthroughAccounts()
