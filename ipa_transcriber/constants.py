# -*- coding: utf-8 -*-
import re
from typing import Dict, Tuple, Union

ConsonantType = Union[str, Tuple[str, ...]]
VowelType = Tuple[str, ...]
ToneMarks = Dict[int, str]

INITIAL_CONSONANTS: Dict[str, ConsonantType] = {
    'b': 'บ',
    'd': 'ด',
    'f': ('ฟ', 'ฝ'),
    'h': ('ฮ', 'ห'),
    'j': ('ย', 'หย'),
    'k': 'ก',
    'kʰ': ('ค', 'ข'),
    'l': ('ล', 'หล'),
    'm': ('ม', 'หม'),
    'n': ('น', 'หน'),
    'ŋ': ('ง', 'หง'),
    'pʰ': ('พ', 'ผ'),
    'p': 'ป',
    'r': ('ร', 'หร'),
    's': ('ซ', 'ส'),
    'tʰ': ('ท', 'ถ'),
    'c': 'จ',
    'cʰ': ('ช', 'ฉ'),
    't': 'ต',
    'w': ('ว', 'หว'),
    'ʔ': 'อ'
}

CONSONANT_CLUSTERS: Dict[str, str] = {
    'l': 'ล',
    'r': 'ร',
    'w': 'ว'
}

FINAL_CONSONANTS: Dict[str, str] = {
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

SHORT_VOWELS: Dict[str, VowelType] = {
    'a': ('อ-ะ', 'อั-', 'เอ-า'),
    'e': ('เอ-ะ', 'เอ็-'),
    'ɛ': ('แอ-ะ', 'แอ็-'),
    'i': ('อิ-', 'อิ-'),
    'o': ('โอ-ะ', 'อ-'),
    'ᴐ': ('เอ-าะ', 'อ็-อ'),
    'u': ('อุ-', 'อุ-'),
    'ɯ': ('อึ-', 'อึ-'),
    'ɤ': ('เอ-อะ', 'เอ-อะ')
}

LONG_VOWELS: Dict[str, VowelType] = {
    'aː': ('อ-า', 'อ-า'),
    'eː': ('เอ-', 'เอ-'),
    'ɛː': ('แอ-', 'แอ-'),
    'iː': ('อี-', 'อี-'),
    'oː': ('โอ-', 'โอ-'),
    'ᴐː': ('อ-อ', 'อ-อ'),
    'uː': ('อู-', 'อู-'),
    'ɯː': ('อื-อ', 'อื-'),
    'ɤː': ('เอ-อ', 'เอิ-', 'เอ-')
}

DIPHTHONGS: Dict[str, VowelType] = {
    'ia': ('เอี-ยะ', 'เอี-ยะ'),  # Note: This sound does not exist in the Thai language.
    'iːa': ('เอี-ย', 'เอี-ย'),
    'ɯa': ('เอื-อะ', 'เอื-อะ'),  # Note: This sound does not exist in the Thai language.
    'ɯːa': ('เอื-อ', 'เอื-อ'),
    'ua': ('อั-วะ', 'อั-วะ'),    # Note: This sound does not exist in the Thai language.
    'uːa': ('อั-ว', 'อ-ว'),
}

TONES_MARK: ToneMarks = {
    1: '',
    2: '่',
    3: '้',
    4: '๊',
    5: '๋',
}

VOWELS: Dict[str, VowelType] = {**SHORT_VOWELS, **LONG_VOWELS, **DIPHTHONGS}

VOWELS_SORTED = sorted(VOWELS.keys(), key=len, reverse=True)

INITIAL_CONSONANTS_SORTED = sorted(INITIAL_CONSONANTS.keys(), key=len, reverse=True)

PATTERN = re.compile(
    rf"({'|'.join(map(re.escape, INITIAL_CONSONANTS_SORTED))})"        # Initial consonant
    rf"(?:([{ '|'.join(map(re.escape, CONSONANT_CLUSTERS.keys()))}]))?" # Optional consonant cluster
    rf"({'|'.join(map(re.escape, VOWELS_SORTED))})"                    # Vowel
    rf"(?:([{ '|'.join(map(re.escape, FINAL_CONSONANTS.keys()))}]))?" # Optional final consonant
    rf"([{ '|'.join(map(str, TONES_MARK.keys()))}])?"                 # Optional tone
)
