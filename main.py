#importing required modules
import json
import datetime
from columnar import columnar
#End user can set their own limit here
limit = 0
#checkFrequency is here to check whether the user has reached the limits multiple times (current setup: array > 5)
def checkFrequency():
    #Setting up variables
    global limit
    count = 0
    tempList = []
    #opening json file
    with open("rename.json", "r") as rename:
        data = json.loads(rename.read())
    #adding to local array the prices
    for i in range(0, len(data['item'])):
        tempList.append(data['item'][i]['price'])
    #scan through array to spot limit surpasses
    for i in tempList:
        if float(i) > limit:
            count = count + 1
        else:
            continue
    if count > len(tempList) / 2 and len(tempList) > 5:
        print("It looks like you have surpassed your limit multiple times! Try harder next time!")
#appendData is to write data to the json db
def appendData(data, filename="rename.json"):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data['item'].append(data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)
#add is for the end user to type in their expenses
def add(name, price):
    global limit
    #warn the user if they have surpassed the preset limit
    if price > limit:
        command = input("You have surpassed your limit. Continue? (Yes/no)")
        if command.lower() == "yes":
            #content is the data to inject into json db
            content = {"name": name, "price": price}
            appendData(content)
        elif command.lower() == "no":
            print("Your input was discarded")
    else:
        content = {"name": name, "price": price}
        appendData(content)
#get a random tip from tips.json
def tips():
    import random
    with open("tips.json", "r") as tips:
        data = json.loads(tips.read())
    print(data['list'][random.randint(0, len(data['list']))])
#printList is to print the expenses in a clean way
def printList(option):
    output = []
    #to calculate the total
    sum = 0
    try:
        #list items in a clean way
        if option.lower() == "list":
            headers = ['NAME', 'PRICE']
            with open("rename.json", "r") as rename:
                data = json.loads(rename.read())
            for i in range(0, len(data['item'])):
                output.append([data['item'][i]['name'], data['item'][i]['price']])
            print(columnar(output, headers, no_borders=True))
        #calculating the total by adding all the recorded prices
        elif option.lower() == "calculate":
            with open("rename.json", "r") as rename:
                data = json.loads(rename.read())
            for i in range(0, len(data['item'])):
                sum = sum + data['item'][i]['price']
            print("Your total spendings: " + str(sum) + "$")
    #error catching
    except TypeError:
        print("It seems like the list is empty")
def main():
    import time
    print("""
======== Help Sheet ========
- Commands: add (to add item to list)
            print (to print eiter the list or the total amount spent)
            tips (print money saving tips)
    """)
    while True:
        #delay for the user experience
        time.sleep(1)
        checkFrequency()
        command = input("Enter your option: ")
        if command.lower() == "add":
            name = input("Enter the name: ")
            price = float(input("Enter the price: "))
            add(name, price)
        elif command.lower() == "print":
            option = input("Enter your option (list | calculate): ")
            printList(option)
        elif command.lower() == "tips":
            tips()
        else:
            print("Wrong command, please try again")
if __name__ == "__main__":
    main()
