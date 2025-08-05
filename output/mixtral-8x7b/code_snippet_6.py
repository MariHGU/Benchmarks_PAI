if __name__ == '__main__':
    dict_change, balanced = check_dataset_balance(output_path=OUTPUT_PATH)
    if augment_cropped_images(output_path=OUTPUT_PATH, num_folders=NUM_FOLDERS, num_files_per_folder=NUM_FILES_PER_FOLDER):
        print("Balancing completed.")