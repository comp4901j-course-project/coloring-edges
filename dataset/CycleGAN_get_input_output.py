import os
import numpy as np
import cv2
from shutil import copyfile

def make_square(image):
    height, width = image.shape[0], image.shape[1]
    size = max(height, width)
    top = bottom = int((size - height) / 2)
    left = right = int((size - width) / 2)
    if height % 2 == 1:
        bottom += 1
    if width % 2 == 1:
        right += 1
    new_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value = [255, 255, 255])
    return new_image

def crop(image, margin = 5):
    height, width = image.shape[0], image.shape[1]
    new_height = height - 2 * margin
    new_width = width - 2 * margin
    return image[margin:new_height, margin:new_width]

# get the directory paths
cwd = os.getcwd()
path_imgs = cwd + "/leedsbutterfly/images"
path_segs = cwd + "/leedsbutterfly/segmentations"
path_input_edge = cwd + "/CycleGAN_input_edge"
path_input_grayscale = cwd + "/CycleGAN_input_grayscale"
path_output = cwd + "/CycleGAN_output"

# path for trainA & trainB & testA & testB
path_input_edge_trainA = cwd + "/CycleGAN_input_edge/trainA"
path_input_edge_testA = cwd + "/CycleGAN_input_edge/testA"

path_input_grayscale_trainA = cwd + "/CycleGAN_input_grayscale/trainA"
path_input_grayscale_testA = cwd + "/CycleGAN_input_grayscale/testA"

path_output_trainB = cwd + "/CycleGAN_output/trainB"
path_output_testB = cwd + "/CycleGAN_output/testB"

# create input and output directory
try:  
    os.mkdir(path_input_edge)
except OSError:  
    print ("Creation of the directory %s failed" % path_input_edge)
else:  
    print ("Successfully created the directory %s" % path_input_edge)

try:  
    os.mkdir(path_input_grayscale)
except OSError:  
    print ("Creation of the directory %s failed" % path_input_grayscale)
else:  
    print ("Successfully created the directory %s" % path_input_grayscale)

try:  
    os.mkdir(path_output)
except OSError:  
    print ("Creation of the directory %s failed" % path_output)
else:  
    print ("Successfully created the directory %s" % path_output)

# create directory for trainA & trainB & testA & testB
try:  
    os.mkdir(path_input_edge_trainA)
    os.mkdir(path_input_edge_testA)
    os.mkdir(path_input_grayscale_trainA)
    os.mkdir(path_input_grayscale_testA)
    os.mkdir(path_output_trainB)
    os.mkdir(path_output_testB)
except OSError:  
    print ("Creation of the trainA & trainB & testA & testB directory failed")
else:  
    print ("Successfully created the trainA & trainB & testA & testB directory")


# Original Dimensions for train
N = 832
image_width = 256
image_height = 256
channels = 3
dimension = (image_width, image_height)

i = 0

X = np.ndarray(shape = (N, image_height, image_width), dtype = np.float32)
Y = np.ndarray(shape = (N, image_height, image_width, channels), dtype = np.float32)

for filename in sorted(os.listdir(path_imgs)):
    if filename.endswith(".png"):
        image1 = cv2.imread(path_imgs + "/" + filename, cv2.IMREAD_UNCHANGED)
        mask1 = cv2.imread(path_segs + "/" + filename.split(".")[0] + "_seg0.png", cv2.IMREAD_UNCHANGED)
        mask2 = np.ndarray.copy(mask1)
        mask1[mask1 == 255] = 1 # get the butterfly
        mask2[mask2 == 0] = 1 # get the background
        mask2[mask2 == 255] = 0
        image = make_square(crop(image1 * mask1 + mask2 * 255))
        image = cv2.resize(image, dimension, interpolation = cv2.INTER_NEAREST)

        image_input_edge = 255 - cv2.Canny(image, 100, 200)
        image_input_edge = np.repeat(image_input_edge.reshape(image_height, image_width, 1), 3, axis = 2)
        image_input_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_input_grayscale = np.repeat(image_input_grayscale.reshape(image_height, image_width, 1), 3, axis = 2)
        image_output = image
        # cv2.imwrite(path_input_edge + "/" + filename.split(".")[0] + ".png", image_input_edge)
        # cv2.imwrite(path_output + "/" + filename.split(".")[0] + ".png", image_output)
        if i < 586:
            cv2.imwrite(path_input_edge_trainA + "/" + filename.split(".")[0] + ".png", image_input_edge)
            cv2.imwrite(path_input_grayscale_trainA + "/" + filename.split(".")[0] + ".png", image_input_grayscale)
            cv2.imwrite(path_output_trainB + "/" + filename.split(".")[0] + ".png", image_output)
        else:
            cv2.imwrite(path_input_edge_testA + "/" + filename.split(".")[0] + ".png", image_input_edge)
            cv2.imwrite(path_input_grayscale_testA + "/" + filename.split(".")[0] + ".png", image_input_grayscale)
            cv2.imwrite(path_output_testB + "/" + filename.split(".")[0] + ".png", image_output)
         
        i += 1
        
        # print out messages
        if i % 100 == 0:
            print(str(i) + " images are done!")
        if i == 586:
            print("train set is done!")
        elif i == 832:
            print("test set is done ")
    else:
        continue
        
print(str(N) + " images are done!")