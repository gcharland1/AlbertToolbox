from piping_item import PipingItem

class StandardBom:

    def __init__(self):
        self.content = []

    def add_item(self, item, qty):
        self.content.append([item, qty])
