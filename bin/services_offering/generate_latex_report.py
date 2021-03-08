import os
import datetime
import subprocess

class ReportBuilder:
    page_header = r'''
                  \documentclass{article}
                  \usepackage[T1]{fontenc}
                  \usepackage[french]{babel}
                  \begin{document}
                  ''' + "\n"

    page_footer = r"\end{document}"

    months = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "novembre", "décembre"]

    newline = r"\newline "
    def __init__(self):
        pass

    def building_mechanics(self, work_dir, data):
        main_tex_file = os.path.join(work_dir, 'ods.tex')
        address_tex_file = os.path.join(work_dir, 'address.tex')
        introduction_tex_file = os.path.join(work_dir, 'introduction.tex')
        mandate_tex_file = os.path.join(work_dir, 'mandate.tex')
        pricing_tex_file = os.path.join(work_dir, 'pricing.tex')
        signature_tex_file = os.path.join(work_dir, 'client_signature.tex')

        with open(address_tex_file, 'w', encoding='utf-8') as f:
            content = r'%s %s\\' % (data['contact_fname'], data['contact_name'])
            content += r'%s\\' % (data['client_company'])
            content += r'%s\\' % (data['client_address'])
            content += r'%s, %s, %s\\' % (data['client_city'], data['client_province'], data['client_zip'])

            f.write(content)

        with open(introduction_tex_file, 'w', encoding='utf-8') as f:
            content = r'SUJET: Offre de services - %s \par ' % (data['project_name'])
            content += r'Bonjour %s, voici notre offre de services pour le projet: %s .' % (data['contact_fname'], data['project_name'])

            f.write(content)

        with open(mandate_tex_file, 'w', encoding='utf-8') as f:
            content = r'DESCRIPTION DU MANDAT\\ '
            content += r'%s' % (data['mandate'])
            categories = ['mec_inc',
                          'mec_exc',
                          'elec_inc',
                          'elec_exc']
            cat_descriptions = ['Inclusions mécaniques:',
                                'Exclusions mécaniques:',
                                'Inclusions électriques:',
                                'Exclusions électriques:']

            for c in range(len(categories)):
                if categories[c] in data:
                    if len(data[categories[c]]) > 0:
                        content += r'\par\underline{%s}\begin{itemize} ' % (cat_descriptions[c])
                        for item in data[categories[c]]:
                            content += r'\item[\textbullet] %s' % (item)
                        content += r'\end{itemize}'

            f.write(content)

        with open(pricing_tex_file, 'w', encoding='utf-8') as f:
            content = r'HONORAIRES* \\ '
            content += r'\begin{center}\begin{tabular}{l@{\hspace{1cm}}|c@{\hspace{1cm}}}'

            for p in range(len(data['prices'])):
                content += r'%s & %s \$  \\ \hline ' % (data['price_descriptions'][p], data['prices'][p])

            total_price = str(sum([int(p) for p in data['prices']]))
            content += r'\textbf{TOTAL} & \textbf{ %s \$} \\ ' % (total_price)
            content += r'\end{tabular} \end{center} '
            content += r'\small{* Ces taux excluent les taxes applicables } '

            f.write(content)

        with open(signature_tex_file, 'w', encoding='utf-8') as f:
            content = r'%s %s \\' % (data['contact_fname'], data['contact_name'])
            content += r'%s \\' % (data['client_company'])

            f.write(content)

        cmd = ['pdflatex', main_tex_file]
        proc = subprocess.Popen(cmd, cwd=work_dir)
        proc.communicate()

        return 'ods.pdf'