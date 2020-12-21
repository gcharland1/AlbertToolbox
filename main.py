##########################################################
# Comment est-ce que je fait agir différement quand on clique sur un icon
# Windows? Est-ce que c'est dans setup.py (run main(GUI=True))
# Va falloir éventuellement que ça soit un installateur .exe
# en attendant, juste permettre d'ajouter le <main> au PATH

import estimator
import tkinter
from tkinter import filedialog
import tkinter.messagebox
import os

import csv

class piping_estimator:

    def __init__(self, path='./', bom_file='bom.csv'):
        self.path = path
        self.bom_file = bom_file
        self.estimator = estimator.Estimator()

        self.setup_GUI()
        self.root.mainloop()

    def change_path(self):
        root = tkinter.Tk()
        root.overrideredirect(1)
        root.withdraw()
        self.path = filedialog.askdirectory(initialdir = self.path,
                title = "Sélectionner le dossier où travailler")
        root.destroy()
        self.root.title(self.path)

    def select_file(self):
        file_name = filedialog.askopenfilename(initialdir = self.path,
                title = 'Sélectionner le fichier BOM',
                filetypes = (('CSV files', '.csv'), ('All files', '.*')))

        if file_name:
            self.bom_file = file_name.split('/')[-1]
            self.path = '/'.join(file_name.split('/')[:-1])
            bom_name_label = '[...] ' + '/'.join(file_name.split('/')[-3:-1])+ '/' + self.bom_file
            self.bom_name_label.config(text=bom_name_label, fg='#000000')

    def create_file(self):
        file_name = filedialog.asksaveasfilename(title = "Sélectionner le fichier BOM",
                initialdir = self.path,
                filetypes = (("CSV files", "*.csv*"), ("All files", '.*')),
                initialfile='New File.csv')

        if file_name:
            self.bom_file = file_name.split('/')[-1]
            self.path = '/'.join(file_name.split('/')[:-1])
            bom_name_label = '[...] ' + '/'.join(file_name.split('/')[-3:-1])+ '/' + self.bom_file
            self.bom_name_label.config(text=bom_name_label, fg='#000000')

            with open(file_name, 'w') as new_file:
                csv_writer = csv.writer(new_file, delimiter=',')
                csv_writer.writerow(self.estimator.headers)

            self.root.update()
            self.open_file()

    def file_is(self, file_name, ext='csv'):
            print(file_name)
            if file_name.split('.')[-1] == ext:
                return True
            else:
                info(f'Impossible d''utiliser ce fichier. Utiliser un {ext}')
                return False

    def open_file(self):
        if self.file_is(self.bom_file, 'csv'):
            try:
                os.startfile(self.path+'/'+self.bom_file)
            except:
                print('##CANNOT OPEN FILE##')

    def read_bom_data(self):
        if not self.bom_file == '':
            while True:   # repeat until the try statement succeeds
                try:
                    file = open(self.path+'/'+self.bom_file, 'r+') # Le plus force d'avoir le plein contrôle
                    break                             # exit the loop
                except IOError as e:
                    print(e)
                    info('Veuillez fermer la fenêtre Excel, puis appuyez sur OK.', 'ERREUR')
                    # restart the loop
            bom_data = []
            csv_reader = csv.reader(file, delimiter=',')
            line_count = 0
            for r in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    bom_data.append(r)

            file.close()
            return bom_data
        else:
            info('Veuillez sélectionner un fichier BOM pour débuter', 'ERREUR')
            return []

    def estimate_total_time(self):
        total_time, updated_bom_data = self.estimator.man_hours(
                                                    self.read_bom_data())
        info(total_time)

    def setup_GUI(self):
        print('Setuping GUI buttons and text')
        self.root = tkinter.Tk()
        self.root.title('Albert Conseil - Piping estimator')
        self.root.iconbitmap(default='./images/icon.ico')
        # Trouver un moyen d'avoir la fenêtre de boutons sur le top sans bloquer
        # le Excel

        main_width = 50
        #main_height = 1000
        button_height = 10
        button_width = 5

        font_name = 'Arial'
        font_size = 12
        division_font_size = 16
        title_font_size = 20
        font = (font_name, font_size)
        division_font = (font_name, division_font_size)
        title_font = (font_name, title_font_size)

        bg_color = '#353535' # Fond foncé
        text_box_color = '#606060'
        font_color = '#d0d0d0' # Écriture Pale
        button_color = '#a0a0a0'
        button_font_color = '#000000'


        PAD_Y = 2
        PAD_X = 2

        #### Section Frames
        self.main_frame = tkinter.Frame(self.root,
                                        bg=bg_color)

        ##### Section Titre #####
        self.head_frame = tkinter.Frame(self.main_frame,
                                        bg=bg_color)
        self.window_title = tkinter.Label(self.head_frame,
                                        anchor='w',
                                        width=main_width - 2*PAD_X,
                                        bg=bg_color,
                                        fg=font_color,
                                        font=title_font,
                                        text='Piping Estimator')
        self.window_title.grid(row=0, sticky='w')
        self.head_frame.grid(row=0, sticky='w', pady=2*PAD_Y)


        #### Section File Selection ####
        self.selecting_frame = tkinter.Frame(self.main_frame,
                                        bg=bg_color)

        self.bom_selection_label = tkinter.Label(self.selecting_frame,
                                        anchor='w',
                                        bg=bg_color,
                                        fg=font_color,
                                        font=division_font,
                                        text='1) Choisir le fichier BOM:')

        self.current_bom_label = tkinter.Label(self.selecting_frame,
                                        anchor='e',
                                        bg=bg_color,
                                        fg=font_color,
                                        font=font,
                                        text='Fichier ouvert:')

        self.bom_name_label = tkinter.Label(self.selecting_frame,
                                        width=main_width,
                                        anchor='w',
                                        bg = '#d0d0d0',
                                        fg = '#333333',
                                        font=font,
                                        text='Choisir un fichier pour débuter')

        self.new_file_button = tkinter.Button(self.selecting_frame,
                                        anchor='e',
                                        font=font,
                                        bg=button_color,
                                        fg=button_font_color,
                                        text='Nouveau Projet',
                                        command=self.create_file)

        self.select_file_button = tkinter.Button(self.selecting_frame,
                                        anchor='e',
                                        font=font,
                                        bg=button_color,
                                        fg=button_font_color,
                                        text='Choisir ...',
                                        command=self.select_file)

        self.bom_selection_label.grid(row=0, column=0, sticky='w', columnspan=2, padx=PAD_X, pady=PAD_Y)
        self.new_file_button.grid(row=0, column=1, columnspan=2, sticky='e', padx=PAD_X, pady=PAD_Y)
        self.current_bom_label.grid(row=1, column=0, sticky='e', padx=PAD_X, pady=PAD_Y)
        self.bom_name_label.grid(row=1, column=1, padx=PAD_X, pady=PAD_Y)
        self.select_file_button.grid(row=1, column=2, sticky='e', padx=PAD_X, pady=PAD_Y)

        self.selecting_frame.grid(row=1, column=0, sticky='w', padx=PAD_X, pady=2*PAD_Y)

        #### File editing section ####
        self.editing_frame = tkinter.Frame(self.main_frame,
                                        bg=bg_color)

        self.bom_editing_label = tkinter.Label(self.editing_frame,
                                        anchor='w',
                                        bg=bg_color,
                                        fg=font_color,
                                        font=division_font,
                                        text='2) Modifier le BOM:')

        self.edit_file_button = tkinter.Button(self.editing_frame,
                                        anchor='w',
                                        font=font,
                                        bg=button_color,
                                        fg=button_font_color,
                                        text='Modifier le fichier dans Excel',
                                        command=self.open_file)

        self.bom_editing_label.grid(row=0, column=0, sticky='w', padx=PAD_X, pady=PAD_Y)
        self.edit_file_button.grid(row=1, column=0, sticky='w', padx=PAD_X, pady=PAD_Y)

        self.editing_frame.grid(row=2, column=0, sticky='w', padx=PAD_X, pady=2*PAD_Y)


        #### Computation section ####
        self.computing_frame = tkinter.Frame(self.main_frame,
                                        bg=bg_color)

        self.calculation_label = tkinter.Label(self.computing_frame,
                                        bg=bg_color,
                                        fg=font_color,
                                        font=division_font,
                                        text='3) Calculer le projet:')

        self.time_estimate_button = tkinter.Button(self.computing_frame,
                                        font=font,
                                        bg=button_color,
                                        fg=button_font_color,
                                        text='Calculer le temps',
                                        command=self.estimate_total_time)


        self.calculation_label.grid(row=0, column=0, sticky='w', padx=PAD_X, pady=PAD_Y)
        self.time_estimate_button.grid(row=1, sticky='w', padx=PAD_X, pady=PAD_Y)
        self.computing_frame.grid(row=3, column=0, sticky='w', padx=PAD_X, pady=2*PAD_Y
        )
        self.main_frame.pack()

def info(message, title="Calcul du temps"):
    root = tkinter.Tk()
    root.overrideredirect(1)
    root.withdraw()
    tkinter.messagebox.showinfo(title, message)
    root.destroy()

def are_you_sure(message, title="ATTENTION"):
    root = tkinter.Tk()
    root.overrideredirect(1)
    root.withdraw()
    decision = tkinter.messagebox.askokcancel(title, message)
    root.destroy()

    print(decision)
    return decision

PROJECT_PATH = './TEST'
BOM_FILE = ''
GUI =  piping_estimator(PROJECT_PATH, BOM_FILE)
