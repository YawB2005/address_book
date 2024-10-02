import csv


class Contact:
    
    def __init__(self, firstName, lastName, phoneNumber):
         self.firstName = firstName
         self.lastName = lastName
         self.phoneNumber = phoneNumber
    


class AddressBook:
    def __init__(self):
        self.contacts = []
        self.readFromFile()

    def getContacts(self):
        self.readFromFile()
        return self.contacts

    def addContact(self, first_name, last_name, phone):
        self.contacts.append(Contact(firstName=first_name, lastName=last_name, phoneNumber=phone))
        self.saveToFile()

    def deleteContact(self, index):
        self.contacts.pop(index)
        self.saveToFile()

    def updateContact(self, index, first_name, last_name, phone):
        contact = self.contacts[index]
        contact.firstName = first_name
        contact.lastName = last_name
        contact.phoneNumber = phone
        
        self.saveToFile()


    def readFromFile(self):
      
        with open('user_data.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                self.contacts = []  # Clear contacts before reading
                for row in rows:
                    self.contacts.append(Contact(
                        firstName=row['firstname'],
                        lastName=row['lastname'],
                        phoneNumber=row['phonenumber']
                    ))
                      
    def saveToFile(self):
        with open("user_data.csv", mode='w', newline='') as file:
            fieldnames = ['firstname', 'lastname', "phonenumber"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for contact in self.contacts:
                writer.writerow({
                    'firstname': contact.firstName,
                    'lastname': contact.lastName,
                    'phonenumber': contact.phoneNumber
                })
    
        


class UI:
    def __init__(self):
        self.addressbook = AddressBook()

    def exitApp(self):
        print("Exiting....Bye")
        exit()
    
    def addContact(self):

        # self.addressbook.addContact(first_name=finally)
        self.handle_change(action="add")
        print("Added contact successfully")

    def viewContacts(self):
        print("Viewing contacts")
        contacts = self.addressbook.getContacts()

        index = 0
        for contact in contacts:
            index += 1
            print(f"{index}. {contact.firstName} {contact.lastName} - {contact.phoneNumber}")


    def validateName(self, name, message):
        is_new = True if name == "" else False
        # new
        if is_new:
            while name == "" :
                name = input(message).strip()
                if name == "":
                    self.handle_invalid_input()
        else:
        # edit 
            name = input(message).strip() or name
        return name
    
    def validatePhone(self, phone, message):
        is_new = True if phone == "" else False
        if is_new:
            while phone == "" or self.isNotCorrectPhone(phone):
                phone = input(message).strip()
                if phone == "" or self.isNotCorrectPhone(phone):
                    self.handle_invalid_input()
        else:
            prev = phone
            phone = input(message).strip()
            if phone != "" and self.isNotCorrectPhone(phone):
                    self.handle_invalid_input()
                    phone = self.while_loop(phone, message, prev)
            elif phone == "":
                phone = prev
            elif phone!="" and self.isNotCorrectPhone(phone):
                print(phone)
                phone = self.while_loop(phone, message, prev)
        return phone
    
    def while_loop(self, phone, message, prev): 
        print(prev)
        while phone != "" and self.isNotCorrectPhone(phone):
            phone = input(message).strip()
            if phone == "":
                phone = prev
            elif phone != "" and self.isNotCorrectPhone(phone):
                self.handle_invalid_input()
        return phone

    def isNotCorrectPhone(self, phone):
        # check if char are numbers
        try :
            int(phone)
        except ValueError:
            return True
        
        #check length
        if len(phone) != 10 and len(phone) != 12:
            return True 
        else:
            if len(phone) == 10 and phone[0] != '0':
                return True
            elif len(phone) == 12 and phone[:2] != '233':
                return True
            else:
                return False

    def summary(self, fn, ln, ph):
        print("=====Summary=====\n")
        print(f"First name: {fn} \n Last name: {ln} \n Phone number: {ph}")


    def handle_change(self, action, firstName= "", lastName= "", phone= "", index=None):
        
        message = self.show_prompt_message(firstName,lastName,phone)
        firstName = self.validateName(firstName, message['firstName'])
        lastName = self.validateName(lastName, message['lastName'])
        phone = self.validatePhone(phone, message['phone'])

        self.summary(firstName, lastName, phone)

        self.menu({
            "Proceed to save": lambda: self.proceed_action(action,  firstName, lastName, phone, index),
            "Edit": lambda: self.handle_change(action,firstName,lastName,phone, index),
            "Go to main menu": self.main_menu,

        })

    
    def proceed_action(self, action,  firstName, lastName, phone, index):
        if action == "add":
            return self.addressbook.addContact(firstName, lastName,phone)
        elif action == "update":
            return self.addressbook.updateContact(index, firstName, lastName, phone)

    def show_prompt_message(self, prevFirstName="", prevLastName="", prevPhone=""):
        arrMssg = {}
        if prevFirstName != "":
            arrMssg['firstName'] = f"Please enter the first name ({prevFirstName}): "
            arrMssg['lastName'] = f"Please enter the last name ({prevLastName}): "
            arrMssg['phone'] = f"Please enter the phone ({prevPhone}): "
        else:
            arrMssg['firstName'] = f"Please enter the first name: "
            arrMssg['lastName'] = f"Please enter the last name: "
            arrMssg['phone'] = f"Please enter the phone: "
        return arrMssg


    def updateContact(self):
        contact_dic = {}
        index = 0
        for contact in self.addressbook.contacts:
            index += 1
            contact_dic[f"{contact.firstName} {contact.lastName} - {contact.phoneNumber}"] = lambda i=index: self.updateDummy(i)

        
        self.menu(contact_dic)


        

    def updateDummy(self, index):
        contact = self.addressbook.contacts[index -1]
        
        self.handle_change("update", contact.firstName, contact.lastName, contact.phoneNumber, index=index - 1)

        print("Updating contact")

    def deleteContact(self):
       self.viewContacts()
       try:
            index = int(input("Enter the index of the contact you want to delete: "))
       except ValueError:
           self.handle_invalid_input()
        
       self.addressbook.deleteContact(index -1)
       print("Deleting contact")

    def display_menu_prompt(self, keys):
        count = 0
        for key in keys:
            count += 1  
            print(f"{count}. {key}")

    def handle_invalid_input(self, message=None):
        mess = message or "Invalid input"
        print(mess + "\n")

    def menu(self, menu_param):
        show_menu_again = True

        while show_menu_again:
            # menu display section 
            self.display_menu_prompt(menu_param.keys())

            # menu action section
            try:
                resp = int(input("\nSelect an option: "))
            except ValueError:
                self.handle_invalid_input()
                continue

            # exception handling
            if resp > len(menu_param) or resp <= 0:
                self.handle_invalid_input()
                continue
            else:
                show_menu_again = False
                # retrieve function and call it
                list(menu_param.values())[int(resp)-1]()

    def main_menu(self):    
      
        self.menu({
            "Add Contact": self.addContact,
            "View Contact": self.viewContacts,
            "Update Contact": self.updateContact,
            "Delete Contact": self.deleteContact,
            "Exit": self.exitApp
        })

        self.menu({
            "Go to Main Menu": self.main_menu, 
            "Exit": self.exitApp
        })


# Start the app
print("Heyyyy, welcome to my address book")
ui_instance = UI()
ui_instance.main_menu()





