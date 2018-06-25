import classes.JsonDictHelper as JsonDictHelper

class ViewContacts(JsonDictHelper.JsonDictHelper):
    """To view all contacts in the txt file in a nicely formated way."""
    def __init__(self, filename, msgbox):   
        self.filename = filename
        self.msgbox = msgbox
        JsonDictHelper.JsonDictHelper.__init__(self)

    def view_contacts(self):
        """
        - Displaying all contacts in a msgbox.
        - Showing msgbox with msg 'No contacts found.' if contacts file is empty.
        """
        with open(self.filename, "r") as contactsFile:
            contacts = self.display_contact(contactsFile.readlines())

        if not contacts:
            return self.msgbox("No contacts found.")

        self.msgbox(msg="\n".join(contacts), title="Showing All Contacts")

    def __repr__(self):
        '''Returns representation of the object'''
        return("{}('{}, {}, {}, {}, {}')".format(self.__class__.__name__, self.filename, 
            self.msgbox, self.re, self.json))