def augment_cropped_images(output_path='out_data/', target_size=300):
    """
    Balances the dataset by adding augmented images until each PLU code has at least 300 images.
    
    Args:
        output_path (str): Path to the output directory containing the categorized images
        target_size (int): Target number of images per category
    """
    # First, check current balance
    missing_dict, _ = check_dataset_balance(output_path)
    
    for plu_code, missing_count in missing_dict.items():
        if missing_count > 0:
            folder_path = os.path.join(output_path, plu_code)
            
            # Get all existing PNG files in the PLU code directory
            existing_files = [f for f in os.listdir(folder_path) 
                            if f.endswith('.png') and not f.startswith('_')]
            
            # Continue until we have enough images or run out of original images to augment
            while len(existing_files) < target_size:
                # Randomly select an image to augment (without _cropped suffix)
                import random
                
                existing_cropped = [f for f in existing_files 
                                  if not any(s in f for s in ['_flip', '_rot'])]
                
                if not existing_cropped:  # If no more images left, skip
                    break
                    
                image_to_augment = random.choice(existing_cropped)
                base_name = image_to_augment[:-len('_cropped.png')]
                image_path = os.path.join(folder_path, image_to_augment)

                try:
                    img = Image.open(image_path)
                except Exception as e:
                    print(f"⚠️ Failed to open image {image_path}: {e}")
                    continue

                # Perform augmentations
                for angle in [90, 180, 270]:
                    rotated_img = img.rotate(angle, expand=True)
                    rotated_save_path = os.path.join(folder_path, 
                                                    f"{base_name}_cropped_rot{angle}.png")
                    rotated_img.save(rotated_save_path)

                flipped_h = img.transpose(Image.FLIP_LEFT_RIGHT)
                flipped_h_save_path = os.path.join(folder_path, 
                                                  f"{base_name}_cropped_flipH.png")
                flipped_h.save(flipped_h_save_path)

                flipped_v = img.transpose(Image.FLIP_TOP_BOTTOM)
                flipped_v_save_path = os.path.join(folder_path, 
                                                  f"{base_name}_cropped_flipV.png")
                flipped_v.save(flipped_v_save_path)

                # Update the list of existing files (including augmented ones)
                existing_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

            print(f"Completed augmentation for PLU {plu_code}: "
                  f"{len(existing_files)} images")