def generate_and_save_augmented_image(img, folder_path, base_name):
    """Generates an augmented image by applying random transformations to the original image."""
    
    # Create an augmented image
    transforms = [
        lambda x: x.rotate(angle=random.uniform(-90, 90), resample=Image.BICUBIC, fillcolor=(255, 255, 255)) for _ in range(4)
    ]
    transforms += [
        lambda x: x.transpose(Image.FLIP_LEFT_RIGHT),
        lambda x: x.transpose(Image.FLIP_TOP_BOTTOM),
        lambda x: x.rotate(angle=random.uniform(-90, 90), resample=Image.BICUBIC, fillcolor=(255, 255, 255)).transpose(Image.FLIP_LEFT_RIGHT),
    ]
    random.shuffle(transforms)
    augmented_img = transforms[0](img.copy())
    
    # Save the augmented image with a unique filename
    while True:
        save_filename = f"{base_name}_augmented_{len(os.listdir(folder_path))}.png"
        if save_filename not in os.listdir(folder_path):
            save_path = os.path.join(folder_path, save_filename)
            augmented_img.save(save_path, format='PNG')
            return augmented_img, save_filename