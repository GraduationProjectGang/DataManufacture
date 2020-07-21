import json
import time
# from openpyxl import Workbook

jsonPath = 'C:\\Users\\sejin\\Desktop\\졸프\\data_set.json'

with open(jsonPath, encoding= 'UTF-8') as json_file:
    usersData = json.load(json_file)
    users = usersData['user']

    # wb = Workbook()
    # sheet1 = wb.active
    # sheet1.title = 'untitled'
    # idx = 1

    # for userName in users:
    #     for property in users[userName]:
    #         if property == 'userName':
    #             sheet1.cell(row=idx, column=1).value = users[userName][property]
    #             print(users[userName][property])
    #         if property == 'userSignInTime':
    #             t = float(users[userName][property])
    #             tm = time.localtime(t/1000)
    #             string = time.strftime('%Y-%m-%d %I:%M:%S %p', tm)
    #             print(string)
    #             sheet1.cell(row=idx, column=2).value = string
    #             idx = idx + 1


    # wb.save(filename= 'data.xlsx')

    appCollection = set([])

    for userKey in users:
        for usageStats in users[userKey]:
            if usageStats == 'usagestatsStress':
                for usageStatsKey in users[userKey][usageStats]:
                    for usageStatsInfo in users[userKey][usageStats][usageStatsKey]:
                        if usageStatsInfo == 'statsList':
                            for AppIndex in users[userKey][usageStats][usageStatsKey][usageStatsInfo]:
                                tempset = set(AppIndex['packageName'])
                                if appCollection.issuperset(tempset):
                                    print(1)
                                else:
                                    appCollection.add(AppIndex['packageName'])
                                    
                                # for PackageName in users[userKey][usageStats][usageStatsKey][usageStatsInfo][AppIndex][property]:
                                #     if PackageName == 'packageName':
                                #         appCollection.add(users[userKey][usageStats][usageStatsKey][usageStatsInfo][AppIndex][property][PackageName][property])

    print(appCollection)

