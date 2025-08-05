def augment_cropped_images(output_path='out_data/', target=300, num_folders=None, num_files_per_folder=None):
       """
       Genererer augmenterte bilder til hver kategori har minst 'target' antall bilder.
       """
       all_items = os.listdir(output_path)
       folders = [f for f in sorted(all_items) if os.path.isdir(os.path.join(output_path, f))]
       
       if num_folders is not None:
           folders = folders[:num_folders]
           
       missing_dict, _ = check_dataset_balance(output_path=output_path)
       
       for folder in folders:
           folder_path = os.path.join(output_path, folder)
           current_count = len([f for f in os.listdir(folder_path) if f.endswith('.png')])
           
           if current_count >= target:
               print(f"Skipping folder '{folder}' - already has {current_count} images.")
               continue
               
           # Generer nødvendige augmenterte bilder
           cropped_files = [f for f in os.listdir(folder_path) if f.endswith('_cropped.png')]
           if num_files_per_folder is not None:
               cropped_files = cropped_files[:num_files_per_folder]
               
           for idx, cropped_file in enumerate(cropped_files):
               print(f"Processing {idx+1}/{len(cropped_files)}: {cropped_file}")
               base_name = cropped_file.replace('_cropped.png', '')
               image_path = os.path.join(folder_path, cropped_file)
               
               try:
                   img = Image.open(image_path)
                   
                   # Rotasjoner
                   for angle in [90, 180, 270]:
                       save_path = os.path.join(folder_path, f"{base_name}_rot{angle}.png")
                       if not os.path.exists(save_path):
                           rotated_img = img.rotate(angle, expand=True)
                           rotated_img.save(save_path)
                           
                   # Flip H og V
                   flipped_h = img.transpose(Image.FLIP_LEFT_RIGHT)
                   flipped_v = img.transpose(Image.FLIP_TOP_BOTTOM)
                   
                   flipped_h.save(os.path.join(folder_path, f"{base_name}_flipH.png"))
                   flipped_v.save(os.path.join(folder_path, f"{base_name}_flipV.png"))
                   
                   # Kombinert transformasjon
                   flipped_rotated = flipped_h.rotate(90, expand=True)
                   flipped_rotated.save(os.path.join(folder_path, f"{base_name}_flipHrot90.png"))
                   
               except Exception as e:
                   print(f"Error processing {cropped_file}: {e}")
               
               # Sjekk om vi har nådd target
               current_count = len([f for f in os.listdir(folder_path) if f.endswith('.png')])
               if current_count >= target:
                   break
           else:
               # Hvis vi ikke break'et, betyr det at vi ikke kunne generere nok bilder
               print(f"Could not reach target ({target}) for folder {folder}. Missing {target - current_count} images.")