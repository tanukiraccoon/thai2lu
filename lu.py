import re
import copy
import csv
from datetime import datetime
from tltk.nlp import th2ipa

I_CONSONANTS = {
    'b': 'บ',
    'd': 'ด',
    'f': ['ฟ', 'ฝ'],
    'h': ['ฮ', 'ห'],
    'j': ['ย', 'หย'],
    'k': 'ก',
    'kʰ': ['ค', 'ข'],
    'l': ['ล', 'หล'],
    'm': ['ม', 'หม'],
    'n': ['น', 'หน'],
    'ŋ': ['ง', 'หง'],
    'pʰ': ['พ', 'ผ'],
    'p': 'ป',
    'r': ['ร', 'หร'],
    's': ['ซ', 'ส'],
    'tʰ': ['ท', 'ถ'],
    'c': 'จ',
    'cʰ': ['ช', 'ฉ'],
    't': 'ต',
    'w': ['ว', 'หว'],
    'ʔ': 'อ'
}

blend = {
    'l': 'ล',
    'r': 'ร',
    'w': 'ว'
}

F_CONSONANTS = {
    'j': 'ย',
    'k': 'ก',
    'm': 'ม',
    'n': 'น',
    'ŋ': 'ง',
    'p': 'บ',
    't': 'ด',
    'w': 'ว',
    'ʔ': 'อ'
}
S_VOWELS = {
    'ia': 'เอี-ยะ',
    'a': ['อ-ะ', 'อั-', 'เอ-า'],
    'e': ['เอ-ะ', 'เอ็-'],
    'ɛ': ['แอ-ะ', 'แอ-'],
    'i': 'อิ-',
    'o': ['โอ-ะ', 'อ-'],
    'ᴐ': ['เอ-าะ', 'อ-อ'],
    'u': 'อุ-',
    'ɯ': 'อึ-',
    'ɤ': 'เอ-ะ'
}
L_VOWELS = {
    'iːa': 'เอี-ย',
    'uːa': ['อั-ว', 'อ-ว'],
    'ɯːa': 'เอื-อ',
    'aː': 'อ-า',
    'eː': 'เอ-',
    'ɛː': 'แอ-',
    'iː': 'อี-',
    'oː': 'โอ-',
    'ᴐː': 'อ-อ',
    'uː': 'อู-',
    'ɯː': ['อื-อ', 'อื-'],
    'ɤː': ['เอ-อ', 'เอิ-', 'เอ-']
}
TONE_MARKS = {
    '1': '',
    '2': '่',
    '3': '้',
    '4': '๊',
    '5': '๋',
    '8': '่'
}

C_PATTERN = '|'.join(list(I_CONSONANTS))
SL_VOWELS = S_VOWELS | L_VOWELS
V_PATTERN = '|'.join(list(SL_VOWELS))
T_PATTERN = '|'.join(list(TONE_MARKS))


class Lu():

    initial = None
    blend = None
    vowel = None
    final = None
    tone = None
    syl = None
    cls = None
    snd = None

    def __init__(self, ipa: str = None):
        if not ipa:
            return
        con_list = re.findall(rf'[{C_PATTERN}]+', ipa)
        if len(con_list) > 1:
            self.initial = con_list[0]
            self.final = con_list[1]
        else:
            self.initial = con_list[0]
        if len(self.initial) > 1 and self.initial[-1] in ['l', 'r', 'w']:
            self.blend = self.initial[-1]
            self.initial = self.initial[:-1]
        vowel_list = re.findall(rf'[{V_PATTERN}]+', ipa)
        self.vowel = vowel_list[0]
        tone_list = re.findall(T_PATTERN, ipa)
        self.tone = tone_list[0]
        self.syl = self.check_syllable()
        self.cls = self.check_class()
        self.snd = self.check_sound()

    # Need to refactoring
    def to_lu(self) -> list:

        head = copy.deepcopy(self)
        tail = copy.deepcopy(self)

        # Head Lu
        if head.initial in list(I_CONSONANTS):
            if head.initial in ['l', 'r']:
                head.initial = 's'
            else:
                head.initial = 'l'
            head.cls = head.check_class()
            head.initial = I_CONSONANTS[head.initial]

            if len(head.initial) > 1 and head.tone == '2' or (head.tone == '5' and head.syl == 'Live'):
                head.initial = head.initial[1]
            else:
                head.initial = head.initial[0]

        head.blend = None

        if head.vowel in list(SL_VOWELS):
            vowel_syl = head.vowel
            head.vowel = SL_VOWELS[head.vowel]

        # Multiple figures exist for some vowels. We need to select them.
        if isinstance(head.vowel, list):
            # Choose a vowel figure without a final consonant.
            if head.final is None:
                head.vowel = head.vowel[0]
            # Choose a vowel figure with a final consonant.
            else:
                # Choose a vowel figure with 'j' or 'w' as the final consonant.
                if vowel_syl == 'ɤː' and head.final == 'j':
                    head.vowel = head.vowel[2]
                elif vowel_syl == 'a' and head.final == 'w':
                    head.vowel = head.vowel[2]
                    head.final = None
                else:
                    head.vowel = head.vowel[1]

        # Change final consonant to Thai char
        if head.final in list(F_CONSONANTS):
            head.final = F_CONSONANTS[head.final]

        # Convert tone base on dead or live syllables
        if head.tone in list(TONE_MARKS):
            head.tone = head.tone_shift()

        # Fix 'อ็' aka 'เอะ' sound without  ็ character when not a first tone
        if 'อ็' in head.vowel and head.tone not in ['1']:
            head.vowel = head.vowel.replace('อ็', 'อ')

        # Change tone to Thai char
        if head.tone in list(TONE_MARKS):
            head.tone = TONE_MARKS[head.tone]

        # Tail Lu
        if tail.initial in list(I_CONSONANTS):
            tail.cls = tail.check_class()
            tail.initial = I_CONSONANTS[tail.initial]
            if len(tail.initial) > 1 and (tail.tone == '2' or (tail.tone == '5' and tail.syl == 'Live')):
                tail.initial = tail.initial[1]
            else:
                tail.initial = tail.initial[0]

        if tail.blend in list(blend):
            tail.blend = blend[tail.blend]

        if tail.snd == 'Long':
            if tail.vowel == 'uː':
                tail.vowel = 'iː'
            else:
                tail.vowel = 'uː'
        else:
            if tail.vowel == 'u':
                tail.vowel = 'i'
            else:
                tail.vowel = 'u'

        if tail.vowel in (SL_VOWELS):
            tail.vowel = SL_VOWELS[tail.vowel]

        if tail.final in (F_CONSONANTS):
            tail.final = F_CONSONANTS[tail.final]

        if tail.tone in list(TONE_MARKS):
            tail.tone = tail.tone_shift()

        if 'อ็' in tail.vowel and tail.tone not in ['1']:
            tail.vowel = tail.vowel.replace('อ็', 'อ')

        if tail.tone in list(TONE_MARKS):
            tail.tone = TONE_MARKS[tail.tone]

        # Combine Head
        head_word = head.initial
        head_word = head.vowel.replace('อ', head_word, 1)
        head_word = head_word.replace('-', head.tone)
        if head.final is not None:
            head_word += head.final

        # Combine Tail
        tail_word = tail.initial
        if tail.blend is not None:
            tail_word += tail.blend
        tail_word = tail.vowel.replace('อ', tail_word, 1)
        tail_word = tail_word.replace('-', tail.tone)
        if tail.final is not None:
            tail_word += tail.final
        return [head_word, tail_word]

    def details(self):
        print([self.initial, self.blend, self.vowel,
              self.final, self.tone, self.cls,
              self.syl, self.snd])

    def check_syllable(self) -> str:
        if (self.final is None and 'ː' not in self.vowel) or self.final in ['k', 't', 'p']:
            return 'Dead'
        return 'Live'

    def check_class(self) -> str:
        if len(I_CONSONANTS[self.initial]) > 1:
            if self.tone == '2' or (self.tone == '5' and self.syl == 'Live'):
                return 'High'
            return 'Low'
        return 'Mid'

    def check_sound(self) -> str:
        return 'Long' if 'ː' in self.vowel else 'Short'

    # Need to refactoring
    def tone_shift(self) -> str:
        if self.cls == 'Mid' and self.syl == 'Dead' and self.tone == '2':
            return '1'
        if self.cls == 'High':
            if self.syl == 'Live' and self.tone == '5':
                return '1'
            if self.syl == 'Dead' and self.tone == '2':
                return '1'
        elif self.cls == 'Low':
            if self.syl == 'Live':
                if self.tone == '3':
                    return '2'
                if self.tone == '4':
                    return '3'
            elif self.syl == 'Dead':
                if self.snd == 'Short':
                    if self.tone == '3':
                        return '2'
                    if self.tone == '4':
                        return '1'
                elif self.snd == 'Long':
                    if self.tone == '3':
                        return '1'
                    if self.tone == '4':
                        return '3'
        return self.tone


def to_ipa(text: str):
    lst = []
    text_ipa = th2ipa(text)
    split_ipa = re.split('[\\.\\s]', text_ipa.replace(' <s/>', ''))
    for ipa in split_ipa:
        result = Lu(ipa)
        lst.append(result)
    return lst


def to_csv(text: str, obj: object, result: str):
    with open('log.csv', 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        date = datetime.now()
        writer.writerow([date, text, obj.initial, obj.blend, obj.vowel,
                        obj.final, obj.tone, obj.cls, obj.syl, obj.snd, result])


def to_thai():
    # lu2thai
    pass


def pangram() -> str:
    return 'นายสังฆภัณฑ์เฮงพิทักษ์ฝั่งผู้เฒ่าซึ่งมีอาชีพเป็นฅนขายฃวดถูก\
        ตำรวจปฏิบัติการจับฟ้องศาลฐานลักนาฬิกาคุณหญิงฉัตรชฎาฌานสมาธิ'


def th2lu(text: str = None) -> str:
    if not text:
        return text
    objs = to_ipa(text)
    result = ''
    for obj in objs:
        head, tail = obj.to_lu()
        word = head + tail
        to_csv(text, obj, word)
        result += f'{word} '
    return result
