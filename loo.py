import tltk
import re


def use_loo(text):
    # text = input("พิมพ์ข้อความที่ต้องการแปลงเป็นภาษาลู: ")

    print("Step -1 : ", text)
    text = re.split('\.| ', text)  # แบ่งคำโดยแปลงเป็น lists
    text.pop(-1)
    print("Step 0 : ", text)
    print("==========")
    x = ''
    for syllable in text:
        r, l = loo(syllable)
        str1 = ''
        str2 = ''
        str1 = str1.join(r)
        str2 = str2.join(l)
        x += str1 + ' ' + str2 + ' '
        print(x)
    return (x)
