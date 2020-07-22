import json
import copy
from openpyxl import Workbook
from collections import OrderedDict
import pprint

data_json_path = 'C:\\Users\\ksh04\\PythonProjects\\DataManufacture\\datacollect.json'
categories_json_path = 'C:\\Users\\ksh04\\PythonProjects\\DataManufacture\\categories.json'
# CELL_DATE = 1
CELL_LAST_USED = 6
CELL_PACKAGE_NAME = 5
CELL_TOTAL_TIME_IN_FOREGROUND = 4
CELL_TIMESTAMPS = 2
CELL_USER_NAME = 1
CELL_CATEGORY = 3
PADDING_STATE = 0
MAX_CATEGORIES_BY_COROUTINE = 5

categories_dict = {}

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

non_categorizable = set([])

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

#Json Parsing code
with open(data_json_path, encoding= 'UTF-8') as json_file:
    usersData = json.load(json_file)
    users = usersData['user']


    idx = 0
    jsonData = dict()
    #appending each user data
    for user_name in users:
        jsonData[user_name] = {}
        for property in users[user_name]:
            
            if property == 'usagestatsCoroutine':
                for coroutines in users[user_name][property]:
                    jsonData[user_name][coroutines] = {}
                    idx = 0
                    for coroutine_attr in users[user_name][property][coroutines]:
                        # if coroutine_attr == 'date':
                        #     sheet1.cell(idx, CELL_DATE).value = users[user_name][property][coroutines][coroutine_attr]
                        
                        
                        if coroutine_attr == 'timestamp':
                            jsonData[user_name][coroutines]['timestamp'] = int((int(users[user_name][property][coroutines][coroutine_attr])/1000))
                        if coroutine_attr == 'statsList': # each app
                            start_idx = idx
                            for element in users[user_name][property][coroutines][coroutine_attr]:
                                #case1 코루틴의 statsList 개수가 5개가 이상일 경우
                                uncategorizable = False
                                for stat_attr in element: 
                                    # if stat_attr == 'lastTimeUsed':
                                    #     sheet1.cell(idx, CELL_LAST_USED).value = element[stat_attr]
                                    
                                    if stat_attr == 'packageName':
                                        jsonData[user_name][coroutines][str(idx)]={}
                                        # jsonData[user_name][coroutines][str(index)]['packageName'] =  element[stat_attr]
                                        if element[stat_attr] in categories_dict.keys():
                                            #Integer로 Mapping한 카테고리 dictionary 내에 값이 있는지 확인.
                                            category_value = categories_dict[element[stat_attr]]
                                            category_label = 0
                                            if category_value == CAMERA_STRING:
                                                category_label = 1
                                            elif category_value in UTILITY_ARRAY:
                                                category_label = 2
                                            elif category_value == SNS_STRING:
                                                category_label = 3
                                            elif category_value in ENTERTAINMENT_ARRAY:
                                                category_label = 4
                                            elif category_value == COMMUNICATION_STRING:
                                                category_label = 5
                                            elif category_value in GAME_ARRAY:
                                                category_label = 6
                                            elif category_value == SYSTEM_STRING:
                                                category_label = 7
                                            elif category_value in EDUCATION_ARRAY:
                                                category_label = 8
                                            elif category_value == SHOPPING_STRING:
                                                category_label = 9
                                            elif category_value in MAPS_VEHICLE_ARRAY:
                                                category_label = 10
                                            elif category_value == HEALTH_STRING:
                                                category_label = 11
                                            elif category_value == FOOD_STRING:
                                                category_label = 12
                                            elif category_value == FINANCE_STRING:
                                                category_label = 13
                                            elif category_value == BROWSER_STRING:
                                                category_label = 14
                                            
                                            jsonData[user_name][coroutines][str(idx)]['category'] =  category_label

                                        else:
                                            #Play store에 없는 APP의 경우.
                                            uncategorizable = True
                                            non_categorizable.add(element[stat_attr])
                                            continue

                                        
                                    if stat_attr == 'totalTimeInForeground':
                                        if not uncategorizable:
                                            jsonData[user_name][coroutines][str(idx)]['totalTimeInForeground'] = element[stat_attr]
                                            idx += 1
                                    if idx >= MAX_CATEGORIES_BY_COROUTINE:
                                        break
                                    
                                    
            
                            #case2 코루틴의 statsList 개수가 5개 미만일 경우
                            if idx < MAX_CATEGORIES_BY_COROUTINE:
                                for i in range(MAX_CATEGORIES_BY_COROUTINE - idx):
                                    jsonData[user_name][coroutines][str(idx)] = 0
                                    idx += 1
                                    if idx >= MAX_CATEGORIES_BY_COROUTINE: break

                            if idx == 0:#statslist가 없으면
                                for i in range(5):
                                    jsonData[user_name][coroutines][str(i)] = 0
                                    

    pp = pprint.PrettyPrinter(width=41, compact=True)
    # pp.pprint(jsonData)


    for user in jsonData:
        for eachCoroutine in jsonData[user]:
            print(user)
            print(eachCoroutine)
            if '0' and '4' in jsonData[user][eachCoroutine]:
                print(jsonData[user][eachCoroutine]['0'])
                print(jsonData[user][eachCoroutine]['4'])
                jsonData[user][eachCoroutine]['0'],jsonData[user][eachCoroutine]['4'] = jsonData[user][eachCoroutine]['4'],jsonData[user][eachCoroutine]['0']
                jsonData[user][eachCoroutine]['1'],jsonData[user][eachCoroutine]['3'] = jsonData[user][eachCoroutine]['3'],jsonData[user][eachCoroutine]['1']
                print(jsonData[user][eachCoroutine]['4'])
                print(jsonData[user][eachCoroutine]['0'])
                # for eachApp in eachCoroutine:

                #     if eachApp == '0':

                #         category_temp = eachApp['category']
                #         total_temp = eachApp['totalTimeInForeground']
                #         jsonData[user][eachApp]['category'] = jsonData[user]['4']['category']
                #         jsonData[user][eachApp]['totalTimeInForeground'] = jsonData[user]['4']['totalTimeInForeground']
                #         jsonData[user]['4']['category'] = category_temp
                #         jsonData[user][['4']]['totalTimeInForeground'] = total_temp

    
    file_path = "C:\\Users\\ksh04\\PythonProjects\\DataManufacture\\appstats.json"
    with open(file_path, 'w') as outfile:
        json.dump(jsonData, outfile)

# print(categories_dict)



