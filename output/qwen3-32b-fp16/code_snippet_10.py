import os
from PIL import Image
import numpy as np
from scipy.ndimage import rotate as nd_rotate
from copy import deepcopy

# Define the target number of images per class
TARGET_IMAGES = 300

# Define the root directory of your dataset
DATASET_DIR = 'path/to/your/dataset'

# Define augmentation functions
def rotate(image_array, angle):
    """Rotate an image by the specified angle (in degrees)."""
    return nd_rotate(image_array, angle, reshape=False, mode='reflect')

def flip(image_array):
    """Flip an image horizontally."""
    return np.fliplr(image_array)

def load_image(image_path):
    """Load an image and convert it to a NumPy array."""
    with Image.open(image_path) as img:
        return np.array(img)

def save_image(array, save_path):
    """Convert a NumPy array to an image and save it."""
    Image.fromarray(array).save(save_path)

def augment_and_save(image_array, base_name, class_dir, required):
    """Apply augmentations and save the resulting images until `required` reaches zero."""
    if required <= 0:
        return 0

    # Generate unique filename for each augmentation
    def save_augmentation(img, suffix):
        nonlocal required
        if required <= 0:
            return
        filename = f"{base_name}_{suffix}.png"
        save_path = os.path.join(class_dir, filename)
        save_image(img, save_path)
        required -= 1

    # Apply augmentations one by one
    if required > 0:
        rotated_90 = rotate(image_array, 90)
        save_augmentation(rotated_90, "rot90")
    if required > 0:
        rotated_180 = rotate(image_array, 180)
        save_augmentation(rotated_180, "rot180")
    if required > 0:
        rotated_270 = rotate(image_array, 270)
        save_augmentation(rotated_270, "rot270")
    if required > 0:
        flipped = flip(image_array)
        save_augmentation(flipped, "flip")

    return required

# Main processing loop
for class_name in os.listdir(DATASET_DIR):
    class_dir = os.path.join(DATASET_DIR, class_name)

    if not os.path.isdir(class_dir):
        continue

    # Count current images
    existing_files = [f for f in os.listdir(class_dir) if f.endswith('.png')]
    current_count = len(existing_files)

    if current_count >= TARGET_IMAGES:
        print(f"Class '{class_name}' already has {current_count} images. Skipping.")
        continue

    required = TARGET_IMAGES - current_count
    print(f"Processing class '{class_name}' - Need {required} more images.")

    # Get list of original images (assumed to be in the class directory)
    original_files = [f for f in os.listdir(class_dir) if f.endswith('.png') and not any(a in f for a in ['rot', 'flip'])]
    original_paths = [os.path.join(class_dir, f) for f in original_files]

    for image_path in original_paths:
        if required <= 0:
            break

        base_name = os.path.splitext(os.path.basename(image_path))[0]
        image_array = load_image(image_path)
        required = augment_and_save(image_array, base_name, class_dir, required)

    # After processing all original images, check if we still need more
    if required > 0:
        print(f"Class '{class_name}' still needs {required} more images. Consider adding more original images.")