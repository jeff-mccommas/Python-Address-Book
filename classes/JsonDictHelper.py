import re
import json
import unittest

class JsonDictHelper():
    """
    - Converting list of json strings to formated list for displaying.
    - Return the contact for a given cid 'contact id'
    """
    def __init__(self):
        self.re = re
        self.json = json
        self.__JsonStringChoices = None
        self.__formatedChoices = []

    def display_contact(self, JsonStringChoices):
        """
        Requires: list of json strings.
        Returns: Formated list of received contacts for viewing.
        """
        self.__formatedChoices = []
        self.__JsonStringChoices = JsonStringChoices
        for choice in self.__JsonStringChoices:
            jsonChoice = self.json.loads(choice)
            displayContact = (jsonChoice["cid"] +"[" + jsonChoice["first_name"] + " " \
                + jsonChoice["last_name"] + "|" + jsonChoice["telephone"] + "," \
                + jsonChoice["email"] + "|" + jsonChoice["address"] + "]")
            self.__formatedChoices.append(displayContact)

        return self.__formatedChoices

    def get_contact_by_cid(self, selectedCid):
        """
        Requires: string of the contact id.
        Returns: The contact for the give contact id in json 'string type'.
        """
        for choice in self.__JsonStringChoices:
            if selectedCid == self.json.loads(choice)["cid"]:
                return choice
                break

    def __repr__(self):
        '''Returns representation of the object'''
        return("{}".format(self.__class__.__name__))

class TestJsonDictHelper(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        from random import randint
        super(TestJsonDictHelper, self).__init__(*args, **kwargs)
        self._lambdaToJsonString = lambda i :'{"cid": "%(i)s", "first_name": "First%(i)s", "last_name": "Last%(i)s", "telephone": "1 (345) 762-3199", "email": "email%(i)s@gmail.com", "address": "address%(i)s"}' % {'i': str(i)}
        self._lambdaToDisplayString = lambda i :'%(i)s[First%(i)s Last%(i)s|1 (345) 762-3199,email%(i)s@gmail.com|address%(i)s]' % {'i': str(i)}
        JDH = JsonDictHelper()
        JsonStringChoices = [self._lambdaToJsonString(i) for i in range(1,15)]
        random_contact_id_num = str(randint(1, 15))
        self._returned_contacts_to_display = JDH.display_contact(JsonStringChoices)
        self._expected_contacts_to_display = [self._lambdaToDisplayString(i) for i in range(1,15)]
        self._returned_selected_contact_by_contact_id = JDH.get_contact_by_cid(random_contact_id_num)
        self._expected_selected_contact_by_contact_id = self._lambdaToJsonString(random_contact_id_num)

    def test_displaying_contacts_as_strings(self):
        self.assertTrue(self._returned_contacts_to_display == self._expected_contacts_to_display, "Expected list of contacts to be displayed are wrong!")
        
    def test_getting_json_syting_contact_by_contact_id(self):
        self.assertTrue(self._returned_selected_contact_by_contact_id == self._expected_selected_contact_by_contact_id, "Expected contact to be returned is wrong!")

if __name__ == '__main__':
    unittest.main()