'''
Write the necessary code to make a POST request to:

    http://demo.codingnomads.co:8080/tasks_api/users

and create a user with your information.

Make a GET request to confirm that your user information has been saved.

'''
import requests, pprint

url = "http://demo.codingnomads.co:8080/tasks_api/users"
json = {"first_name": "Sam", "last_name": "Turner", "email": "fake_email@gmail.com"}
response = requests.post(url, json=json)
print(response.status_code)
response = requests.get(url)
pprint.pprint(response.content)