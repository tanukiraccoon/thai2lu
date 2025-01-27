# -*- coding: utf-8 -*-
from tltk import th2ipa
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'thai-ipa-transcriber', 'src')))

from ipa_transcriber import ThaiIPA

import copy

def process_ipa_text(txt: str) -> list[str]:
    try:
        ipas = th2ipa(txt)
        
        replace_str = {
        ' <s/>': ' ',
        '.': ' ',
        '-': '', # Handle คาปูชิโน่หวานน้อย kʰaː1 puː1 cʰi4 noː-3 waːn1 nᴐːj4 <s/>
        }
            
        for key ,value in replace_str.items():     
            ipas = ipas.replace(key, value)
        ipas = ipas.strip()    
        return [ipa for ipa in ipas.split(' ') if ipa.strip()]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(f"Input text: {txt}")
        return []
    
def generate_lu_first_syllable(obj: ThaiIPA) -> str:
    o = copy.deepcopy(obj)
    
    #คำที่มี ร หรือ ล จะถูกแทนด้วย ซ เช่น ลอง -> ซอง และ รัก -> ซัก
    if o.initial_en in ['l','r']:
        o.initial_en = 's'
    else:
        o.initial_en = 'l'
   
    o.cluster_en = ''

    return o.spell()

def generate_lu_last_syllable(obj: ThaiIPA) -> str:
    o = copy.deepcopy(obj)
    # คำที่มีสระอุหรืออู ให้เติม 'สระอี' สำหรับเสียงยาว และ 'สระอิ' สำหรับเสียงสั้น
    # คำที่ไม่มีสระอุหรืออู ให้เติม 'สระอู' สำหรับเสียงยาว และ 'สระอุ' สำหรับเสียงสั้น
    if o.vowel_en in ['u','uː']:
        o.vowel_en = 'iː' if o.is_long else 'i'
    else:
        o.vowel_en = 'uː' if o.is_long else 'u'

    return o.spell() 

def generate_lu_all_syllable(obj :ThaiIPA) -> str:
    return generate_lu_first_syllable(obj) + generate_lu_last_syllable (obj)

def convert_to_lu(txt: str) -> list[str]:
    results  = []
    for ipa in process_ipa_text(txt) :
        obj  = ThaiIPA(ipa)
        result  = generate_lu_all_syllable(obj)
        results.append(result)

    return results