import unittest

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from thai2lu import convert_to_lu

CASES_1 = {
    "นายสังฆภัณฑ์เฮงพิทักษ์": "ลายนูย หลังสุง ละคุ ลันพุน เลงฮูง ลิพุ ลักทุก",
    "ฝั่งผู้เฒ่าซึ่งมีอาชีพเป็นฅนขายฃวด":"หลั่งฝุ่ง ลู่พี่ เล่าทุ่ว ลึ่งซุ่ง ลีมู ลาอู ลีบชูบ เล็นปุน ลนคุน หลายขูย หลวดขูด",
    "ถูกตำรวจปฏิบัติการจับฟ้องศาล":"หลูกถีก ลัมตุม สวดหรูด หละปุ หลิตุ หลัดบุด ลานกูน หลับจุบ ล้องฟู้ง หลานสูน",
    "ฐานลักนาฬิกาคุณหญิงฉัตรชฎาฌานสมาธิ":"หลานถูน ซักลุก ลานู ซิลุ ลากู ลุนคิน หลิงหยุง หลัดฉุด ละชุ ลาดู ลานชูน หละสุ ลามู ลิทุ"
}
CASES_2 = {
    "เป็นมนุษย์สุดประเสริฐเลิศคุณค่า":"เล็นปุน ละมุ ลุดนิด หลุดสิด หละปรุ เหลิดสูด เซิดลูด ลุนคิน ล่าคู่",
    "ยังดีกว่าฝูงสัตว์เดรัจฉาน":"ลังยุง ลีดู หล่ากวู่ หลูงฝีง หลัดสุด เลดู ซัดรุด หลานฉูน",
    "จงฝ่าฟันพัฒนาวิชาการ":"ลงจุง หล่าฝู่ ลันฟุน ลัดพุด ละทุ ลานู ลิวุ ลาชู ลานกูน",
    "อย่าล้างผลาญฤาเข่นฆ่าบีฑาใคร":"หล่าหยู่ ซ้างลู้ง หลานผลูน ซือรู เหล่นขู่น ล่าคู่ ลีบู ลาทู ลัยครุย",
    "ไม่ถือโทษโกรธแช่งซัดฮึดฮัดด่า":"ลั่ยมุ่ย หลือถู โลดทูด โหลดกรูด แล่งชู่ง ลัดซุด ลึดฮุด ลัดฮุด หล่าดู่",
    "หัดอภัยเหมือนกีฬาอัชฌาศัย":"หลัดหุด หละอุ ลัยพุย เหลือนหมูน ลีกู ซาลู หลัดอุด ลาชู หลัยสุย",
    "ปฏิบัติประพฤติกฎกำหนดใจ":"หละปุ หลิตุ หลัดบุด หละปรุ ลึดพรุด หลดกุด ลัมกุม หลดหนุด ลัยจุย",
    "พูดจาให้จ๊ะจ๋าน่าฟังเอย": "ลูดพีด ลาจู ลั่ยฮุ่ย ละจุ๊ หลาจู๋ ล่านู่ ลังฟุง เลยอูย",
}


class TestThai2Lu(unittest.TestCase):
    def setUpClass():
        print("Starting test case in TestThai2Lu...")

    def tearDownClass():
        print("Finished test case in TestThai2Lu.")
        
    def test_thai2lu_conversion_set1(self):
        print("Running test: test_thai2lu_conversion_set1")
        for case in CASES_1:
            result_list = convert_to_lu(case)
            result = " ".join(result_list)
            self.assertEqual(result, CASES_1[case])
    def test_thai2lu_conversion_set2(self):
        print("Running test: test_thai2lu_conversion_set2")
        for case in CASES_2:
            result_list = convert_to_lu(case)
            result = " ".join(result_list)
            self.assertEqual(result, CASES_2[case])
            
if __name__ == "__main__":
    unittest.main()