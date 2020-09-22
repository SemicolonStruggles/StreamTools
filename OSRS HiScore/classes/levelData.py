class LevelData:
    def __init__(self, itemData, itemName, position):
        self.name = itemName
        self.position = position
        self.rank = itemData[0]
        self.level = itemData[1]
        self.experience = itemData[2]

    def __repr__(self):
        return f"Name: {self.name}, Rank: {self.rank}, Level: {self.level}, Experience: {self.experience}, X: {self.position.x}, Y: {self.position.y}"
