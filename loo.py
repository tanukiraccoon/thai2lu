from tltk.nlp import th2ipa
import re


def loo(text):
    # พยัญชนะ
    consonants = {'b': 'บ', 'd': 'ด', 'f': ['ฟ', 'ฝ'], 'h': ['ฮ', 'ห'], 'j': ['ย', 'หย'], 'kʰ': ['ค', 'ข'], 'k': 'ก', 'l': ['ล', 'หล'],
                  'm': ['ม', 'หม'], 'n': ['น', 'หน'], 'ŋ': ['ง', 'หง'], 'pʰ': ['พ', 'ผ'], 'p': 'ป', 'r': ['ร', 'หร'], 's': ['ซ', 'ส'], 'tʰ': ['ท', 'ถ'],  'cʰ': ['ช', 'ฉ'], 'c': 'จ', 't': 'ต',  'w': ['ว', 'หว'], 'ʔ': 'อ'}

    # สระเดี่ยวเสียงสั้น
    vowels_short_mono = {'a': ['ะ', 'ั'], 'e': ['เะ', 'เ็'], 'ɛ': ['แะ', 'แ็'], 'i': 'ิ',
                         'o': ['โะ', ' '], 'ᴐ': ['เาะ', '็อ'], 'u': 'ุ', 'ɯ': 'ึ', 'ɤ': ['เอะ', '']}

    # สระเดี่ยวเสียงยาว
    vowels_long_mono = {'aː': 'า', 'eː': 'เ', 'ɛː': 'แ', 'iː': 'ี',
                        'oː': 'โ', 'ᴐː': 'อ', 'uː': 'ู', 'ɯː': ['ือ', 'ื'], 'ɤː': ['เอ', 'เิ']}

    # สระประสม
    vowels_dip = {'iːa': ['เีย', 'เีย'], 'ua': ['ัว', 'ว'], 'ɯa': ['เือ', '']}

    # สระเกิน
    vowels_syl = {'aw': ['เา', ''], 'uːa': ['ัว', 'ว'], 'ɯːa': ['เือ', 'เือ']}

    # วรรณยุกต์
    tones = {'1': '', '2': '่', '3': '้', '4': '๊', '5': '๋'}

    # Merge Dictionary
    ipa = {**consonants, **vowels_syl, **vowels_dip, **
           vowels_long_mono, **vowels_short_mono, **tones}
    # regex = re.compile('|'.join(map(re.escape, ipa)))
    regex = '|'.join(list(ipa.keys()))

    # แบ่ง ipa เป็นลิสต์
    first = re.findall(regex, text)
    last = re.findall(regex, text)
    print("Step 1 : ", first)
    if first:
        # ทำลูหน้า เปลี่ยนพยัญชนะต้นเป็น l, r หรือ s
        first = front_loo(first)
        print("Step 2 : ", first)  # หลอก ['l', 'ᴐː', 'k', '2']
        # เปลี่ยน ipa เป็นตัวอักษรไทย
        first = ipa2thai(first, ipa)
        print("Step 3 : ", first)
        # เปลี่ยนพยัญชนะต้น พยัญชนะท้าย วรรณยุกต์ ตามอักษรสูงกลางต่ำ และคำเป็นคำตาย
        first = front_rules(first, vowels_short_mono)
        print("Step 4 : ", first)
        print("==========")

        # print('Word: ', l)  # ดอก ['d', 'ᴐː', 'k', '2']
        last = back_loo(last, vowels_syl, vowels_dip, vowels_long_mono,
                        vowels_short_mono)  # ดูก ['d', 'uː', 'k', '2']
        print("Step 2 : ", last)
        last = ipa2thai(last, ipa)
        print("Step 3 : ", last)
        last = back_rules(last, vowels_short_mono)
        print("Step 4 : ", last)
        print("==========")
        return (first, last)
    return("error", "error")


def ipa2thai(text, dictionary):
    # แปลง ipa เป็นตัวอักษรไทย
    ntxt = []
    for char in text:
        if char in dictionary:
            ntxt += [dictionary[char]]
        else:
            ntxt += ['error']
            print('Not Found Character in Dictionary: ', char)
            exit()
    return ntxt


def front_loo(text):

    # เปลี่ยนตำแหน่งแรกเป็น ซ หรือ ล
    if text[0] in ['l', 'r']:
        text[0] = 's'
    else:
        text[0] = 'l'

    # ลบพยัญชนะควบกล้ำ
    if text[1] in ['l', 'r', 'w']:
        text.pop(1)
    return text


def back_loo(text, vs, vd, vlm, vsm):
    # เปลี่ยนสระของคำเป็นสระ "อุ" หรือ "อู"
    short = list(vsm.keys())
    long = list(vs.keys()) + list(vd.keys()) + list(vlm.keys())
    for char in text:
        # สระเดี่ยวเสียงสั้นเปลี่ยนเป็นสระอุ
        if char in short:
            index = text.index(char)
            # ถ้าเป็นสระ อุ เปลี่ยนเป็นสระ อิ
            if text[index] == 'u':
                text[index] = 'i'
            else:
                text[index] = 'u'
        if char in long:
            index = text.index(char)
            # ถ้าเป็นสระ อู เปลี่ยนเป็นสระ อี
            if text[index] == 'uː':
                text[index] = 'iː'
            else:
                text[index] = 'uː'
    return text


def front_rules(text, vsm):

    # เปลี่ยนพยัญชนะท้าย ต เป็น ด // รอเขียนอัลกอรืทึมใหม่
    if text[-2] == 'ต':
        text[-2] = 'ด'
    # เปลี่ยนพยัญชนะท้าย ป เป็น บ // รอเขียนอัลกอรืทึมใหม่
    if text[-2] == 'ป':
        text[-2] = 'บ'
    if len(text[0]) > 1:
        # อักษรต่ำ
        if text[-1] in ['', '้', '๊']:  # 1,3,4
            text[0] = text[0][0]
            # รูปโทเสียงโทเขียนด้วยอักษรต่ำรูปเอกเสียงโท
            if text[-1] == '้':
                text[-1] = '่'
            # รูปตรีเสียงตรีเขียนด้วยอักษรต่ำรูปโทเสียงตรี
            if text[-1] == '๊':
                text[-1] = '้'
                # คำตาย // รอแก้
            if text[-2] in ['ก', 'บ', 'ด'] or text[-2] in list(vsm.values()):
                text[-1] = ''
        # อักษรสูง
        else:  # 2,5
            text[0] = text[0][1]
            # รูปสามัญเสียงจัตวาไม่ต้องใส่วรรณยุกต์
            if text[-1] == '๋':
                text[-1] = ''
            # รูปเอกเสียงเอกเขียนด้วยอักษรสูงรูปสามัญเสียงเอก
            if text[-2] in ['ก', 'บ', 'ด'] or text[-2] in list(vsm.values()):
                text[-1] = ''

    # อักษรกลางคำตาย ต้องแก้วรรณยุกต์
    if text[-2] in ['ก', 'บ', 'ต']:
        text[-1] = ''
        # สระท้าย
    if len(text[-2]) > 1:
        if text[-2][0] == "ือ":
            text[-2] = 'ื'
            text.insert(-1, 'อ')
        elif text[-2][0] == "เา":
            text[-2] = 'เ'
            text.insert(-1, 'า')
        else:
            text[-2] = text[-2][0]
    # สระกลาง
    if len(text[-3]) > 1 and len(text) > 3:
        if text[-3][1] == 'เิ' and text[-2] == 'ย':
            text[-3] = 'เ'
        else:
            text[-3] = text[-3][1]

    # สลับตำแหน่งวรณยุกต์
    text.insert(2, text[-1])
    text.pop(-1)
    # สลับตำแหน่งสระ
    if text[1][0] in ['แ', 'เ', 'โ', 'ไ']:
        text[0], text[1] = text[1][0], text[1].replace(text[1][0], text[0])
    # สลับวรรณยุกต์
    if text[-2] in ["า", "ะ", "อ"]:
        text[-2], text[-1] = text[-1], text[-2]
    elif text[1] in ["า", "ะ", "อ", "ว"]:
        text[1], text[2] = text[2], text[1]
    # สระโอะไม่มีรูป
    if text[1] == ' ':
        text.pop(1)
    return text


def back_rules(text, vsm):
    # พยัญชนะควบกล้ำใช้ ล ร
    if len(text[1]) > 1:
        text[1] = text[1][0]

    # เปลี่ยนพยัญชนะท้าย ต เป็น ด // รอเขียนอัลกอรืทึมใหม่
    if text[-2] == 'ต':
        text[-2] = 'ด'
    # เปลี่ยนพยัญชนะท้าย ป เป็น บ // รอเขียนอัลกอรืทึมใหม่
    if text[-2] == 'ป':
        text[-2] = 'บ'
    if len(text[0]) > 1:
        # อักษรต่ำ
        if text[-1] in ['', '้', '๊']:  # 1,3,4
            text[0] = text[0][0]
            # รูปโทเสียงโทเขียนด้วยอักษรต่ำรูปเอกเสียงโท
            if text[-1] == '้':
                text[-1] = '่'
            # รูปตรีเสียงตรีเขียนด้วยอักษรต่ำรูปโทเสียงตรี
            if text[-1] == '๊':
                text[-1] = '้'
            # คำตาย // รอแก้
            if text[-2] in ['ก', 'บ', 'ต'] or text[-2] in list(vsm.values()):
                text[-1] = ''
        # อักษรสูง
        else:  # 2,5
            text[0] = text[0][1]
            # รูปสามัญเสียงจัตวาไม่ต้องใส่วรรณยุกต์
            if text[-1] == '๋':
                text[-1] = ''
            # คำตาย // รอแก้
            if text[-2] in ['ก', 'บ', 'ต'] or text[-2] in list(vsm.values()):
                text[-1] = ''

    # อักษรกลางคำตาย ต้องแก้วรรณยุกต์
    if text[-2] in ['ก', 'บ', 'ด', 'ิ', 'ุ']:
        text[-1] = ''
        # สระท้าย
    if len(text[-2]) > 1:
        text[-2] = text[-2][0]
    # สระกลาง
    if len(text[-3]) > 1 and len(text) > 3:
        text[-3] = text[-3][1]
    # สลับตำแหน่งวรณยุกต์
    text.insert(2, text[-1])
    text.pop(-1)
    return text


def use_loo(text):
    # text = input("พิมพ์ข้อความที่ต้องการแปลงเป็นภาษาลู: ")
    text = th2ipa(text)  # แปลงภาษาไทยเป็น ipa
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
