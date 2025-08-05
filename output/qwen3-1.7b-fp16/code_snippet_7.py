def process_images(folder):
    """Process all images in the folder and generate augmentations."""
    # Process each image in the folder
    for image in folder.images:
        generate_augmentation(image)

def augment_cropped_images(folder):
    """Augment all images in the folder until it reaches 300 images."""
    # Count the number of images already in the folder
    current_count = len(folder.images)

    # If the folder has less than 300 images, generate the remaining
    if current_count < 300:
        remaining = 300 - current_count
        for _ in range(remaining):
            process_images(folder)