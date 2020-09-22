# Configuration

This tool can be configured in the `config` folder. There are four different configuration files all of which will be mentioned below.

## accounts.json

### accounts
The accounts object can be used to specify the accounts for which a hiscore image will be generated. In order to request the account data from the correct hiscores the account type is also required.

**Format:**
`"[osrsName]": "[accountType]"`

| Name | Description | DataType |  Notes
|---|---|---|---|
| osrsName | The name of the account | string |   
| accountType  | The gamemode of the account | string | Value must be present in accountTypes configuration (see below)

### accountTypes
The accountTypes object is used to specify the supported account types, with their corresponding API parameter. The API parameter will be to set  the `m` parameter during the [API call](https://runescape.wiki/w/Application_programming_interface#Old_School_Hiscores).

**Format:**
`"[accountType]": "[apiParameter]"`

| Name | Description | DataType | Notes 
|---|---|---|---|
| accountType | The gamemode  of the account | string |  Can be set to any value, but must be used by the accounts configuration. 
| apiParameter | The API parameter that corresponds with the gamemode | string |  See [OSRS API](https://runescape.wiki/w/Application_programming_interface#Old_School_Hiscores) for supported values

### Example
<details>
  <summary>accounts.json</summary>

  ```json
{
  "accounts": {
    "Ludic Blade": "normal",
    "Heroic Blade": "hcim",
    "BladeBTW": "uim",
    "Edenic Blade": "gim"
},
  "accountTypes": {
    "normal": "hiscore_oldschool",
    "hcim": "hiscore_oldschool_hardcore_ironman",
    "uim": "hiscore_oldschool_ultimate",
    "gim": "unknown",
    "im": "hiscore_oldschool_ironman",
    "deadman": "hiscore_oldschool_deadman",
    "league": "hiscore_oldschool_seasonal",
    "tournament": "hiscore_oldschool_tournament"
    }
}
  ```
</details>

## api.json

### apiResponseOrder
Unfortunately the OSRS API returns very minimalistic highscore data, This configuration file is required to match the API response with the correct skill and boss data. If the API ever changes (response order changes, new skill, new boss) this list can be edited to convienantly match the data to the correct skill/boss again.

**Format:**
`[hiscoreItem]`

| Name | Description | DataType | Notes 
|---|---|---|---|
| hiscoreItem | The name of the hiscore item | string[] |  Can be set to any value, but must match the order in which the API returns hiscore items.

### Example
<details>
  <summary>api.json</summary>

  ```json
{
  "apiResponseOrder": [
    "Overall",
    "Attack",
    "Defence",
    "Strength",
    "Hitpoints",
  ]
}
  ```
</details>

## app.json
Used to specify the path to the input directory containing the base images.

### inputDir
**format:**
`[inputDir]`

| Name | Description | DataType | Notes 
|---|---|---|---|
| inputDir | Path to the input directory containing the base images | string |  Path can be absolute or relative. If the path is relative an absolute path will automatically be generated using the `OSRS HISCORE` directory as starting point.

### outputDir
Used to specify the path to the output directory for the hiscore images.

**format:**
`[outputDir]`

| Name | Description | DataType | Notes 
|---|---|---|---|
| outputDir | Path to the output directory for the hiscore images | string |  Path can be absolute or relative. If the path is relative an absolute path will automatically be generated using the `OSRS HISCORE` directory as starting point.

### Example
<details>
  <summary>app.json</summary>

  ```json
{
  "inputDir": "./images",
  "outputDir": "C:\\Users\\YourEpicName\\Desktop\\output"
}
  ```
</details>

## positions.json
This configuration file is used to specify at which coordinates to draw the hiscore items on the base image. Each hiscore item has a position at which it will be drawn on the base image.

Aditionally a position can specified as grid item, meaning the actual postion will be calculated using the grid system. The grid can be used to convieniently move mutiple highscore items at once based on row and colum positions. Additionally the entire grid can be moved using the gridOffset. To enable the grid system for a specfic item see below.

### gridOffset
Used to specify the grid offset. Pushes the grid down (x) and right (y) the specified amount of pixels

**format:**
`"[dimension]": [pixels]`

| Name | Description | DataType | Notes 
|---|---|---|---|
| dimension | Dimension to offset | string |  Must either be "x" or "y"
| pixels | Amount of pixels to offset in the specified dimension | int |

### gridAxis
Used to specify the position of the grid axis. Additional axis can be added by simply extending the axisPostions array.

**format:**
`"[dimension]": [axisPositions]`

| Name | Description | DataType | Notes 
|---|---|---|---|
| dimension | Dimension of the axis | string |  Must either be "x" or "y"
| axisPositions | Array of the positions on the axis | int[] | 

### positions
Used to specify the position on the base image in pixels or on the grid.

**format:**
`"[hiscoreItem]": [x, y, usesGrid]`

| Name | Description | DataType | Notes 
|---|---|---|---|
| hiscoreItem | Name of the hiscore item | string |  Must match a value from the ApiReponseOrder configuration otherwise the item will not be displayed.
| x | X position in pixels or on the grid for the hiscore item | int | 
| y | Y position in pixels or on the grid for the hiscore item | int | 
| usesGrid | Whether to use the grid system or not | bool | When set to true the grid location is automatically converted to the correct coordinates

### Example
<details>
  <summary>positions.json</summary>

  ```json
{
  "gridOffset": {
    "x": 76,
    "y": 97
  },
  "gridAxis": {
    "x": [
      0,
      63,
      126,
      189,
      252,
      315,
      376,
      439,
      502,
      565
    ],
    "y": [
      0,
      30,
      60,
      90,
      120,
      150,
      180,
      210
    ]
  },
  "positions": {
    "Combat": [
      738,
      781,
      false
    ],
    "Overall": [
      183,
      44,
      false
    ],
    "Bounty Hunter - Hunter": [
      0,
      6,
      true
    ],
    "Bounty Hunter - Rogue": [
      0,
      7,
      true
    ],
    "Attack": [
      1,
      0,
      true
    ],
    "Strength": [
      1,
      1,
      true
    ],
    "Defence": [
      1,
      2,
      true
    ],
    "Ranged": [
      1,
      3,
      true
    ]
  }
}
  ```
</details>
