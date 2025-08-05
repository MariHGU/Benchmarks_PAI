if __name__ == '__main__':
    missing_dict, balanced = check_dataset_balance(output_path=OUTPUT_PATH)
    if not balanced:
        print("Dataset is imbalanced. Starting augmentation.")
        for category in missing_dict:
            if missing_dict[category] > 0:
                # Remove previously generated images to avoid duplication
                remove_augmented_images(output_path=OUTPUT_PATH, folder=category)
        print("Starting augmentation.")
        augment_cropped_images(missing_dict, output_path=OUTPUT_PATH, num_folders=NUM_FOLDERS, num_files_per_folder=NUM_FILES_PER_FOLDER)