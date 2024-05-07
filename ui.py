import json
import requests
import os
import time

def commands():
    print("\nCommands | Type into console and press 'Enter' key to activate:\n")
    print("\tn, new\t\tAdd a new hike")
    print("\te, edit\t\tEdit an existing hike")
    print("\tr, remove\tDelete an existing hike")
    print("\th, help\t\tShow list of these commands at any screen")
    print("\tq, quit\t\tExits program\n")
    
def clear_screen(delay=0):
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
    
def add():
    
    clear_screen()
    
    print("\nAdding a new hike is easy - you will be prompted for name, elevation, distance, and rating into the console. After typing in your answer with each prompt, press 'Enter' key to add.")
    print("\tUsage | Ensure each alphabetical input is properly capatalized, and each numerical input is all digits or digits with a decimal point.")
    print("Type the 'h' or 'help' command at any time to view a list of all program commands.")
    time.sleep(.5)
    
    name = input("\tName: ")
    if name.lower() == "h" or name.lower() == "help":
        return
    elevation = input ("\tElevation: ")
    if elevation.lower() == "h" or elevation.lower() == "help":
        return
    distance = input ("\tDistance: ")
    if distance.lower() == "h" or distance.lower() == "help":
        return
    rating = input("\tRating: ")
    if rating.lower() == "h" or rating.lower() == "help":
        return

    data = {
        "name": name,
        "elevationGain": elevation,
        "distance": distance,
        "rating": rating
    }
    
    time.sleep(.5)
    clear_screen()

    print("\nPlease review your entry before it is added to the log.")
    print("Press the 'Enter' key to submit your entry. Otherwise, enter 'q' or 'quit' to cancel and go back to main menu.\n")

    print("Here is what you entered:")
    print("\t", json.dumps(data), "\n")

    usr_confirmation = input("Confirm: ")

    if usr_confirmation != "":
        return

    data_json = json.dumps(data)
    response = requests.post("http://127.0.0.1:5000/hikes", data_json, headers={'Content-Type': 'application/json'})

    print("\nYour hike entry was successfully added to the log.")
    print("You will be redirected to the main menu in 3...2..1.\n")
    time.sleep(1)
    clear_screen()

def delete():

    clear_screen()
    print("Delete a previously logged hike entry. Type the hike name into the console and press the 'Enter' key to select a hike to delete. You can also type the 'a' or 'all' command to list all hikes in the log. Then, type the associated ID into the console to select a hike to delete.")
    print("Type the 'h' or 'help' command at any time to view a list of all program commands.")

    usr_input = input("Entry: ")
    usr_input = usr_input.lower()
    folder = "database/hikes/"
    files = os.listdir(folder)

    id = ""
    json_data = ""

    if usr_input.lower() == "h" or usr_input.lower() == "help":
         return
    elif usr_input.lower() == "a" or usr_input.lower() == "all":
        for file_name in files:
            file_path = os.path.join(folder, file_name)
            with open(file_path, "r") as file:
                json_data = json.load(file)
                file_id = os.path.basename(file_name)
                print(f"ID {file_id}:")
                print(json_data)
                print()
        id = input("Please enter the id of the hike to delete: ")
        files = os.listdir(folder)
        for file in files:
            if file == id:
                with open((folder + id), "r") as file:
                    json_data = json.load(file)
    else:
        for file_name in files:
            file_path = os.path.join(folder, file_name)
            with open(file_path, "r") as file:
                json_data = json.load(file)
                if (json_data.get("name").lower()) == usr_input:
                    id = file_name
                    break

    clear_screen()
    print("\nHere is the hike you have selected to delete:")
    print(json_data)
            
    print("\nAre you sure you want to delete the hike? If yes, enter 'y' or 'yes'. If no, enter 'n' or 'no'. *WARNING* Please note: if you select 'y' or 'yes', the entry will be permanently deleted and it will not be possible to retrieve.")
    usr_input = input("Entry: ")
    usr_input = usr_input.lower()
    
    if usr_input == "y" or usr_input == "yes":
        response = requests.delete("http://127.0.0.1:5000/hikes/" + id)
        if (response.status_code == 200):
            print("Your hike has been deleted")
        elif (response.status_code == 404):
            print("Hike could not be found")
        else:
            print("An internal server error occurred while deleting hike")
    else:
        return
  
    print("Your hike entry was successfully deleted from the log.")
    print("You will be redirected to the main menu in 3...2..1.")
    time.sleep(1)
    clear_screen()


def edit():
    clear_screen()
    print("Edit a previously logged hike entry. Type the hike name into the console and press the 'Enter' key to select a hike to edit. You can also type the 'a' or 'all' command to list all hikes in the log. Then, type the associated ID into the console to select a hike edit.")
    print("Type the 'h' or 'help' command at any time to view a list of all program commands.")
    
    usr_input = input("Entry: ")
    usr_input = usr_input.lower()
    folder = "database/hikes/"
    files = os.listdir(folder)
    file_path = ""

    id = ""
    json_data = ""

    if usr_input.lower() == "h" or usr_input.lower() == "help":
         return
    elif usr_input.lower() == "a" or usr_input.lower() == "all":
        for file_name in files:
            file_path = os.path.join(folder, file_name)
            with open(file_path, "r") as file:
                json_data = json.load(file)
                file_id = os.path.basename(file_name)
                print(f"ID {file_id}:")
                print(json_data)
                print()
        id = input("Please enter the id of the hike to edit: ")
        files = os.listdir(folder)
        for file in files:
            if file == id:
                with open((folder + id), "r") as file:
                    json_data = json.load(file)
                    break
    else:
        for file_name in files:
            file_path = os.path.join(folder, file_name)
            with open(file_path, "r") as file:
                json_data = json.load(file)
                if (json_data.get("name").lower()) == usr_input:
                    id = file_name
                    break

    print("\nHere is the hike you have selected to edit. To edit, you must re-enter all the input fields:")
    print(json_data)
    
    name = input("Name: ")
    elevation = input ("Elevation: ")
    distance = input ("Distance: ")
    rating = input("Rating: ")
    
    json_data["name"] = name
    json_data["elevationGain"] = elevation
    json_data["distance"] = distance
    json_data["rating"] = rating
    
    time.sleep(.5)
    clear_screen()

    print("Please review your entry before the revision is processed.")
    print("\t", json.dumps(json_data), "\n")
    print("Press the 'Enter' key to submit your entry. Otherwise, enter 'q' or 'quit' to cancel and go back to main menu.")
    
    usr_confirmation = input("Confirm: ")

    if usr_confirmation == 'q' or usr_confirmation == "quit":
        return
    
    try:
        with open(folder + file_name, 'w') as outfile:
            json.dump(json_data, outfile)
        print("Your hike was revised successfully")
    except json.JSONDecodeError:
        print("Your hike was not revised due to an internal server error.")

    print("You will be redirected to the main menu in 3...2..1.")
    time.sleep(1)
    clear_screen()

def main():  
    print("\n         ~~~ HIKE  LOG ~~~           ")
    print("~Track and view your completed hikes~")
 
    while True:
        commands()
        command = input("Please enter command: ")
        command = command.lower()
        
        if command == "q" or command == "quit":
            exit(0)
            #break
        elif command == "n" or command == "new":
            add()
        elif command == "e" or command == "edit":
             edit()
        elif command == "r" or command == "remove":
            delete()
        elif command == "h" or command == "help":
            commands()
        else:
            print("Command doese not exist. Please try again.")
        
if __name__ == "__main__":
    main()
