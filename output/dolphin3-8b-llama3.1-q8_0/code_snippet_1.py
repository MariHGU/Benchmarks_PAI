def augment_cropped_images(output_path='out_data/', num_folders=None, num_files_per_folder=None):
    """...
    
    # ... previous code ...

    if len(total_png_files) < 300:  # If the folder has less than 300 files
        for cropped_file in cropped_files:
            ...
            # Generate augmentations and save them here...

            # Count the number of images after generating new ones
            total_png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    else:
        print(f"Skipping folder '{folder}' because it already has {len(total_png_files)} images.")