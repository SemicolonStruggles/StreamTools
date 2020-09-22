def calculateCombatLevel(stats):
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