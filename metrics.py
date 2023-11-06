import numpy as np
import visualize_cube

# NB!! The position 'pos' goes from 1 to 54 , not 0 to 53.

centres=[5,14,23,32,41,50]
edges = [2,4,6,8,11,13,15,17,20,22,24,26,29,31,33,35,38,40,42,44,47,49,51,53]

def nearest_neighbours_fn(pos,zero_index=False): # returns the indeces of the tiles directly adjacent to pos
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
    neighbour_array = np.array(neighbours)
    if zero_index==True:
        neighbour_array = neighbour_array - 1
    return neighbour_array
    
def splash_neighbours_fn(pos,zero_index=False):  # returns the indeces of the tiles surrounding pos
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
    neighbour_array = np.array(neighbours)
    if zero_index==True:
        neighbour_array = neighbour_array - 1
    return neighbour_array





def face_neighbours(pos):   # returns the indeces of all the tiles on the same face as pos
    if pos < 1 or pos > 54:
        raise ValueError("x should be in the range 1 to 54")

    # Calculate the starting number of the interval of 6
    interval_start = (pos - 1) // 6 * 6 + 1

    # Generate a list of numbers in the same interval of 6
    numbers_in_interval = list(range(interval_start, interval_start + 6))

    return numbers_in_interval




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



def Miles_Metric_splash_neighbours(config):
    sum=0
    if len(config)==54:
        face_split = np.split(np.copy(config), 6)
    else:
        print("Metric input not 54x1")

    total_sum = 0

    for face in face_split:

        face_sum = 0
        for square in range(9):
            #colour of the current square
            segment_colour = face[square]

            #finds the unique colours amongst the neighbours of square, and its multiplicity
            unique, counts = np.unique(face[splash_neighbours_fn(square,zero_index=True)], return_counts=True)
            unique_dict = dict(zip(unique, counts))
            
            try:# finds how many amongst the neighbours have the same colour as square
                segment_count = unique_dict[segment_colour]
            except KeyError:
                segment_count = 0
            segment_frac = segment_count / len(splash_neighbours_fn(square))
            
            face_sum += segment_frac
        
        face_avg = face_sum / 9

        total_sum += face_avg

    total_avg = total_sum / 6

    return total_avg



def Miles_Metric(config):
    sum=0
    for pos in np.arange(1,len(config)+1,1):
        colour_at_pos = config[pos]
        config_neighbours = face_neighbours(pos)

        #find all unique colours in neighbours and how many of each there are
        unique, counts = np.unique(config_neighbours, return_counts=True)
        #makes tuple of colours and their multiplicity
        unique_dict = dict(zip(unique, counts))
        
        try:
            segment_count = unique_dict[colour_at_pos]
        except KeyError:
            segment_count = 0
        segment_frac = segment_count / len(config_neighbours)

        sum+=segment_frac

    avg=sum/len(config)
    return avg



