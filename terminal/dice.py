from random import randint

def roll_die():
    return randint(1, 6)

def roll_dice():
    return roll_die(), roll_die()

if __name__ == '__main__':
    for i in range(10):
        print(roll_dice())