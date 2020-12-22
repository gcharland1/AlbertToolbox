class PipingItem:
    library = "libraries/lib.json"

    def __init__(self, type=None, diameter=None, schedule=None, material=None, joint_type=None):
        self.type = type
        self.diameter = diameter
        self.schedule = schedule
        self.material = material
        self.joint_type = joint_type
        self.manipulations = self.list_manipulations()

    def list_manipulations(self):
        return []
