from random import randint

def roll_die():
    return randint(1, 6)

def roll_dice():
    return roll_die(), roll_die()