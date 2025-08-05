import os
from PIL import Image
from collections import defaultdict

# Konfigurasjonsvariabler
OUTPUT_PATH = 'out_data/'
TARGET_COUNT = 300  # Antall bilder ønsket i hver kategori

def check_dataset_balance(output_path=OUTPUT_PATH):
    """Teller antall bilder i hver PLU-kode og returnerer overskud/manglende bilder"""
    plu_counts = defaultdict(int)
    
    for filename in os.listdir(output_path):
        if filename.endswith('.png'):
            # Finner PLU-koden (antatt å være først i filnavnet før ett '_')
            parts = filename.split('_')
            plu_code = parts[0]
            plu_counts[plu_code] += 1
            
    missing_dict = {}
    max_count = TARGET_COUNT
    is_balanced = True
    
    for plu, count in plu_counts.items():
        missing = max_count - count
        missing_dict[plu] = missing
        if missing > 0:
            is_balanced = False
            
    return dict(missing_dict), is_balanced

def augment_cropped_images(output_path=OUTPUT_PATH):
    """Augmenterer bilder for PLU-koder som har færre enn TARGET_COUNT bilder"""
    
    # Teller antall bilder i hver PLU-kode
    plu_counts = defaultdict(int)
    missing_info, _ = check_dataset_balance()
    
    for filename in os.listdir(output_path):
        if filename.endswith('.png'):
            parts = filename.split('_')
            plu_code = parts[0]
            plu_counts[plu_code] += 1
    
    # Gjennomgår PLU-koder som har færre enn TARGET_COUNT bilder
    for plu, current_count in plu_counts.items():
        if current_count < TARGET_COUNT:
            folder_path = os.path.join(output_path, plu)
            
            # Teller totalt antall bilder i kategorien
            all_png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
            if len(all_png_files) >= TARGET_COUNT:
                continue
                
            remaining = TARGET_COUNT - current_count
            
            cropped_files = [f for f in os.listdir(folder_path) 
                            if f.endswith('_cropped.png') and remaining > 0]
            
            for cropped_file in cropped_files[:remaining]:
                base_name = cropped_file.replace('_cropped.png', '')
                
                try:
                    img = Image.open(os.path.join(folder_path, cropped_file))
                    
                    # Rotasjoner
                    for angle in [90, 180, 270]:
                        rotated_img = img.rotate(angle, expand=True)
                        save_path = os.path.join(folder_path, f"{base_name}_aug_rot{angle}.png")
                        rotated_img.save(save_path)
                        
                    # Vertikal flip
                    flipped_v = img.transpose(Image.FLIP_TOP_BOTTOM)
                    save_path = os.path.join(folder_path, f"{base_name}_aug_flipV.png")
                    flipped_v.save(save_path)
                    
                    # Horisontal flip + rotasjon
                    flipped_h = img.transpose(Image.FLIP_LEFT_RIGHT)
                    flipped_h_rotated = flipped_h.rotate(90, expand=True)
                    save_path = os.path.join(folder_path, f"{base_name}_aug_flipH_rot90.png")
                    flipped_h_rotated.save(save_path)
                    
                except Exception as e:
                    print(f"Feil ved augmentering av {cropped_file}: {e}")
    
    # Printer hvilke PLU-koder som mangler bilder
    missing_info, _ = check_dataset_balance()
    if not all(count == 0 for count in missing_info.values()):
        print("\nManglende bilder i følgende PLU-koder:")
        for plu, missing in sorted(missing_info.items(), key=lambda x: -x[1]):
            print(f"{plu}: {missing} manglende")
    else:
        print("\nDatasettet er nå balansert!")

if __name__ == '__main__':
    augment_cropped_images()