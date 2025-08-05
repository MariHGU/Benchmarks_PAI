def check_dataset_balance(output_path=OUTPUT_PATH):
    """... (Same as before) ... """
    # Find the maximum image count among categories
    max_count = max(category_counts.values())
    # Build a dictionary of missing images per category
    missing_dict = {}
    is_balanced = True
    for category, count in sorted(category_counts.items()):
        if 300 - count > 0:
            missing = 300 - count
            missing_dict[category] = missing
            if missing > 0:
                is_balanced = False
    return missing_dict, is_balanced