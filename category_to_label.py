import json

categories_dict = {}

non_category_count = 0
CAMERA_STRING = 'Photography'
UTILITY_ARRAY = {'Productivity', 'Beauty', 'Weather', 'News & Magazines', 'Dating', 'Tools'}
SNS_STRING = 'Social'
ENTERTAINMENT_ARRAY = {'Entertainment', 'Books & Reference', 'Music & Audio', 'House & Home', 'Sports', 'Video Players & Editors', 'Travel & Local', 'Lifestyle', 'Comics'}
COMMUNICATION_STRING = 'Communication'
GAME_ARRAY = {'Action', 'Racing', 'Adventure', 'Arcade', 'Puzzle', 'Simulation', 'Strategy', 'Role Playing', 'Auto & Vehicles', 'Casual', 'Card', 'Music'}
SYSTEM_STRING = 'Personalization'
EDUCATION_ARRAY = {'Education', 'Business'}
SHOPPING_STRING = 'Shopping'
MAPS_VEHICLE_ARRAY = {'Maps & Navigation', 'Auto & Vehicles'}
HEALTH_STRING = 'Health & Fitness'
FOOD_STRING = 'Food & Drink'
FINANCE_STRING = {'Finance'}

#catergory의 이름(String)을 번호(Integer)로 Mapping하는 code
with open(categories_json_path, encoding= 'UTF-8') as json_file:
    categories_array = json.load(json_file)
    for app in categories_array:
        package_name = ''
        category = ''
        for app_attr in categories_array[app]:
            if app_attr == 'packageName':
                package_name = categories_array[app][app_attr]
            if app_attr == 'category':
                category = categories_array[app][app_attr]
        categories_dict[package_name] = category

    data[userKey].append({
        "posture": int(pos),
        "posture_accuracy": bincount_x[pos],
        "std_posture": float(std_x),
        "orientation": int(ori),
        "orientation_accuracy": bincount_y[ori],
        "std_orientation": float(std_y),
        "timestamp": timeStamp
    })