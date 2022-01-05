from tltk.nlp import th2ipa
import re
# text = 'คาค่าค้าขาข่าข้า'
# x = th2ipa(text)
# x = re.split('\.| ', x)
# x.pop(-1)
# print(x)
# y = []
# for i in x:
#     y.append(list(i))
# print(y)


# processString(txt)
def loo(text):
    # พยัญชนะ
    consonants = {'b': 'บ', 'd': 'ด', 'f': ['ฟ', 'ฝ'], 'h': ['ฮ', 'ห'], 'j': ['ย', 'หย'], 'kʰ': ['ค', 'ข'], 'k': 'ก', 'l': ['ล', 'หล'],
                  'm': ['ม', 'หม'], 'n': ['น', 'หน'], 'ŋ': ['ง', 'หง'], 'pʰ': ['พ', 'ผ'], 'p': 'ป', 'r': ['ร', 'หร'], 's': ['ซ', 'ส'], 'tʰ': ['ท', 'ถ'],  'cʰ': ['ช', 'ฉ'], 'c': 'จ', 't': 'ต',  'w': ['ว', 'หว'], 'ʔ': 'อ'}
    # สระเดี่ยวเสียงสั้น
    vowels_short_mono = {'a': ['ะ', 'ั'], 'e': ['เะ', 'เ็'], 'ɛ': ['แะ', 'แ็'], 'i': 'ิ',
                         'o': ['โ◌ะ', ''], 'ɔ': ['เาะ', '็อ'], 'u': 'ุ', 'ɯ': 'ึ', 'ɤ': 'เอะ'}
    # สระเดี่ยวเสียงยาว
    vowels_long_mono = {'aː': 'า', 'e': 'เ◌', 'ɛː': 'แ', 'iː': 'ี',
                        'oː': 'โ', 'ᴐː': 'อ', 'uː': 'ู', 'ɯː': ['ือ', 'ื'], 'ɤː': ['เอ', 'เิ']}
    # สระประสม
    vowels_dip = {'iːa': 'เีย', 'ua': ['ัว', 'ว'], 'ɯa': 'เือ'}
    # สระเกิน
    vowels_syl = {'uːa': ['ัว', 'ว'], 'aj': 'ไ',
                  'aw': 'เา', 'ew': 'เ็ว', 'ɛw': 'แ็ว'}
    # วรรณยุกต์
    tones = {'1': '', '2': '่', '3': '้', '4': '๊', '5': '๋'}
    # Merge Dictionary
    ipa = {**consonants, **vowels_syl, **vowels_dip, **
           vowels_long_mono, **vowels_short_mono, **tones}
    # regex = re.compile('|'.join(map(re.escape, ipa)))
    regex = '|'.join(list(ipa.keys()))
    # print(regex)
    # แบ่งตัวอักษร
    first = re.findall(regex, text)
    last = re.findall(regex, text)
    first = front_loo(first)
    print("Step 2 : ", first)  # หลอก ['l', 'ᴐː', 'k', '2']
    first = ipa2thai(first, ipa)
    print("Step 3 : ", first)
    first = front_rules(first)
    print("Step 4 : ", first)
    print("==========")
    # print('Word: ', l)  # ดอก ['d', 'ᴐː', 'k', '2']
    last = back_loo(last, vowels_syl, vowels_dip, vowels_long_mono,
                    vowels_short_mono)  # ดูก ['d', 'uː', 'k', '2']
    print("Step 2 : ", last)
    last = ipa2thai(last, ipa)
    print("Step 3 : ", last)
    last = back_rules(last)
    print("Step 4 : ", last)
    print("==========")
    return (first, last)


def ipa2thai(text, dictionary):
    # แปลง ipa เป็นตัวอักษรไทย
    ntxt = []
    for char in text:
        if char in dictionary:
            ntxt += [dictionary[char]]
        else:
            ntxt += ['error']
    return ntxt


def front_loo(text):  # pass
    # เปลี่ยนตำแหน่งแรกเป็น ซ หรือ ล
    if text[0] in ['l', 'r']:
        text[0] = 's'
    else:
        text[0] = 'l'
    # ลบพยัญชนะควบกล้ำ
    if text[1] in ['l', 'r']:
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
            if text[index] == 'u':
                text[index] = 'i'
            else:
                text[index] = 'u'
        if char in long:
            index = text.index(char)
            if text[index] == 'uː':
                text[index] = 'iː'
            else:
                text[index] = 'uː'
    return text


def front_rules(text):

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
            if text[-2] in ['ก', 'บ', 'ด']:
                text[-1] = ''
        # อักษรสูง
        else:  # 2,5
            text[0] = text[0][1]
            # รูปสามัญเสียงจัตวาไม่ต้องใส่วรรณยุกต์
            if text[-1] == '๋':
                text[-1] = ''
            # รูปเอกเสียงเอกเขียนด้วยอักษรสูงรูปสามัญเสียงเอก
            if text[-2] in ['ก', 'บ', 'ด']:
                text[-1] = ''

    # อักษรกลางคำตาย ต้องแก้วรรณยุกต์
    if text[-2] in ['ก', 'บ', 'ต']:
        text[-1] = ''
        # สระท้าย
    if len(text[-2]) > 1:
        text[-2] = text[-2][0]
    # สระกลาง
    if len(text[-3]) > 1 and len(text) > 3:
        text[-3] = text[-3][1]
    # สลับตำแหน่งสระ
    # if text[1][0] in ['แ', 'เ']:
    #     text[0], text[1] = text[1][0], text[1].replace(text[1][0], text[0])
    if text[-2] in ["า", "ะ"]:
        text[-2], text[-1] = text[-1], text[-2]
    return text


def back_rules(text):
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
                print("T")
            # รูปตรีเสียงตรีเขียนด้วยอักษรต่ำรูปโทเสียงตรี
            if text[-1] == '๊':
                text[-1] = '้'
            # คำตาย // รอแก้
            if text[-2] in ['ก', 'บ', 'ต']:
                text[-1] = ''
        # อักษรสูง
        else:  # 2,5
            text[0] = text[0][1]
            # รูปสามัญเสียงจัตวาไม่ต้องใส่วรรณยุกต์
            if text[-1] == '๋':
                text[-1] = ''
            # คำตาย // รอแก้
            if text[-2] in ['ก', 'บ', 'ต']:
                text[-1] = ''

    # อักษรกลางคำตาย ต้องแก้วรรณยุกต์
    if text[-2] in ['ก', 'บ', 'ด']:
        text[-1] = ''
        # สระท้าย
    if len(text[-2]) > 1:
        text[-2] = text[-2][0]
    # สระกลาง
    if len(text[-3]) > 1 and len(text) > 3:
        text[-3] = text[-3][1]
    return text


while(True):
    text = input("พิมพ์ข้อความที่ต้องการแปลงเป็นภาษาลู: ")
    text = th2ipa(text)  # แปลงภาษาไทยเป็น ipa
    text = re.split('\.| ', text)  # แบ่งคำโดยแปลงเป็น lists
    text.pop(-1)
    print("Step 1 : ", text)
    print("==========")
    for syllable in text:
        r, l = loo(syllable)
        str1 = ''
        str2 = ''
        str1 = str1.join(r)
        str2 = str2.join(l)
        print(str1, str2)
