import numpy as np


centres=[5,14,23,32,41,50]
edges = [2,4,6,8,11,13,15,17,20,22,24,26,29,31,33,35,38,40,42,44,47,49,51,53]

def nearest_neighbours_fn(pos): # returns the indeces of the tiles directly adjacent to pos
    # print("pos input: ", pos)
    if pos%9 == 1:
        neighbours = [pos+1,pos+3]
    elif pos%9 == 2:
        neighbours = [pos-1,pos+1,pos+3]
    elif pos%9 == 3:
        neighbours = [pos-1,pos+3]
    elif pos%9 == 4:
        neighbours = [pos-3,pos+1,pos+3]
    elif pos%9 == 5:
        neighbours = [pos-3,pos-1,pos+1,pos+3]
    elif pos%9 == 6:
        neighbours = [pos-3,pos-1,pos+3]
    elif pos%9 == 7:
        neighbours = [pos-3,pos+1]
    elif pos%9 == 8:
        neighbours = [pos-3,pos-1,pos+1]
    elif pos%9 == 0:
        neighbours = [pos-3,pos-1]
    else:
        raise Exception("pos argument provided not an int")
    return neighbours
    
def splash_neighbours_fn(pos):  # returns the indeces of the tiles surrounding pos
    # print("pos input: ", pos)
    if pos%9 == 1:
        neighbours = [pos+1,pos+3,pos+4]
    elif pos%9 == 2:
        neighbours = [pos-1,pos+1,pos+3,pos+2,pos+4]
    elif pos%9 == 3:
        neighbours = [pos-1,pos+3,pos+2]
    elif pos%9 == 4:
        neighbours = [pos-3,pos+1,pos+3,pos-2,pos+4]
    elif pos%9 == 5:
        neighbours = [pos-3,pos-1,pos+1,pos+3,pos-4,pos-2,pos+2,pos+4]
    elif pos%9 == 6:
        neighbours = [pos-3,pos-1,pos+3,pos-4,pos+2]
    elif pos%9 == 7:
        neighbours = [pos-3,pos+1,pos-2]
    elif pos%9 == 8:
        neighbours = [pos-3,pos-1,pos+1,pos-2,pos-4]
    elif pos%9 == 0:
        neighbours = [pos-3,pos-1,pos-4]
    else:
        raise Exception("pos argument provided not an int")
    return neighbours



def Ising_energy_of_config(config): # Classical Ising energy with nearest_neighbours
    energy=0
    for pos in np.arange(1,len(config)+1,1):
        config_neighbours = nearest_neighbours_fn(pos)
        for x in config_neighbours:
            if config[pos-1] == config[x-1]:
                energy -= 1
            else:
                energy += 1
    return energy

def splash_energy_of_config(config):  # Classical Ising energy with splash_neighbours
    energy=0
    for pos in np.arange(1,len(config)+1,1):
        config_neighbours = splash_neighbours_fn(pos)
        for x in config_neighbours:
            if config[pos-1] == config[x-1]:
                energy -= 1
            else:
                energy += 1
    return energy