#Created by Brooks Duggan at Simpson University on 9/2/2020
#Purpose: To ensure that course files tab in Canvas courses are not revealed to the students

import json
import requests
import time
#to measure how long it takes to execute
start_time = time.time()

#Initialize the Canvas POST request through the requests package, don't forget to initialize an API key also
headers = {'Authorization': 'Bearer ###'}  #***Replace the ### with your API Key

#Initialize Lists
courses_list = []
errors = []


#For loop to go through every user
for x in range(1, *): #Change the * to a small number (80) to start, and then utilize larger numbers as it begins to work
    try:        
        #create a PUT url to update individual courses x that the for loop is on
        url = "https://###.instructure.com/api/v1/courses/{}/tabs/files?hidden=1".format(x) #Replace the ### with your school
        
        #NOTE: The URL above can be changed to any of the tabs, except for Home & Settings, to be globally hidden
        
        #create PUT request to necessary url, to update the files tab to hidden
        r = requests.put(url, headers = headers)
        
        #Store Course information and PUSH request status code to a list
        if(r.status_code != 404):
            courses_list.append(["CourseID: ", x, r.status_code, r.text])
    except:
        pass
        
#create a txt file logged with all status codes
file1 = open("Course_Log_Canvas.txt","w+")
for stat in courses_list:
    file1.write("%s\n" % stat)
file1.write("Completed: " + str(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())))
file1.close()

#print status and timestamp in console
print("Course Links Tab Now Hidden!")
print("--- %s seconds ---" % (time.time() - start_time))