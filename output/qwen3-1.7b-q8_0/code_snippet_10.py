def augment_cropped_images(folder_path, num_augmentations_per_image=2):
    """
    Generate augmented images for a folder to reach around 300 images.
    
    Args:
        folder_path: Path to the folder containing the images.
        num_augmentations_per_image: Number of augmentations to generate per image.
    """
    current_images = len(os.listdir(folder_path))
    needed = 300 - current_images
    
    for _ in range(needed):
        # Generate a new augmented image
        new_image = generate_augmented_image(folder_path)
        os.rename(new_image, os.path.join(folder_path, f"{current_images}_augmented_{random.randint(1000, 9999)}.jpg"))
        current_images += 1