from tltk import th2ipa
from ipa_transcriber.index import ThaiIPA

def convert_to_lu(text: str) -> list[str]:
    ipa_text = th2ipa(text).replace(' <s/>', ' ').replace('.', ' ').replace('-', '')
    tokens = ipa_text.split()

    results = []
    for token in tokens:
        ipa_obj = ThaiIPA(token)
        
        if ipa_obj.initial_en in {'l', 'r'}:
            ipa_obj.initial_en = 's'
        else:
            ipa_obj.initial_en = 'l'
        ipa_obj.cluster_en = ''
        spelled1 = ipa_obj.spell()
        
        if ipa_obj.vowel_en in {'u', 'uː'}:
            ipa_obj.vowel_en = 'iː' if ipa_obj.is_long else 'i'
        else:
            ipa_obj.vowel_en = 'uː' if ipa_obj.is_long else 'u'
        spelled2 = ipa_obj.spell()
        
        results.append(spelled1 + spelled2)

    return results

if __name__ == "__main__":
    print(convert_to_lu("สวัสดี"))
