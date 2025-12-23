import json, sys
from pathlib import Path

NGCycleOffset = {
0: 0,
1: 60,
2: 90,
3: 110,
4: 130,
5: 150
}

ScriptOffset = {
    # For dialogue-triggered fights:
    "QUEST_FrancoisDuel": 14, # NOTE: BP_Dialogue_EsquieRelationshipQuest
    "GV_Golgra": 80, # NOTE: BP_Dialogue_GV_Golgra
    "LU_Act1_PunchingBall": -49, # NOTE: BP_Dialogue_Benoit, BP_Dialogue_Eugene, BP_Dialogue_Eloise
    "LU_Act1_MaelleTutorialCivilian": -49, # NOTE: BP_Dialogue_Gardens_Maelle_FirstDuel 
    "QUEST_JarNeedLight*1": 3, # NOTE: BP_Dialog_JarNeedLight 

    # For cutscenes and special interactions:
    "CFH_Boss_Clea": 7,
    #"Boss_Clea_ALPHA": 120, NOTE: calculations seem to break using this offset, kept just in case for the future
    #"Boss_Duolliste_P1": 120, NOTE: ditto
    #"Boss_Duolliste_P2": 120, NOTE: ditto
    #"Boss_LampmasterALPHA": 120, NOTE: ditto
    #"Boss_SimonALPHA*1": 120 NOTE: ditto
}

def loadJson(path):
    with open(path, 'r') as f:
        data = json.load(f)
        return data

def getCharStats(enemy, area, encounter, scriptLv=0, difficulty='Expert', ng=0):
    global basepath

    if difficulty not in ['Story', 'Expeditioner', 'Expert']:
        raise ValueError

    #defaultLv = enemydata.get('Level', None) # this gets defaulted to if none of the other values are used. Currently unneeded

    encounterLv = loadJson(basepath / "DT_Encounters_Composite.json")[encounter].get('Level', 0)
    areaLv = loadJson(basepath / "DT_LevelData.json")[area].get('Level', 0)
    scriptLv = ScriptOffset.get(encounter, 0) # set level to default 0 if not in the dictionary, aka no offset
    enemydata = loadJson(basepath / "DT_jRPG_Enemies.json")[enemy]
    archetype = enemydata.get('Archetype')

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

    archetypedata = loadJson(basepath / 'ScalingSystems' / difficulty / f"DT_EnemyArchetype_{archetype}.json")
    stats = archetypedata.get(f'Level_{level}', None)
    scaling = enemydata.get('EnemyScaling', None)

    calculated = {}
    for k, v in scaling.items():
        calculated[k] = v * stats[k]

    return calculated

def ParseBattleStats(encounter, area, difficulty='Expert', ng=0):
    data = {}
    try:
        battle = loadJson(basepath / "DT_Encounters_Composite.json").get(encounter, None)
        enemies = battle.get('Enemies', None)

        for enemy in enemies:
            data[enemy] = getCharStats(enemy=enemy, area=area, encounter=encounter, difficulty=difficulty, ng=ng)

        return data

    except Exception as e:
        print(f'Error Fetching Encounter:\n{e}')
        return
    
if __name__ == '__main__':
    basepath = Path(sys.argv[0]).parent / "Data"

    """Example usage:"""
    stats = ParseBattleStats(encounter="Boss_SimonALPHA*1", area='SideLevel_CleasTower', difficulty='Expert', ng=1)

    for k, v in stats.items():
        print(f"{k}:")
        for ik, iv in v.items():
            print(f"  {ik} - {iv}")

    """ Outputs:

    Boss_Simon_ALPHA:
        HP - 238143000.0
        PhysicalAttack - 42419.0
        PhysicalDefense - 0.0
        MagicalAttack - 0.0
        MagicalDefense - 0.0
        Mastery - 0.0
        Accuracy - 0.0
        Speed - 7674.0
        CriticalChance - 0.1
        Chroma - 473700.0
        Experience - 22500000.0
    """