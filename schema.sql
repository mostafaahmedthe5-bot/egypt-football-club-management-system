PRAGMA foreign_keys = ON;

-- =========================================================
-- 1. LOOKUP TABLES
-- =========================================================

CREATE TABLE IF NOT EXISTS "BloodType" (
    "Id" INTEGER PRIMARY KEY,
    "BloodTypeNameAR" TEXT,
    "BloodTypeNameEN" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "Club" (
    "Id" INTEGER PRIMARY KEY,
    "ClubNameAR" TEXT,
    "ClubNameEN" TEXT,
    "Logo" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "EducationLevel" (
    "Id" INTEGER PRIMARY KEY,
    "EducationLevelNameAR" TEXT,
    "EducationLevelNameEN" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "Equipment" (
    "Id" INTEGER PRIMARY KEY,
    "EquipmentNameAR" TEXT,
    "EquipmentNameEN" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "GuardianType" (
    "Id" INTEGER PRIMARY KEY,
    "GuardianTypeNameAR" TEXT,
    "GuardianTypeNameEN" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "MedicalReportState" (
    "Id" INTEGER PRIMARY KEY,
    "MedicalReportStateNameAR" TEXT,
    "MedicalReportStateNameEN" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "MembershipStatus" (
    "Id" INTEGER PRIMARY KEY,
    "MembershipStatusNameAR" TEXT,
    "MembershipStatusNameEN" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "MembershipType" (
    "Id" INTEGER PRIMARY KEY,
    "MembershipTypeNameAR" TEXT,
    "MembershipTypeNameEN" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "Nationality" (
    "Id" INTEGER PRIMARY KEY,
    "NationalityNameAR" TEXT,
    "NationalityNameEN" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "Religion" (
    "Id" INTEGER PRIMARY KEY,
    "ReligionNameAR" TEXT,
    "ReligionNameEN" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "SalaryPeriod" (
    "Id" INTEGER PRIMARY KEY,
    "SalaryPeriodNameAR" TEXT,
    "SalaryPeriodNameEN" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "Sport" (
    "Id" INTEGER PRIMARY KEY,
    "SportNameAR" TEXT,
    "SportNameEN" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "TeamCategory" (
    "Id" INTEGER PRIMARY KEY,
    "TeamCategoryNameAR" TEXT,
    "TeamCategoryNameEN" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "T-shirtNumber" (
    "Id" INTEGER PRIMARY KEY,
    "T-ShirtNumber" INTEGER,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);

CREATE TABLE IF NOT EXISTS "WearingSize" (
    "Id" INTEGER PRIMARY KEY,
    "WearingSizeName" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME
);


-- =========================================================
-- 2. TOURNAMENT
-- =========================================================

CREATE TABLE IF NOT EXISTS "Tournament" (
    "Id" INTEGER PRIMARY KEY,
    "TournamentNameAR" TEXT,
    "TournamentNameEN" TEXT,
    "TournamentStartDate" DATE,
    "TournamentEndDate" DATE,
    "TournamentLocation" TEXT,
    "TournamentCountryCity" TEXT,
    "TournamentType" TEXT,
    "SportId" INTEGER,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME,
    FOREIGN KEY ("SportId") REFERENCES "Sport" ("Id")
);


-- =========================================================
-- 3. RELATIONAL TABLES
-- =========================================================

CREATE TABLE IF NOT EXISTS "Guardian" (
    "Id" INTEGER PRIMARY KEY,
    "GuardianNameAR" TEXT,
    "GuardianNameEN" TEXT,
    "EducationLevelId" INTEGER,
    "NationalityId" INTEGER,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME,
    FOREIGN KEY ("EducationLevelId") REFERENCES "EducationLevel" ("Id"),
    FOREIGN KEY ("NationalityId") REFERENCES "Nationality" ("Id")
);

CREATE TABLE IF NOT EXISTS "Player" (
    "Id" INTEGER PRIMARY KEY,
    "PlayerNameAR" TEXT,
    "PlayerNameEN" TEXT,
    "ClubId" INTEGER,
    "NationalityId" INTEGER,
    "WearingSizeId" INTEGER,
    "EducationLevelId" INTEGER,
    "MedicalReportStatueId" INTEGER,
    "BloodTypeId" INTEGER,
    "MembershipStatueId" INTEGER,
    "MembershipTypeId" INTEGER,
    "ReligionId" INTEGER,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME,
    FOREIGN KEY ("BloodTypeId") REFERENCES "BloodType" ("Id"),
    FOREIGN KEY ("ClubId") REFERENCES "Club" ("Id"),
    FOREIGN KEY ("EducationLevelId") REFERENCES "EducationLevel" ("Id"),
    FOREIGN KEY ("MedicalReportStatueId") REFERENCES "MedicalReportState" ("Id"),
    FOREIGN KEY ("MembershipStatueId") REFERENCES "MembershipStatus" ("Id"),
    FOREIGN KEY ("MembershipTypeId") REFERENCES "MembershipType" ("Id"),
    FOREIGN KEY ("NationalityId") REFERENCES "Nationality" ("Id"),
    FOREIGN KEY ("ReligionId") REFERENCES "Religion" ("Id"),
    FOREIGN KEY ("WearingSizeId") REFERENCES "WearingSize" ("Id")
);

CREATE TABLE IF NOT EXISTS "PlayerEquipment" (
    "id" INTEGER PRIMARY KEY,
    "Playerid" INTEGER,
    "Eqid" INTEGER,
    FOREIGN KEY ("Eqid") REFERENCES "Equipment" ("Id"),
    FOREIGN KEY ("Playerid") REFERENCES "Player" ("Id")
);

CREATE TABLE IF NOT EXISTS "PlayerGuradian" (
    "Id" INTEGER PRIMARY KEY,
    "GuardianTypeId" INTEGER,
    "PlayerId" INTEGER,
    "GuradianId" INTEGER,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME,
    FOREIGN KEY ("GuradianId") REFERENCES "Guardian" ("Id"),
    FOREIGN KEY ("GuardianTypeId") REFERENCES "GuardianType" ("Id"),
    FOREIGN KEY ("PlayerId") REFERENCES "Player" ("Id")
);

CREATE TABLE IF NOT EXISTS "Team" (
    "Id" INTEGER PRIMARY KEY,
    "TeamAR" TEXT,
    "TeamEN" TEXT,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME,
    "Teamcatgoryid" INTEGER,
    "Clubid" INTEGER,
    "Sportid" INTEGER,
    FOREIGN KEY ("Clubid") REFERENCES "Club" ("Id"),
    FOREIGN KEY ("Sportid") REFERENCES "Sport" ("Id"),
    FOREIGN KEY ("Teamcatgoryid") REFERENCES "TeamCategory" ("Id")
);

CREATE TABLE IF NOT EXISTS "PlayerTeamSubscribtion" (
    "Id" INTEGER PRIMARY KEY,
    "Teamid" INTEGER,
    "Playerid" INTEGER,
    "Salaryid" INTEGER,
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME,
    "T-shritnumberid" INTEGER,
    FOREIGN KEY ("Playerid") REFERENCES "Player" ("Id"),
    FOREIGN KEY ("Salaryid") REFERENCES "SalaryPeriod" ("Id"),
    FOREIGN KEY ("Teamid") REFERENCES "Team" ("Id"),
    FOREIGN KEY ("T-shritnumberid") REFERENCES "T-shirtNumber" ("Id")
);

CREATE TABLE IF NOT EXISTS "TournamentTable" (
    "CreatedBy" TEXT,
    "CreatedOn" DATETIME,
    "UpdatedBy" TEXT,
    "UpdatedOn" DATETIME,
    "DeletedBy" TEXT,
    "DeletedOn" DATETIME,
    "id" INTEGER PRIMARY KEY,
    "TournamentId" INTEGER,
    "Teamid" INTEGER,
    FOREIGN KEY ("Teamid") REFERENCES "Team" ("Id"),
    FOREIGN KEY ("TournamentId") REFERENCES "Tournament" ("Id")
);

CREATE TABLE IF NOT EXISTS "Users" (
    "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Username" TEXT UNIQUE NOT NULL,
    "Password" TEXT NOT NULL,
    "Role" TEXT NOT NULL,
    "ClubId" INTEGER,
    FOREIGN KEY ("ClubId") REFERENCES "Club" ("Id")
);


-- =========================================================
-- 4. BLOOD TYPES
-- =========================================================

INSERT OR IGNORE INTO "BloodType"
("Id", "BloodTypeNameAR", "BloodTypeNameEN")
VALUES
(1, 'A موجب', 'A+'),
(2, 'A سالب', 'A-'),
(3, 'B موجب', 'B+'),
(4, 'B سالب', 'B-'),
(5, 'AB موجب', 'AB+'),
(6, 'AB سالب', 'AB-'),
(7, 'O موجب', 'O+'),
(8, 'O سالب', 'O-');


-- =========================================================
-- 5. EDUCATION LEVEL
-- =========================================================

INSERT OR IGNORE INTO "EducationLevel"
("Id", "EducationLevelNameAR", "EducationLevelNameEN")
VALUES
(1, 'بدون تعليم', 'No Education'),
(2, 'ابتدائي', 'Primary'),
(3, 'إعدادي', 'Preparatory'),
(4, 'ثانوي', 'Secondary'),
(5, 'دبلوم فني', 'Technical Diploma'),
(6, 'معهد متوسط', 'Intermediate Institute'),
(7, 'بكالوريوس', 'Bachelor''s Degree'),
(8, 'ليسانس', 'Bachelor''s Degree'),
(9, 'دبلوم دراسات عليا', 'Postgraduate Diploma'),
(10, 'ماجستير', 'Master''s Degree'),
(11, 'دكتوراه', 'PhD');


-- =========================================================
-- 6. MEDICAL REPORT STATES
-- =========================================================

INSERT OR IGNORE INTO "MedicalReportState"
("Id", "MedicalReportStateNameAR", "MedicalReportStateNameEN")
VALUES
(1, 'لم يتم الفحص', 'Not Examined'),
(2, 'قيد الفحص', 'Under Examination'),
(3, 'لائق طبيًا', 'Medically Fit'),
(4, 'لائق مع متابعة', 'Fit with Follow-up'),
(5, 'يحتاج إعادة فحص', 'Requires Re-examination'),
(6, 'غير لائق طبيًا', 'Medically Unfit'),
(7, 'التقرير منتهي', 'Report Expired');


-- =========================================================
-- 7. MEMBERSHIP STATUS
-- =========================================================

INSERT OR IGNORE INTO "MembershipStatus"
("Id", "MembershipStatusNameAR", "MembershipStatusNameEN")
VALUES
(1, 'نشطة', 'Active'),
(2, 'معلقة', 'Suspended'),
(3, 'منتهية', 'Expired'),
(4, 'ملغاة', 'Cancelled'),
(5, 'قيد التجديد', 'Renewal Pending'),
(6, 'غير نشطة', 'Inactive');


-- =========================================================
-- 8. MEMBERSHIP TYPES
-- =========================================================

INSERT OR IGNORE INTO "MembershipType"
("Id", "MembershipTypeNameAR", "MembershipTypeNameEN")
VALUES
(1, 'لاعب', 'Player'),
(2, 'لاعب أكاديمية', 'Academy Player'),
(3, 'لاعب ناشئين', 'Youth Player'),
(4, 'عضو عامل', 'Active Member'),
(5, 'عضو منتسب', 'Associate Member');


-- =========================================================
-- 9. NATIONALITIES
-- =========================================================

INSERT OR IGNORE INTO "Nationality"
("Id", "NationalityNameAR", "NationalityNameEN")
VALUES
(1, 'مصري', 'Egyptian'),
(2, 'سوداني', 'Sudanese'),
(3, 'ليبي', 'Libyan'),
(4, 'فلسطيني', 'Palestinian'),
(5, 'سوري', 'Syrian'),
(6, 'أردني', 'Jordanian'),
(7, 'لبناني', 'Lebanese'),
(8, 'عراقي', 'Iraqi'),
(9, 'سعودي', 'Saudi'),
(10, 'إماراتي', 'Emirati'),
(11, 'كويتي', 'Kuwaiti'),
(12, 'قطري', 'Qatari'),
(13, 'بحريني', 'Bahraini'),
(14, 'عُماني', 'Omani'),
(15, 'يمني', 'Yemeni'),
(16, 'تونسي', 'Tunisian'),
(17, 'جزائري', 'Algerian'),
(18, 'مغربي', 'Moroccan'),
(19, 'موريتاني', 'Mauritanian'),
(20, 'نيجيري', 'Nigerian'),
(21, 'غاني', 'Ghanaian'),
(22, 'سنغالي', 'Senegalese'),
(23, 'كاميروني', 'Cameroonian'),
(24, 'إثيوبي', 'Ethiopian'),
(25, 'كيني', 'Kenyan'),
(26, 'جنوب أفريقي', 'South African'),
(27, 'فرنسي', 'French'),
(28, 'ألماني', 'German'),
(29, 'إيطالي', 'Italian'),
(30, 'إسباني', 'Spanish'),
(31, 'بريطاني', 'British'),
(32, 'أمريكي', 'American'),
(33, 'برازيلي', 'Brazilian'),
(34, 'أرجنتيني', 'Argentine'),
(35, 'تركي', 'Turkish'),
(36, 'هندي', 'Indian'),
(37, 'باكستاني', 'Pakistani'),
(38, 'أفغاني', 'Afghan'),
(39, 'بنجلاديشي', 'Bangladeshi'),
(40, 'نيبالي', 'Nepalese'),
(41, 'صيني', 'Chinese'),
(42, 'ياباني', 'Japanese'),
(43, 'كوري', 'Korean'),
(44, 'أسترالي', 'Australian'),
(45, 'جنسية أخرى', 'Other');


-- =========================================================
-- 10. RELIGIONS
-- =========================================================

INSERT OR IGNORE INTO "Religion"
("Id", "ReligionNameAR", "ReligionNameEN")
VALUES
(1, 'مسلم', 'Muslim'),
(2, 'مسيحي', 'Christian'),
(3, 'يهودي', 'Jewish'),
(4, 'ديانة أخرى', 'Other'),
(5, 'غير محدد', 'Not Specified');


-- =========================================================
-- 11. SALARY PERIOD
-- =========================================================

INSERT OR IGNORE INTO "SalaryPeriod"
("Id", "SalaryPeriodNameAR", "SalaryPeriodNameEN")
VALUES
(1, 'شهري', 'Monthly'),
(2, 'سنوي', 'Yearly');


-- =========================================================
-- 12. WEARING SIZE
-- =========================================================

INSERT OR IGNORE INTO "WearingSize"
("Id", "WearingSizeName")
VALUES
(1, 'XXS'),
(2, 'XS'),
(3, 'S'),
(4, 'M'),
(5, 'L'),
(6, 'XL'),
(7, 'XXL'),
(8, '3XL'),
(9, '4XL'),
(10, '5XL');


-- =========================================================
-- 13. TEAM CATEGORIES
-- =========================================================

INSERT OR IGNORE INTO "TeamCategory"
("Id", "TeamCategoryNameAR", "TeamCategoryNameEN")
VALUES
(1, 'الفريق الأول', 'First Team'),
(2, 'فريق الشباب', 'Youth Team'),
(3, 'فريق الناشئين', 'Junior Team'),
(4, 'فريق البراعم', 'Junior Academy'),
(5, 'فريق الأكاديمية', 'Academy Team'),
(6, 'فريق السيدات', 'Women''s Team'),
(7, 'فريق الرجال', 'Men''s Team');


-- =========================================================
-- 14. SPORTS
-- =========================================================

INSERT OR IGNORE INTO "Sport"
("Id", "SportNameAR", "SportNameEN")
VALUES
(1, 'كرة القدم', 'Football'),
(2, 'كرة السلة', 'Basketball'),
(3, 'كرة اليد', 'Handball'),
(4, 'الكرة الطائرة', 'Volleyball'),
(5, 'تنس الطاولة', 'Table Tennis'),
(6, 'التنس', 'Tennis'),
(7, 'السباحة', 'Swimming'),
(8, 'ألعاب القوى', 'Athletics'),
(9, 'الكاراتيه', 'Karate'),
(10, 'التايكوندو', 'Taekwondo'),
(11, 'الجودو', 'Judo'),
(12, 'الملاكمة', 'Boxing'),
(13, 'المصارعة', 'Wrestling'),
(14, 'رفع الأثقال', 'Weightlifting'),
(15, 'الجمباز', 'Gymnastics'),
(16, 'الرماية', 'Shooting'),
(17, 'الفروسية', 'Equestrian'),
(18, 'الإسكواش', 'Squash'),
(19, 'الريشة الطائرة', 'Badminton'),
(20, 'الدراجات', 'Cycling');


-- =========================================================
-- 15. EQUIPMENT
-- =========================================================

INSERT OR IGNORE INTO "Equipment"
("Id", "EquipmentNameAR", "EquipmentNameEN")
VALUES
(1, 'تيشيرت تدريب', 'Training Shirt'),
(2, 'شورت', 'Shorts'),
(3, 'جوارب', 'Socks'),
(4, 'حذاء كرة قدم', 'Football Boots'),
(5, 'بدلة تدريب', 'Training Suit'),
(6, 'جاكت', 'Jacket'),
(7, 'حقيبة رياضية', 'Sports Bag'),
(8, 'واقي ساق', 'Shin Guards'),
(9, 'قفازات حارس مرمى', 'Goalkeeper Gloves');


-- =========================================================
-- 16. T-SHIRT NUMBERS
-- =========================================================

INSERT OR IGNORE INTO "T-shirtNumber"
("Id", "T-ShirtNumber")
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13),
(14, 14),
(15, 15),
(16, 16),
(17, 17),
(18, 18),
(19, 19),
(20, 20),
(21, 21),
(22, 22),
(23, 23),
(24, 24),
(25, 25),
(26, 26),
(27, 27),
(28, 28),
(29, 29),
(30, 30),
(31, 31),
(32, 32),
(33, 33),
(34, 34),
(35, 35),
(36, 36),
(37, 37),
(38, 38),
(39, 39);


-- =========================================================
-- 17. GUARDIAN TYPES
-- =========================================================

INSERT OR IGNORE INTO "GuardianType"
("Id", "GuardianTypeNameAR", "GuardianTypeNameEN")
VALUES
(1, 'الأب', 'Father'),
(2, 'الأم', 'Mother'),
(3, 'ولي أمر', 'Legal Guardian'),
(4, 'أخ', 'Brother'),
(5, 'أخت', 'Sister');


-- =========================================================
-- 18. CLUBS
-- =========================================================

INSERT OR IGNORE INTO "Club"
(
    "Id",
    "ClubNameAR",
    "ClubNameEN",
    "Logo",
    "CreatedBy",
    "CreatedOn"
)
VALUES
(
    1,
    'الأهلي',
    'Al Ahly SC',
    'https://assets.footylogos.com/logos/al-ahly-sc/al-ahly-sc-logo-footylogos.png',
    'SYSTEM',
    datetime('now')
),
(
    2,
    'الزمالك',
    'Zamalek SC',
    'https://assets.footylogos.com/logos/zamalek-sc/zamalek-sc-logo-footylogos.png',
    'SYSTEM',
    datetime('now')
),
(
    3,
    'بيراميدز',
    'Pyramids FC',
    NULL,
    'SYSTEM',
    datetime('now')
),
(
    4,
    'المصري',
    'Al Masry SC',
    NULL,
    'SYSTEM',
    datetime('now')
),
(
    5,
    'الإسماعيلي',
    'Ismaily SC',
    NULL,
    'SYSTEM',
    datetime('now')
);


-- =========================================================
-- 19. AL AHLY TEAMS
-- IDs ثابتة لتجنب مشاكل الـ Teamid
-- =========================================================

INSERT OR IGNORE INTO "Team"
(
    "Id",
    "TeamAR",
    "TeamEN",
    "Teamcatgoryid",
    "Clubid",
    "Sportid",
    "CreatedBy",
    "CreatedOn"
)
VALUES
(
    1,
    'الفريق الأول لكرة القدم',
    'Football First Team',
    1,
    1,
    1,
    'SYSTEM',
    datetime('now')
),
(
    2,
    'فريق الشباب لكرة القدم',
    'Football Youth Team',
    2,
    1,
    1,
    'SYSTEM',
    datetime('now')
),
(
    3,
    'فريق الناشئين لكرة القدم',
    'Football Junior Team',
    3,
    1,
    1,
    'SYSTEM',
    datetime('now')
),
(
    4,
    'فريق البراعم لكرة القدم',
    'Football Junior Academy Team',
    4,
    1,
    1,
    'SYSTEM',
    datetime('now')
),
(
    5,
    'فريق الأكاديمية لكرة القدم',
    'Football Academy Team',
    5,
    1,
    1,
    'SYSTEM',
    datetime('now')
),
(
    6,
    'فريق السيدات لكرة القدم',
    'Women Football Team',
    6,
    1,
    1,
    'SYSTEM',
    datetime('now')
),
(
    7,
    'فريق الرجال لكرة القدم',
    'Men Football Team',
    7,
    1,
    1,
    'SYSTEM',
    datetime('now')
);


-- =========================================================
-- 20. AL AHLY PLAYERS
-- Seed data
-- Medical/Blood/Religion values غير مستنتجة من معلومات عامة
-- =========================================================

INSERT OR IGNORE INTO "Player"
(
    "Id",
    "PlayerNameAR",
    "PlayerNameEN",
    "ClubId",
    "NationalityId",
    "WearingSizeId",
    "EducationLevelId",
    "MedicalReportStatueId",
    "BloodTypeId",
    "MembershipStatueId",
    "MembershipTypeId",
    "ReligionId",
    "CreatedBy",
    "CreatedOn"
)
VALUES

-- GOALKEEPERS

(
    1001,
    'محمد الشناوي',
    'Mohamed El Shenawy',
    1,
    1,
    7,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1002,
    'مصطفى شوبير',
    'Mostafa Shobeir',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1003,
    'حمزة علاء',
    'Hamza Alaa',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

-- DEFENDERS

(
    1004,
    'ياسين مرعي',
    'Yassin Marei',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1005,
    'ياسر إبراهيم',
    'Yasser Ibrahim',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1006,
    'هادي رياض',
    'Hady Reyad',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1007,
    'محمد هاني',
    'Mohamed Hany',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1008,
    'عمرو الجزار',
    'Amr El Gazar',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1009,
    'أحمد عيد',
    'Ahmed Eid',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1010,
    'كريم الدبيس',
    'Karim El Debes',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1011,
    'أشرف داري',
    'Achraf Dari',
    1,
    18,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1012,
    'كريم فؤاد',
    'Karim Fouad',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1013,
    'توفيق محمد',
    'Tawfik Mohamed',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

-- MIDFIELDERS

(
    1014,
    'أكرم توفيق',
    'Akram Tawfik',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1015,
    'مروان عطية',
    'Marwan Attia',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1016,
    'إمام عاشور',
    'Emam Ashour',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1017,
    'أحمد رضا',
    'Ahmed Reda',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1018,
    'محمد مجدي أفشة',
    'Mohamed Magdy Afsha',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1019,
    'عمر الساعي',
    'Omar El Saaiy',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1020,
    'طاهر محمد طاهر',
    'Taher Mohamed Taher',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1021,
    'أحمد سيد زيزو',
    'Ahmed Sayed Zizo',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1022,
    'أشرف بن شرقي',
    'Achraf Bencharki',
    1,
    18,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1023,
    'علي محمود',
    'Ali Mahmoud',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1024,
    'أحمد نبيل كوكا',
    'Ahmed Nabil Koka',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1025,
    'رضا سليم',
    'Reda Slim',
    1,
    18,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1026,
    'حسين الشحات',
    'Hussein El Shahat',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

-- FORWARDS

(
    1027,
    'أقطاي عبدالله',
    'Aqtay Abdallah',
    1,
    1,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1028,
    'منصف بقرار',
    'Monsef Bakrar',
    1,
    17,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1029,
    'سفيان بنجديدة',
    'Soufiane Benjdida',
    1,
    18,
    6,
    4,
    1,
    NULL,
    1,
    1,
    NULL,
    'SYSTEM',
    datetime('now')
),

-- BORN 2005 / YOUTH

(
    1030,
    'محمد عبدالله',
    'Mohamed Abdallah',
    1,
    1,
    5,
    4,
    1,
    NULL,
    1,
    3,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1031,
    'محمد رأفت',
    'Mohamed Raafat',
    1,
    1,
    5,
    4,
    1,
    NULL,
    1,
    3,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1032,
    'عمر سيد معوض',
    'Omar Sayed Moawad',
    1,
    1,
    5,
    4,
    1,
    NULL,
    1,
    3,
    NULL,
    'SYSTEM',
    datetime('now')
),

(
    1033,
    'أحمد خالد كباكا',
    'Ahmed Khaled Kabaka',
    1,
    1,
    5,
    4,
    1,
    NULL,
    1,
    3,
    NULL,
    'SYSTEM',
    datetime('now')
);


-- =========================================================
-- 21. PLAYER TEAM SUBSCRIPTIONS
-- =========================================================

INSERT OR IGNORE INTO "PlayerTeamSubscribtion"
(
    "Id",
    "Teamid",
    "Playerid",
    "Salaryid",
    "CreatedBy",
    "CreatedOn",
    "T-shritnumberid"
)
VALUES

(2001, 1, 1001, 1, 'SYSTEM', datetime('now'), 1),
(2002, 1, 1002, 1, 'SYSTEM', datetime('now'), 31),
(2003, 1, 1003, 1, 'SYSTEM', datetime('now'), 33),

(2004, 1, 1004, 1, 'SYSTEM', datetime('now'), 2),
(2005, 1, 1005, 1, 'SYSTEM', datetime('now'), 6),
(2006, 1, 1006, 1, 'SYSTEM', datetime('now'), 5),
(2007, 1, 1007, 1, 'SYSTEM', datetime('now'), 30),
(2008, 1, 1008, 1, 'SYSTEM', datetime('now'), 26),
(2009, 1, 1009, 1, 'SYSTEM', datetime('now'), 4),
(2010, 1, 1010, 1, 'SYSTEM', datetime('now'), 11),
(2011, 1, 1011, 1, 'SYSTEM', datetime('now'), 3),
(2012, 1, 1012, 1, 'SYSTEM', datetime('now'), 28),
(2013, 1, 1013, 1, 'SYSTEM', datetime('now'), 24),

(2014, 1, 1014, 1, 'SYSTEM', datetime('now'), 12),
(2015, 1, 1015, 1, 'SYSTEM', datetime('now'), 13),
(2016, 1, 1016, 1, 'SYSTEM', datetime('now'), 22),
(2017, 1, 1017, 1, 'SYSTEM', datetime('now'), 8),
(2018, 1, 1018, 1, 'SYSTEM', datetime('now'), 19),
(2019, 1, 1019, 1, 'SYSTEM', datetime('now'), 15),
(2020, 1, 1020, 1, 'SYSTEM', datetime('now'), 7),
(2021, 1, 1021, 1, 'SYSTEM', datetime('now'), 25),
(2022, 1, 1022, 1, 'SYSTEM', datetime('now'), 17),
(2023, 1, 1023, 1, 'SYSTEM', datetime('now'), 21),
(2024, 1, 1024, 1, 'SYSTEM', datetime('now'), 36),
(2025, 1, 1025, 1, 'SYSTEM', datetime('now'), 29),
(2026, 1, 1026, 1, 'SYSTEM', datetime('now'), 14),

(2027, 1, 1027, 1, 'SYSTEM', datetime('now'), 27),
(2028, 1, 1028, 1, 'SYSTEM', datetime('now'), 10),
(2029, 1, 1029, 1, 'SYSTEM', datetime('now'), 9),

(2030, 1, 1030, 1, 'SYSTEM', datetime('now'), 38),
(2031, 1, 1031, 1, 'SYSTEM', datetime('now'), 32),
(2032, 1, 1032, 1, 'SYSTEM', datetime('now'), 18),
(2033, 1, 1033, 1, 'SYSTEM', datetime('now'), NULL);


-- =========================================================
-- 22. PLAYER EQUIPMENT
-- =========================================================

INSERT OR IGNORE INTO "PlayerEquipment"
("id", "Playerid", "Eqid")
SELECT
    3000 + p."Id" - 1000,
    p."Id",
    1
FROM "Player" p
WHERE p."ClubId" = 1
AND p."Id" BETWEEN 1001 AND 1033;


INSERT OR IGNORE INTO "PlayerEquipment"
("id", "Playerid", "Eqid")
SELECT
    4000 + p."Id" - 1000,
    p."Id",
    2
FROM "Player" p
WHERE p."ClubId" = 1
AND p."Id" BETWEEN 1001 AND 1033;


INSERT OR IGNORE INTO "PlayerEquipment"
("id", "Playerid", "Eqid")
SELECT
    5000 + p."Id" - 1000,
    p."Id",
    3
FROM "Player" p
WHERE p."ClubId" = 1
AND p."Id" BETWEEN 1001 AND 1033;


INSERT OR IGNORE INTO "PlayerEquipment"
("id", "Playerid", "Eqid")
SELECT
    6000 + p."Id" - 1000,
    p."Id",
    4
FROM "Player" p
WHERE p."ClubId" = 1
AND p."Id" BETWEEN 1001 AND 1033;


-- =========================================================
-- 23. GOALKEEPER EQUIPMENT
-- =========================================================

INSERT OR IGNORE INTO "PlayerEquipment"
("id", "Playerid", "Eqid")
VALUES
(7001, 1001, 9),
(7002, 1002, 9),
(7003, 1003, 9);


-- =========================================================
-- 24. SAMPLE TOURNAMENTS
-- =========================================================

INSERT OR IGNORE INTO "Tournament"
(
    "Id",
    "TournamentNameAR",
    "TournamentNameEN",
    "TournamentStartDate",
    "TournamentEndDate",
    "TournamentLocation",
    "TournamentCountryCity",
    "TournamentType",
    "SportId",
    "CreatedBy",
    "CreatedOn"
)
VALUES
(
    1,
    'الدوري المصري الممتاز',
    'Egyptian Premier League',
    '2026-08-01',
    '2027-05-31',
    'مصر',
    'القاهرة - مصر',
    'League',
    1,
    'SYSTEM',
    datetime('now')
),
(
    2,
    'كأس مصر',
    'Egypt Cup',
    '2026-10-01',
    '2027-06-30',
    'مصر',
    'القاهرة - مصر',
    'Cup',
    1,
    'SYSTEM',
    datetime('now')
);


-- =========================================================
-- 25. TOURNAMENT TEAMS
-- =========================================================

INSERT OR IGNORE INTO "TournamentTable"
(
    "id",
    "TournamentId",
    "Teamid",
    "CreatedBy",
    "CreatedOn"
)
VALUES
(
    1,
    1,
    1,
    'SYSTEM',
    datetime('now')
),
(
    2,
    2,
    1,
    'SYSTEM',
    datetime('now')
);


-- =========================================================
-- 26. SAMPLE USERS
-- =========================================================

INSERT OR IGNORE INTO "Users"
(
    "Username",
    "Password",
    "Role",
    "ClubId"
)
VALUES
(
    'admin',
    'admin123',
    'SUPER_ADMIN',
    NULL
),
(
    'alahly',
    'alahly123',
    'CLUB_ADMIN',
    1
);


-- =========================================================
-- 27. FINAL PLAYER CHECK
-- =========================================================

SELECT
    p."Id",
    p."PlayerNameAR",
    p."PlayerNameEN",

    n."NationalityNameAR" AS "Nationality",

    ms."MembershipStatusNameAR" AS "MembershipStatus",

    mt."MembershipTypeNameAR" AS "MembershipType",

    mr."MedicalReportStateNameAR" AS "MedicalStatus",

    ws."WearingSizeName" AS "WearingSize",

    ts."T-ShirtNumber" AS "ShirtNumber",

    sp."SalaryPeriodNameAR" AS "SalaryPeriod",

    t."TeamAR"

FROM "Player" p

LEFT JOIN "Nationality" n
    ON n."Id" = p."NationalityId"

LEFT JOIN "MembershipStatus" ms
    ON ms."Id" = p."MembershipStatueId"

LEFT JOIN "MembershipType" mt
    ON mt."Id" = p."MembershipTypeId"

LEFT JOIN "MedicalReportState" mr
    ON mr."Id" = p."MedicalReportStatueId"

LEFT JOIN "WearingSize" ws
    ON ws."Id" = p."WearingSizeId"

LEFT JOIN "PlayerTeamSubscribtion" pts
    ON pts."Playerid" = p."Id"

LEFT JOIN "T-shirtNumber" ts
    ON ts."Id" = pts."T-shritnumberid"

LEFT JOIN "SalaryPeriod" sp
    ON sp."Id" = pts."Salaryid"

LEFT JOIN "Team" t
    ON t."Id" = pts."Teamid"

WHERE p."ClubId" = 1

ORDER BY
    CASE
        WHEN ts."T-ShirtNumber" IS NULL THEN 999
        ELSE ts."T-ShirtNumber"
    END;


-- =========================================================
-- 28. DASHBOARD COUNTS
-- =========================================================

SELECT
    COUNT(*) AS "TotalAlAhlyPlayers"
FROM "Player"
WHERE "ClubId" = 1;


SELECT
    COUNT(*) AS "TotalFirstTeamPlayers"
FROM "PlayerTeamSubscribtion" pts
JOIN "Team" t
    ON t."Id" = pts."Teamid"
WHERE t."Clubid" = 1
AND t."Id" = 1;


SELECT
    COUNT(*) AS "TotalAlAhlyEquipmentRecords"
FROM "PlayerEquipment" pe
JOIN "Player" p
    ON p."Id" = pe."Playerid"
WHERE p."ClubId" = 1;


-- =========================================================
-- 29. ADDITIONAL VALIDATION
-- =========================================================

SELECT
    t."Id",
    t."TeamAR",
    t."TeamEN",
    c."ClubNameAR",
    s."SportNameAR",
    tc."TeamCategoryNameAR"
FROM "Team" t
JOIN "Club" c
    ON c."Id" = t."Clubid"
JOIN "Sport" s
    ON s."Id" = t."Sportid"
JOIN "TeamCategory" tc
    ON tc."Id" = t."Teamcatgoryid"
WHERE t."Clubid" = 1
ORDER BY t."Id";


SELECT
    COUNT(*) AS "ForeignKeyViolations"
FROM pragma_foreign_key_check;


SELECT
    p."PlayerNameAR",
    COUNT(pts."Id") AS "SubscriptionCount"
FROM "Player" p
LEFT JOIN "PlayerTeamSubscribtion" pts
    ON pts."Playerid" = p."Id"
WHERE p."ClubId" = 1
GROUP BY p."Id", p."PlayerNameAR"
ORDER BY p."Id";