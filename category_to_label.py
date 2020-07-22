import json

categories_dict = {}
categories_label = list([])
non_category_count = 0

non_category_list = list([])

categories_json_path = 'C:\\Users\\sejin\\Documents\\GitHub\\DataManufacture\\categories.json'
file_path = 'C:\\Users\\sejin\\Documents\\GitHub\\DataManufacture\\category_labels.json'

CAMERA_STRING = 'Photography'
UTILITY_ARRAY = {'Productivity', 'Beauty', 'Weather', 'News & Magazines', 'Dating', 'Tools', 'Utility'}
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
FINANCE_STRING = 'Finance'
BROWSER_STRING = 'Browser'

#catergory의 이름(String)을 번호(Integer)로 Mapping하는 code
with open(categories_json_path, encoding= 'UTF-8') as json_file:

    data = {}

    categories_array = json.load(json_file)
    for app in categories_array:
        package_name = ''
        category = ''
        category_label = 0
        for app_attr in categories_array[app]:
            if app_attr == 'packageName':
                package_name = categories_array[app][app_attr]
            if app_attr == 'category':
                category = categories_array[app][app_attr]
                if category == CAMERA_STRING:
                    category_label = 1
                elif category in UTILITY_ARRAY:
                    category_label = 2
                elif category == 'SNS_STRING':
                    category_label = 3
                elif category in ENTERTAINMENT_ARRAY:
                    category_label = 4
                elif category == COMMUNICATION_STRING:
                    category_label = 5
                elif category in GAME_ARRAY:
                    category_label = 6
                elif category == SYSTEM_STRING:
                    category_label = 7
                elif category in EDUCATION_ARRAY:
                    category_label = 8
                elif category == SHOPPING_STRING:
                    category_label = 9
                elif category == MAPS_VEHICLE_ARRAY:
                    category_label = 10
                elif category == HEALTH_STRING:
                    category_label = 11
                elif category == FOOD_STRING:
                    category_label = 12
                elif category == FINANCE_STRING:
                    category_label = 13
                elif category == BROWSER_STRING:
                    category_label = 14
                else:
                    non_category_count += 1
                    non_category_list.append(package_name)

        data[package_name] = []
        data[package_name].append({
            "category": category,
            "category_label": category_label
        })
    
    print(data)
    print(non_category_count)
    print(non_category_list)

    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)