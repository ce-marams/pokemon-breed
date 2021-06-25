from numpy import random
from numpy.lib.utils import safe_eval

# All stats
STATS = ["PS", "ATK", "DEF", "SATK", "SDEF", "VEL"]

# List of natures
NATS = ["Activa", "Afable", "Agitada", "Alegre", "Alocada", "Amable", "Audaz", "Cauta", "Docil", "Firme", "Floja", "Fuerte",
"Grosera", "Huraña", "Ingenua", "Mansa", "Miedosa", "Modesta", "Osada", "Picara", "Placida", "Rara", "Serena", "Seria", "Timida"]

# Pokemon are dictionaries -> change to Class
def create_pkmn(gender, PS, Atk, Def, SAtk, SDef, Vel, Nature, Obj=None):
    return {"GENDER": gender, "PS": PS, "ATK": Atk, "DEF": Def, "SATK": SAtk, "SDEF": SDef, "VEL": Vel, "NAT": Nature, "OBJ": Obj}


def siblingIVs(pokemon1, pokemon2, num_inhIVs):
    """ Choose num_inhIVs (3 or 5) from the parents and the rest IVs are random. """
    IVs = {}
    inhIVs = random.choice(STATS, num_inhIVs, replace=False)
    noninhIVs = list(set(STATS) - set(inhIVs))

    for IV in inhIVs:
        if (pokemon1['OBJ'] == 'Br'+IV):
            IVs[IV] = pokemon1[IV]
        elif (pokemon2['OBJ'] == 'Br'+IV):
            IVs[IV] = pokemon2[IV]
        elif (random.random() < 0.5):
            IVs[IV] = pokemon1[IV]
        else:
            IVs[IV] = pokemon2[IV]
    
    for IV in noninhIVs:
        IVs[IV] = random.randint(0, 32)

    return IVs


def breed(pokemon1, pokemon2, pfemale=0.5):
    """ Determines number of inherited IVs, gender and nature. """

    if (pokemon1['OBJ'] == 'DK') or (pokemon2['OBJ'] == 'DK'):    # Destiny Knot. Inherit 5 stats.
        num_inhIVs = 5
    else:
        num_inhIVs = 3
    
    sibling = siblingIVs(pokemon1, pokemon2, num_inhIVs)
    
    if random.random() <= pfemale:
        sibling['GENDER'] = "F"
    else:
        sibling['GENDER'] = "M"
    
    if pokemon1['OBJ'] == 'ES':
        sibling['NAT'] = pokemon1['NAT']
    elif pokemon2['OBJ'] == 'ES':
        sibling['NAT'] = pokemon2['NAT']
    else:
        sibling['NAT'] = random.choice(NATS)
    
    sibling['OBJ'] = None

    return sibling


def check_sibling(test_sibling, goal_pkmn):
    """Checks if we obtained the desired Pokémon"""
    checkpoints = STATS + ['GENDER', 'NAT']

    for item in checkpoints:
        if goal_pkmn[item] == None:
            pass

        elif test_sibling[item] != goal_pkmn[item]:
            return False
        
        else:
            pass
    
    return True


def probs_goal(pokemon1, pokemon2, goal_pkmn, tries=50000):
    
    success = 0
    # str_genders = ''
    good_iters = []
    
    for i in range(tries):

        sibling = breed(pokemon1, pokemon2)

        if check_sibling(sibling, goal_pkmn):
            success += 1
            # str_genders = str_genders + sibling['GENDER']
            good_iters = good_iters +  [i+1]
    
    return success/tries, good_iters

pokemon1 = create_pkmn("M", 31, 31, 23, 31, 0, 10, "Mansa", "ES")
pokemon2 = create_pkmn("F", 8, 31, 29, 31, 31, 31, "Grosera", "DK")
goal = create_pkmn(None, 31, 31, None, 31, 31, 31, "Mansa")

prob, good_ecl = probs_goal(pokemon1, pokemon2, goal)

num_events = list(range(1, len(good_ecl)+1))

prevecl = good_ecl[0]
eggs2perfect = [prevecl]
for ecl in good_ecl[1:]:
    eggs2perfect = eggs2perfect + [ecl -prevecl]
    prevecl = ecl


from matplotlib import pyplot as plt

#plt.plot(good_ecl, num_events, '.', alpha=0.8, markersize=1)
plt.hist(eggs2perfect, bins=25, density=True, alpha=0.8)
plt.show()

