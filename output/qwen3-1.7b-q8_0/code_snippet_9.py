def augment_cropped_images(folder_path, num_augmentations_per_image=2):
    """
    Generate augmented images for a folder to reach around 300 images.
    
    Args:
        folder_path: Path to the folder containing the images.
        num_augmentations_per_image: Number of augmentations to generate per image.
    """
    # Ensure the folder has enough images to begin with
    current_images = len(os.listdir(folder_path))
    
    # Calculate how many more images are needed to reach 300
    needed = 300 - current_images
    
    # Generate the required number of augmentations
    for _ in range(needed):
        # Generate a new augmented image
        new_image = generate_augmented_image(folder_path)
        os.rename(new_image, os.path.join(folder_path, f"{current_images}_augmented_{random.randint(1000, 9999)}.jpg"))
        current_images += 1