import sqlite3
import os


def setup_database():
    db_file = 'sports_club.db'

    if os.path.exists(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        with open('schema.sql', 'r', encoding='utf-8') as f:
            cursor.executescript(f.read())

        # =====================================================
        # قائمة الأندية
        # =====================================================

        clubs_list = [
            "الأهلي",
            "الزمالك",
            "بيراميدز",
            "المصري",
            "الإسماعيلي",
            "الاتحاد السكندري",
            "سموحة",
            "إنبي",
            "البنك الأهلي",
            "سيراميكا كليوباترا",
            "الجونة",
            "طلائع الجيش",
            "مودرن سبورت",
            "زد",
            "المقاولون العرب",
            "وادي دجلة",
            "غزل المحلة",
            "فاركو",
            "حرس الحدود",
            "بتروجيت",
            "كهرباء الإسماعيلية"
        ]

        # =====================================================
        # إضافة الأندية
        # لو النادي موجود بالفعل في schema.sql يتم تجاهله
        # =====================================================

        for index, club_name in enumerate(clubs_list, start=1):

            cursor.execute(
                """
                INSERT OR IGNORE INTO Club
                (
                    Id,
                    ClubNameAR,
                    ClubNameEN,
                    CreatedBy,
                    CreatedOn
                )
                VALUES (?, ?, ?, ?, datetime('now'))
                """,
                (
                    index,
                    club_name,
                    club_name,
                    'SYSTEM'
                )
            )

        # =====================================================
        # إضافة مستخدمي الأندية
        # =====================================================

        for index in range(1, len(clubs_list) + 1):

            cursor.execute(
                """
                INSERT OR IGNORE INTO Users
                (
                    Username,
                    Password,
                    Role,
                    ClubId
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    f'club_{index}',
                    '123',
                    'CLUB_ADMIN',
                    index
                )
            )

        conn.commit()

        print('==============================================')
        print('✅ تم إنشاء قاعدة البيانات بنجاح')
        print(f'✅ عدد الأندية: {len(clubs_list)}')
        print('✅ تم إنشاء مستخدمي الأندية')
        print('✅ كلمة المرور الافتراضية: 123')
        print('==============================================')

    except Exception as e:

        conn.rollback()

        print(
            f'❌ خطأ أثناء إنشاء قاعدة البيانات: '
            f'{type(e).__name__}: {e}'
        )

        raise

    finally:
        conn.close()


if __name__ == '__main__':
    setup_database()