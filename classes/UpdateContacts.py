import classes.JsonDictHelper as JsonDictHelper
import classes.CleanInput as CleanInput

class UpdateContacts(CleanInput.CleanInput):    
    """Show choicebox to select one of the contacts to update"""
    def __init__(self, OrderedDict, filename, multenterbox, choicebox, msgbox, indexbox):    
        self.filename = filename
        self.multenterbox = multenterbox
        self.choicebox = choicebox
        self.msgbox = msgbox
        self.indexbox = indexbox
        self.OrderedDict = OrderedDict
        self.__msg = "Update contact's information"
        self.__title = "Updating Contacts"
        self.__fieldNames = ["First Name", "Last Name", "Phone Number", "E-mail", "Address"]
        CleanInput.CleanInput.__init__(self)


    def update_contacts(self):
        """
        - Displaying choicebox to select one of the contacts to update, the cancel button returns to main menu.
        - multenterbox cancel button returns to choicebox to select different contact to update.
        - All fields are populated with the selected contact info.
        - All fields are required and can't be empty, an error will be displayed with the empty field name.
        - indexbox displayed when no changes were made to any field -after submission- to choice to either return to updating multenterbox or main menu.
        """
        self.__contacts_file = open(self.filename, "r+")
        self.__JsonStringChoices = self.__contacts_file.readlines()
        self.__choices = self.display_contact(self.__JsonStringChoices)

        if not self.__choices:
            return self.msgbox("No contacts found!")

        selected_contact = self.choicebox(msg="Select the contact you wish to update.",
                           title="Select Contact To Update",
                           choices=list(map(str.strip, self.__choices)),
                           preselect=0)
        if selected_contact == None:
            return
        else:
            selected_cid = self.re.search(r'^(\d+)\[', selected_contact).group(1)
            self.__selected_record = self.get_contact_by_cid(selected_cid)
            self.__contactVaules = self.json.loads(self.__selected_record)
            
            fieldValues = [self.__contactVaules["first_name"], self.__contactVaules["last_name"], self.__contactVaules["telephone"], 
                            self.__contactVaules["email"], self.__contactVaules["address"]]

        self.__updateHelper(fieldValues=fieldValues)


    def __updateHelper(self, fieldValues):
        updatedValues = self.multenterbox(self.__msg, self.__title, self.__fieldNames, fieldValues)

        if updatedValues == None:
            return self.update_contacts()

        while 1:
            if updatedValues == None: break
            errmsg = ""
            for i in range(len(self.__fieldNames)):
                if updatedValues[i].strip() == "":
                    errmsg = errmsg + ('"{}" is a required field.\n\n'.format(self.__fieldNames[i]))
                elif self.__fieldNames[i] == "First Name":
                    isValidFirst = self.regexValidation(r'^[a-zA-Z]{3,20}$', updatedValues[i].strip())
                    if not isValidFirst:
                        errmsg = errmsg + "Provided first name isn't valid!\nOnly 3 to 20 alphabetical characters allowed.\n\n"
                elif self.__fieldNames[i] == "Last Name":
                    isValidLast = self.regexValidation(r'^[a-zA-Z]{3,20}$', updatedValues[i].strip())
                    if not isValidLast:
                        errmsg = errmsg + "Provided first name isn't valid!\nOnly 3 to 20 alphabetical characters allowed.\n\n"
                elif self.__fieldNames[i] == "Phone Number":
                    isValidPhone = self.regexValidation(r'^1[ \(]{2}[\d]{3}[ )]{2}[\d]{3}-?[\d]{4}', updatedValues[i].strip())
                    if not isValidPhone:
                        errmsg = errmsg + "Provided phone number isn't valid. Correct phone format is:\n1 (###) ###-####\n\n"
                elif self.__fieldNames[i] == "E-mail":
                    isValidEmail = self.regexValidation(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', updatedValues[i].strip())
                    if not isValidEmail:
                        errmsg = errmsg + "Provided e-mail address isn't valid.\n\n"

            if errmsg == "":
                updatedValues[0] = updatedValues[0][0].upper() + updatedValues[0][1:]
                updatedValues[1] = updatedValues[1][0].upper() + updatedValues[1][1:]
                break
            updatedValues = self.multenterbox(errmsg, self.__title, self.__fieldNames, updatedValues)
        
        if updatedValues == fieldValues:
            confirm = self.indexbox(msg="No changes were made to any field!", title="Update Notice", 
                choices=('Back', 'Main menu'), default_choice='Back', cancel_choice='Main menu')
            if confirm == 0:
                return self.__updateHelper(fieldValues=fieldValues)
            elif confirm in (1, None):
                return
        elif updatedValues == None:
            return self.update_contacts()


        self.__contacts_file.seek(0)
        self.__contacts_file.truncate()
        for contact in self.__JsonStringChoices:
            if contact == self.__selected_record:
                updatedValues = list(map(str.strip, updatedValues))
                initContact = [("cid", self.__contactVaules["cid"]), ("first_name", updatedValues[0]), 
                                ("last_name", updatedValues[1]), ("telephone", updatedValues[2]), 
                                ("email", updatedValues[3]), ("address", updatedValues[4])]
                contact = self.OrderedDict(initContact)
                self.__contacts_file.write("{}\n".format(self.json.dumps(contact)))
            else:
                self.__contacts_file.write(contact)
        
        self.__contacts_file.close()

        self.msgbox("Contact has been successfully updated!")
 
    def __repr__(self):
        '''Returns representation of the object'''
        return("{}('{}, {}, {}, {}, {}')".format(self.__class__.__name__, self.OrderedDict, self.filename,
         self.multenterbox, self.choicebox, self.msgbox, self.indexbox, self.re, self.json))