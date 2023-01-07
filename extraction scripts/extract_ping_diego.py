"""extract ping data of diego"""
import re
from tkinter import filedialog  # need pip install
import scipy.io as sio  # need pip install


def get_time(text: str) -> list or None:
    """find the timestamp of each ping and store in a list"""
    regex_exp = r'(\d{2}/\d{2}/\d{2} à \d{2}:\d{2}) sur'  # \n to ignore Ping request could not find host
    return re.findall(regex_exp, text, re.S)


def get_delay(text: str) -> list or None:
    """find the delay of each ping and store in a list"""
    regex_exp = r'/ moy (\d+?) /'  # int ms!!!
    return list(map(int, re.findall(regex_exp, text, re.S)))  # use fct map(int, str)


if __name__ == '__main__':
    filename = filedialog.askopenfilename()
    savename = filedialog.asksaveasfilename(title=u'Saving path for MatLab file:', filetypes=[("MAT", ".mat")])
    file = open(filename)
    lines = file.read()
    assert lines != ''
    assert savename != ''
    sio.savemat(savename, {'time': get_time(lines), 'delay': get_delay(lines)})  # collection txt do not contain loss
