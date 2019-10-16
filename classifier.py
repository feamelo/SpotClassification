#################################### Recognizer #####################################
# Autora: Fernanda Amaral Melo, Luiz Fernando Neves de Araújo   				
# Contato: fernanda.amaral.melo@gmail.com										
#																				
# Script detecção e classificação de manchas				
#																				
#####################################################################################

from matplotlib import pyplot as plt
from numpy import genfromtxt
import numpy as np
import cv2
import csv
import sys
import os

# Macros
IMAGE = True
GRAPH = False
RUN = 3  # 1 - Get shapes, 2 - Get holes, 3 - Analyze neighborhood
fileDir = os.path.dirname(os.path.abspath(__file__))

# Methods


def img_plot(img_title, image, img_type):
    plt.figure()
    if (img_type):
        plt.imshow(image, cmap='gray')
        plt.title(img_title)
    else:
        plt.plot(image, 'go')
        plt.title(img_title)


def append_equivalence(equivalence, label):
    # Create a list of equivalence labels in which each element i has all j equivalent labels
    for i in range(0, np.shape(equivalence)[0]):
        for j in range(0, np.shape(equivalence[i])[0]):
            if (equivalence[i][j] == label[0]):
                equivalence[i].append(label[1])
                return equivalence
            elif (equivalence[i][j] == label[1]):
                equivalence[i].append(label[0])
        return equivalence

    equivalence.append(label)
    return equivalence


def replace_equivalence(equivalence, image, x, y):
    # Replace equivalent labels
    for i in range(0, np.shape(equivalence)[0]):
        for j in range(0, np.shape(equivalence[i])[0]):
            if (image[x][y] == equivalence[i][j]):
                image[x][y] = equivalence[i][0]
                return image
    return image


def mapping(equivalence, pixel):
    if (pixel == 0):
        return 1
    j = 2
    for i in range(0, np.shape(equivalence)[0]):
        if (pixel == equivalence[i][0]):
            return j
        j += 1


def labeling(p, img_height, img_width):
    label = 2
    p_label = [[0 for x in range(img_height + 2)]
               for y in range(img_width + 2)]
    equivalence = []

    for y in range(0, img_height + 2):
        for x in range(0, img_width + 2):
            if (p[x][y] == 0):
                t = p[x-1][y]
                r = p[x][y-1]

                # Create a new label when r=t=1
                if (r == 1 and t == 1):
                    p_label[x][y] = label
                    label += 1

                # When r=t=0, use one of the labels and set equivalence
                elif (r == 0 and t == 0):
                    # If one of the labels is 0, change it to avoid mess with background
                    if (p_label[x-1][y] * p_label[x][y-1] == 0):
                        p_label[x-1][y] = p_label[x-1][y] + p_label[x][y-1]
                        p_label[x][y-1] = p_label[x-1][y] + p_label[x][y-1]

                    # If labels are different, append the labels to the equivalence list
                    if(p_label[x-1][y] != p_label[x][y-1]):
                        append_equivalence(
                            equivalence, [p_label[x-1][y], p_label[x][y-1]])
                    p_label[x][y] = p_label[x-1][y]

                # When r or t is 0, set this label to the current pixel
                elif (r == 0 and t == 1):
                    p_label[x][y] = p_label[x][y-1]
                else:
                    p_label[x][y] = p_label[x-1][y]

    # Replace equivalent labels
    for x in range(0, np.shape(p_label)[0]):
        for y in range(0, np.shape(p_label)[1]):
            if (p[x][y] != 1):
                p_label = replace_equivalence(equivalence, p_label, x, y)

    # Rearrange labels
    for x in range(0, np.shape(p_label)[0]):
        for y in range(0, np.shape(p_label)[1]):
            p_label[x][y] = mapping(equivalence, p_label[x][y])

    return p_label


#####################  Assignment 1: Could there be life?  #####################

image = cv2.imread(fileDir + '/data/spots.tiff', 0)
img_height = image.shape[0]
img_width = image.shape[1]

if (RUN == 1):  # Find microorganisms
    # Create binary matrix (1 for white and 0 for black)
    p = [[1 for x in range(img_height + 3)] for y in range(img_width + 3)]
    for x in range(3, img_height+3):
        for y in range(3, img_width+3):
            if (image[x-3][y-3] == 255):
                p[y][x] = 1
            else:
                p[y][x] = 0

    # Analyze pixels to define different labels for each microorganism
    p_label = labeling(p, img_height, img_width)
    img_plot('Microorganisms', p_label, IMAGE)
    np.savetxt(fileDir + '/data/microorganism.csv',
               p_label, delimiter=",", fmt='%s')

elif (RUN == 2):  # Find holes
    # Create negative binary matrix (0 for white and 1 for black)
    p2 = [[1 for x in range(img_height + 4)] for y in range(img_width + 4)]
    for x in range(3, img_height+3):
        for y in range(3, img_width+3):
            if (image[x-3][y-3] == 255):
                p2[y][x] = 0
            else:
                p2[y][x] = 1

    # Analyze pixels to define different labels for each hole
    p_label_hole = labeling(p2, img_height, img_width)
    img_plot('Holes', p_label_hole, IMAGE)

    np.savetxt(fileDir + '/data/holes.csv', p_label_hole, delimiter=",", fmt='%s')

else:  # Analyze neighborhood
    p_label = genfromtxt(fileDir + '/data/microorganism.csv', delimiter=',')
    p_label_hole = genfromtxt(fileDir + '/data/holes.csv', delimiter=',')
    img_height = p_label.shape[0]
    img_width = p_label.shape[1]

    # Get the number of total microorganisms on the picture (both types)
    label = 0
    for x in range(1, img_height):
        for y in range(1, img_width):
            if(p_label[x][y] > label):
                label = p_label[x][y]

    label = [0] * int(label + 1)
    label[1] = 2  # Background label

    # Associate the holes (containing labels different than the background one) with the microorganisms labels (analyzing neighborhood)
    for x in range(1, img_height):
        for y in range(1, img_width):
            if (p_label_hole[x][y] != 4 and p_label_hole[x][y] != 5 and p_label_hole[x][y] != 1):
                if(p_label[x-1][y-1] != 1):
                    label[int(p_label[x-1][y-1])] = 1

    type = [0, 0]
    # Give one label for each type of microorganism and plot final image
    for x in range(1, img_height):
        for y in range(1, img_width):
            p_label[x][y] = label[int(p_label[x][y])]

    for i in range(2, np.shape(label)[0]):
        if (label[i] == 1):
            type[0] += 1
        else:
            type[1] += 1

    print ("Numero de bacterias do tipo 1: ", type[0])
    print ("Numero de bacterias do tipo 2: ", type[1])

    img_plot('Microorganisms', p_label, IMAGE)
plt.show()
