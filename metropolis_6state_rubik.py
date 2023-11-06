import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from cube import cube
import visualize_cube
import metrics
import matplotlib
matplotlib.rcParams.update({
    'figure.figsize': (10,10),
    'font.size': 18
})

my_cube = cube()
fig, ax = plt.subplots()



def hot_start(dist):
    possible_moves = my_cube.get_move_list()
    for i in range(dist):
        ran = np.random.randint(len(possible_moves))
        my_cube.string_operation(possible_moves[ran])


def metropolis_sweep(metric,beta):
        config = my_cube.get_curr_state()
        # Energy of configuration before 'spin flip'
        old_energy = metric(config)
        
        # select a random move to make, i.e. a random 'spin flip'
        possible_moves = my_cube.get_move_list()
        ran = np.random.randint(0,len(possible_moves))
        prospective_state = my_cube.string_operation(possible_moves[ran],prospective=True, return_state=True)

        # what the energy of the configuration would be after the random move is performed
        new_energy = metric(prospective_state)

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



def execute_metropolis(chosen_metric,sweeps,beta):
    swept_cubes = np.empty([sweeps,54])
    metric_values = np.empty(sweeps)

    for i in range(sweeps):
        swept_cubes[i] = metropolis_sweep(chosen_metric,beta)
        metric_values[i] = chosen_metric(swept_cubes[i])

    return swept_cubes, metric_values


sweeps=100
beta=0.9
animation_speed = 50


hot_start(10)


swept_cubes,metric_values = execute_metropolis(metrics.splash_energy_of_config,sweeps,beta)

    

# visualize_cube.animate(swept_cubes,animation_speed,fig,ax)

visualize_cube.animate(swept_cubes[::10],animation_speed,fig,ax)

# visualize_cube.animate([swept_cubes[1],swept_cubes[50],swept_cubes[99]],animation_speed,fig,ax)

plt.plot(metric_values)
plt.xlabel("sweeps")
plt.ylabel("metric value")

plt.show()
