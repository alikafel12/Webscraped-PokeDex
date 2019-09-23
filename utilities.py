import re

class Pokemon:

    def __init__(self, number, name, type, total, hp, attack, defense, sp_atk, sp_def, speed):
        self.number = number
        self.name = fix_name(name)
        self.type = fix_type(type)
        self.total = total
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_atk = sp_atk
        self.sp_def = sp_def
        self.speed = speed
        self.img = ''

def fix_name(string):
    # function to clean up pokemon names
    words = ['Form', 'Size', 'Mode', 'Forme', 'Cloak', 'Confined', 'Style']
    if any(word in string for word in words):
        string = re.findall('[A-Z][^A-Z]*', string)
        string = string[0]
    return string

def fix_type(string):
    # function to clean up pokemon types
    if len(re.findall(r'[A-Z]', string)) == 2:
        string = re.findall('[A-Z][^A-Z]*', string)
        string = ' '.join(string)
        return string
    return string