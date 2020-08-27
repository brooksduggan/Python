#Created by Brooks Duggan from Simpson University in August, 2020
#Purpose: To add a secondary login for all users within Canvas with one script.
#Reason for Creation: The SIS Import feature did not have a feature like this at the time.
#Please be sure to let me know if this helped or worked for you!

from canvasapi import Canvas
import json
import requests
import time
#to measure how long it takes to execute
start_time = time.time()

#Initialize the Canvas API Objects and pass t into the canvasapi package | starting on the TEST account, delete the .test to have production
API_URL = "https://###.test.instructure.com" #***Replace the ### with your School
API_KEY = "###" #***Replace the ### with the API Key
canvas = Canvas(API_URL, API_KEY)

#Initialize the Canvas POST request through the requests package, don't forget to initialize an API key also
url = "https://###.test.instructure.com/api/v1/accounts/1/logins/?user[id]={}&login[unique_id]={}" #***Replace the ### with your School
headers = {'Authorization': 'Bearer ###'}  #***Replace the ### with your API Key

#Initialize Lists
logins_list = []
errors = []

#For loop to go through every user
for x in range(1, *): #Change the * to a small number like 80 to start, and then utilize larger numbers as it begins to work - I had to use 1600 for example
    try:
        #GET user x to obtain user attributes
        users = canvas.get_user(x)
        
        #GET request for all login information that is from Canvas for that specific user
        logins = users.get_user_logins()
        
        #loop through each login
        for login in logins:
            #If a student's unique ID (login id) is not equal to their email, then create/POST new login
            if(login.unique_id != users.email and users.name != 'Test Student'):
            
                #create a POST Payload to use for this user to create the new login
                payload = {'user[id]': users.id, 'login[unique_id]':users.email}
                
                #create POST request to necessary url and the payload above
                r = requests.post(url, headers = headers, params = payload)
                
                #send login information and POST request status code to a list
                logins_list.append([login.user_id, users.name, r.status_code, r.text])
            else:
                #break this loop if user login id is equal to their email
                break
    except:
    #if there is an error (usually no user for x ID), pass this user and move to next user ID
        pass
        
#create a txt file logged with all status codes
file1 = open("Log_Canvas.txt","w+")
for err in logins_list:
    file1.write("%s\n" % err)
file1.write("Completed: " + str(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())))
file1.close()

#print status and timestamp in console
print("Student Login creation done!")
print("--- %s seconds ---" % (time.time() - start_time))
#Done!