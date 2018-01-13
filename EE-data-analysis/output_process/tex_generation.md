\documentclass{oblivoir}

\setmainfont{NanumGothic}

\begin{document}

{\Large{$send_address}{$send_name}}
{\LARGE $send_zipcodeA}
{\LARGE $send_zipcodeB}

{\Large {$recv_address}{$recv_name}}
{\LARGE $recv_zipcodeA}
{\LARGE $recv_zipcodeB}

\end{document}




# -*- coding: utf-8 -*-

import os
import tempfile
import shutil
import subprocess
from string import Template


baseDir = os.path.dirname(os.path.abspath(__file__))
templatefile = 'template.tex'


def makePDF():
    texfile = os.path.join(baseDir, templatefile)
    with open(texfile) as template:
        template = template.read().decode('utf-8')
    texsource = Template(template)

    tmpfolder = tempfile.mkdtemp()
    os.chdir(tmpfolder)

    d = {'send_address': 'Newyork, US',
         'send_name': 'Gabdol',
         'send_zipcodeA': '111',
         'send_zipcodeB': '222',
         'recv_address': 'Chicago, US',
         'recv_name': 'Gabsun',
         'recv_zipcodeA': '333',
         'recv_zipcodeB': '444'
         }
    texcode = texsource.substitute(d)
    with open('letter.tex', 'w') as tex:
        tex.write(texcode.encode('utf-8'))
    cmd = 'xelatex letter'
    subprocess.call(cmd, shell=True)
    shutil.copyfile('letter.pdf', os.path.join(baseDir, 'myletter.pdf'))
    shutil.rmtree(tmpfolder)


if __name__ == '__main__':
    makePDF()
