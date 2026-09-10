import sqlite3
import os

def setup_database():
    db_file = 'sports_club.db'
    if os.path.exists(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    with open('schema.sql', 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())

    # قائمة الأندية
    teams_list = [
        "الأهلي", "الزمالك", "بيراميدز", "المصري", "الإسماعيلي",
        "الاتحاد السكندري", "سموحة", "إنبي", "البنك الأهلي",
        "سيراميكا كليوباترا", "الجونة", "طلائع الجيش", "مودرن سبورت",
        "زد", "المقاولون العرب", "وادي دجلة", "غزل المحلة", "فاركو",
        "حرس الحدود", "بتروجيت", "كهرباء الإسماعيلية"
    ]

    # إدخال الأندية ومستخدميها بكلمة مرور افتراضية "123"
    for index, team_name in enumerate(teams_list, start=1):
        cursor.execute("INSERT INTO Club (Id, ClubNameAR, ClubNameEN) VALUES (?, ?, ?)", (index, team_name, team_name))
        cursor.execute("INSERT INTO Users (Username, Password, Role, ClubId) VALUES (?, ?, ?, ?)", 
                       (f"club_{index}", "123", "CLUB_ADMIN", index))

    conn.commit()
    conn.close()
    print("✅ تم إنشاء القاعدة وكل الأندية وأزرار الدخول بنجاح!")

if __name__ == '__main__':
    setup_database()