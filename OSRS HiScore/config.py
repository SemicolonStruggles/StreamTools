# This file contains global variables that are shared between modules

import json
from pathlib import Path
from utilities.common import getFileContents

### Import classed into all modules that use config
from classes.position import Position
from classes.bossData import BossData
from classes.levelData import LevelData

### Define manually initialized globals

# Define score lists
levelScores = []
bossScores = []

### Define auto-initialized globals

# Define config paths
accountsConfigPath = Path("./config/accounts.json").absolute()
apiConfigPath = Path("./config/api.json").absolute()
appConfigPath = Path("./config/app.json").absolute()
positionsConfigPath = Path("./config/positions.json").absolute()

# Accounts
accountConfig = json.loads(getFileContents(accountsConfigPath))
accounts = accountConfig.get("accounts")
accountTypes = accountConfig.get("accountTypes")

# Api
apiResponseOrder = json.loads(getFileContents(
    apiConfigPath)).get("apiResponseOrder")

# App
appConfig = json.loads(getFileContents(appConfigPath))

# Positions
positionConfig = json.loads(getFileContents(positionsConfigPath))
positions = positionConfig.get("positions")
gridOffset = positionConfig.get("gridOffset")
gridAxis = positionConfig.get("gridAxis")