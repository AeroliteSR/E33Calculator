import json, sys, os
from pathlib import Path
from Data.Misc import *
import copy

def loadJson(path):
    if not os.path.exists(path):
        raise FileNotFoundError
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

def getCharStats(enemy, area, encounter, scriptLv=0, difficulty='Expert', ng=0, hpMod=1):
    global basepath

    if difficulty not in ['Story', 'Expeditioner', 'Expert']:
        raise ValueError("Invalid Difficulty")
    
    if not 6 > ng >= 0:
        raise ValueError("Invalid NG Cycle")

    #defaultLv = enemydata.get('Level', None) # this gets defaulted to if none of the other values are used. Currently unneeded

    encounterLv = loadJson(basepath / "Encounters.json")[encounter].get('Level', 0)
    areaLv = loadJson(basepath / "Area Levels.json")[area].get('Level', 0)
    scriptLv = ScriptOffset.get(encounter, 0) # set level to default 0 if not in the dictionary, aka no offset
    enemydata = loadJson(basepath / "Enemies.json")[enemy]
    archetype = enemydata.get('Archetype')

    archDrops = ArchetypeDrops[archetype]
    lootTable = loadJson(basepath / "Loot Tables" / f"DT_LootTable_UpgradeItems_{archDrops['Table']}.json")

    effectdata = loadJson(basepath / "Effects.json")
    itemdata = loadJson(basepath / "Items.json")

    if 'HardOnly_' in archetype:
        archetype = archetype.replace('HardOnly_', '')
        difficulty = 'Expert'

    if encounterLv > 0:
        level = encounterLv + NGCycleOffset[ng]
    else:
        level = areaLv + NGCycleOffset[ng]

    level += scriptLv

    if level > 300:
        level = 300

    archetypedata = loadJson(basepath / 'Scaling' / difficulty / f"DT_EnemyArchetype_{archetype}_{OriginalDifficultyNames[difficulty]}.json")
    stats = archetypedata.get(f'Level_{level}', None)
    scaling = enemydata.get('Enemy Scaling', {})

    # Multiply by optional modifier (default is 1x)
    stats['HP'] = stats['HP'] * hpMod

    calculated = {}
    for k, v in scaling.items():
        calculated[k] = v * stats[k]

    drops = enemydata.get("Loot", None)
    loot = []
    if drops:
        for entry in drops:
            name = entry['Name']
            iteminfo = copy.deepcopy(itemdata[name])
            item = {"Name": iteminfo.pop("Display Name"),
                    "Quantity": entry['Quantity'],
                    "Chance": entry['Chance'],
                    "Info": iteminfo}
            if name in effectdata:
                effect = effectdata.get(name, {})
                item['Info']['Lumina Cost'] = effect.get('Lumina Cost', "N/A")
                item['Info']['Categories'] = effect.get('Categories', [])

            loot.append(item)

    rewards = {"Roll Count": archDrops['Rolls']}
    for _, entry in lootTable.items():
        if entry['Min Level'] < level < entry['Max Level']:
            drops = entry['Drops']
            total_weight = sum(drop['Weight'] for drop in drops)

            entry_drops = []
            for drop in drops:
                iteminfo = copy.deepcopy(itemdata[drop['Item']])

                chance = drop['Weight'] / total_weight * 100
                item = {"Name": iteminfo.pop("Display Name"),
                        "Quantity": drop['Quantity'],
                        "Chance": chance,
                        "Info": iteminfo}
                entry_drops.append(item)

            rewards[f"Entry #{len(rewards)+1}"] = {
                "Chance": entry['Chance'],
                "Table": entry_drops}

    return {"Stats": calculated, "Affinities": enemydata.get("Affinities", []), "Rewards": loot, "Archetype Drops": rewards}

def ParseBattleStats(encounter, area, difficulty='Expert', ng=0, hpMod=1, dataPath=None):
    global basepath
    if dataPath:
        basepath = dataPath

    data = {"Calculator Config": {"Encounter": encounter,
                                  "Area": AreaNames.get(area, 'N/A'),
                                  "Difficulty": difficulty,
                                  "NG Cycle": "NG" if ng==0 else f"NG+{ng}",
                                  "HP Modifier": f"{hpMod}x"}}
    
    battle = loadJson(basepath / "Encounters.json").get(encounter, None)
    enemyData = loadJson(basepath / "Enemies.json")

    if battle is None:
        raise KeyError(f"Encounter '{encounter}' not found")
    
    enemies = battle.get('Enemies', [])
    for enemy in enemies:
        name = enemyData[enemy].get("Display Name", "N/A")
        data[name] = getCharStats(enemy=enemy, area=area, encounter=encounter, difficulty=difficulty, ng=ng, hpMod=hpMod)

    return data
    
if __name__ == '__main__':
    basepath = Path(sys.argv[0]).parent / "Data"

    """Example usage:"""
    stats = ParseBattleStats(encounter="CFH_Boss_Dualliste", area='SmallLevel_SimonArea', difficulty='Expert', ng=3, hpMod=2)

    with open('Output.json', 'w') as file:
        json.dump(stats, file, indent=4)
