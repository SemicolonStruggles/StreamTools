import requests
import lxml.html
import math
import json

from config import *
from PIL import Image, ImageFont, ImageDraw
from utilities.common import buildPath


def processHiscoreItem(itemData, itemCount):
    itemData = itemData.split(',')
    for i in range(0, len(itemData)):
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


def getPosition(name):
    x = positions.get(name)[0]
    y = positions.get(name)[1]
    return Position(x, y)


def calculatePositions():
    # Configure grid
    xGridOffset = gridOffset.get("x")
    yGridOffset = gridOffset.get("y")
    xGridAxis = gridAxis.get("x")
    yGridAxis = gridAxis.get("y")

    # Calculate grid positions
    for position in positions:
        positionData = positions.get(position)
        x = positionData[0]
        y = positionData[1]
        usesGrid = positionData[2]

        if usesGrid:
            x = xGridAxis[x] + xGridOffset
            y = yGridAxis[y] + yGridOffset
            positions.update({position: [x, y, True]})


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


def loopthroughAccounts():
    for account in accounts:
        accountType = accounts.get(account)
        accountTypeParameter = accountTypes.get(accountType)
        apiUrl = f"https://secure.runescape.com/m={accountTypeParameter}/index_lite.ws?player={account}"
        baseImagePath = appConfig.get("inputDir")
        imagePath = Path(baseImagePath, f"{accountType}.png")
        baseImage = Image.open(imagePath)

        # TODO: Error handling
        html_string = requests.get(apiUrl).content
        body = lxml.html.document_fromstring(html_string).find('body')
        text = body.text_content()

        # Old code starts here

        temp_list = text.splitlines()
        processPlayerHiscore(text)

        # TODO: Leagues - unsure what old code function was. See line 103 in base repo

        # TODO: Combat level calculation

        font = ImageFont.truetype(
            buildPath("fonts/reckoner.ttf"), 14, encoding="unic")
        drawImg = ImageDraw.Draw(baseImage)
        text_color = (255, 255, 255)

        for levelScore in levelScores:
            text = levelScore.level
            x = levelScore.position.x
            y = levelScore.position.y
            width, height = drawImg.textsize(text, font=font)

            drawImg.text((x, y), text, font=font, fill=text_color)

        for bossScore in bossScores:
            text = bossScore.kills
            x = bossScore.position.x
            y = bossScore.position.y
            width, height = drawImg.textsize(text, font=font)

            drawImg.text((x, y), text, font=font, fill=text_color)

        outputPath = appConfig.get("outputDir")
        print(f"{outputPath}/{account}_hiscore.png")
        baseImage.save(f"{outputPath}/{account}_hiscore.png")

        # TODO: remove exit()
        print("The end")
        exit()
