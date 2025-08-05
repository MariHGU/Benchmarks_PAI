def balance_data(output_path='out_data/', num_folders=None, num_files_per_folder=None):
    missing_dict, is_balanced = check_dataset_balance(output_path)
    
    if not is_balanced:
        augment_cropped_images(output_path, num_folders, num_files_per_folder)