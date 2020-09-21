import requests
from pathlib import Path
import lxml.html
import os
from PIL import Image, ImageFont, ImageDraw
import math
import json

# TODO: move positions to config
# TODO: Hiscore show wrong values (fix order or add api id)
positions = {
    "Combat": [738, 781, False],
    "Overall": [800, 781, False],
    "LMS - Rank": [1120, 781, False],
    "League Points": [1182, 781, False],
    "All Clue Scrolls": [1244, 781, False],

    "Beginner Clues": [0, 0, True],
    "Easy Clues": [0, 1, True],
    "Medium Clues": [0, 2, True],
    "Hard Clues": [0, 3, True],
    "Elite Clues": [0, 4, True],
    "Master Clues": [0, 5, True],
    "Bounty Hunter - Hunter": [0, 6, True],
    "Bounty Hunter - Rogue": [0, 7, True],

    "Attack": [1, 0, True],
    "Strength": [1, 1, True],
    "Defence": [1, 2, True],
    "Ranged": [1, 3, True],
    "Prayer": [1, 4, True],
    "Magic": [1, 5, True],
    "Runecraft": [1, 6, True],
    "Construction": [1, 7, True],

    "Hitpoints": [2, 0, True],
    "Agility": [2, 1, True],
    "Herblore": [2, 2, True],
    "Thieving": [2, 3, True],
    "Crafting": [2, 4, True],
    "Fletching": [2, 5, True],
    "Slayer": [2, 6, True],
    "Hunter": [2, 7, True],

    "Mining": [3, 0, True],
    "Smithing": [3, 1, True],
    "Fishing": [3, 2, True],
    "Cooking": [3, 3, True],
    "Firemaking": [3, 4, True],
    "Woodcutting": [3, 5, True],
    "Farming": [3, 6, True],
    
    "Abyssal Sire": [4, 0, True],
    "Alchemical Hydra": [4, 1, True],
    "Barrows Chests": [4, 2, True],
    "Bryophyta": [4, 3, True],
    "Callisto": [4, 4, True],
    "Cerberus": [4, 5, True],
    "Chambers of Xeric": [4, 6, True],
    "Chambers of Xeric: Challenge Mode": [4, 7, True],

    "Chaos Elemental": [5, 0, True],
    "Chaos Fanatic": [5, 1, True],
    "Commander Zilyana": [5, 2, True],
    "Corporal Beast": [5, 3, True],
    "Crazy Archaeologist": [5, 4, True],
    "Deranged Archaeologist": [5, 5, True],
    "Dagannoth Prime": [5, 6, True],
    "Dagannoth Rex": [5, 7, True],
    
    "Dagannoth Supreme": [6, 0, True],
    "General Graardor": [6, 1, True],
    "Giant Mole": [6, 2, True],
    "Grotesque Guardians": [6, 3, True],
    "Hespori": [6, 4, True],
    "Kalphite Queen": [6, 5, True],
    "King Black Dragon": [6, 6, True],
    "Kraken":[6, 7, True],

    "Kree'Arra": [7, 0, True],
    "K'ril Tsutsaroth": [7, 1, True],
    "Mimic": [7, 2, True],
    "Nightmare": [7, 3, True],
    "Obor": [7, 4, True],
    "Sarachnis": [7, 5, True],
    "Scorpia": [7, 6, True],
    "Skotizo": [7, 7, True],

    "The Gauntlet": [8, 0, True],
    "The Corrupted Gauntlet": [8, 1, True],
    "Theater of Blood": [8, 2, True],
    "Thermonuclear Smoke Devil": [8, 3, True],
    "TzKal-Zuk": [8, 4, True],
    "TzTok-Jad": [8, 5, True],
    "Venenatis": [8, 6, True],
    "Vet'ion": [8, 7, True],
    
    "Vorkath": [9, 0, True],
    "Wintertodt": [9, 1, True],
    "Zalcano": [9, 2, True],
    "Zulrah": [9, 3, True],
}

# TODO: Move to helper file
def getFileContents(path):
    file = open(path, "r")
    contents = file.read()
    file.close()
    return contents


configPath = Path("./config.json").absolute()
config = json.loads(getFileContents(configPath))

LevelScores = []
BossScores = []
# Order of this dictionary must match with API response
xGridOffset = 685
yGridOffset = 834

def calculatePositions(positions):
    # todo: get spokes from config
    xSpokes = [0, 63, 126, 189, 252, 315, 376, 439, 502, 565]
    ySpokes = [0, 30, 60, 90, 120, 150, 180, 210]

    for position in positions:
        positionData = positions.get(position)
        x = positionData[0]
        y = positionData[1]
        usesGrid = positionData[2]
        
        if usesGrid:
            print(f"Using grid position for {position}")
            x = xSpokes[x] + xGridOffset
            y = ySpokes[y] + yGridOffset

            positions.update({position: [x, y, True]})

            print(f"Calculated grid positions at x={x} y={y}")
            print("")

accounts = config.get("accounts")
accountTypeParameters = config.get("accountTypeParameters")
calculatePositions(positions)

class Position:
    def __init__(self, x, y):

        self.x = x
        self.y = y


class LevelData:
    def __init__(self, itemData, itemName):
        self.name = itemName
        self.rank = itemData[0]
        self.level = itemData[1]
        self.experience = itemData[2]
        self.Position = getPosition(self.name)

    def __repr__(self):
        return f"Name: {self.name}, Rank: {self.rank}, Level: {self.level}, Experience: {self.experience}, X: {self.Position.x}, Y: {self.Position.y}"


class BossData:
    def __init__(self, itemData, itemName):
        self.name = itemName
        self.rank = itemData[0]
        self.kills = itemData[1]
        self.Position = getPosition(self.name)

    def __repr__(self):
        return f"Rank: {self.rank}, Kills: {self.kills}"


def processHiscoreItem(itemData, itemCount):
    itemData = itemData.split(',')
    for i in range(0, len(itemData)):
        # print(itemData[i])
        if itemData[i] == "-1":
            itemData[i] = '-'
    # TODO: skip list creation and take directly from dict
    itemName = list(positions.keys())[itemCount]

    if len(itemData) == 2:
        # Hiscore entry is boss
        bossScore = BossData(itemData, itemName)
        # print(repr(bossScore))
        BossScores.append(bossScore)
    elif len(itemData) == 3:
        # Hiscore entry is level
        levelScore = LevelData(itemData, itemName)
        # print(repr(levelScore))
        LevelScores.append(levelScore)


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
    x = positions[name][0]
    y = positions[name][1]
    return Position(x, y)


def absolutePath(__file__):
    "This function returns the directory path of the file being ran, the __file__ variable accepts __file__ inputs"
    return os.path.join(os.path.dirname(__file__))


def combat_level(stats):
    # 1.	Take your Prayer level and divide it by two and round down
    base = math.trunc(stats[5]/2)
    # 2.	Add this to your Hitpoints and Defence levels and divide the result by 4.
    base = (base+stats[3]+stats[1])/4
    # 3. Add your Strength and Attack levels together and multiply by 0.325.
    melee = (stats[2]+stats[0])*0.325
    # Add this to your base combat level and you should have your melee combat level.
    # 4.	If your Magic or Ranged level is exceptionally higher than your Attack and Strength,
    # carry on - in the calculation noted below Magic is used,
    # but if your Ranged is exceptionally higher, use that instead in all cases
    higher = stats[6]
    if (higher < stats[4]):
        higher = stats[4]
    if (higher > stats[0]+14 and higher > stats[2]+14):
        # 5. Divide your Magic level by 2 and round down, and then add your Magic level again to this
        magic = math.trunc(higher/2)+higher
    # 6. Multiply this by 0.325 and add the result to your base combat level calculated above,
    # and you should have your magic combat level
        magic = magic*0.325
        return "{0:0.1f}".format(base+magic)
    else:
        return "{0:0.1f}".format(base+melee)


absolutePath = absolutePath(__file__)

outputPath = Path(Path(__file__).parent.absolute() / "output")

# sample text and font
unicode_text = u"Hello World!"
font = ImageFont.truetype("{}\\Reckoner.ttf".format(
    absolutePath), 18, encoding="unic")
# font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 28, encoding="unic")

# get the line size
text_width, text_height = font.getsize(unicode_text)

HiScoreList = ["Overall", "Attack", "Defence", "Strength", "Hitpoints", "Ranged", "Prayer", "Magic", "Cooking", "Woodcutting", "Fletching", "Fishing", "Firemaking", "Crafting", "Smithing", "Mining", "Herblore", "Agility", "Thieving", "Slayer", "Farming", "Runecraft", "Hunter", "Construction", "League Points", "Bounty Hunter - Hunter", "Bounty Hunter - Rogue", "All Clue Scrolls", "Beginner Clues", "Easy Clues", "Medium Clues", "Hard Clues", "Elite Clues", "Master Clues", "LMS - Rank", "Abyssal Sire", "Alchemical Hydra", "Barrows Chests", "Bryophyta", "Callisto", "Cerberus", "Chambers of Xeric",
               "Chambers of Xeric: Challenge Mode", "Chaos Elemental", "Chaos Fanatic", "Commander Zilyana", "Corporal Beast", "Crazy Archaeologist", "Dagannoth Prime", "Dagannoth Rex", "Dagannoth Supreme", "Deranged Archaeologist", "General Graardor", "Giant Mole", "Grotesque Guardians", "Hespori", "Kalphite Queen", "King Black Dragon", "Kraken", "Kree'Arra", "K'ril Tsutsaroth", "Mimic", "Nightmare", "Obor", "Sarachnis", "Scorpia", "Skotizo", "The Gauntlet", "The Corrupted Gauntlet", "Theater of Blood", "Thermonuclear Smoke Devil", "TzKal-Zuk", "TzTok-Jad", "Venenatis", "Vet'ion", "Vorkath", "Wintertodt", "Zalcano", "Zulrah", "Combat"]


def returnText(HiscoreKeyList):
    if len(HiscoreKeyList) > 0:
        msg = HiscoreKeyList[1]
        if msg == '-1':
            msg = '-'
    else:
        msg = '-'
    return msg


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
        accountTypeParameter = accountTypeParameters.get(accountType)
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

        for levelScore in LevelScores:
            text = levelScore.level
            x = levelScore.Position.x
            y = levelScore.Position.y
            # print(drawImg.textsize(text, font=font))
            width, height = drawImg.textsize(text, font=font)

            print(f"Drew skill: {levelScore.name} at X={levelScore.Position.x} and Y={levelScore.Position.y}")

            drawImg.text((x, y), text, font=font, fill=text_color)

        for bossScore in BossScores:
            text = bossScore.kills
            x = bossScore.Position.x
            y = bossScore.Position.y
            # print(drawImg.textsize(text, font=font))
            width, height = drawImg.textsize(text, font=font)

            # print(f"Drew boss: {bossScore.name} at X={bossScore.Position.x} and Y={bossScore.Position.y}")

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
