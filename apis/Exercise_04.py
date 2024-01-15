'''
Write a program that makes a PUT request to update your user information to a new first_name, last_name and email.

Again make a GET request to confirm that your information has been updated.

'''
import requests, pprint

url = "http://demo.codingnomads.co:8080/tasks_api/users"
json = {"first_name": "Mr Sam", "last_name": "ToughNStuff", "email": "cool_email@gmail.com"}

response = requests.put(url + "/1775", json=json)
print(response.status_code)
response = requests.get(url)
pprint.pprint(response.content)