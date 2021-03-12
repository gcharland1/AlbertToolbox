import os
import unidecode
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

    def building_mechanics(self, work_dir, data, save_dir=None):
        if not save_dir:
            save_dir = work_dir

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
            categories = data['mandate_details'].keys()

            for c in categories:
                if len(data['mandate_details'][c]) > 0:
                    content += r'\par\underline{%s }: \par\begin{itemize} ' % (c)
                    for item in data['mandate_details'][c]:
                        content += r'\item[\textbullet] %s' % (item)
                    content += r'\end{itemize}\vspace{0.5cm}'

            f.write(content)

        with open(pricing_tex_file, 'w', encoding='utf-8') as f:
            content = r'HONORAIRES* \\ '
            content += r'\begin{center}\begin{tabular}{l@{\hspace{1cm}}|c@{\hspace{1cm}}}'

            fixed_price = True
            for p in range(len(data['prices'])):
                if p < len(data['prices'])-1:
                    content += r'%s & %s %s \\ \hline ' % (data['price_descriptions'][p], data['prices'][p], data['price_units'][p].replace('$', r'\$'))
                else:
                    content += r'%s & %s %s \\ ' % (data['price_descriptions'][p], data['prices'][p], data['price_units'][p].replace('$', r'\$'))
                if not data['price_units'][p] == '$':
                    fixed_price = False

            if fixed_price:
                total_price = str(sum([int(p) for p in data['prices']]))
                content += r'\hline \textbf{TOTAL} & \textbf{ %s \$} \\ ' % (total_price)

            content += r'\end{tabular} \end{center} '
            content += r'\small{* Ces taux excluent les taxes applicables } '

            f.write(content)

        with open(signature_tex_file, 'w', encoding='utf-8') as f:
            content = r'%s %s \\' % (data['contact_fname'], data['contact_name'])
            content += r'%s \\' % (data['client_company'])

            f.write(content)

        cmd = ["pdflatex", main_tex_file]
        proc = subprocess.Popen(cmd, cwd=work_dir)
        proc.communicate()


        pdf_file_name = unidecode.unidecode(data['project_number'] + "_" + data['project_name'].replace(' ', '_') + '.pdf')
        print(pdf_file_name)
        if os.path.isfile(os.path.join(save_dir, pdf_file_name)):
            os.remove(os.path.join(save_dir, pdf_file_name))

        if os.path.isfile(os.path.join(work_dir, 'ods.aux')):
            os.remove(os.path.join(work_dir, 'ods.aux'))

        os.rename(os.path.join(work_dir, 'ods.pdf'), os.path.join(save_dir, pdf_file_name))

        return pdf_file_name