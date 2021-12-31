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
def custom_make_translation(text):
    consonants = {'b': 'บ', 'd': 'ด', 'f': ['ฝ', 'ฟ'], 'h': ['ห', 'ฮ'], 'j': ['หย', 'ย'], 'k': 'ก', 'kʰ': 'ข,ค', 'l': ['หล', 'ล'],
                  'm': ['หม', 'ม'], 'n': ['หน', 'น'], 'ŋ': ['หง', 'ง'], 'pʰ': ['ผ', 'พ'], 'p': 'ป', 'r': ['หร', 'ร'], 's': 'ซ', 'tʰ': ['ถ', 'ท'],  'tɕʰ': ['ฉ', 'ช'], 'tɕ': 'จ', 't': 'ต',  'w': ['หว', 'ว'], 'ʔ': 'อ'}
    vowels_short_mono = {'a': '◌, ◌ะ, ◌ั◌', 'e': 'เ◌ะ, เ◌็◌', 'ɛ': 'แ◌ะ, แ◌็◌', 'i': '◌ิ, ◌ิ◌',
                         'o': 'โ◌ะ, ◌◌', 'ɔ': 'เ◌าะ, ◌็อ', 'u': '◌ุ, ◌ุ◌ุ', 'ɯ': '◌ึ', 'ɤ': 'เ◌อะ'}
    vowels_long_mono = {'aː': '◌า, ◌า◌', 'e': 'เ◌, เ◌◌', 'ɛː': 'แ◌, แ◌◌', 'iː': '◌ี, ◌ี◌',
                        'oː': 'โ◌, โ◌◌', 'ɔː': '◌, ◌อ, ◌อ◌', 'uː': '◌ู, ◌ู◌', 'ɯː': '◌ือ, ◌ื◌', 'ɤː': 'เ◌อ, เ◌ิ◌'}
    vowels_dip = {'ia': 'เ◌ีย, เ◌ีย◌', 'ua': '◌ัว, ◌ว◌', 'ɯa': 'เ◌ือ, เ◌ือ◌'}
    vowels_syl = {'aj': 'ไ◌'}
    tones = {'1': '-', '2': '่', '3': '้', '4': '๊', '5': '๋'}
    transliterate = {**consonants, **vowels_syl, **vowels_dip, **
                     vowels_long_mono, **vowels_short_mono, **tones}
    regex = re.compile('|'.join(map(re.escape, transliterate)))
    print(regex)
    r = re.findall(regex, text)
    print('Before:', r)
    r = thai2loo(r)
    print('After:', r)
    ntxt = []
    for char in r:
        if char in transliterate:
            ntxt += [transliterate[char]]
        else:
            ntxt += ['error']

    # regex.sub(lambda match: transliterate[match.group()], ls_to_str)
    return ntxt


def thai2loo(text):
    loo = text
    # เปลี่ยนตำแหน่งแรกเป็น ซ หรือ ล
    if loo[0] == 'l':
        loo[0] = 's'
    else:
        loo[0] = 'l'
    return loo


text = "วัย"
text = th2ipa(text)
text = re.split('\.| ', text)
text.pop(-1)
print(text)
for syllable in text:
    transliterate = custom_make_translation(syllable)
    if transliterate[-1] == '-':
        transliterate[0] = transliterate[0][1]
    print(transliterate)
