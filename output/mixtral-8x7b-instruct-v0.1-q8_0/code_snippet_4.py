def add_augmented_images(image_dict, num_augmentations=4):
    for plu_code, image_files in image_dict.items():
        if len(image_files) < 300:
            missing = 300 - len(image_files)
            target = min(missing, num_augmentations * len(image_files))
            for i, img_path in enumerate(image_files):
                if (i + len(image_files)) > target:
                    break
                filename = os.path.basename(img_path)
                folder = os.path.dirname(img_path)
                img = Image.open(img_path).convert('RGB')

                # --- Augmentations ---
                augmented_files = []
                for _ in range(num_augmentations):
                    # 1. Rotations (90°, 180°, 270°)
                    for angle in [90, 180, 270]:
                        rotated_img = img.rotate(angle, expand=True).convert('RGB')
                        new_filename = f"{os.path.splitext(filename)[0]}_rot{angle}.png"
                        augmented_files.append(new_filename)

                    # 2. Horizontal Flip
                    flipped_h = img.transpose(Image.FLIP_LEFT_RIGHT).convert('RGB')
                    new_filename = f"{os.path.splitext(filename)[0]}_flipH.png"
                    augmented_files.append(new_filename)

                    # 3. Vertical Flip
                    flipped_v = img.transpose(Image.FLIP_TOP_BOTTOM).convert('RGB')
                    new_filename = f"{os.path.splitext(filename)[0]}_flipV.png"
                    augmented_files.append(new_filename)

                # Save the augmented files to the same folder
                for filename in augmented_files:
                    new_file_path = os.path.join(folder, filename)
                    if new_file_path not in image_files:
                        img.save(new_file_path)
                        image_dict[plu_code].append(new_file_path)