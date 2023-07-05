# -*- coding: utf-8 -*-
from tltk import th2ipa
from ..thai-ipa-transcriber.src import ipa_transcriber
import copy

def extract_ipa_list(txt: str) -> list[str]:
    try:
        ipas = th2ipa(txt).replace(' <s/>', '').replace('.', ' ')
        return [ipa for ipa in ipas.split(' ') if ipa.strip()]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print(txt)
        return []

def gen_lu_first(obj: IPA) -> str:

    o = copy.deepcopy(obj)
    
    if o.initial_en in ['l','r']:
        o.initial_en = 's'
    else:
        o.initial_en = 'l'

    o.cluster_en = ''
    o.process()

    return o.spell()

def gen_lu_second(obj: IPA) -> str:

    o = copy.deepcopy(obj)
    
    if o.long_vow:
        o.vowel_th = 'อี-' if o.vowel_en == 'uː' else 'อู-'
    elif o.vowel_en == 'u':
        o.vowel_th = 'อิ-'
    else:
        o.vowel_th = 'อุ-'
    return o.spell() 

def gen_lu_all(obj :IPA) -> str:
    return gen_lu_first(obj) + gen_lu_second(obj)

def thai2lu(txt: str) -> list[str]:
    results  = []
    for ipa in extract_ipa_list(txt) :
        obj  = IPA(ipa)
        result  = gen_lu_all(obj)
        results.append(result)

    return results

def gen_lu2thai(objs: list):
    fs = objs[0]
    ls = objs[-1]
    ls.vowel_th = fs.vowel_th
    return ls.spell()

def lu2thai(txt:str)-> list[str]:
    txts = txt.split(' ')
    results =[]
    for i in txts:
        objs = []
        for ipa in extract_ipa_list(i):
            obj = IPA(ipa)
            objs.append(obj)
        result = gen_lu2thai(objs)
        results.append(result)
    return results
    