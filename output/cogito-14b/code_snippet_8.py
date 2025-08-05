if __name__ == '__main__':
    # Check initial balance and get missing counts
    dict_change, balanced = check_dataset_balance()
    
    if not balanced:
        print("Dataset is imbalanced. Proceeding with augmentation...")
        augment_cropped_images(target_size=300)
        
        # Verify the new balance after augmentation
        new_dict_change, new_balanced = check_dataset_balance()
        
        if new_balanced:
            print("Successfully balanced dataset!")
        else:
            print("Dataset still needs more images.")