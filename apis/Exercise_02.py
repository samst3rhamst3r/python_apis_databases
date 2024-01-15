'''
Building on the previous example, create a list of all of the emails of the users and print
the list to the console.

'''
import requests, pprint

response = requests.get("http://demo.codingnomads.co:8080/tasks_api/users")

json = response.json()
emails = [d["email"] for d in json["data"]]
print(emails)