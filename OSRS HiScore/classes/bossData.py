class BossData:
    def __init__(self, itemData, itemName, position):
        self.name = itemName
        self.position = position
        self.rank = itemData[0]
        self.kills = itemData[1]

    def __repr__(self):
        return f"Rank: {self.rank}, Kills: {self.kills}"