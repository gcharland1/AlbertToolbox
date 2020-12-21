import time
import math
import json

class Estimator:
    pipe_length = 12 # Class Variable. C'est la valeur de base, on pourrait la
    # changer avec self.pipe_length = new_length
    headers = ['No', 'Description', 'Diametre', 'Schedule', 'Materiel', 'Quantite', 'Temps']
    def __init__(self):
        with open('dictionaries/operation_times.json', 'r') as json_file:
            op_data = json.load(json_file)
            self.time_dict = op_data['Time']
            self.count_dict = op_data['Count']

    def man_hours(self, bom_data):
        i_typ = self.headers.index('Description')
        i_dia = self.headers.index('Diametre')
        i_mtl = self.headers.index('Materiel')
        i_qty = self.headers.index('Quantite')
        i_time = self.headers.index('Temps')

        total_time = 0
        for item in bom_data: # For ELEMENT in BOM: (Dans une liste)
            item_qty = float(item[i_qty])
            item_dia = item[i_dia]
            item_mtl = item[i_mtl]
            item_typ = item[i_typ]
            item_time = 0
            try:
                item_ops = self.count_dict[item_typ]
            except:
                print(f'Item type {item_typ} is not in current dictionary. Ingoring...')
                continue

            try:
                for op in item_ops: # Joue dans un dictionnaire
                    op_count = item_ops[op]#
                    action_time = self.time_dict[op][item_dia]
                    item_time += action_time * op_count
                    bom_item_time = round(item_qty * item_time, 2)
            except:
                    print(f'Problem w/ item {item_typ} and dia {item_dia}')
                    bom_item_time = 0

            item[i_time] = bom_item_time
            total_time += bom_item_time

        return round(total_time, 2), bom_data
