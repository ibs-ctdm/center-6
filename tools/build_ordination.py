#!/usr/bin/env python3
"""สร้างหน้า "สมัครบวช" สองภาษาจากแม่แบบเดียว

    python3 tools/build_ordination.py

ได้ไฟล์ ordination.html (ไทย) และ ja/ordination.html (ญี่ปุ่น)
ข้อความหลัก กำหนดการ และรายชื่อวัด ผู้ดูแลแก้ได้เองที่หน้าผู้ดูแล
(https://dmctochigi-ordination.ctdm-ibs.workers.dev/admin/) — หน้าเว็บโหลดค่าล่าสุดจาก API ทับข้อความตั้งต้นในไฟล์นี้
แก้ไฟล์นี้เฉพาะเมื่อจะเปลี่ยนโครงหน้า ป้ายของฟอร์ม หรือข้อความที่ไม่ได้อยู่ในหน้าผู้ดูแล
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSET_VER = "1"
API_BASE = "https://dmctochigi-ordination.ctdm-ibs.workers.dev"
R2 = "https://pub-a71ab4f1880d46c9ba975e0786421c77.r2.dev/projects/6/images/"
LOGO = R2 + "logo_tochigi_golden_6_1.png"
HERO = R2 + "25670811-12_80_084_6_147.jpg"
GALLERY = [
    "25670811-12_80_084_6_146.jpg", "25670811-12_80_225_6_148.jpg", "25670811-12_80_236_6_149.jpg",
    "25670811-12_80_253_6_150.jpg", "25670811-12_80_282_6_151.jpg", "25670811-12_80_297_6_152.jpg",
    "25670811-12_80_369_6_153.jpg", "25670811-12_80_412_6_154.jpg", "25670811-12_80_442_6_155.jpg",
    "25670811-12_80_447_6_156.jpg", "25670811-12_80_497_6_157.jpg", "25670811-12_80_590_6_158.jpg",
]
MAP = ("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12814.094280852285!2d139.8050610871582!3d36.589697300000005"
       "!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x601f6f320a4fffff%3A0xa08b77ba66d3da01"
       "!2z4Lin4Lix4LiU4Lie4Lij4Liw4LiY4Lij4Lij4Lih4LiB4Liy4Lii4LmC4LiX4LiK4Li04Lir4LiH4Li0!5e0!3m2!1sth!2sth!4v1775307311383!5m2!1sth!2sth")

# ข้อความตั้งต้น (ตรงกับ migrations/0001_init.sql ของ dmctochigi-ordination) — ใช้ตอน API ยังไม่ตอบ
ROUNDS = [
    (1, "พฤษภาคม 2570", "2027年5月", "29 เม.ย.–9 พ.ค. 2570", "2027年4月29日〜5月9日", "เสาร์ 1 พ.ค. 2570", "2027年5月1日（土）"),
    (2, "สิงหาคม 2570", "2027年8月", "6–15 ส.ค. 2570", "2027年8月6日〜15日", "อาทิตย์ 8 ส.ค. 2570", "2027年8月8日（日）"),
    (3, "กันยายน 2570", "2027年9月", "17–26 ก.ย. 2570", "2027年9月17日〜26日", "อาทิตย์ 19 ก.ย. 2570", "2027年9月19日（日）"),
    (4, "เม.ย.–พ.ค. 2571", "2028年4月〜5月", "28 เม.ย.–7 พ.ค. 2571", "2028年4月28日〜5月7日", "อาทิตย์ 30 เม.ย. 2571", "2028年4月30日（日）"),
    (5, "สิงหาคม 2571", "2028年8月", "11–23 ส.ค. 2571", "2028年8月11日〜23日", "เสาร์ 12 และอาทิตย์ 13 ส.ค. 2571 (งานบวชใหญ่)", "2028年8月12日（土）・13日（日）（大得度式）"),
]
CONTENT = {
    "hero_kicker": ("พ.ศ. 2570–2571 · ประเทศญี่ปุ่น", "2027〜2028年・日本"),
    "hero_title": ("โครงการบวชบูชาธรรม 84 ปี\nหลวงพ่อธัมมชโย", "タンマチャヨー師 84歳記念\n出家得度プロジェクト"),
    "hero_subtitle": ("อุปสมบทพระภิกษุสะสม 84 รูป ณ พัทธสีมา วัดพระธรรมกายโทชิหงิ", "栃木別院の結界にて、84名の比丘得度をめざします"),
    "hero_quote": ("ครั้งหนึ่งในชีวิตลูกผู้ชาย ได้บวชบูชาธรรม ในวาระอายุวัฒนมงคล 84 ปี หลวงพ่อธัมมชโย",
                   "人生に一度の出家を、タンマチャヨー師の84歳を祝う法の供養として"),
    "intro": ("อุปสมบทพระภิกษุสะสม 84 รูป เพื่อบูชาธรรมในวาระอายุวัฒนมงคล 84 ปี หลวงพ่อธัมมชโย เปิดรับทั้งชาวไทยและชาวญี่ปุ่น โดยเน้นชักชวนชาวญี่ปุ่นผ่านเครือข่ายวัดและศูนย์สาขาในประเทศญี่ปุ่น",
              "タンマチャヨー師の84歳の慶賀にあたり、法への供養として累計84名の比丘得度をめざします。タイ人・日本人のどなたでも参加でき、とくに日本各地の寺院・支部を通じて日本の方の参加を広く呼びかけています。"),
    "schedule_note": ("พิธีอุปสมบททุกครั้งจัด ณ พัทธสีมา วัดพระธรรมกายโทชิหงิ · กำหนดการนี้เป็นฉบับหารือ วันเปิด–ปิดรับสมัครและศูนย์อบรมของแต่ละรอบจะแจ้งยืนยันอีกครั้ง",
                      "得度式はすべて栃木別院の結界（布薩堂）で行います。日程は検討段階のもので、各回の受付期間と研修先は確定しだいお知らせします。"),
    "process": (
        "การรับสมัครและพิธี | วัดต้นสังกัดชักชวน ตรวจความพร้อมและเอกสาร ประสานนิมนต์พระอุปัชฌาย์ที่มีคุณสมบัติ และส่งข้อมูลเข้าทะเบียนกลาง วัดพระธรรมกายโทชิหงิรับผิดชอบพิธีอุปสมบท\n"
        "การอบรมหลังบวช | ฝึกพระธรรมวินัย สมาธิ ทำวัตร และกิจวัตรสงฆ์ที่วัดต้นสังกัดเป็นหลัก หรือส่งต่อศูนย์ที่พร้อมตามภาษา ศูนย์อบรมภาษาญี่ปุ่นที่เสนอ ได้แก่ วัดป่าธรรมกายนานาชาติโทชิหงิ กุมมะ และนางาโน ส่วนภาษาไทยประสานวัดต้นสังกัดหรือวัดพระธรรมกายโทชิหงิ\n"
        "กิจกรรมคู่ขนาน | อบรมอุบาสกอุบาสิกาแก้วในรอบที่ 1–3 และอาจจัดบรรพชาสามเณรเพิ่มเติมตามความพร้อม โดยเสนอศูนย์อบรมสามเณรที่วัดภาวนานางาโน่และวัดพระธรรมกายโอซาก้า",
        "受付と得度式 | 所属寺院が参加を呼びかけ、準備と書類を確認し、資格ある戒師（和尚）を招請して中央名簿に登録します。得度式は栃木別院が執り行います。\n"
        "得度後の研修 | 戒律・瞑想・読経・僧侶の日課を、主に所属寺院で修習します。言語に応じて受け入れ可能な研修先へ送ることもあります。日本語の研修先は国際森林寺院 栃木・群馬・長野を予定しています。タイ語は所属寺院または栃木別院が担当します。\n"
        "並行行事 | 第1〜3回では在家の八戒研修（ウバーサカ・ウバーシカー）を行い、準備が整えば沙弥出家も行う予定です。沙弥の研修先は長野瞑想寺院と大阪を予定しています。"),
    "qualifications": (
        "ชายแท้ อายุ 20 ปีขึ้นไป (บวชพระ) หรือ 7 ปีขึ้นไป (บวชสามเณร)\nใช้ภาษาไทยหรือภาษาญี่ปุ่นได้\nสุขภาพแข็งแรง ไม่เป็นโรคติดต่อ\nไม่ข้องเกี่ยวกับยาเสพติด\nท่องคำขานนาคและคำขอบวชได้",
        "男性で、比丘は20歳以上、沙弥は7歳以上\nタイ語または日本語ができる方\n心身ともに健康で、感染症のない方\n薬物と関わりのない方\n得度式の唱え言葉（出家の請願文）を暗唱できる方"),
    "preparation": (
        "เสื้อธรรมทายาท สีขาว 2 ตัว\nกางเกงธรรมทายาท สีขาว 2 ตัว\nเสื้อพระราชทาน สีขาว 1 ตัว\nอุปกรณ์ส่วนตัว",
        "白い研修用シャツ 2枚\n白い研修用ズボン 2本\n白い式典用シャツ 1枚\n身の回り品"),
    "register_note": ("สมัครออนไลน์ได้ที่หน้านี้ หรือสมัครด้วยตนเองที่วัดพระธรรมกายทุกแห่งในประเทศญี่ปุ่น",
                      "このページからオンラインで申し込めます。日本各地のタンマガーイ寺院でも受け付けています。"),
    "contacts": (
        "น้องกาว | LINE ID: ppkaw075\nน้องปัทม์ | LINE ID: ampatt\nโทรศัพท์ | (+81) 28-652-8701\nอีเมล | dimc.tochigi2004@gmail.com",
        "カオ | LINE ID: ppkaw075\nパット | LINE ID: ampatt\n電話 | (+81) 28-652-8701\nメール | dimc.tochigi2004@gmail.com"),
}

T = {
    "th": dict(
        html_lang="th", title="โครงการบวชบูชาธรรม 84 ปี หลวงพ่อธัมมชโย — วัดพระธรรมกายโทชิหงิ",
        desc="สมัครบวชพระภิกษุ 5 รอบ พ.ศ. 2570–2571 ณ พัทธสีมา วัดพระธรรมกายโทชิหงิ ประเทศญี่ปุ่น เปิดรับชาวไทยและชาวญี่ปุ่น",
        temple="วัดพระธรรมกายโทชิหงิ", home="หน้าแรก", visit="เยี่ยมชมวัด", about="เกี่ยวกับวัด", ordain="สมัครบวช",
        cta="สมัครออนไลน์", cta_hero="สมัครบวชออนไลน์", see_schedule="ดูกำหนดการ 5 รอบ", prefix="",
        stat1="รูป", stat1l="เป้าหมายพระภิกษุ", stat2="รอบ", stat2l="พิธีอุปสมบท", stat3="ภาษา", stat3l="ไทย · ญี่ปุ่น",
        goal_kicker="เป้าหมายของโครงการ", goal_h="บวชบูชาธรรม 84 ปี",
        sch_kicker="กำหนดการ", sch_h="กำหนดการอบรมและวันอุปสมบท 5 รอบ",
        th_round="รอบ", th_training="ช่วงอบรม", th_ceremony="วันอุปสมบท / วันงาน", round_word="รอบที่",
        apply_round="สมัครรอบนี้", st_open="เปิดรับสมัคร", st_upcoming="เร็ว ๆ นี้", st_closed="ปิดรับสมัคร", st_done="เสร็จสิ้นแล้ว",
        proc_kicker="แนวทางดำเนินงาน", proc_h="จากวัดต้นสังกัด สู่พัทธสีมา",
        qual_h="คุณสมบัติผู้สมัคร", prep_h="สิ่งที่ต้องเตรียม", contact_h="ติดต่อสอบถาม",
        reg_kicker="ใบสมัคร", reg_h="สมัครบวชออนไลน์",
        reg_lead="กรอกข้อมูลให้ครบ ทีมงานของวัดต้นสังกัดจะติดต่อกลับเพื่อสัมภาษณ์และตรวจเอกสาร · ช่องที่มี * ต้องกรอก",
        s1="เลือกรอบและวัดต้นสังกัด", s2="ข้อมูลส่วนตัว", s3="ช่องทางติดต่อ", s4="การศึกษาและครอบครัว", s5="ข้อมูลเพิ่มเติม",
        f_round="รอบที่ต้องการบวช", f_type="ประเภทการบวช", f_type_b="บวชพระภิกษุ", f_type_b2="อายุ 20 ปีขึ้นไป",
        f_type_s="บวชสามเณร", f_type_s2="อายุ 7 ปีขึ้นไป · ตามความพร้อมของแต่ละรอบ",
        f_tlang="ภาษาที่ใช้อบรม", f_tlang_th="ภาษาไทย", f_tlang_ja="ภาษาญี่ปุ่น",
        f_temple="วัดต้นสังกัด", f_temple_ph="— เลือกวัด —", f_temple_other="วัดอื่น / ยังไม่มีวัดต้นสังกัด", f_temple_other_ph="ระบุชื่อวัดหรือศูนย์ หรือพิมพ์ว่า ไม่มี",
        f_prefix="คำนำหน้า", f_prefix_ph="นาย / ด.ช.", f_name="ชื่อ-นามสกุล", f_name_alt="ชื่อ-นามสกุล ภาษาอังกฤษ (ตามหนังสือเดินทาง)",
        f_birth="วันเดือนปีเกิด (ค.ศ.)", f_id="เลขบัตรประชาชน หรือเลขหนังสือเดินทาง", f_nat="สัญชาติ", f_nat_ph="ไทย", f_rel="ศาสนา", f_rel_ph="พุทธ",
        f_marital="สถานภาพ", f_height="ส่วนสูง (ซม.)", f_weight="น้ำหนัก (กก.)",
        f_phone="เบอร์มือถือ", f_email="อีเมล", f_line="LINE ID", f_addr="ที่อยู่ปัจจุบัน",
        f_edu_status="การศึกษา", f_edu_level="ระดับการศึกษา", f_father="ชื่อ-นามสกุล บิดา", f_mother="ชื่อ-นามสกุล มารดา",
        f_em_name="ผู้ปกครอง / ผู้ติดต่อฉุกเฉิน", f_em_rel="เกี่ยวข้องเป็น", f_em_rel_ph="เช่น บิดา ภรรยา พี่ชาย", f_em_phone="เบอร์ผู้ติดต่อฉุกเฉิน",
        f_before="เคยบวชมาก่อนหรือไม่", yes="เคย", no="ไม่เคย", f_before_detail="บวชที่ไหน เมื่อไร (ถ้าเคย)",
        f_health="โรคประจำตัว / ยาที่ใช้ประจำ (ถ้ามี)", f_expect="สิ่งที่คาดว่าจะได้รับจากการบวชครั้งนี้", f_source="ทราบข่าวโครงการจากที่ใด",
        f_interview="วันที่สะดวกสัมภาษณ์กับพระอาจารย์", f_note="ข้อความถึงเจ้าหน้าที่",
        f_consent="ข้าพเจ้ายินยอมให้วัดพระธรรมกายในประเทศญี่ปุ่นใช้ข้อมูลนี้เพื่อการรับสมัครและจัดโครงการบวชเท่านั้น",
        submit="ส่งใบสมัคร", choose="— เลือก —",
        marital=[("single", "โสด"), ("married", "สมรส"), ("widowed", "หม้าย"), ("divorced", "หย่า"), ("separated", "แยกกันอยู่")],
        edu_status=[("studying", "กำลังศึกษาอยู่"), ("graduated", "จบการศึกษาแล้ว")],
        edu_level=["มัธยมศึกษา หรือ ปวส.", "อุดมศึกษา", "ปริญญาตรี", "ปริญญาโท", "ปริญญาเอก", "อื่น ๆ"],
        gal_kicker="ภาพบรรยากาศ", gal_h="โครงการบรรพชาอุปสมบทหมู่ ที่ผ่านมา",
        don_kicker="ร่วมอุปถัมภ์พระพุทธศาสนา", don_h="ร่วมทำบุญได้ที่", don_bank_h="🏦 ข้อมูลบัญชีธนาคาร", don_bank="ธนาคาร / BANK", don_bank_v="ออมสิน (สาขาคลองหลวง)",
        don_name="ชื่อบัญชี / ACCOUNT NAME", don_no="เลขที่บัญชี / ACCOUNT NUMBER", copy="คัดลอก", copied="✓ คัดลอกแล้ว",
        don_thanks="✨ ขออนุโมทนาบุญกับทุกท่านที่ร่วมสนับสนุนวัดพระธรรมกายโทชิหงิ ✨", don_slip="กรุณาส่งหลักฐานการโอนเงินมาที่ LINE ID: ppkaw075",
        don_bless="สาธุ 🙏 ขอให้มีความสุข ความเจริญ และได้บุญกุศลทุกประการ",
        ct_kicker="📍 ติดต่อเรา", ct_h="ติดต่อสอบถาม", ct_lead="ยินดีต้อนรับทุกท่านสู่วัดพระธรรมกายโทชิหงิ ติดต่อเราได้หลายช่องทาง",
        ct_addr="ที่อยู่", ct_drive="🚗 ประมาณ 20 นาทีจากสถานี JR Utsunomiya โดยรถยนต์", ct_tel="โทรศัพท์", ct_mail="อีเมล", ct_online="🌐 ช่องทางออนไลน์",
        ft_tag="ศูนย์ปฏิบัติธรรมแห่งความสงบ ใจกลางเมืองโอยะ จังหวัดโทชิหงิ", ft_contact="ติดต่อเรา", ft_other="ช่องทางอื่น ๆ", ft_copy="© 2569 วัดพระธรรมกายโทชิหงิ",
        other_lang="日本語", other_href="/ja/ordination", base="",
    ),
    "ja": dict(
        html_lang="ja", title="タンマチャヨー師 84歳記念 出家得度プロジェクト — タンマガーイ寺院栃木別院",
        desc="2027〜2028年、全5回。タンマガーイ寺院栃木別院の結界で行う出家得度（比丘）への参加申込。タイ人・日本人どなたでも申し込めます。",
        temple="タンマガーイ寺院栃木別院", home="ホーム", visit="寺院のご案内", about="寺院について", ordain="出家得度の申込",
        cta="オンライン申込", cta_hero="オンラインで申し込む", see_schedule="全5回の日程を見る", prefix="",
        stat1="名", stat1l="比丘得度の目標", stat2="回", stat2l="得度式", stat3="言語", stat3l="タイ語・日本語",
        goal_kicker="プロジェクトの目的", goal_h="84歳を祝う、法の供養としての出家",
        sch_kicker="日程", sch_h="研修期間と得度式（全5回）",
        th_round="回", th_training="研修期間", th_ceremony="得度式の日", round_word="第",
        apply_round="この回に申し込む", st_open="受付中", st_upcoming="近日受付", st_closed="受付終了", st_done="終了",
        proc_kicker="進め方", proc_h="所属寺院から、栃木別院の結界へ",
        qual_h="参加資格", prep_h="持ち物", contact_h="お問い合わせ",
        reg_kicker="申込フォーム", reg_h="オンライン申込",
        reg_lead="ご記入いただいた内容をもとに、所属寺院の担当者から面談と書類確認のご連絡をします。＊印は必須項目です。",
        s1="参加する回と所属寺院", s2="ご本人について", s3="連絡先", s4="学歴・ご家族", s5="その他",
        f_round="参加を希望する回", f_type="出家の種類", f_type_b="比丘として得度", f_type_b2="20歳以上",
        f_type_s="沙弥として出家", f_type_s2="7歳以上・各回の準備状況によります",
        f_tlang="研修で使う言語", f_tlang_th="タイ語", f_tlang_ja="日本語",
        f_temple="所属寺院", f_temple_ph="— 寺院を選択 —", f_temple_other="その他の寺院・所属なし", f_temple_other_ph="寺院・センター名、または「なし」とご記入ください",
        f_prefix="", f_prefix_ph="", f_name="氏名", f_name_alt="フリガナ",
        f_birth="生年月日（西暦）", f_id="パスポート番号または在留カード番号", f_nat="国籍", f_nat_ph="日本", f_rel="宗教", f_rel_ph="仏教",
        f_marital="婚姻状況", f_height="身長（cm）", f_weight="体重（kg）",
        f_phone="携帯電話番号", f_email="メールアドレス", f_line="LINE ID", f_addr="現住所",
        f_edu_status="学歴", f_edu_level="最終学歴・在学中の課程", f_father="父の氏名", f_mother="母の氏名",
        f_em_name="保護者・緊急連絡先の氏名", f_em_rel="ご関係", f_em_rel_ph="例：父、妻、兄", f_em_phone="緊急連絡先の電話番号",
        f_before="出家の経験", yes="あり", no="なし", f_before_detail="時期と寺院（経験がある場合）",
        f_health="持病・常用薬（ある場合）", f_expect="今回の出家で得たいこと", f_source="このプロジェクトを知ったきっかけ",
        f_interview="面談のご都合のよい日", f_note="担当者への連絡事項",
        f_consent="入力した情報を、日本のタンマガーイ寺院が本プロジェクトの受付と運営のためにのみ利用することに同意します",
        submit="申込を送信する", choose="— 選択 —",
        marital=[("single", "未婚"), ("married", "既婚"), ("widowed", "死別"), ("divorced", "離婚"), ("separated", "別居")],
        edu_status=[("studying", "在学中"), ("graduated", "卒業")],
        edu_level=["高校・専門学校", "短大・高専", "大学", "大学院（修士）", "大学院（博士）", "その他"],
        gal_kicker="これまでの様子", gal_h="過去の出家得度プロジェクト",
        don_kicker="仏教を支える", don_h="ご寄付のご案内", don_bank_h="🏦 振込先", don_bank="銀行 / BANK", don_bank_v="タイ政府貯蓄銀行（クローンルアン支店）",
        don_name="口座名義 / ACCOUNT NAME", don_no="口座番号 / ACCOUNT NUMBER", copy="コピー", copied="✓ コピーしました",
        don_thanks="✨ 栃木別院へのご支援に、心より感謝申し上げます ✨", don_slip="お振込みの控えは LINE ID: ppkaw075 までお送りください",
        don_bless="サートゥ 🙏 皆さまのご多幸をお祈りいたします",
        ct_kicker="📍 アクセス", ct_h="お問い合わせ", ct_lead="タンマガーイ寺院栃木別院へようこそ。以下の方法でお気軽にご連絡ください。",
        ct_addr="所在地", ct_drive="🚗 JR宇都宮駅から車で約20分", ct_tel="電話", ct_mail="メール", ct_online="🌐 オンライン",
        ft_tag="栃木県宇都宮市大谷町の瞑想と修行の寺院", ft_contact="連絡先", ft_other="SNS・地図", ft_copy="© 2026 タンマガーイ寺院栃木別院",
        other_lang="ไทย", other_href="/ordination", base="../",
    ),
}


def e(s):
    return escape(s, quote=True)


def lines(s):
    return [x.strip() for x in s.split("\n") if x.strip()]


def li_list(text, key, lang):
    items = "".join(f'<li class="flex gap-2"><span class="text-accent mt-0.5">◆</span><span>{e(x)}</span></li>' for x in lines(text))
    return f'<ul class="space-y-2 text-dark/75" data-c="{key}" data-kind="list">{items}</ul>'


def pairs(text):
    out = []
    for x in lines(text):
        a, _, b = x.partition("|")
        out.append((a.strip(), b.strip()))
    return out


def build(lang):
    t = T[lang]
    L = 0 if lang == "th" else 1
    c = {k: v[L] for k, v in CONTENT.items()}
    b = t["base"]

    rounds_rows = "".join(
        f'''<div class="round-card">
          <div class="round-no"><span class="text-xs">{e(t["round_word"])}</span>{n}{"" if lang == "th" else '<span class="text-xs">回</span>'}</div>
          <div class="flex-1 min-w-0">
            <div class="font-serif font-bold text-lg text-dark">{e(r[1 + L])}</div>
            <div class="grid sm:grid-cols-2 gap-x-6 gap-y-1 mt-2 text-sm">
              <div><span class="text-primary">{e(t["th_training"])}</span><div class="font-semibold text-dark">{e(r[3 + L])}</div></div>
              <div><span class="text-primary">{e(t["th_ceremony"])}</span><div class="font-semibold text-dark">{e(r[5 + L])}</div></div>
            </div>
          </div>
          <div class="round-side"><span class="badge badge-open">{e(t["st_open"])}</span>
            <a href="#register" data-round="{n}" class="round-apply">{e(t["apply_round"])} →</a></div>
        </div>'''
        for (n, *r) in [(x[0], *x) for x in ROUNDS]
    )

    process_cards = "".join(
        f'<div class="proc-card"><div class="proc-no">{i + 1}</div><h3 class="font-serif font-bold text-xl text-dark mb-2">{e(h)}</h3><p class="text-dark/70 leading-relaxed">{e(d)}</p></div>'
        for i, (h, d) in enumerate(pairs(c["process"]))
    )
    contacts = "".join(f'<li><span class="text-primary">{e(a)}</span> <strong class="text-dark">{e(bb)}</strong></li>' for a, bb in pairs(c["contacts"]))
    gallery = "".join(f'<button type="button" class="gal-item" data-full="{R2}{g}"><img src="{R2}{g}" alt="" loading="lazy"></button>' for g in GALLERY)

    def opt(items):
        return "".join(f'<option value="{e(v)}">{e(l)}</option>' for v, l in items)

    edu_levels = "".join(f'<option value="{e(x)}">{e(x)}</option>' for x in t["edu_level"])
    prefix_field = (f'<div class="sm:col-span-1"><label class="flbl" for="f-prefix">{e(t["f_prefix"])}</label><input id="f-prefix" name="prefix" class="finp" placeholder="{e(t["f_prefix_ph"])}" maxlength="40"></div>'
                    if t["f_prefix"] else "")
    name_span = "sm:col-span-3" if t["f_prefix"] else "sm:col-span-4"

    return f'''<!DOCTYPE html>
<html lang="{t["html_lang"]}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<link rel="icon" type="image/png" href="{LOGO}">
<link rel="apple-touch-icon" href="{LOGO}">
<link rel="alternate" hreflang="th" href="https://dmctochigi.org/ordination">
<link rel="alternate" hreflang="ja" href="https://dmctochigi.org/ja/ordination">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["desc"])}">
<meta property="og:image" content="{HERO}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://dmctochigi.org{"/ordination" if lang == "th" else "/ja/ordination"}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#4b2502">
<script src="https://cdn.tailwindcss.com/3.4.16"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&family=Noto+Serif+Thai:wght@400;600;700&family=Noto+Sans+JP:wght@400;500;700&family=Noto+Serif+JP:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/ordination.css?v={ASSET_VER}">
</head>
<body class="bg-stone-50 lang-{lang}" data-lang="{lang}" data-api="{API_BASE}">

<div id="announcement" class="announcement hidden"><span data-c="announcement"></span></div>

<nav class="site-nav">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between gap-3">
    <a href="{b}index.html" class="flex items-center gap-3 min-w-0">
      <img src="{LOGO}" alt="" class="h-11 w-auto object-contain">
      <div class="min-w-0">
        <div class="text-dark font-serif text-base font-bold leading-tight truncate">{e("วัดพระธรรมกายโทชิหงิ" if lang == "th" else "タンマガーイ寺院栃木別院")}</div>
        <div class="text-primary text-xs truncate">{e("タンマガーイ寺院栃木別院" if lang == "th" else "Wat Phra Dhammakaya Tochigi")}</div>
      </div>
    </a>
    <div class="hidden md:flex items-center gap-7">
      <a href="{b}index.html" class="nav-link">{e(t["home"])}</a>
      <a href="{b}about.html" class="nav-link">{e(t["visit"])}</a>
      <a href="{t["other_href"]}" class="lang-switch" hreflang="{"ja" if lang == "th" else "th"}">{e(t["other_lang"])}</a>
      <a href="#register" class="btn-accent text-sm px-6 py-2">{e(t["cta"])}</a>
    </div>
    <div class="flex md:hidden items-center gap-2">
      <a href="{t["other_href"]}" class="lang-switch">{e(t["other_lang"])}</a>
      <button type="button" class="p-2 text-dark" aria-label="menu" onclick="document.getElementById('mobile-menu').classList.toggle('hidden')">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </div>
  <div id="mobile-menu" class="hidden md:hidden bg-white border-t border-stone-100 px-6 py-4 space-y-1">
    <a href="{b}index.html" class="block text-dark/70 py-2">{e(t["home"])}</a>
    <a href="{b}about.html" class="block text-dark/70 py-2">{e(t["about"])}</a>
    <a href="#schedule" class="block text-dark/70 py-2">{e(t["sch_kicker"])}</a>
    <a href="#register" class="block btn-accent text-center px-6 py-2 mt-2" onclick="document.getElementById('mobile-menu').classList.add('hidden')">{e(t["cta"])}</a>
  </div>
</nav>

<header class="hero">
  <img src="{HERO}" alt="" class="hero-img">
  <div class="hero-overlay"></div>
  <div class="relative z-10 text-center px-5 max-w-4xl mx-auto">
    <p class="hero-kicker" data-c="hero_kicker">{e(c["hero_kicker"])}</p>
    <h1 class="hero-title" data-c="hero_title">{e(c["hero_title"])}</h1>
    <div class="w-24 h-0.5 bg-accent mx-auto my-6"></div>
    <p class="text-white/90 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed" data-c="hero_subtitle">{e(c["hero_subtitle"])}</p>
    <p class="text-accent-light font-semibold mt-4 max-w-2xl mx-auto" data-c="hero_quote">{e(c["hero_quote"])}</p>
    <div class="flex flex-col sm:flex-row gap-3 justify-center mt-10">
      <a href="#register" class="btn-accent text-lg px-10 py-4 shadow-2xl">{e(t["cta_hero"])}</a>
      <a href="#schedule" class="btn-ghost-light text-lg px-8 py-4">{e(t["see_schedule"])}</a>
    </div>
  </div>
</header>

<section class="py-16 md:py-20 bg-white">
  <div class="max-w-5xl mx-auto px-5 text-center">
    <p class="kicker">{e(t["goal_kicker"])}</p>
    <h2 class="sec-title">{e(t["goal_h"])}</h2>
    <div class="w-16 h-0.5 bg-accent mx-auto mb-6"></div>
    <p class="text-dark/75 text-lg leading-relaxed max-w-3xl mx-auto" data-c="intro">{e(c["intro"])}</p>
    <div class="grid grid-cols-3 gap-3 sm:gap-6 mt-10 max-w-3xl mx-auto">
      <div class="stat"><div class="stat-n">84<span>{e(t["stat1"])}</span></div><div class="stat-l">{e(t["stat1l"])}</div></div>
      <div class="stat"><div class="stat-n"><span id="stat-rounds">5</span><span>{e(t["stat2"])}</span></div><div class="stat-l">{e(t["stat2l"])}</div></div>
      <div class="stat"><div class="stat-n">2<span>{e(t["stat3"])}</span></div><div class="stat-l">{e(t["stat3l"])}</div></div>
    </div>
  </div>
</section>

<section id="schedule" class="py-16 md:py-20 bg-stone-50">
  <div class="max-w-5xl mx-auto px-5">
    <div class="text-center mb-10">
      <p class="kicker">{e(t["sch_kicker"])}</p>
      <h2 class="sec-title">{e(t["sch_h"])}</h2>
      <div class="w-16 h-0.5 bg-accent mx-auto"></div>
    </div>
    <div id="rounds" class="space-y-4">{rounds_rows}</div>
    <p class="schedule-note" data-c="schedule_note">{e(c["schedule_note"])}</p>
  </div>
</section>

<section class="py-16 md:py-20 bg-white">
  <div class="max-w-6xl mx-auto px-5">
    <div class="text-center mb-10">
      <p class="kicker">{e(t["proc_kicker"])}</p>
      <h2 class="sec-title">{e(t["proc_h"])}</h2>
      <div class="w-16 h-0.5 bg-accent mx-auto"></div>
    </div>
    <div id="process" class="grid md:grid-cols-3 gap-5" data-c="process" data-kind="process">{process_cards}</div>
    <div class="grid md:grid-cols-3 gap-5 mt-8">
      <div class="info-card"><h3 class="info-h">🙏 {e(t["qual_h"])}</h3>{li_list(c["qualifications"], "qualifications", lang)}</div>
      <div class="info-card"><h3 class="info-h">🎒 {e(t["prep_h"])}</h3>{li_list(c["preparation"], "preparation", lang)}</div>
      <div class="info-card"><h3 class="info-h">📞 {e(t["contact_h"])}</h3><ul class="space-y-2 text-sm" data-c="contacts" data-kind="pairs">{contacts}</ul></div>
    </div>
  </div>
</section>

<section id="register" class="py-16 md:py-20 reg-section">
  <div class="max-w-3xl mx-auto px-4 sm:px-5">
    <div class="text-center mb-8">
      <p class="kicker">{e(t["reg_kicker"])}</p>
      <h2 class="sec-title">{e(t["reg_h"])}</h2>
      <div class="w-16 h-0.5 bg-accent mx-auto mb-4"></div>
      <p class="text-dark/70" data-c="register_note">{e(c["register_note"])}</p>
    </div>

    <form id="reg-form" class="reg-card" novalidate>
      <p class="text-sm text-dark/60 mb-6">{e(t["reg_lead"])}</p>
      <input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">

      <fieldset class="fset"><legend class="fleg"><span>1</span>{e(t["s1"])}</legend>
        <div class="fgroup" data-field="round_id">
          <div class="flbl req">{e(t["f_round"])}</div>
          <div id="round-options" class="grid sm:grid-cols-2 gap-2"></div>
          <p class="ferr"></p>
        </div>
        <div class="fgroup" data-field="ord_type">
          <div class="flbl req">{e(t["f_type"])}</div>
          <div class="grid sm:grid-cols-2 gap-2">
            <label class="choice"><input type="radio" name="ord_type" value="bhikkhu" checked><span><b>{e(t["f_type_b"])}</b><small>{e(t["f_type_b2"])}</small></span></label>
            <label class="choice"><input type="radio" name="ord_type" value="samanera"><span><b>{e(t["f_type_s"])}</b><small>{e(t["f_type_s2"])}</small></span></label>
          </div>
          <p class="ferr"></p>
        </div>
        <div class="fgroup" data-field="training_lang">
          <div class="flbl req">{e(t["f_tlang"])}</div>
          <div class="grid grid-cols-2 gap-2">
            <label class="choice"><input type="radio" name="training_lang" value="th"{" checked" if lang == "th" else ""}><span><b>🇹🇭 {e(t["f_tlang_th"])}</b></span></label>
            <label class="choice"><input type="radio" name="training_lang" value="ja"{" checked" if lang == "ja" else ""}><span><b>🇯🇵 {e(t["f_tlang_ja"])}</b></span></label>
          </div>
          <p class="ferr"></p>
        </div>
        <div class="fgroup" data-field="temple_id">
          <label class="flbl req" for="f-temple">{e(t["f_temple"])}</label>
          <select id="f-temple" name="temple_id" class="finp" required><option value="">{e(t["f_temple_ph"])}</option></select>
          <input id="f-temple-other" name="temple_other" class="finp mt-2 hidden" placeholder="{e(t["f_temple_other_ph"])}" maxlength="200">
          <p class="ferr"></p>
        </div>
      </fieldset>

      <fieldset class="fset"><legend class="fleg"><span>2</span>{e(t["s2"])}</legend>
        <div class="grid sm:grid-cols-4 gap-4">
          {prefix_field}
          <div class="{name_span} fgroup" data-field="full_name"><label class="flbl req" for="f-name">{e(t["f_name"])}</label><input id="f-name" name="full_name" class="finp" autocomplete="name" maxlength="160" required><p class="ferr"></p></div>
          <div class="sm:col-span-4"><label class="flbl" for="f-name-alt">{e(t["f_name_alt"])}</label><input id="f-name-alt" name="full_name_alt" class="finp" maxlength="160"></div>
          <div class="sm:col-span-2 fgroup" data-field="birth_date"><label class="flbl req" for="f-birth">{e(t["f_birth"])}</label><input id="f-birth" name="birth_date" type="date" class="finp" min="1930-01-01" max="2022-12-31" required><p class="ferr"></p></div>
          <div class="sm:col-span-2"><label class="flbl" for="f-id">{e(t["f_id"])}</label><input id="f-id" name="id_number" class="finp" maxlength="40" autocomplete="off"></div>
          <div class="sm:col-span-2"><label class="flbl" for="f-nat">{e(t["f_nat"])}</label><input id="f-nat" name="nationality" class="finp" placeholder="{e(t["f_nat_ph"])}" maxlength="60"></div>
          <div class="sm:col-span-2"><label class="flbl" for="f-rel">{e(t["f_rel"])}</label><input id="f-rel" name="religion" class="finp" placeholder="{e(t["f_rel_ph"])}" maxlength="60"></div>
          <div class="sm:col-span-2"><label class="flbl" for="f-marital">{e(t["f_marital"])}</label><select id="f-marital" name="marital" class="finp"><option value="">{e(t["choose"])}</option>{opt(t["marital"])}</select></div>
          <div><label class="flbl" for="f-h">{e(t["f_height"])}</label><input id="f-h" name="height" class="finp" inputmode="numeric" maxlength="10"></div>
          <div><label class="flbl" for="f-w">{e(t["f_weight"])}</label><input id="f-w" name="weight" class="finp" inputmode="numeric" maxlength="10"></div>
        </div>
      </fieldset>

      <fieldset class="fset"><legend class="fleg"><span>3</span>{e(t["s3"])}</legend>
        <div class="grid sm:grid-cols-2 gap-4">
          <div class="fgroup" data-field="phone"><label class="flbl req" for="f-phone">{e(t["f_phone"])}</label><input id="f-phone" name="phone" type="tel" class="finp" autocomplete="tel" maxlength="40" required><p class="ferr"></p></div>
          <div><label class="flbl" for="f-line">{e(t["f_line"])}</label><input id="f-line" name="line_id" class="finp" maxlength="80"></div>
          <div class="sm:col-span-2 fgroup" data-field="email"><label class="flbl" for="f-email">{e(t["f_email"])}</label><input id="f-email" name="email" type="email" class="finp" autocomplete="email" maxlength="160"><p class="ferr"></p></div>
          <div class="sm:col-span-2"><label class="flbl" for="f-addr">{e(t["f_addr"])}</label><textarea id="f-addr" name="address" rows="2" class="finp" maxlength="600" autocomplete="street-address"></textarea></div>
        </div>
      </fieldset>

      <fieldset class="fset"><legend class="fleg"><span>4</span>{e(t["s4"])}</legend>
        <div class="grid sm:grid-cols-2 gap-4">
          <div><label class="flbl" for="f-edu-s">{e(t["f_edu_status"])}</label><select id="f-edu-s" name="edu_status" class="finp"><option value="">{e(t["choose"])}</option>{opt(t["edu_status"])}</select></div>
          <div><label class="flbl" for="f-edu-l">{e(t["f_edu_level"])}</label><select id="f-edu-l" name="edu_level" class="finp"><option value="">{e(t["choose"])}</option>{edu_levels}</select></div>
          <div><label class="flbl" for="f-father">{e(t["f_father"])}</label><input id="f-father" name="father_name" class="finp" maxlength="120"></div>
          <div><label class="flbl" for="f-mother">{e(t["f_mother"])}</label><input id="f-mother" name="mother_name" class="finp" maxlength="120"></div>
          <div class="sm:col-span-2"><label class="flbl" for="f-em">{e(t["f_em_name"])}</label><input id="f-em" name="emergency_name" class="finp" maxlength="120"></div>
          <div><label class="flbl" for="f-em-r">{e(t["f_em_rel"])}</label><input id="f-em-r" name="emergency_relation" class="finp" placeholder="{e(t["f_em_rel_ph"])}" maxlength="60"></div>
          <div><label class="flbl" for="f-em-p">{e(t["f_em_phone"])}</label><input id="f-em-p" name="emergency_phone" type="tel" class="finp" maxlength="40"></div>
        </div>
      </fieldset>

      <fieldset class="fset"><legend class="fleg"><span>5</span>{e(t["s5"])}</legend>
        <div class="grid sm:grid-cols-2 gap-4">
          <div class="sm:col-span-2"><div class="flbl">{e(t["f_before"])}</div>
            <div class="flex gap-2"><label class="choice choice-sm"><input type="radio" name="ordained_before" value="no"><span><b>{e(t["no"])}</b></span></label><label class="choice choice-sm"><input type="radio" name="ordained_before" value="yes"><span><b>{e(t["yes"])}</b></span></label></div></div>
          <div class="sm:col-span-2 hidden" id="before-detail"><label class="flbl" for="f-bd">{e(t["f_before_detail"])}</label><input id="f-bd" name="ordained_before_detail" class="finp" maxlength="300"></div>
          <div class="sm:col-span-2"><label class="flbl" for="f-health">{e(t["f_health"])}</label><textarea id="f-health" name="health" rows="2" class="finp" maxlength="600"></textarea></div>
          <div class="sm:col-span-2"><label class="flbl" for="f-exp">{e(t["f_expect"])}</label><textarea id="f-exp" name="expectations" rows="3" class="finp" maxlength="1000"></textarea></div>
          <div><label class="flbl" for="f-src">{e(t["f_source"])}</label><input id="f-src" name="source" class="finp" maxlength="200"></div>
          <div><label class="flbl" for="f-iv">{e(t["f_interview"])}</label><input id="f-iv" name="interview_date" type="date" class="finp"></div>
          <div class="sm:col-span-2"><label class="flbl" for="f-note">{e(t["f_note"])}</label><textarea id="f-note" name="note" rows="2" class="finp" maxlength="1000"></textarea></div>
        </div>
      </fieldset>

      <div class="fgroup" data-field="consent">
        <label class="consent"><input type="checkbox" name="consent" value="1"><span>{e(t["f_consent"])}</span></label>
        <p class="ferr"></p>
      </div>
      <div id="form-alert" class="form-alert hidden" role="alert"></div>
      <button type="submit" id="reg-submit" class="btn-accent w-full text-lg py-4 mt-4">{e(t["submit"])}</button>
    </form>

    <div id="reg-done" class="reg-card text-center hidden" tabindex="-1"></div>
  </div>
</section>

<section class="py-16 bg-white">
  <div class="max-w-6xl mx-auto px-5">
    <div class="text-center mb-8"><p class="kicker">{e(t["gal_kicker"])}</p><h2 class="sec-title">{e(t["gal_h"])}</h2><div class="w-16 h-0.5 bg-accent mx-auto"></div></div>
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">{gallery}</div>
  </div>
</section>

<section class="donate">
  <div class="relative max-w-2xl mx-auto px-5 py-20">
    <div class="text-center mb-10">
      <div class="donate-icon">🙏</div>
      <p class="text-xs font-semibold mb-3 text-accent">{e(t["don_kicker"])}</p>
      <h2 class="text-white font-bold text-4xl md:text-5xl mb-5">{e(t["don_h"])}</h2>
      <div class="w-24 h-0.5 mx-auto" style="background:linear-gradient(90deg,transparent,#DAA520,transparent)"></div>
    </div>
    <div class="donate-card">
      <div class="donate-strip">{e(t["don_bank_h"])}</div>
      <div class="px-6 sm:px-8 py-4">
        <div class="donate-row"><span class="donate-ic">🏛️</span><div><p class="donate-lbl">{e(t["don_bank"])}</p><p class="font-bold text-white text-lg">{e(t["don_bank_v"])}</p></div></div>
        <div class="donate-row"><span class="donate-ic">👤</span><div><p class="donate-lbl">{e(t["don_name"])}</p><p class="font-bold text-white text-lg">Wat Phra Dhammakaya Tochigi</p></div></div>
        <div class="donate-row border-0"><span class="donate-ic">🔢</span><div class="flex-1 min-w-0"><p class="donate-lbl">{e(t["don_no"])}</p><p class="donate-no">020-4-79246-363</p></div>
          <button type="button" class="copy-btn" data-copy="020479246363" data-done="{e(t["copied"])}">{e(t["copy"])}</button></div>
      </div>
      <div class="px-6 sm:px-8 pb-8"><div class="donate-note"><p class="text-sm text-white/75">{e(t["don_thanks"])}</p><p class="text-xs mt-2 text-white/50">{e(t["don_slip"])}</p></div></div>
    </div>
    <p class="text-center text-white/50 text-sm mt-8">{e(t["don_bless"])}</p>
  </div>
</section>

<section class="py-20 bg-gradient-to-b from-[#f5f0eb] to-white">
  <div class="max-w-6xl mx-auto px-5">
    <div class="text-center mb-12">
      <span class="pill">{e(t["ct_kicker"])}</span>
      <h2 class="sec-title mt-4">{e(t["ct_h"])}</h2>
      <p class="text-primary max-w-xl mx-auto">{e(t["ct_lead"])}</p>
    </div>
    <div class="grid lg:grid-cols-2 gap-8 items-start">
      <div class="rounded-3xl overflow-hidden shadow-xl border border-accent/20"><iframe src="{MAP}" class="w-full h-80 lg:h-[460px] border-0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="map"></iframe></div>
      <div class="flex flex-col gap-4">
        <div class="ct-card"><div class="flex gap-4"><span class="ct-ic">📍</span><div><h3 class="font-bold text-dark mb-2">{e(t["ct_addr"])}</h3>
          <p class="text-primary text-sm leading-relaxed">タンマガーイ寺院栃木別院<br>〒321-0345 栃木県宇都宮市大谷町 1068<br><br>Wat Phra Dhammakaya Tochigi<br>1068 Oya-machi, Utsunomiya-shi,<br>Tochigi-ken, Japan 321-0345</p>
          <p class="text-accent text-xs mt-2 font-medium">{e(t["ct_drive"])}</p></div></div></div>
        <div class="grid sm:grid-cols-2 gap-4">
          <a href="tel:+81286528701" class="ct-card"><div class="flex items-center gap-3 mb-1"><span class="ct-ic">📞</span><h3 class="font-bold text-dark text-sm">{e(t["ct_tel"])}</h3></div><p class="text-primary text-sm">(+81) 28-652-8701</p></a>
          <a href="mailto:dimc.tochigi2004@gmail.com" class="ct-card"><div class="flex items-center gap-3 mb-1"><span class="ct-ic">✉️</span><h3 class="font-bold text-dark text-sm">{e(t["ct_mail"])}</h3></div><p class="text-primary text-sm break-all">dimc.tochigi2004@gmail.com</p></a>
        </div>
        <div class="ct-card"><div class="flex items-center gap-3"><span class="ct-ic">💬</span><div><h3 class="font-bold text-dark text-sm">LINE ID</h3><p class="text-primary text-sm">ppkaw075</p></div></div></div>
        <div class="ct-card bg-gradient-to-br from-[#4b2502]/5 to-[#DAA520]/10"><h3 class="font-bold text-dark text-sm mb-3">{e(t["ct_online"])}</h3>
          <div class="grid grid-cols-2 gap-2 text-xs">
            <a class="ct-link" href="https://www.facebook.com/วัดพระธรรมกายโทชิหงิ" target="_blank" rel="noopener">📘 Facebook</a>
            <a class="ct-link" href="https://www.youtube.com/@jeabmy123" target="_blank" rel="noopener">📺 YouTube</a>
            <a class="ct-link" href="https://thaimeisou.jp" target="_blank" rel="noopener">🧘 タイ瞑想</a>
            <a class="ct-link" href="https://meisounomori.jp" target="_blank" rel="noopener">🌿 タイ瞑想の森</a>
          </div></div>
      </div>
    </div>
  </div>
</section>

<footer class="bg-dark text-white/80 pt-14 pb-8">
  <div class="max-w-7xl mx-auto px-6">
    <div class="grid md:grid-cols-3 gap-10 mb-10">
      <div><img src="{LOGO}" alt="" class="h-16 w-auto mb-4 opacity-90">
        <p class="text-white font-bold text-lg mb-1">{e(t["temple"])}</p>
        <p class="text-white/60 text-sm">{e("タンマガーイ寺院栃木別院" if lang == "th" else "วัดพระธรรมกายโทชิหงิ")}</p>
        <p class="text-white/60 text-sm">Wat Phra Dhammakaya Tochigi</p>
        <p class="text-white/50 text-xs mt-3">{e(t["ft_tag"])}</p></div>
      <div><h4 class="text-accent font-semibold text-xs mb-4">{e(t["ft_contact"])}</h4>
        <div class="space-y-2 text-sm text-white/70"><p>📍 1068 Oya-machi, Utsunomiya-shi, Tochigi-ken, Japan 321-0345</p><p>📞 (+81) 28-652-8701</p><p>✉️ dimc.tochigi2004@gmail.com</p><p>📲 LINE ID: ppkaw075</p></div></div>
      <div><h4 class="text-accent font-semibold text-xs mb-4">{e(t["ft_other"])}</h4>
        <div class="space-y-3 text-sm">
          <a href="https://www.facebook.com/วัดพระธรรมกายโทชิหงิ" target="_blank" rel="noopener" class="block text-white/70 hover:text-white">📘 Facebook</a>
          <a href="https://www.youtube.com/@jeabmy123" target="_blank" rel="noopener" class="block text-white/70 hover:text-white">📺 YouTube Channel</a>
          <a href="https://maps.app.goo.gl/R6XF6vDPd2WkYS9h6" target="_blank" rel="noopener" class="block text-white/70 hover:text-white">🗺️ Google Maps</a>
        </div></div>
    </div>
    <div class="border-t border-white/10 pt-6 text-center text-white/40 text-xs">{e(t["ft_copy"])} · 1068 Oya-machi, Utsunomiya-shi, Tochigi-ken, Japan 321-0345</div>
  </div>
</footer>

<div id="lightbox" class="lightbox hidden" role="dialog" aria-modal="true"><button type="button" class="lightbox-x" aria-label="close">×</button><img alt=""></div>
<script src="/assets/ordination.js?v={ASSET_VER}"></script>
</body>
</html>
'''


def main():
    (ROOT / "ordination.html").write_text(build("th"), encoding="utf-8")
    (ROOT / "ja").mkdir(exist_ok=True)
    (ROOT / "ja" / "ordination.html").write_text(build("ja"), encoding="utf-8")
    print("wrote ordination.html, ja/ordination.html")


if __name__ == "__main__":
    main()
