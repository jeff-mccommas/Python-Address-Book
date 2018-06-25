"""Address Book and Contacts manager
"""
from easygui import *
import sys
import json
from collections import OrderedDict
from classes.CleanInput import CleanInput
from classes.SearchContacts import SearchContacts
from classes.DeleteContacts import DeleteContacts
from classes.UpdateContacts import UpdateContacts
from classes.ViewContacts import ViewContacts

def initiation():
    """
    This initiates the address books.
    - Displaying enterbox to get the filename which is a required field.
    - enterbox field is required and can't be empty, an error will be displayed -after submission- if the field was empty
    - Declaring (contacts_filename,CI,VC,SC,DC,UC) as global variables.
    - Creating instances of classes (CleanInput,ViewContacts, SearchContact, DeleteContacts, UpdateContasts) into global variables(contacts_filename,CI,VC,SC,DC,UC) respectively.
    - Checking if contacts file has records, and asserting if all records have valid structure
    """
    msg = "Enter file name."
    while 1:
        inputbox = enterbox(title="What would you like to call your address book?", msg=msg)

        if not inputbox:
            if inputbox is None:
                sys.exit(0)
            msg="You must type something in!"
        else:
            global contacts_filename,CI,VC,SC,DC,UC
            contacts_filename = inputbox + ".txt"

            CI = CleanInput(enterbox)
            VC = ViewContacts(contacts_filename, msgbox)
            SC = SearchContacts(contacts_filename, enterbox, msgbox)
            DC = DeleteContacts(contacts_filename, choicebox, msgbox)
            UC = UpdateContacts(OrderedDict, contacts_filename, multenterbox, choicebox, msgbox, indexbox)
            break

    # Checking if file has contacts, and if contacts present asserting their structure.
    try:
        with open(contacts_filename, 'a+') as fh:
            fh.seek(0)
            contactsList = fh.readlines()
            if contactsList:
                for i,contact in enumerate(contactsList):
                    # Asserting record structure with regular expression matching.
                    assert VC.re.match(r'{"cid":[^,]+, "first_name":[^,]+, "last_name":[^,]+, '
                        r'"telephone":[^,]+, "email":[^,]+, "address":[^}]+}', contact), \
                        'Line {} structure is wrong! Filename: {}'.format(i+1, contacts_filename)
    except IOError as e:
        raise SystemExit("Unable to create or read filename: {} \nPlease change the folder permission for read and write.\n{}".format(contacts_filename, e))


def main_menu(init=False):
    """Allows users to select which feature to use"""
    if init:
        initiation()

    choice = choicebox(msg="Press one of the following numeric keys:\n 1 To view your contacts\n 2 To enter a new contact\n 3 To search your contacts\n 4 To delete your contacts\n 5 To update your contacts",
                       title="Press 1 to view your contacts, 2 to enter a new contact, 3 to search your contacts, 4 to delete your contacts and 5 to update your contacts",
                       choices=[1, 2, 3, 4, 5])
    if choice == "1":
        VC.view_contacts()
        main_menu()
    elif choice == "2":
        enter_contacts()
        main_menu()
    elif choice == "3":
        returned_choice = SC.search_contacts()
        if returned_choice == 2: enter_contacts()
        main_menu()
    elif choice == "4":
        DC.delete_contacts()
        main_menu()
    elif choice == "5":
        UC.update_contacts()
        main_menu()

def enter_contacts():
    """
    - Collects contact info.
    - Saves contact info to a dictionary
    """
    with open(contacts_filename, "a+") as text_file:
        text_file.seek(0)
        contacts = text_file.readlines()
        if not contacts:
            cid = "1"
        else:
            last_cid = json.loads(contacts[-1])['cid']
            if last_cid:
                cid = str(int(last_cid) + 1)

        first = CI.clean_first()
        if first is None: return
        last = CI.clean_last()
        if last is None: return
        telephone = CI.clean_phone()
        if telephone is None: return
        email = CI.clean_mail()
        if email is None: return
        addie = CI.clean_address()
        if addie is None: return

        initContact = [("cid", cid), ("first_name", first), ("last_name", last), ("telephone", telephone), 
                    ("email", email), ("address", addie)]
        contact = OrderedDict(initContact)
        displayContact = (cid +"[" + first + " " + last + "|" + telephone + "," + email + "|" + addie + "]")
        text_file.write("{}\n".format(json.dumps(contact)))
        msgbox(msg="The contact " + displayContact + " has been added to your address book",
               title="contact added to your address book", ok_button="ok")

main_menu(init=True)
