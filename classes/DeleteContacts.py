import classes.JsonDictHelper as JsonDictHelper

class DeleteContacts(JsonDictHelper.JsonDictHelper):
    """Show choicebox to select one of the contacts to delete"""
    def __init__(self, filename, choicebox, msgbox):    
        self.filename = filename
        self.choicebox = choicebox
        self.msgbox = msgbox
        JsonDictHelper.JsonDictHelper.__init__(self)

    def delete_contacts(self):
        contacts_file = open(self.filename, "r+")
        JsonStringChoices = contacts_file.readlines()
        choices = self.display_contact(JsonStringChoices)

        if not choices:
            return self.msgbox("No contacts found.")

        selected_contacts = self.choicebox(msg="Select the contact you wish to delete.",
                           title="Deleting Contacts",
                           choices=list(map(str.strip, choices)),
                           preselect=0)
        if selected_contacts == None:
            return
        else:
            selected_cid = self.re.search(r'^(\d+)\[', selected_contacts).group(1)
            selected_record = self.get_contact_by_cid(selected_cid)

            contacts_file.seek(0)
            contacts_file.truncate()

            for line in JsonStringChoices:
                if selected_record != line:
                    contacts_file.write(line)

            self.msgbox(msg="The following contact has been successfully deleted.\n{}".format(selected_contacts))
            contacts_file.close()

    def __repr__(self):
        '''Returns representation of the object'''
        return("{}('{}, {}, {}, {}, {}')".format(self.__class__.__name__, self.filename,
         self.choicebox, self.msgbox, self.re, self.json))