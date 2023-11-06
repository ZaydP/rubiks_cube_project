import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


colours = ['white', 'yellow', 'red', 'orange', 'blue', 'green']

def my_create_vis_cube_state(matrix): # split cube state matrix from 52x1 into 6x3x3

    cube_state_split_1 = np.split(np.copy(matrix), 6)
    cube_state_split_final = []

    for i in cube_state_split_1:
        cube_state_split_final.append(np.split(i, 3))

    return np.array(cube_state_split_final)

def my_visualise_face(face, translation, ax):   # input face and pos, output patch object on ax

    ax.add_patch(plt.Rectangle((translation[0]-1, translation[1]+1), 0.8, 0.8, color=colours[int(face[0][0])]))
    ax.add_patch(plt.Rectangle((translation[0]+0, translation[1]+1), 0.8, 0.8, color=colours[int(face[0][1])]))
    ax.add_patch(plt.Rectangle((translation[0]+1, translation[1]+1), 0.8, 0.8, color=colours[int(face[0][2])]))

    ax.add_patch(plt.Rectangle((translation[0]-1, translation[1]+0), 0.8, 0.8, color=colours[int(face[1][0])]))
    ax.add_patch(plt.Rectangle((translation[0]+0, translation[1]+0), 0.8, 0.8, color=colours[int(face[1][1])]))
    ax.add_patch(plt.Rectangle((translation[0]+1, translation[1]+0), 0.8, 0.8, color=colours[int(face[1][2])]))

    ax.add_patch(plt.Rectangle((translation[0]-1, translation[1]-1), 0.8, 0.8, color=colours[int(face[2][0])]))
    ax.add_patch(plt.Rectangle((translation[0]+0, translation[1]-1), 0.8, 0.8, color=colours[int(face[2][1])]))
    ax.add_patch(plt.Rectangle((translation[0]+1, translation[1]-1), 0.8, 0.8, color=colours[int(face[2][2])]))

def my_visualise_state(matrix,ax):  # input full matrix outputs visualization

    ax.add_patch(plt.Rectangle((-15, -15), 30, 30, color='gray'))

    vis_state = my_create_vis_cube_state(matrix)

    my_visualise_face(vis_state[0], [0, 0], ax)
    my_visualise_face(vis_state[1], [8, 0], ax)
    my_visualise_face(vis_state[2], [0, 4], ax)
    my_visualise_face(vis_state[3], [0, -4], ax)
    my_visualise_face(vis_state[4], [4, 0], ax)
    my_visualise_face(vis_state[5], [-4, 0], ax)

def animate(lattices,animation_speed,fig,ax):   # input set of state matrices, makes animation with animation speed in ms
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

