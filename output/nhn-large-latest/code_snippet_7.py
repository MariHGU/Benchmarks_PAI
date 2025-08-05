if __name__ == '__main__':
    # Sjekk balansen først
    missing_dict, is_balanced = check_dataset_balance(output_path=OUTPUT_PATH)
    
    if not is_balanced:
        print("Starting augmentation process...")
        augment_cropped_images(output_path=OUTPUT_PATH, target=300, num_folders=NUM_FOLDERS, num_files_per_folder=NUM_FILES_PER_FOLDER)
        print("Augmentation completed. New balance:")
        check_dataset_balance(output_path=OUTPUT_PATH)
    else:
        print("Dataset is already balanced with at least 300 images per category.")