import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from cube import cube
import metrics
import matplotlib
matplotlib.rcParams.update({
    'figure.figsize': (10,10),
    'font.size': 18
})

my_cube = cube()
fig, ax = plt.subplots()



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





def Miles_Metric_Move():
    old_dist=my_cube.calculate_metric()

    possible_moves = my_cube.get_move_list()
    opposite_moves = ["F'","F","F2","B'","B", "B2", "U'","U", 'U2', "D'", "D", 'D2', "R'", "R", 'R2', "L'", "L", 'L2', "M'", "M", 'M2', "E'", "E", 'E2', "S'", "S", 'S2']
    new_dists=np.empty(len(possible_moves))
    for i in range(len(possible_moves)):
        my_cube.string_operation(possible_moves[i],prospective=False)
        new_dists[i]=my_cube.calculate_metric()
        my_cube.string_operation(opposite_moves[i],prospective=False)
    min_dist_index = np.argmin(new_dists)

    move_selected = possible_moves[min_dist_index]
    return move_selected



    














colours = ['white', 'yellow', 'red', 'orange', 'blue', 'green']
def my_visualise_face(face, translation, ax):

    ax.add_patch(plt.Rectangle((translation[0]-1, translation[1]+1), 0.8, 0.8, color=colours[int(face[0][0])]))
    ax.add_patch(plt.Rectangle((translation[0]+0, translation[1]+1), 0.8, 0.8, color=colours[int(face[0][1])]))
    ax.add_patch(plt.Rectangle((translation[0]+1, translation[1]+1), 0.8, 0.8, color=colours[int(face[0][2])]))

    ax.add_patch(plt.Rectangle((translation[0]-1, translation[1]+0), 0.8, 0.8, color=colours[int(face[1][0])]))
    ax.add_patch(plt.Rectangle((translation[0]+0, translation[1]+0), 0.8, 0.8, color=colours[int(face[1][1])]))
    ax.add_patch(plt.Rectangle((translation[0]+1, translation[1]+0), 0.8, 0.8, color=colours[int(face[1][2])]))

    ax.add_patch(plt.Rectangle((translation[0]-1, translation[1]-1), 0.8, 0.8, color=colours[int(face[2][0])]))
    ax.add_patch(plt.Rectangle((translation[0]+0, translation[1]-1), 0.8, 0.8, color=colours[int(face[2][1])]))
    ax.add_patch(plt.Rectangle((translation[0]+1, translation[1]-1), 0.8, 0.8, color=colours[int(face[2][2])]))

def my_visualise_state(matrix,ax):

    ax.add_patch(plt.Rectangle((-15, -15), 30, 30, color='gray'))

    vis_state = my_create_vis_cube_state(matrix)

    # ax.add_patch(plt.Rectangle((0, 0), 0.8, 0.8, color=colours[state[0][0][0]]))
    my_visualise_face(vis_state[0], [0, 0], ax)
    my_visualise_face(vis_state[1], [8, 0], ax)
    my_visualise_face(vis_state[2], [0, 4], ax)
    my_visualise_face(vis_state[3], [0, -4], ax)
    my_visualise_face(vis_state[4], [4, 0], ax)
    my_visualise_face(vis_state[5], [-4, 0], ax)

    # plt.xlim(-7.5, 12.5)
    # plt.ylim(-10, 10)
    # plt.axis('off')
    # plt.gca().set_aspect('equal')

def my_create_vis_cube_state(matrix):

    cube_state_split_1 = np.split(np.copy(matrix), 6)
    cube_state_split_final = []

    for i in cube_state_split_1:
        cube_state_split_final.append(np.split(i, 3))

    return np.array(cube_state_split_final)



sweeps=10000
beta=0.9
num_frames = sweeps
animation_speed = 500
hot_start(30)


def animate(lattices):
    matrices = lattices
    num_frames=len(lattices)
    # Create a figure and axis for the animation
    # fig, ax = plt.subplots()
    plt.xlim(-7.5, 12.5)
    plt.ylim(-10, 10)
    plt.axis('off')
    plt.gca().set_aspect('equal')
    # Function to update the plot for each frame
    def update(frame):
        # ax.clear()
        my_visualise_state(matrices[frame],ax)
        ax.set_title(f'Frame {frame + 1}/{num_frames}')

    # Create the animation
    animation = FuncAnimation(fig, update, frames=num_frames, repeat=False, interval=animation_speed)
    plt.show()





swept_cubes = np.empty([sweeps,54])
energies = np.empty(sweeps)
metric = np.empty(sweeps)

for i in range(sweeps):
    swept_cubes[i] = metropolis_sweep(metrics.splash_energy_of_config,0.6)
    energies[i] = metrics.splash_energy_of_config(swept_cubes[i])


def Minimize(n,func):
    for i in range(n):
        move_selected_by_metric = func()
        my_cube.string_operation(move_selected_by_metric)
        swept_cubes[i] = my_cube.get_curr_state()
        metric[i] = my_cube.calculate_metric()
    

# Minimize(sweeps,Miles_Metric_Move)

animate([swept_cubes[1],swept_cubes[50],swept_cubes[99]])

plt.plot(energies)

plt.show()
