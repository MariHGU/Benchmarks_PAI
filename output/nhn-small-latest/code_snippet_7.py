import os
from PIL import Image
from collections import defaultdict

def augment_cropped_images(output_path='out_data/', num_folders=None, num_files_per_folder=None):
    """ Augmenter bilder for PLU-koder som har færre enn 300 bilder """
    
    def count_png_files(folder_path):
        return len([f for f in os.listdir(folder_path) if f.endswith('.png')])
    
    def augment_image(img, base_name, folder_path):
        # Rotasjoner
        angles = [90, 180, 270]
        for angle in angles:
            rotated_img = img.rotate(angle, expand=True)
            save_path = os.path.join(folder_path, f"{base_name}_rot{angle}.png")
            rotated_img.save(save_path)
            
        # Flip
        flipped_h = img.transpose(Image.FLIP_LEFT_RIGHT)
        save_path = os.path.join(folder_path, f"{base_name}_flipH.png")
        flipped_h.save(save_path)
        
        flipped_v = img.transpose(Image.FLIP_TOP_BOTTOM)
        save_path = os.path.join(folder_path, f"{base_name}_flipV.png")
        flipped_v.save(save_path)

    all_folders = [f for f in sorted(os.listdir(output_path)) if os.path.isdir(os.path.join(output_path, f))]
    
    # Begrens antall mapper
    if num_folders is not None:
        all_folders = all_folders[:num_folders]

    target_count = 300
    for folder in all_folders:
        folder_path = os.path.join(output_path, folder)
        
        current_count = count_png_files(folder_path)
        images_to_create = max(0, target_count - current_count)
        
        if images_to_create > 0:
            print(f"Processing {folder} to add {images_to_create} augmented images")
            
            # Begrens antall bilder som skal augmenteres
            if num_files_per_folder is not None:
                files = [f for f in os.listdir(folder_path) 
                        if f.endswith('.png') and '_cropped' not in f][:num_files_per_folder]
            else:
                files = [f for f in os.listdir(folder_path) 
                        if f.endswith('.png') and '_cropped' not in f]

            augmented_count = 0
            while augmented_count < images_to_create and files:
                file_name = files.pop(0)
                base_name, _ = os.path.splitext(file_name)

                try:
                    img = Image.open(os.path.join(folder_path, file_name))
                    augment_image(img, base_name, folder_path)
                    augmented_count += 4  # Hver original gir 3 augmenterte bilder
                
                    if augmented_count >= images_to_create:
                        break
                except Exception as e:
                    print(f"Could not process {file_name}: {e}")

def check_dataset_balance(output_path='out_data/'):
    """ Sjekker om datasettet er balansert """
    
    category_counts = defaultdict(int)
    
    for folder in os.listdir(output_path):
        if not os.path.isdir(os.path.join(output_path, folder)):
            continue
            
        png_files = [f for f in os.listdir(os.path.join(output_path, folder)) 
                    if f.endswith('.png')]
        
        # Finner PLU-kode (antatt å være første del av filnavnet)
        plu_code = folder.split('_')[0]
        category_counts[plu_code] += len(png_files)

    target_count = max(category_counts.values())
    
    missing_dict = {}
    is_balanced = True
    
    for category, count in sorted(category_counts.items()):
        missing = target_count - count
        if missing > 0:
            missing_dict[category] = missing
            is_balanced = False
            
    return missing_dict, is_balanced

if __name__ == '__main__':
    # Sjekk balansen først
    print("Checking dataset balance...")
    missing_files, is_balanced = check_dataset_balance()
    
    if not is_balanced:
        print(f"Datasett er ikke balansert. {len(missing_files)} kategorier har bilder manglende.")
        
        # Augmenter bilder for ulike PLU-koder
        augment_cropped_images(num_folders=None, num_files_per_folder=5)
        
        # Sjekk om datasettet nå er balansert
        missing_files_after, is_balanced_after = check_dataset_balance()
        print(f"\nDatasett etter augmentation:")
        if is_balanced_after:
            print("Balansert!")
        else:
            print(f"Stillingsjusteringer fortsatt nødvendige: {missing_files_after}")
    else:
        print("Datasettet er allerede balansert!")