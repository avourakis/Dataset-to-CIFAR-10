from dataset_to_cifar import process_dataset


# Set square dimensions of images
size = (32,32) # 32 by 32 pixels

# Set number of batches
batch = 1

# Source of image dataset (Use absolute path)
source = '/'

# Destination of processed dataset (use absolute path)
destination = '/'

# Process dataset
process_dataset(source, destination, size, batch)
