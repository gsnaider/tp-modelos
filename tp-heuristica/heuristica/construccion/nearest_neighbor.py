'''
Created on Jun 20, 2016

@author: gaston
'''
from __builtin__ import True, False
from random import randint

# Number of banks
N = 10

# Truck money
MAX_MONEY = 10000
INITIAL_MONEY = 0

BANKS = {0:"Origen", 1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H", 9:"I", 10:"J"}

# Banks money movements
MOV_O = 0  # Origin
MOV_A = 2000
MOV_B = -3000
MOV_C = 2000
MOV_D = 500
MOV_E = -1000
MOV_F = 5000
MOV_G = -1000
MOV_H = -1000
MOV_I = 1000
MOV_J = 1000

MOVEMENTS = [MOV_O, MOV_A, MOV_B, MOV_C, MOV_D, MOV_E, MOV_F, MOV_G, MOV_H, MOV_I, MOV_J]

# Distances
DIST_O = [0, 2314, 2789, 2728, 2553, 1504, 1581, 1661, 2320, 1387, 1697]
DIST_A = [2314, 0, 509, 501, 312, 1019, 736, 656, 60, 1039, 726]
DIST_B = [2789, 509, 0, 126, 474, 1526, 1226, 1133, 532, 1449, 1122]
DIST_C = [2728, 501, 126, 0, 541, 1516, 1184, 1084, 536, 1371, 1045]
DIST_D = [2553, 312, 474, 541, 0, 1157, 980, 919, 271, 1333, 1029]
DIST_E = [1504, 1019, 1526, 1516, 1157, 0, 478, 583, 996, 858, 855]
DIST_F = [1581, 736, 1226, 1184, 980, 478, 0, 115, 740, 470, 379]
DIST_G = [1661, 656, 1133, 1084, 919, 583, 115, 0, 667, 455, 288]
DIST_H = [2320, 60, 532, 536, 271, 996, 740, 667, 0, 1066, 759]
DIST_I = [1387, 1039, 1449, 1371, 1333, 858, 470, 455, 1066, 0, 328]
DIST_J = [1697, 726, 1122, 1045, 1029, 855, 379, 288, 759, 328, 0]

DISTANCES = [DIST_O, DIST_A, DIST_B, DIST_C, DIST_D, DIST_E, DIST_F, DIST_G, DIST_H, DIST_I, DIST_J]


def random_route():
    route = [0]
    money = 0
    while (len(route) <= N):
        next_bank = randint(1,N)
        if (not next_bank in route) and (have_enough_money(money, next_bank)):
                money = go_to_bank(route, money, next_bank)
                
    route.append(0)            
    return route        
    

def add_banks_idx_to_list(lst):
    tuple_list = []
    i = 0
    for x in lst:
        tup = (i, x)
        tuple_list.append(tup)
        i += 1
        
    return tuple_list
    

def get_sorted_bank_distances(bank):
    
    distances = DISTANCES[bank]
    distances = add_banks_idx_to_list(distances)
    sorted_distances = sorted(distances, key=lambda x: x[1])
    return sorted_distances


def have_enough_money(money, bank):
    movement = MOVEMENTS[bank]
    return (money + movement >= 0)

def have_enough_space(money, bank):
    movement = MOVEMENTS[bank]
    return (money + movement <= MAX_MONEY)
    
def go_to_bank(route, money, next_bank):
    route.append(next_bank)
    money = money + MOVEMENTS[next_bank]
    return money
    
def print_route(route):
    money = 0
    distance = 0
    idx = 0
    output = []
    
    for bank in route:
        if (idx > 0):
            previous_bank = route[idx - 1]
            dist_from_previous_bank = DISTANCES[previous_bank][bank]
            distance += dist_from_previous_bank
        movement = MOVEMENTS[bank]
        money += movement
        
        output_row = (BANKS[bank] + "\t", str(distance) + "\t"*3, str(money))
        output.append(output_row)
        
        idx += 1
    
    output_header = ("Banco","Distancia recorrida", "Dinero acumulado")
    print "\t".join(output_header)
    for output_row in output:
        print "".join(output_row)
    
    print ""
           
    
            
def find_bank_idx(distances, bank):
    idx = 0
    for tup in distances:
        if(tup[0] == bank):
            return idx
        idx += 1
            
def backtrack_one_bank(route, money):
    last_bank = route[-1]
    money = money - MOVEMENTS[last_bank]
    del route[-1]
    return money


def nearest_neighbor():
    money = MOV_O
    route = [0]
    
    done = False
    backtracked = False
    backtracked_bank = ""
    
    while not done:
    #    done = True
        current_bank = route[-1]
        found_next_bank = False
        sorted_bank_distances = get_sorted_bank_distances(current_bank)
        
        if(backtracked):
            idx = find_bank_idx(sorted_bank_distances, backtracked_bank) + 1
        else:
            # 0 is the current bank
            idx = 1 
    
        while (idx <= N) and (not found_next_bank):
            next_bank = sorted_bank_distances[idx][0]
            if (not next_bank in route) and (have_enough_money(money, next_bank) and (have_enough_space(money, next_bank))):
                money = go_to_bank(route, money, next_bank)
                found_next_bank = True
            else:
                idx += 1
                
        if (found_next_bank):
            backtracked = False
        else:
            money = backtrack_one_bank(route, money)
            backtracked_bank = current_bank
            backtracked = True
        
        
        if(len(route) == 0):
            done = True
            print "No hay ruta posible."
            print ""
        
        if (len(route) == N + 1):
            route.append(0) # Return to start
            done = True
            print "Ruta encontrada."
            print ""
            return route


