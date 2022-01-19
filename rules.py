from tltk.nlp import th2ipa


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
            print("Hi")
            text[0] = text[0][1]
            # รูปสามัญเสียงจัตวาไม่ต้องใส่วรรณยุกต์
            if text[-1] == '๋':
                text[-1] = ''
            # รูปเอกเสียงเอกเขียนด้วยอักษรสูงรูปสามัญเสียงเอก
            print(text[-2])
            if text[-2] in ['ก', 'บ', 'ด'] or text[-2] in list(vsm.values()):
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
    print(text)
    if text[1][0] in ['แ', 'เ', 'โ', 'ไ']:
        text[0], text[1] = text[1][0], text[1].replace(text[1][0], text[0])
    if text[-2] in ["า", "ะ"]:
        text[-2], text[-1] = text[-1], text[-2]
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
    if text[-2] in ['ก', 'บ', 'ด']:
        text[-1] = ''
        # สระท้าย
    if len(text[-2]) > 1:
        text[-2] = text[-2][0]
    # สระกลาง
    if len(text[-3]) > 1 and len(text) > 3:
        text[-3] = text[-3][1]
    return text
