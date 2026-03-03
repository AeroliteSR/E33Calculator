import json, pathlib, os
from typing import Callable
from Data.Misc import *

"""This file is used to trim down exported UASSET properties by extracting only the important data.
    Useful for if the game updates and I haven't updated the data for it."""

def get_encounter_data(data):
    extracted_data = {}
    enemyName = []
    enemieslist = data.get('Enemies_14_3D2609EC487DFDF67CB27FAC3F632728', [])

    for enemy in enemieslist:
        enemyName.append(enemy['Value'].get('RowName', None))

    extracted_data['Enemies'] = enemyName
    extracted_data['Level'] = data.get('EncounterLevelOverride_17_FF0AA3B94D98F48F0541B8B7F8EC5A57', 0)
    extracted_data['CanRetry'] = data.get('IsRetryableBattle_26_1EDE597E49DB47E1A4F66C8AC61FF72B', None)
    extracted_data['CantFlee'] = data.get('FleeImpossible_13_2764B2B94142E1FC99C8A182A4BC0B06', None)
    
    return extracted_data

def get_area_level(data):
    return {"Level": data.get('ScalingMaxLevel_45_389D00474B3DAD3D274A2FB0BDA15EA9', None)}

def get_enemy_data(data):
    output = {}

    output['Display Name'] = data.get("EnemyDisplayName_5_D5F33F5245600FA905D7EDBC701052B9", {}).get('SourceString', "N/A")
    output['Gender'] = data.get('GenderTag_92_6F3990474DBB8EB2DEE06CB3CADDF2C5', 'ETextGender::Unknown').replace('ETextGender::', '')
    output['Level'] = data.get("Level_8_C5168BF64AE02187C5DC54BDD3C3AA6B", 0)
    output['Is Flying Enemy'] = data.get('IsFlying_84_64A513A54C958FAACD87EAB245A681D3', False)
    output['Is Boss'] = data.get('IsBoss_46_F2839289483FE917FB914594C70C7CE4', False)

    archetype = data.get('EnemyArchetype_73_3AAC717A431AF83C143E8E96B2471F55', {}).get('ObjectName', None)
    output['Archetype'] = archetype.split("_Archetype_")[1].replace("'", '')

    output['Enemy Scaling'] = {split_CCase(k.split('_')[0]): v for k,v in data.get('EnemyScaling_63_BC7A78364C5ADED643FC63A6373F575B', {}).items()}
    stats = {stat['Key']: stat['Value'] for stat in data.get('EnemyStats_44_F9C77A10450C7173ACD1AE8DF682A1F5', [])}
    output['Enemy Stats'] = applyMap(stats, EnemyStatsMap)
    
    loot = data.get('PossibleLoot_49_4083979C4864530BB4DB9EB51A43C8AA', None)
    drops = []
    if loot:
        for item in loot:
            itemname = item['Item_3_70B128FA450367A9238446B74FC936F1']['RowName']
            amount = item['Quantity_7_568BFEC649698C01749B2DBD1D349850']
            chance = item['LootPercentageChance_10_28FD2A004A7AF8A838C478891D665926']
            drops.append({"Name": itemname, "Quantity": amount, "Chance": chance})
    output['Loot'] = drops
    output['Loot Chance Multiplier'] = data.get('LootChanceMultiplier_76_152782FA4E34549F958CD08454131072', 1.0)
    output['Monoco Foot'] = data.get('ShapeshiftCaptureLootItem_82_D4811B7B414B72342F54A1ACB7AC120A', None).replace('Foot', ' Foot')

    commonstats = data.get('CommonCharacterStats_40_C6BD93574F13EDC24C2A9EADFF59BD96', {})
    output['Shields on Spawn'] = commonstats.get('ShieldPointsAtSpawn_17_7C33A6DB40E55DF7A672D2BAA5CFCE14', 0)
    output['Skill Damage Taken'] = commonstats.get('ReceivedSkillDamageMultiplier_21_13627A1741A465D26AE518BA8D3FA731', 1.0)
    output['Free Aim Damage Taken'] = commonstats.get('ReceivedFreeAimDamageMultiplier_23_FCCDD66342086D44FF9197AA36895E0E', 1.0)

    output['Break Bar HP'] = data.get('BreakBarHPPercent_66_8D532DFC404115297498D597484E00A8', 'N/A')
    output['Stun Duration'] = data.get('BreakBarStunDuration_70_6BB695004BDBF84B04A780883755F68E', 1)

    affinities = {aff['Key']: aff['Value'] for aff in data.get('InitialElementalAffinities_89_562E68B049820C479633AC85726A9E71', [])}
    output['Affinities'] = []
    if affinities:
        output['Affinities'].append(applyMap(affinities, ElementsMap, AffinityMap))

    return output

def get_item_data(data):
    output = {}

    output['Display Name'] = data.get('Item_DisplayName_89_41C0C54E4A55598869C84CA3B5B5DECA', {}).get('SourceString', "N/A")
    output['Type'] = applyMap(data.get("Item_Type_88_2F24F8FB4235429B4DE1399DBA533C78"), ItemTypeMap)
    output['Sub-Type'] = applyMap(data.get("Item_Subtype_87_0CE0028F4D632385B61EDABBFBDF5360"), ItemSubTypeMap)
    output['Rarity'] = applyMap(data.get("Item_Rarity_86_4D9579394454700B6BC0ABAECA0714C8"), ItemRarityMap)
    output['Targets'] = applyMap(data.get('Consumable_TargetingType_79_04B50DFD410E7F51F4E5E1A128555D0B'), TargetingTypeMap)

    output['Description'] = data.get('ItemDescription_32_0A978AFB4AB4B316342DD6A72ACDD4E1', {}).get("SourceString", "N/A")

    output['Usable In Battle'] = data.get('Consumable_CanBeUsedInBattle?_74_5EA5813946B70E3FD9333289C000D538', False)
    output['Usable In Inventory'] = data.get('Consumable_CanBeUsedInInventory?_75_55B1EE634A155E1A8A4F439A77864154', False)
    output['Maximum Held'] = data.get('Consumable_MaxStackAmount_76_2DD073774D235ED7EE5C8F99817D7FFA', 99)

    stats = {stat['Key']: stat['Value'] for stat in data.get('Pictos_ItemStats_91_229F4A00415AB214191377B73987FF7B', [])}
    output['Pictos Stats'] = []
    if stats:
        output['Pictos Stats'].append(applyMap(stats, EnemyStatsMap))

    return output

def get_effect_data(data):
    output = {}

    output['Display Name'] = data.get('Name_2_10859E81431F2583F434998C9A00D4AC', {}).get('SourceString', "N/A")
    output['Description'] = data.get('Description_12_EEFC7EED42F5C4FA14BBD7B356617893', {}).get("SourceString", "N/A")

    output['Lumina Cost'] = data.get('LuminaCost_15_BC10A93D48987A14F96279AC521E94CF', 0)
    output['Steps To Unlock Lumina'] = data.get('LuminaUnlockStepsCount_19_B80447FF455A4D693EAD2991AD473004', 4)

    categories = data.get('Categories_23_4052AE7B40B336B43096B7A2E554F50D', [])
    output['Categories'] = []
    if categories:
        for category in categories:
            output['Categories'].append(applyMap(category, EffectCategoryMap))

    return output

def get_lootTable_data(data):
    output = {}

    output['Min Level'] = data.get('LevelRangeMin_4_B29308774CD00C1A52F8D79BA86F477B', 1)
    output['Max Level'] = data.get('LevelRangeMax_5_F72AF1DC4BF48572B21360B7ADC22C17', 300)
    output['Chance'] = data.get('ChancePercent_10_D60438D64925BB0788FBFCB605B0518A', 100)

    loot = data.get('LootEntries_14_4A650E0F4C998FBA66B50DAEE60C253A', [])
    output['Drops'] = []
    for entry in loot:
        output['Drops'].append({"Item": entry['ItemID_7_8AE2C1FA4D5144FF4549F59430C1FC3A'],
                                "Quantity": entry['Quantity_4_E9AC4373432C806BD7F0B4BE05A1303D'],
                                "Weight": entry['Weight_2_748348484D98C53FEC988399AA400A74']})
        
    return output

def get_scaling_data(data):
    output = {}

    output['HP'] = data.get('HP_27_9B8F0EF14EBC6DBDE30E86A7FFE48646', 1)
    output['Physical Attack'] = data.get('PhysicalAttack_28_82A69E334B7A1E723084829AFCCEAA25', 1)
    output['Physical Defense'] = data.get('PhysicalDefense_29_F610675445A2768C30612FBAB57F46DE', 1)
    output['Magical Attack'] = data.get('MagicalAttack_30_653EB84143B61538EFE2F1BE21539BC7', 1)
    output['Magical Defense'] = data.get('MagicalDefense_31_5972F1F24C89F844C3B6DEBF6AE09DD0', 1)
    output['Mastery'] = data.get('Mastery_32_6E8B50B847CAA10796C547931DA5B71F', 1)
    output['Accuracy'] = data.get('Accuracy_33_75BBC9AE40CCAAD4B40F23983475A0D8', 1)
    output['Speed'] = data.get('Speed_36_FC80E04941CF184AEFA369950419F557', 1)
    output['Critical Chance'] = data.get('CriticalChance_18_29F8B957479C0D953C447E95FF3492E4', 1)
    output['Chroma'] = data.get('Chroma_34_6C260F8F48BCE6E6C43C568C38941012', 1)
    output['Experience'] = data.get('Experience_35_BEE8A0DD4ED59C6C6782B88443AB9AE8', 1)

    return output

def split_CCase(text):
    if len(text)<3:
        return text
    result = ""
    for i, char in enumerate(text):
        if i > 0 and char.isupper():
            result += " "
        result += char
    return result

def applyMap(data, k_map, v_map=None):
    if isinstance(data, dict):
        fixed_data = {}
        for name, value in data.items():
            k_id = int(name.replace(f'{k_map['title']}::NewEnumerator', ''))
            if v_map:
                v_id = int(value.replace(f'{v_map['title']}::NewEnumerator', ''))
                value = v_map[v_id]

            fixed_data[k_map[k_id]] = value
        return fixed_data
    else:
        id = int(data.replace(f'{k_map['title']}::NewEnumerator', ''))
        return k_map[id]

def extract_rows(json_file, func: Callable):
    with open(json_file, 'r') as f:
        data = json.load(f)[0]  # Assuming the data is wrapped in a list
    
    if 'Rows' in data:
        rows = data['Rows']
        extracted_data = {}
        for row_name, row_data in rows.items():
            print(f"Extracting data for row: {row_name}")  # Debugging output
            extracted_row = func(row_data)
            if extracted_row:
                extracted_data[row_name] = extracted_row
        return extracted_data
    else:
        print(f"Warning: 'Rows' not found in {json_file}")
        return None
    
def process_json_files(path, func: Callable):
    all_data = {}
    if os.path.isdir(path):
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                json_file_path = os.path.join(path, filename)
                extracted_data = extract_rows(json_file_path, func)
                
                if extracted_data:
                    all_data[filename] = extracted_data
                else:
                    print(f"No data extracted from {filename}")  # Debugging output
    else:
        all_data = extract_rows(path, func)

    return all_data


def writeOutput(_path, name, data):
    print(_path, name)
    if not os.path.exists(_path):
        os.makedirs(_path, exist_ok=True)

    with open(f'{_path}/{name}', 'w+') as file:
        json.dump(data, file, indent=4)

def main():
    global base_path

    tasks = {
        #"Area Levels.json": ["Gameplay/LevelData/DT_LevelData.json", get_area_level],
        #"Enemies.json": ["jRPGTemplate/Datatables/DT_jRPG_Enemies.json", get_enemy_data],
        #"Loot Tables": ["Gameplay/Inventory/LootSystem/Content", get_lootTable_data],
        #"Scaling/Story": ["Gameplay/Battle/ScalingSystem/Content/Easy_Difficulty", get_scaling_data],
        #"Scaling/Expeditioner": ["Gameplay/Battle/ScalingSystem/Content/Normal_Difficulty", get_scaling_data],
        #"Scaling/Expert": ["Gameplay/Battle/ScalingSystem/Content/Hard_Difficulty", get_scaling_data],
        #"Encounters.json": ["jRPGTemplate/Datatables/Encounters_Datatables/DT_Encounters_Composite.json", get_encounter_data],
        #"Items.json": ["jRPGTemplate/Datatables/DT_jRPG_Items_Composite.json", get_item_data],
        #"Effects.json": ["Gameplay/Lumina/DT_PassiveEffects.json", get_effect_data],
    }

    for name, values in tasks.items():
        path, func = values
        data = process_json_files(base_path / path, func)

        if '.' not in name:
            _path = rf"Output/{name}"
            for filename, returned in data.items():
                writeOutput(_path, filename, returned)

        else:
            writeOutput("Output", name, data)

if __name__ == "__main__":
    base_path = pathlib.Path(r'C:\Users\Aero\Programming\FModel\Output\Exports\Sandfall\Content') # path to your exports
    main()


    """Loot Tables - Sandfall/Content/Gameplay/Inventory/LootSystem/Content
      Encounters - Sandfall/Content/jRPGTemplate/Datatables/Encounters_Datatables
      Scaling Systems - Sandfall/Content/Gameplay/Battle/ScalingSystem
      Area Levels - Sandfall/Content/Gameplay/LevelData/DT_LevelData.uasset
      Enemy Data - Sandfall/Content/jRPGTemplate/Datatables/DT_jRPG_Enemies.uasset
    """