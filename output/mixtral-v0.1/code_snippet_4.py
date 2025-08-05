for folder in folders:
    ...
    for cropped_file in cropped_files:
        base_name = cropped_file.replace('_cropped.png', '')
        category = get_category(base_name)  # Assume this function returns the PLU number from the filename
        if missing_dict.get(category, 0) > 0:
            try:
                img = Image.open(image_path)
                ...