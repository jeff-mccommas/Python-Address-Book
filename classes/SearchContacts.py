import classes.JsonDictHelper as JsonDictHelper

class SearchContacts(JsonDictHelper.JsonDictHelper):
    """Case insensitive search for all contacts"""
    def __init__(self, filename, enterbox, msgbox):
        self.filename = filename
        self.enterbox = enterbox
        self.msgbox = msgbox
        JsonDictHelper.JsonDictHelper.__init__(self)

    def search_contacts(self):
        """
        - Get search term from enterbox.
        - Returns multiple contacts that matches the given search term.
        - Cancel button returns to the main menu.
        - If no contacts found for the given search term show enterbox to add a new contact. 
        """
        searchTerm = self.enterbox("Search for a contact by any kind of information: ")

        if not searchTerm:
            return

        with open(self.filename, "r") as search_file:
            found = []
            for line in search_file:
                if searchTerm.lower() in ','.join(self.json.loads(line).values()).lower():
                    found.append(line)

            foundLength = len(found)
            if foundLength > 0:
                if foundLength == 1:
                    title = "1 Contact Found"
                else:
                    title = "{} Contacts Found".format(foundLength)

                displayFoundContacts = self.display_contact(found)
                self.msgbox(msg="\n".join(displayFoundContacts), title=title)
                return
            
            searchTerm = self.enterbox("There's no one named " + searchTerm + " in your contact list. Press 2 to enter them now")
            if searchTerm == "2":
                return 2
            else:
                self.msgbox(msg="Please choose an item from the menu", title="please an item", ok_button="ok")

    def __repr__(self):
        '''Returns representation of the object'''
        return("{}('{}, {}, {}, {}, {}')".format(self.__class__.__name__, self.filename,
         self.enterbox, self.msgbox, self.re, self.json))