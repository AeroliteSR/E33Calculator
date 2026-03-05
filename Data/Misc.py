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

ArchetypeDrops = {
    "Alpha": {
        "Rolls": 1,
        "Table": "Alpha"
    },
    "Boss_NoAchievement": {
        "Rolls": 3,
        "Table": "Elite"
    },
    "Boss": {
        "Rolls": 3,
        "Table": "Elite"
    },
    "Elite": {
        "Rolls": 1,
        "Table": "Elite"
    },
    "Elusive": {
        "Rolls": 1,
        "Table": "Regular"
    },
    "HardOnly_Boss": {
        "Rolls": 2,
        "Table": "Elite"
    },
    "HardOnly_OPBoss": {
        "Rolls": 0,
        "Table": None
    },
    "Petank": {
        "Rolls": 1,
        "Table": "Petank"
    },
    "Regular": {
        "Rolls": 1,
        "Table": "Regular"
    },
    "Strong": {
        "Rolls": 2,
        "Table": "Regular"
    },
    "Weak": {
        "Rolls": 1,
        "Table": "Regular"
    },
}

OriginalDifficultyNames = {
    "Story": "Easy",
    "Expeditioner": "Normal",
    "Expert": "Hard"
}

EnemyStatsMap = { # Sandfall/Content/jRPGTemplate/Enumerations/E_jRPG_StatType.uasset
    'title': 'E_jRPG_StatType',
    1: "Max HP",
    2: "Max AP",
    3: "Physical Attack",
    13: "Magical Attack",
    10: "Accuracy",
    4: "Physical Defense",
    14: "Magical Defense",
    7: "Speed",
    6: "Crit Rate",
    15: "Mastery"
}

ElementsMap = { # Sandfall/Content/Gameplay/ElementalTypes/EAttackType.uasset
    'title': 'EAttackType',
    0: "Fire",
    1: "Ice",
    2: "Lightning",
    3: "Earth",
    4: "Dark",
    5: "Light",
    6: "Physical",
    7: "Void",
    9: "Invalid"
}

AffinityMap = { # Sandfall/Content/Gameplay/ElementalTypes/EElementalAffinity.uasset
    'title': 'EElementalAffinity',
    0: "Invalid",
    1: "Weakness",
    2: "Resistant",
    3: "Nullify",
    4: "Absorb",
    5: "Neutral"
}

ItemTypeMap = { # Sandfall/Content/jRPGTemplate/Enumerations/E_jRPG_ItemType.uasset
    'title': 'E_jRPG_ItemType',
    0: "Weapon",
    6: "N/A",
    7: "Consumable",
    10: "Pictos",
    11: "Key",
    12: "Inventory",
    14: "Shard",
    15: "Gold",
    16: "Outfit", #internally "CharacterCustomization"
    17: "Skill", #internally "SkillUnlocker"
}

ItemSubTypeMap = { # Sandfall/Content/jRPGTemplate/Enumerations/E_jRPG_ItemSubtype.uasset
    'title': 'E_jRPG_ItemSubtype',
    0: "Lune Weapon",
    1: "Monoco Weapon",
    2: "Sciel Weapon",
    11: "Consumable",
    14: "Maelle Weapon",
    15: "Pictos",
    16: "Gustave Weapon", #internally "Noah Weapon"
    18: "Key",
    19: "Inventory",
    20: "Invalid",
    21: "Verso Weapon",
    22: "Journal",
    23: "Music Record"
}

ItemRarityMap = { # Sandfall/Content/jRPGTemplate/Enumerations/E_jRPG_ItemRarity.uasset
    'title': 'E_jRPG_ItemRarity',
    0: "Weapon",
    1: "Offensive", #internally "Red Core"
    2: "Misc", #internally "Green Core"
    3: "Support", #internally "Blue Core"
    4: "Legendary",
    5: "N/A",
    6: "Ancient"
}

TargetingTypeMap = { # Sandfall/Content/jRPGTemplate/Enumerations/E_jRPG_TargetingType.uasset
    'title': 'E_jRPG_TargetingType',
    0: "Only Self",
    1: "Single Living Enemy",
    2: "Single Living Ally",
    7: "All Enemies",
    8: "All Allies",
    12: "Single Dead Ally",
    13: "All Dead Allies",
    16: "Single Ally Then Enemy",
    17: "Any Single Ally",
    18: "Any Single Enemy",
    19: "All Living Enemies"
}

EffectCategoryMap = { # Sandfall/Content/Gameplay/Lumina/E_PassiveEffectCategory.uasset
    'title': 'E_PassiveEffectCategory',
    0: "Invalid",
    2: "Free Aim",
    3: "Base Attack",
    4: "AP",
    5: "Heal",
    6: "Shield",
    7: "Critical",
    8: "Damage",
    9: "Burn",
    10: "Buff",
    11: "Status Effect",
    12: "Parry",
    13: "Counter",
    14: "Death",
    15: "Solo",
    16: "Defense",
    17: "Speed",
    18: "Mark",
    19: "Debuff",
    20: "Break",
    21: "Items",
    22: "Gradient"
}

AreaNames = {
"MainMenu": "Main Menu",
"WorldMap": "The Continent",
"Camps": "Camp",
"Manor": "The Manor",
"Lumiere": "Lumière",
"SpringMeadows": "Spring Meadows",
"GoblusLair": "Flying Waters",
"AncientSanctuary": "Ancient Sanctuary",
"GestralVillage": "Gestral Village",
"EsquieNest": "Esquie's Nest",
"SeaCliff": "Stone Wave Cliffs",
"ForgottenBattlefield": "Forgotten Battlefield",
"MonocoStation": "Monoco's Station",
"OldLumiere": "Old Lumière",
"Visages": "Visages",
"Sirene": "Sirène",
"TheBarrier": "The Barrier",
"Monolith_Interior_PaintressIntro": "The Monolith",
"Monolith_Interior_Climb": "Inside The Monolith",
"Monolith_Exterior_Peak": "Monolith Peak",
"SideLevel_Reacher": "The Reacher",
"SideLevel_YellowForest": "Yellow Harvest",
"SideLevel_OrangeForest": "Falling Leaves",
"SideLevel_RedForest": "Crimson Forest",
"SidelLevel_FrozenHearts": "Frozen Hearts",
"SideLevel_AxonPath": "Renoir's Drafts",
"SideLevel_DarkShores": "Dark Shores",
"SideLevel_TwilightSanctuary": "Endless Night Sanctuary",
"SideLevel_CleasFlyingHouse": "Flying Manor",
"SideLevel_CleasTower_Entrance": "Endless Tower",
"SideLevel_CleasTower": "Endless Tower",
"SideLevel_CleasWorkshop": "Painting Workshop",
"SideLevel_VersosDraft": "Verso's Drafts",
"MiniLevel_Spring": "The Meadows",
"MiniLevel_WhiteTree": "White Tree",
"MiniLevel_GestralTreeCity": "Ancient Gestral City",
"MiniLevel_CleasOrangeArea": "Lost Woods",
"MiniLevel_BoatGraveyardPurple": "Boat Graveyard",
"MiniLevel_BoatGraveyardBlue": "Twilight Quarry",
"MiniLevel_BladesGraveyard": "Blades' Graveyard",
"SmallLevel_SpringMeadows": "The Fountain",
"SmallLevel_WhiteSands": "White Sands",
"SmallLevel_CaveAbbest": "Abbest Cave",
"SmallLevel_RedWoods": "Red Woods",
"SmallLevel_GoblusLair_02": "The Small Bourgeon",
"SmallLevel_StonewaveCliffsCave": "Stone Wave Cliffs Cave",
"SmallLevel_ChosenPath": "The Chosen Path",
"SmallLevel_FloatingIsland": "Sky Island",
"SmallLevel_StoneQuarry": "Stone Quarry",
"SmallLevel_Sirene": "Sirène's Dress",
"SmallLevel_Visages": "Isle of the Eyes",
"SmallLevel_Reacher": "The Crows",
"SmallLevel_GestralHiddenArena": "Hidden Gestral Arena",
"SmallLevel_FlyingCasinoEntrance": "Flying Casino",
"SmallLevel_SimonArea": "The Abyss",
"SmallLevel_Cemetery": "Floating Cemetery",
"SmallLevel_CoastalCave": "Coastal Cave",
"SmallLevel_ChromaZoneEntry": "Sunless Cliffs",
"SmallLevel_CavernCrusher": "Crushing Cavern",
"SmallLevel_DoorMaze": "Esoteric Ruins",
"SmallLevel_DarkGestralArena": "Dark Gestral Arena",
"SmallLevel_SacredRiver": "Sacred River",
"SmallLevel_GestralBeach": "Gestral Beach",
"SmallLevel_SinisterCave": "Sinister Cave",
"SmallLevel_TheCanvas": "The Canvas",
"SmallLevel_TheCarrousel": "The Carousel",
"SmallLevel_EsquieRealCousin": "Root of All Evil",
"Map_BattleTesting": "N/A"
}


