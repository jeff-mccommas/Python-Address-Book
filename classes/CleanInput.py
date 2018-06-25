import classes.JsonDictHelper as JsonDictHelper

class CleanInput(JsonDictHelper.JsonDictHelper):
    def __init__(self, enterbox=''):
        self.enterbox = enterbox
        JsonDictHelper.JsonDictHelper.__init__(self)

    def clean_first(self, error=''):
        # Ensures that the first name of a user is capitalized
        # Ensures that only legal names are accepted in this field
        first = self.__getInputValue("First name ", error)
        if first is None: return None
        isValidFirst = self.regexValidation(r'^[a-zA-Z]{3,20}$', first)
        if not isValidFirst:
            return self.clean_first("\nProvided first name isn't valid!\nOnly 3 to 20 alphabetical characters allowed")

        return first[0].upper() + first[1:]

    def clean_last(self, error=''):
        # Ensures that the first name of a user is capitalized
        # Ensures that only legal names are accepted in this field
        last = self.__getInputValue("Last name ", error)
        if last is None: return None
        isValidLast = self.regexValidation(r'^[a-zA-Z]{3,20}$', last)
        if not isValidLast:
            return self.clean_last("\nProvided last name isn't valid!\nOnly 3 to 20 alphabetical characters allowed")


        return last[0].upper() + last[1:]

    def clean_phone(self, error=''):
        # Takes a 10 digit input and presents it in the [(###) ###-####] format
        # Avoids mistakes & stupidity surrounding 10-digit phone numbers
        phone = self.__getInputValue('Phone number with area code ', error)
        if phone is None: return None
        isValidPhone = self.regexValidation(r'^[\d]{10}$', phone)
        if not isValidPhone:
            return self.clean_phone("\nProvided phone number isn't valid!\nOnly 10 numerals are accepted in this field\n")

        return "1 " + "(" + phone[0:3] + ")" + " " + phone[3:6] + "-" + phone[6:10]

    def clean_mail(self, error=''):
        # Ensures that an email is valid before allowing a user to assign it to a contact
        email = self.__getInputValue('E-mail ', error)
        if email is None: return None
        isValidEmail = self.regexValidation(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)
        if not isValidEmail:
            return self.clean_mail("\nProvided e-mail address isn't valid!\n")
        return email

    def clean_address(self):
        addie = self.__getInputValue('Address ')
        if addie is None: return None
        return addie

    def __getInputValue(self, fieldName, error=''):
        while 1:
            inputField = self.enterbox(fieldName + error)
            if not inputField:
                if inputField is None:
                    break
                error = "is a required field."
            else:
                break
        return inputField

    def regexValidation(self, regex, value):
        regex_format = self.re.compile(regex)
        return self.re.match(regex_format, value)

    def __repr__(self):
        '''Returns representation of the object'''
        return("{}('{}')".format(self.__class__.__name__, self.enterbox))