from piping_item import PipingItem

class StandardBom:

    def __init__(self):
        self.items = []
        self.quantities = []

    def add_item(self, item=PipingItem(), qty=0):
        self.items.append(item)
        self.quantities.append(qty)
