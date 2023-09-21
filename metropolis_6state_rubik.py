import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from cube import cube
import matplotlib
matplotlib.rcParams.update({
    'figure.figsize': (10,10),
    'font.size': 18
})

my_cube = cube()
fig, ax = plt.subplots()

centres=[5,14,23,32,41,50]
# edges = [2,4,6,8,11,13,15,17,20,22,24,26,29,31,33,35,38,40,42,44,47,49,51,53]

def Ising_energy_of_config(config):     # Energy contribution of site [j,k]
    energy=0
    for pos in np.arange(1,len(config)+1,1):
        config_neighbours = nearest_neighbours_fn(pos)
        for x in config_neighbours:
            if config[pos-1] == config[x-1]:
                energy -= 1
            else:
                energy += 1
    return energy

def splash_energy_of_config(config):     # Energy contribution of site [j,k]
    energy=0
    for pos in np.arange(1,len(config)+1,1):
        config_neighbours = splash_neighbours_fn(pos)
        for x in config_neighbours:
            if config[pos-1] == config[x-1]:
                energy -= 1
            else:
                energy += 1
    return energy


def nearest_neighbours_fn(pos):
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
    
def splash_neighbours_fn(pos):
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


def do_random_op():
    possible_moves = my_cube.get_move_list()
    ran = np.random.randint(len(possible_moves))
    my_cube.string_operation(possible_moves[ran])

def test_random_op():
    possible_moves = my_cube.get_move_list()
    ran = np.random.randint(len(possible_moves))
    return my_cube.string_operation(possible_moves[ran],prospective=True, return_state=True)




def hot_start(dist):
    for i in range(dist):
        do_random_op()


def metropolis_sweep():
        config = my_cube.get_curr_state()
        # Energy of configuration before 'spin flip'
        old_energy = splash_energy_of_config(config)
        
        # select a random move to make, i.e. a random 'spin flip'
        possible_moves = my_cube.get_move_list()
        ran = np.random.randint(0,len(possible_moves))
        prospective_state = my_cube.string_operation(possible_moves[ran],prospective=True, return_state=True)

        # what the energy of the configuration would be after the random move is performed
        new_energy = splash_energy_of_config(prospective_state)

        # If the change in energy is negative, accept the spin flip.
        # If the change is positive, accept only if it satisfies the 'temperature requirement'
        # The probablity of transition is given by the ratio of the boltzmann weightings of the old and new state : exp(-dE/T).
        dE =  new_energy - old_energy
        if dE <= 0.:
            my_cube.string_operation(possible_moves[ran])
        elif np.exp(-beta*dE) > np.random.rand():
            print("np.exp(-beta*dE) ",np.exp(-beta*dE),"    ran: ",ran)
            my_cube.string_operation(possible_moves[ran])
        else:
            # print("Energy increased too much")
            None
        return my_cube.get_curr_state()





sweeps=10000
beta=1
num_frames = sweeps
animation_speed = 1000
hot_start(30)


energies = np.empty(sweeps)
for i in range(sweeps):
    swept_cube = metropolis_sweep()
    energies[i] = splash_energy_of_config(swept_cube)






plt.plot(energies)
plt.show()



# my_cube.visualise_state(ax)
# plt.show()