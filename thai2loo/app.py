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
                  'm': ['ม', 'หม'], 'n': ['น', 'หน'], 'ŋ': ['ง', 'หง'], 'pʰ': ['พ', 'ผ'], 'p': 'ป', 'r': ['ร', 'หร'], 's': ['ซ', 'ส'], 'tʰ': ['ท', 'ถ'],  'tɕʰ': ['ช', 'ฉ'], 'tɕ': 'จ', 't': 'ต',  'w': ['ว', 'หว'], 'ʔ': 'อ'}
    # สระเดี่ยวเสียงสั้น
    vowels_short_mono = {'a': ['◌ะ', '◌ั'], 'e': ['เ◌ะ', 'เ◌็◌'], 'ɛ': ['แ◌ะ', 'แ◌็◌'], 'i': '◌ิ',
                         'o': ['โ◌ะ', ''], 'ɔ': ['เ◌าะ', '◌็อ'], 'u': '◌ุ', 'ɯ': '◌ึ', 'ɤ': 'เ◌อะ'}
    # สระเดี่ยวเสียงยาว
    vowels_long_mono = {'aː': 'า', 'e': 'เ◌', 'ɛː': 'แ', 'iː': '◌ี',
                        'oː': 'โ', 'ɔː': 'อ', 'uː': '◌ู', 'ɯː': ['◌ือ', '◌ื'], 'ɤː': ['เ◌อ', 'เ◌ิ◌']}
    # สระประสม
    vowels_dip = {'ia': 'เ◌ีย', 'ua': ['◌ัว', 'ว'], 'ɯa': 'เ◌ือ'}
    # สระเกิน
    # vowels_syl = {'aj': 'ไ◌','aw':'เ◌า','ew': 'เ◌็ว','ɛw':'แ◌็ว','uj':}
    # วรรณยุกต์
    tones = {'1': '-', '2': '่', '3': '้', '4': '๊', '5': '๋'}
    # Merge Dictionary
    ipa = {**consonants, **vowels_dip, **
           vowels_long_mono, **vowels_short_mono, **tones}
    # regex = re.compile('|'.join(map(re.escape, ipa)))
    regex = '|'.join(list(ipa.keys()))
    # print(regex)
    # แบ่งตัวอักษร
    r = re.findall(regex, text)
    l = re.findall(regex, text)
    # print('Word: ', l)
    l = thai2loo_l(l, vowels_dip, vowels_long_mono, vowels_short_mono)
    # print("Last: ", l)
    # print("ipa: ", ipa2thai(l, ipa))
    # print("cvRule: ", cvRules(ipa2thai(l, ipa)))
    r = thai2loo_f(r)
    # print('First:', r)
    # print("ipa: ", ipa2thai(r, ipa))
    # print("cvRule: ", cvRules(ipa2thai(r, ipa)))
    # regex.sub(lambda match: transliterate[match.group()], ls_to_str)
    # return ipa2thai(r, ipa)


def ipa2thai(text, dictionary):
    # แปลง ipa เป็นตัวอักษรไทย
    ntxt = []
    for char in text:
        if char in dictionary:
            ntxt += [dictionary[char]]
        else:
            ntxt += ['error']
    return ntxt


def thai2loo_l(text, vd, vlm, vsm):
    # เปลี่ยนสระของคำเป็นสระ "อุ" หรือ "อู"
    short = list(vsm.keys())
    long = list(vd.keys()) + list(vlm.keys())
    for char in text:
        # สระเดี่ยวเสียงสั้นเปลี่ยนเป็นสระอุ
        if char in short:
            index = text.index(char)
            text[index] = 'uː'
        if char in long:
            index = text.index(char)
            text[index] = 'u'
    return text


def thai2loo_f(text):
    # เปลี่ยนตำแหน่งแรกเป็น ซ หรือ ล
    if text[0] == 'l':
        text[0] = 's'
    else:
        text[0] = 'l'
    if text[1] in ['l', 'r']:
        text.pop(1)
    return text


def cvRules(text):
    if len(text[0]) > 1:
        # อักษรต่ำ
        if text[-1] in ['-', '้', '๊']:
            text[0] = text[0][0]
        # อักษรสูง
        else:
            text[0] = text[0][1]
    # สระท้าย
    if len(text[-2]) > 1:
        text[-2] = text[-2][0]
    # สระกลาง
    if len(text[-3]) > 1 and len(text) > 3:
        text[-3] = text[-3][1]
    return text


text = "สา"
text = th2ipa(text)
text = re.split('\.| ', text)
text.pop(-1)
print("IPA: ", text)
for syllable in text:
    tran = loo(syllable)
    # print("Result: ", tran)
