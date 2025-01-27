import re
from .constants import (
    CONSONANT_CLUSTERS,
    FINAL_CONSONANTS,
    INITIAL_CONSONANTS,
    PATTERN,
    TONES_MARK,
    VOWELS,
)

class ThaiIPA:
    __slots__ = (
        '_ipa',
        '_initial_en',
        '_cluster_en',
        '_vowel_en',
        '_final_en',
        '_tone',
        '_initial_th',
        '_cluster_th',
        '_vowel_th',
        '_final_th',
        '_tone_mark',
    )

    def __init__(self, ipa: str = "pʰrɯk4"):
        self._ipa = ipa
        match = PATTERN.match(self._ipa)
        if not match:
            raise ValueError(f"Unexpected IPA: {self._ipa}.")
        self._extract_ipa(match)
        self._process()

    def _extract_ipa(self, match: re.Match):
        (
            self._initial_en,
            self._cluster_en,
            self._vowel_en,
            self._final_en,
            tone_str,
        ) = match.groups()
        self._tone = int(tone_str)

    def _process(self):
        self._select_initial_th()
        self._select_cluster_th()
        self._select_vowel_th()
        self._select_final_th()
        self._select_tone_mark()

    @property
    def initial_en(self):
        return self._initial_en

    @initial_en.setter
    def initial_en(self, value: str):
        self._initial_en = value
        self._process()

    @property
    def cluster_en(self):
        return self._cluster_en

    @cluster_en.setter
    def cluster_en(self, value: str):
        self._cluster_en = value
        self._process()

    @property
    def vowel_en(self):
        return self._vowel_en

    @vowel_en.setter
    def vowel_en(self, value: str):
        self._vowel_en = value
        self._process()

    @property
    def final_en(self):
        return self._final_en

    @final_en.setter
    def final_en(self, value: str):
        self._final_en = value
        self._process()

    @property
    def tone(self):
        return self._tone

    @tone.setter
    def tone(self, value: int):
        self._tone = int(value)
        self._process()

    @property
    def initial_th(self):
        return self._initial_th

    @property
    def cluster_th(self):
        return self._cluster_th

    @property
    def vowel_th(self):
        return self._vowel_th

    @property
    def final_th(self):
        return self._final_th

    @property
    def tone_mark(self):
        return self._tone_mark

    @property
    def is_long(self) -> bool:
        return "ː" in self._vowel_en

    @property
    def is_dead(self) -> bool:
        return self._final_en in {"k", "p", "t"} or (not self.is_long and not self._final_en)

    @property
    def is_open(self) -> bool:
        return not self._final_en

    @property
    def is_mid(self) -> bool:
        return len(INITIAL_CONSONANTS.get(self._initial_en, [])) == 1

    def _select_initial_th(self):
        if self.is_mid:
            self._initial_th = INITIAL_CONSONANTS[self._initial_en]
        else:
            self._initial_th = self._get_initial_th_by_tone()

    def _get_initial_th_by_tone(self) -> str:
        tone_initial_map = {
            1: 0,
            2: 1,
            3: 0,
            4: 0,
            5: 1,
        }
        index = tone_initial_map.get(self._tone)
        if index is None:
            raise ValueError(f"Unexpected tone value: {self._tone}, IPA: {self._ipa} in _get_initial_th_by_tone")
        initial_options = INITIAL_CONSONANTS.get(self._initial_en)
        if not initial_options or index >= len(initial_options):
            raise ValueError(f"Invalid initial consonant or tone mapping for IPA: {self._ipa}")
        return initial_options[index]

    def _select_cluster_th(self):
        self._cluster_th = CONSONANT_CLUSTERS.get(self._cluster_en, "")

    def _select_vowel_th(self):
        special_cases = {("a", "w"), ("ɤː", "j")}
        if (self._vowel_en, self._final_en) in special_cases:
            self._vowel_th = VOWELS[self._vowel_en][2]
        else:
            vowel_options = VOWELS.get(self._vowel_en, [])
            if not vowel_options:
                self._vowel_th = ""
                return
            self._vowel_th = vowel_options[0] if self.is_open else vowel_options[1]

    def _select_final_th(self):
        if (self._vowel_en, self._final_en) == ("a", "w"):
            self._final_th = ""
        else:
            self._final_th = FINAL_CONSONANTS.get(self._final_en, "")

    def _select_tone_mark(self):
        if self.is_mid:
            if self.is_dead and self._tone == 2:
                self._tone_mark = TONES_MARK[1]
            else:
                self._tone_mark = TONES_MARK.get(self._tone, "")
        else:
            self._tone_mark = self._get_tone_mark_by_initial()

    def _get_tone_mark_by_initial(self) -> str:
        tone = self._tone
        if tone == 1:
            return TONES_MARK.get(tone, "")
        elif tone == 2:
            return TONES_MARK[1] if self.is_dead else TONES_MARK.get(tone, "")
        elif tone == 3:
            return TONES_MARK[1] if (self.is_dead and self.is_long) else TONES_MARK.get(3, "")
        elif tone == 4:
            return TONES_MARK[1] if (self.is_dead and not self.is_long) else TONES_MARK.get(4, "")
        elif tone == 5:
            return TONES_MARK.get(tone, "") if self.is_dead else TONES_MARK.get(1, "")
        else:
            raise ValueError(f"Unexpected tone value: {self._tone}, IPA: {self._ipa} in _get_tone_mark_by_initial")

    def spell(self) -> str:
        s = f"{self._initial_th}{self._cluster_th}"
        s = self._vowel_th.replace("อ", s, 1)
        s = s.replace("-", self._tone_mark)
        s += self._final_th
        return s
