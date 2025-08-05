import os
import image_dict

output_path = 'out_data/'
num_folders = None  # Set to None to process all folders or a specific number (e.g., 5)
num_files_per_folder = None  # Set to None to process all cropped images per folder or a specific number (e.g., 5)
num_augmentations = 4  # Number of augmentations to apply for each image

if __name__ == '__main__':
    balance_data(output_path=output_path, num_folders=num_folders, num_files_per_folder=num_files_per_folder)
    image_dict = image_dict.get_image_dict()  # Replace this line with import if needed
    add_augmented_images(image_dict, num_augmentations=num_augmentations)