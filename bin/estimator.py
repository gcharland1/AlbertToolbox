import json

class Estimator:
    headers = ['No', 'Description', 'Diamètre', 'Schedule', 'Materiel', 'Quantité', 'Temps']
    def __init__(self):
        with open('bin/dictionaries/operation_times.json', 'r') as json_file:
            op_data = json.load(json_file)
            self.time_dict = op_data['Time']
            self.count_dict = op_data['Count']
            self.sch_factors_dict = op_data['Schedule Factors']
            self.mtl_factors_dict = op_data['Material Factors']

    def man_hours(self, bom_data):
        i_typ = self.headers.index('Description')
        i_dia = self.headers.index('Diamètre')
        i_sch = self.headers.index('Schedule')
        i_mtl = self.headers.index('Materiel')
        i_qty = self.headers.index('Quantité')
        i_time = self.headers.index('Temps')

        total_time = 0
        for item in bom_data: # For ELEMENT in BOM: (Dans une liste)
            try:
                item_qty = abs(float(item[i_qty]))
            except:
                item_qty = 0
                item[i_qty] = 0
            item_typ = item[i_typ]
            item_dia = item[i_dia]
            item_sch = item[i_sch]
            item_mtl = item[i_mtl]
            item_time = 0
            try:
                item_ops = self.count_dict[item_typ]
            except:
                print(f'Item type {item_typ} is not in current dictionary. Ingoring...')
                continue

            bom_item_time = 0
            try:
                for op in item_ops:
                    op_count = item_ops[op]
                    op_time = self.time_dict[op][item_dia]
                    sch_factor = self.sch_factors_dict[item_sch][op]
                    mtl_factor = self.mtl_factors_dict[item_mtl][op]
                    item_time += op_time * op_count * sch_factor * mtl_factor
                    bom_item_time = round(item_qty * item_time, 2)
            except:
                    print(f'Problem w/ item {item_typ} and dia {item_dia}')
                    bom_item_time = 0

            item[i_time] = bom_item_time
            total_time += bom_item_time

        return round(total_time, 2), bom_data
