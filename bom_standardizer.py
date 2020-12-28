from standard_bom import StandardBom
from piping_item import PipingItem
import difflib
import json

class BomStandaridizer:
    lib_file = "libraries/lib.json"

    def __init__(self, language='en'):
        self.language = language
        pass

    def list_to_bom(self, bom_list, headers=None):
        bom = StandardBom()

        return bom

    def find_closest(self, input, category=None):
        with open(self.lib_file) as json_file:
            lib = json.load(json_file)

        if not category == None:
            cat_lib = lib[category]
            return difflib.get_close_matches(input, cat_lib, 1, 0.5)
        else:
            print("Please select a categoty. Feature to be added soon")
            return "N/A"


if __name__=='__main__':
    BS = BomStandaridizer()
