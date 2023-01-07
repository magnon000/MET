"""extract ping data"""
# import math
import re
from tkinter import filedialog  # need pip install
import scipy.io as sio  # need pip install


def get_time(text: str) -> list or None:
    """find the timestamp of each ping and store in a list"""
    regex_exp = r'(2022-1[0-1]-\d{2} \d{2}:\d{2}:\d{2})\n'  # \n to ignore Ping request could not find host
    return re.findall(regex_exp, text, re.S)


def get_delay(text: str) -> list or None:
    """find the delay of each ping and store in a list"""
    regex_exp = r'Average = (\d+?)ms'  # int ms!!!
    return list(map(int, re.findall(regex_exp, text, re.S)))  # use fct map(int, str)


def get_loss(text: str) -> list or None:
    """find the loss percentage and store in a list"""
    regex_exp = r'\((\d+?)% loss\)'  # %!!!
    return list(map(int, re.findall(regex_exp, text, re.S)))


# def calculate_mdev(text: str) -> list or None:  # data exception
#     """calculate standard deviation and store in a list"""
#     regex_exp = r'time=(\d*?)ms'  # every single time record
#     list_raw = re.findall(regex_exp, text, re.S)  # 4 times of list_mdev
#     list_mdev = []
#     index, sum_eles, sum_dev = 0, 0, 0
#     for ele in list_raw:
#         index += 1
#         list_temp.append(ele)
#         if index // 4 == 0:
#             for sub_ele in list_temp:
#                 sum_eles += sub_ele
#             for sub_ele in list_temp:
#                 sum_dev += (sub_ele - sum_eles / 4) ^ 2
#             list_mdev.append(math.sqrt(sum_dev / 4))
#             list_temp = []
#             index, sum_eles, sum_dev = 0, 0, 0
#     return list_mdev


if __name__ == '__main__':
    filename = filedialog.askopenfilename()
    savename = filedialog.asksaveasfilename(title=u'Saving path for MatLab file:', filetypes=[("MAT", ".mat")])
    file = open(filename)
    lines = file.read()
    assert lines != ''
    assert savename != ''
    sio.savemat(savename, {'time': get_time(lines), 'delay': get_delay(lines), 'loss': get_loss(lines)})
