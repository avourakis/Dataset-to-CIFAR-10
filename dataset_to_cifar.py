''' Image dataset processing (IDP) for machine learning '''

import serialization as serial
import io
from PIL import Image
import numpy as np
import os

__author__ = "Andres Vourakis"
__email__ = "andresvourakis@gmail.com"
__license__ = "GPL"
__data__ = "May 25, 2017"


def image_to_byte_array(image, class_index, size):

    img = Image.open(image)
    
    #Resize
    img = img.resize(size) #TODO Check if resizing to given dim can be done

    #Convert image to 3 dimensional array
    img_array = np.array(img)

    #Convert 3 dimensional array into row major order
    img_array_R = img_array[:,:,0].flatten()
    img_array_G = img_array[:,:,1].flatten()
    img_array_B = img_array[:,:,2].flatten()
    class_index = [class_index]

    # Turn row-major array into bytes
    #img_byte_array = np.concatenate((img_array_R, img_array_G, img_array_B)).tobytes() #Turn into row-major byte array
    img_byte_array = np.array(list(class_index) + list(img_array_R) + list(img_array_G) + list(img_array_B), np.uint8) #Turn into row-major byte array
    
    return img_byte_array

def create_meta_data(class_labels, destination):
    
    '''
        TODO: Check if directory exists
    '''
    
    file_name = 'batches_meta.txt'
    file_path = os.path.join(destination, file_name)
    with open(file_path, 'w') as file:
        for label in class_labels:
            file.write(str(label) + '\n')


def label_to_index(class_labels, class_label):
    return class_labels.index(class_label)

def open_batch(destination):
    file_name = 'data_batch_' + str(CURRENT_BATCH) + '.bin'
    file_path = os.path.join(destination, file_name)
    return open(file_path, 'wb')

def close_batch(file):
    file.close()

def process_image_dataset(source, destination, size = (32, 32), batch = 1):
    """ 
        Processes dataset into binary version of CIFAR-10 dataset

    Args:
        source: Abosulute path to directory containing subdirectories of image datasets.
        destination: Absolute path of directory where to save process image datasets.
        size (default = (32,32)): square dimensions (width and height) to resize images
        batch (default = 1): Number of batches to divide image dataset.
        
    """

    class_labels = next(os.walk(source))[1]
    #dataset_size = len(next(os.walk(source))[2]) #Only gives tot number of files in current directory

    dataset_size = 0

    for root, subdirs, files in os.walk(source):
        dataset_size += len(files) #TODO: Find more efficient way of getting tot num of files
    
   
    batch_size = dataset_size / batch # Total number of images per batch
    REACHED_BATCH_MAX = False
    CURRENT_BATCH = 1

    #create meta data file
    create_meta_data(class_labels, destination) #TODO: Check time complex. 
    batch = open_batch(destination)

    #load data and output data
    for root, subdirs, files in os.walk(source):

        class_label = os.path.relpath(root, source) 

        if(class_label != '.'): # Ignore source directory

            class_index = label_to_index(class_labels, class_label) # class index in bytes
             
            #data = np.array([image_to_byte_array(os.path.join(root, file), size) for file in files]) #Turn images to numpy array and save into data array
            for counter, file in enumerate(files):
                
                if(REACHED_BATCH_MAX):
                    #open new batch and increment CURRENT_BATCH
                    CURRENT_BATCH += 1
                    batch = open_batch(destination)
    
                file_path = os.path.join(root, file)
                image_byte_array = image_to_byte_array(file_path, class_index, size)
                
                #write to file while max batch size hasnt been reached!
                batch.write(image_byte_array)
                
                if(counter == batch_size):
                    #close current batch and set REACHED_MAX_BATCH to TRUE
                    close_batch(batch)
                    REACHED_BATCH_MAX = True
                        

    close_batch(batch) 

