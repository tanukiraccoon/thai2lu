# Thai2Lu 

[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Website](https://img.shields.io/website?url=https://lang.tanukiraccoon.com/thai2lu/)](https://lang.tanukiraccoon.com/thai2lu/)
[![GitHub issues](https://img.shields.io/github/issues/tanukiraccoon/thai2lu)](https://github.com/tanukiraccoon/thai2lu/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/tanukiraccoon/thai2lu)](https://github.com/tanukiraccoon/thai2lu/pulls)

โลปรู แลมกรูม แลงปลูง ลาพู หลาสู ลัยทุย เล็นปุน ลาพู หลาสู ซูลี

# Example

```python
from thai2lu import convert_to_lu
result = convert_to_lu('ฝันดี')
print(result) # Output: ['หลันฝุน','ลีดู']
```
# Limitation

- ไม่รองรับเครื่องหมายวรรคตอน เช่น ไม้ยมก (ๆ) จุลภาค (,) ยกเว้น ทัณฑฆาต ( ์)
- ไม่รองรับการเขียนด้วยตัวอักษรภาษาต่างประเทศ เช่น Johnสบายดีไหม ฉันไปparagonมา
- ไม่รองรับการเขียนด้วยตัวเลขทั้งตัวเลขไทยและตัวเลขอารบิก เช่น ค่าขนม50บาท ราคาตั๋ว๑,๒๕๐บาท
- ผลลัพธ์ที่ได้อาจไม่ถูกต้อง หากเขียนด้วยคำศัพท์ที่ผิดหลักการสะกดคำและวรรณยุกต์ เช่น เด๋ว โน๊ต น๊ะ ป่ะ ฟลุ๊ค
- ผลลัพธ์ที่ได้อาจไม่ถูกต้อง หากเขียนด้วยคำทับศัพท์ ศัพท์แสลง หรือคำศัพท์ภาษาไทยที่ไม่ได้ระบุไว้ในพจนานุกรม เช่น เฟซบุ๊ก รรรรร (ระ-รัน-รอน) สรวน (สะ-รวน)
