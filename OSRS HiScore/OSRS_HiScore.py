import requests
from pathlib import Path
import lxml.html
import os
from PIL import Image, ImageFont, ImageDraw
import math
import json

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
yGridOffset = 836

# TODO: move positions to config
Positions = {
    "Overall": [800, 781],
    "Attack": [685 + (63 * 1), 836],
    "Defence": [685 + (63 * 1), 896],
    "Strength": [685 + (63 * 1), 866],
    "Hitpoints": [685 + (63 * 2), 836],
    "Ranged": [685 + (63 * 1), 926],
    "Prayer": [685 + (63 * 1), 956],
    "Magic": [685 + (63 * 1), 986],
    "Cooking": [685 + (63 * 3), 926],
    "Woodcutting": [685 + (63 * 3), 986],
    "Fletching": [685 + (63 * 2), 986],
    "Fishing": [685 + (63 * 3), 896],
    "Firemaking": [685 + (63 * 3), 956],
    "Crafting": [685 + (63 * 2), 956],
    "Smithing": [685 + (63 * 3), 866],
    "Mining": [685 + (63 * 3), 836],
    "Herblore": [685 + (63 * 2), 896],
    "Agility": [685 + (63 * 2), 866],
    "Thieving": [685 + (63 * 2), 926],
    "Slayer": [685 + (63 * 2), 1016],
    "Farming": [685 + (63 * 3), 1016],
    "Runecraft": [685 + (63 * 1), 1016],
    "Hunter": [685 + (63 * 2), 1046],
    "Construction": [685 + (63 * 1), 1046],
    "League Points": [1182, 781],
    "Bounty Hunter - Hunter": [685 + (63 * 0), 1016],
    "Bounty Hunter - Rogue": [685 + (63 * 0), 1046],
    "All Clue Scrolls": [1244, 781],
    "Beginner Clues": [685, 836],
    "Easy Clues": [685 + (63 * 0), 866],
    "Medium Clues": [685 + (63 * 0), 896],
    "Hard Clues": [685 + (63 * 0), 926],
    "Elite Clues": [685 + (63 * 0), 956],
    "Master Clues": [685 + (63 * 0), 986],
    "LMS - Rank": [1120, 781],
    "Abyssal Sire": [685 + (63 * 4), 836],
    "Alchemical Hydra": [685 + (63 * 4), 866],
    "Barrows Chests": [685 + (63 * 4), 896],
    "Bryophyta": [685 + (63 * 4), 926],
    "Callisto": [685 + (63 * 4), 956],
    "Cerberus": [685 + (63 * 4), 986],
    "Chambers of Xeric": [685 + (63 * 4), 1016],
    "Chambers of Xeric: Challenge Mode": [685 + (63 * 4), 1046],
    "Chaos Elemental": [685 + (63 * 5), 836],
    "Chaos Fanatic": [685 + (63 * 5), 866],
    "Commander Zilyana": [685 + (63 * 5), 896],
    "Corporal Beast": [685 + (63 * 6), 836],
    "Crazy Archaeologist": [685 + (63 * 5), 926],
    "Dagannoth Prime": [685 + (63 * 5), 1016],
    "Dagannoth Rex": [685 + (63 * 5), 1046],
    "Dagannoth Supreme": [685 + (63 * 5), 986],
    "Deranged Archaeologist": [685 + (63 * 5), 956],
    "General Graardor": [685 + (63 * 6), 866],
    "Giant Mole": [685 + (63 * 6), 896],
    "Grotesque Guardians": [685 + (63 * 6), 926],
    "Hespori": [685 + (63 * 6), 956],
    "Kalphite Queen": [685 + (63 * 6), 986],
    "King Black Dragon": [685 + (63 * 6), 1016],
    "Kraken": [685 + (63 * 6), 1046],
    "Kree'Arra": [685 + (63 * 7), 836],
    "K'ril Tsutsaroth": [685 + (63 * 7), 866],
    "Mimic": [685 + (63 * 7), 896],
    "Nightmare": [685 + (63 * 7), 926],
    "Obor": [685 + (63 * 7), 956],
    "Sarachnis": [685 + (63 * 7), 986],
    "Scorpia": [685 + (63 * 7), 1016],
    "Skotizo": [685 + (63 * 7), 1046],
    "The Gauntlet": [685 + (63 * 8), 836],
    "The Corrupted Gauntlet": [685 + (63 * 8), 866],
    "Theater of Blood": [685 + (63 * 8), 896],
    "Thermonuclear Smoke Devil": [685 + (63 * 8), 926],
    "TzKal-Zuk": [685 + (63 * 8), 956],
    "TzTok-Jad": [685 + (63 * 8), 986],
    "Venenatis": [685 + (63 * 8), 1016],
    "Vet'ion": [685 + (63 * 8), 1046],
    "Vorkath": [685 + (63 * 9), 836],
    "Wintertodt": [685 + (63 * 9), 866],
    "Zalcano": [685 + (63 * 9), 896],
    "Zulrah": [685 + (63 * 9), 926],
    "Combat": [738, 781]
}

accounts = config.get("accounts")
accountTypeParameters = config.get("accountTypeParameters")

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
        print(itemData[i])
        if itemData[i] == "-1":
            itemData[i] = '-'
    # TODO: skip list creation and take directly from dict
    itemName = list(Positions.keys())[itemCount]

    if len(itemData) == 2:
        # Hiscore entry is boss
        bossScore = BossData(itemData, itemName)
        print(repr(bossScore))
        BossScores.append(bossScore)
    elif len(itemData) == 3:
        # Hiscore entry is level
        levelScore = LevelData(itemData, itemName)
        print(repr(levelScore))
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
    x = Positions[name][0]
    y = Positions[name][1]
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

# TODO: remove this

Accounts_old = ['Mystic Blade', 'Xeric Blade', 'Epic Blade', 'Magic Blade', 'Garlic Blade', 'Cyclic Blade', 'Irenic Blade', 'Lyric Blade', 'Agonic Blade', 'Arabic Blade', 'Auric Blade', 'Azoic Blade', 'Azotic Blade', 'Bardic Blade', 'Baric Blade', 'Boric Blade', 'Bromic Blade', 'Cadmic Blade', 'Calcic Blade', 'Ceric Blade', 'Citric Blade', 'Cleric Blade', 'Cultic Blade', 'Cupric Blade', 'Cyanic Blade', 'Dyadic Blade', 'Emic Blade', 'Erotic Blade', 'Ethnic Blade', 'Etic Blade', 'Felsic Blade', 'Gnomic Blade', 'Holmic Blade', 'Humic Blade', 'Iodic Blade', 'Ionic Blade', 'Iridic Blade', 'Laic Blade', 'Lithic Blade', 'Logic Blade', 'Mafic Blade', 'Mantic Blade', 'Melic Blade', 'Mimic Blade', 'Music Blade', 'Niobic Blade', 'Nitric Blade', 'Odic Blade', 'Ontic Blade', 'Orphic Blade',
                'Osmic Blade', 'Oxalic Blade', 'Oxidic Blade', 'Ozonic Blade', 'Panic Blade', 'Photic Blade', 'Poetic Blade', 'Rhodic Blade', 'Sodic Blade', 'Steric Blade', 'Telic Blade', 'Terbic Blade', 'Thic Blade', 'Thoric Blade', 'Toluic Blade', 'Typic Blade', 'Uranic Blade', 'Vitric Blade', 'Yttric Blade', 'Zincic Blade', 'Mastic Blade', 'Pyric Blade', 'Pelvic Blade', 'Daric Blade', 'Sepic Blade', 'Limbic Blade', 'Picnic Blade', 'Mesic Blade', 'Civic Blade', 'Ethic Blade', 'Medic Blade', 'Ovonic Blade', 'Azonic Blade', 'Chemic Blade', 'Echoic Blade', 'Fustic Blade', 'Toric Blade', 'Conic Blade', 'Hemic Blade', 'Salic Blade', 'Biotic Blade', 'Hydric Blade', 'Axenic Blade', 'Syndic Blade', 'Critic Blade', 'Frolic Blade', 'Fabric Blade', 'Zoic Blade', 'Emetic Blade', 'Antic Blade', 'Ludic Blade']
HCIMAccounts = ['Heroic Blade']
UIMAccounts = ['BladeBTW']
GIMAccounts = ['Edenic Blade', 'Deific Blade',
               'Ferric Blade', 'Exilic Blade', 'Orphic Blade']
IMAccounts = []
DeadmanModeAccounts = []
LeaguesAccounts = []
Tournamentaccounts = []

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

        if len(HiScoreDictionary) > 0:
            Numeric = True
            for key in HiScoreDictionary.values():
                if key == '':
                    Numeric = False
                HiscoreKeyList = []
                if ',' in key:
                    HiscoreKeyList = key.split(',')
                    for key in HiscoreKeyList:
                        if key.isnumeric() == False:
                            Numeric = False
            # print('Numeric = {}'.format(Numeric))
            if Numeric == True:
                # print('Numeric = {}'.format(Numeric))
                print('HiScoreDictionary = {}'.format(HiScoreDictionary))
                stats = [float(HiScoreDictionary['Attack'].split(',')[1]), float(HiScoreDictionary['Hitpoints'].split(',')[1]), float(HiScoreDictionary['Strength'].split(',')[1]),
                         float(HiScoreDictionary['Defence'].split(',')[1]), float(
                             HiScoreDictionary['Ranged'].split(',')[1]), float(HiScoreDictionary['Prayer'].split(',')[1]),
                         float(HiScoreDictionary['Magic'].split(',')[1])]
                if stats[0] == (float(-1.0)):
                    # print('stats[0]==float(-1.0))')
                    combatlvl = '-'
                else:
                    # print('combatlvl calced through combat_level(stats)')
                    combatlvl = combat_level(stats)
                    # print('combatlvl = {}'.format(combatlvl))
                temp_list.append('{},{},{}'.format(
                    combatlvl, combatlvl, combatlvl))
        HiScoreDictionary = dict(zip(HiScoreList, temp_list))

        font = ImageFont.truetype("{}\\Reckoner.ttf".format(
            absolutePath), 14, encoding="unic")
        d = ImageDraw.Draw(im)
        text_color = (255, 255, 255)

        for levelScore in LevelScores:
            text = levelScore.level
            x = levelScore.Position.x
            y = levelScore.Position.y
            print(d.textsize(text, font=font))
            width, height = d.textsize(text, font=font)

            print(
                f"Drew skill: {levelScore.name} at X={levelScore.Position.x} and Y={levelScore.Position.y}")

            d.text((x, y), text, font=font, fill=text_color)

        for bossScore in BossScores:
            text = bossScore.kills
            x = bossScore.Position.x
            y = bossScore.Position.y
            print(d.textsize(text, font=font))
            width, height = d.textsize(text, font=font)

            print(
                f"Drew boss: {bossScore.name} at X={bossScore.Position.x} and Y={bossScore.Position.y}")

            d.text((x, y), text, font=font, fill=text_color)

        print(f"{outputPath}/{account}_hiscore.png")
        im.save(f"{outputPath}/{account}_hiscore.png")

        # print("{}{}_hiscore.png".format(outputPath, account))
        # TODO: remove exit()
        print("The end")
        exit()


while True:
    loopthroughAccounts()
