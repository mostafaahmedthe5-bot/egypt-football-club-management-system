-- تفعيل دعم Foreign Keys في SQLite
PRAGMA foreign_keys = ON;

CREATE TABLE "BloodType" (
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

CREATE TABLE "Club" (
	"Id" INTEGER PRIMARY KEY,
	"ClubNameAR" TEXT,
	"ClubNameEN" TEXT,
	"CreatedBy" TEXT,
	"CreatedOn" DATETIME,
	"UpdatedBy" TEXT,
	"UpdatedOn" DATETIME,
	"DeletedBy" TEXT,
	"DeletedOn" DATETIME
);

CREATE TABLE "EducationLevel" (
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

CREATE TABLE "Equipment" (
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

CREATE TABLE "GuardianType" (
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

CREATE TABLE "MedicalReportState" (
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

CREATE TABLE "MembershipStatus" (
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

CREATE TABLE "MembershipType" (
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

CREATE TABLE "Nationality" (
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

CREATE TABLE "Religion" (
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

CREATE TABLE "SalaryPeriod" (
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

CREATE TABLE "Sport" (
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

CREATE TABLE "TeamCategory" (
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

CREATE TABLE "Tournament" (
	"Id" INTEGER PRIMARY KEY,
	"TournamentNameAR" TEXT,
	"TournamentNameEN" TEXT,
	"CreatedBy" TEXT,
	"CreatedOn" DATETIME,
	"UpdatedBy" TEXT,
	"UpdatedOn" DATETIME,
	"DeletedBy" TEXT,
	"DeletedOn" DATETIME,
	"ToouramentDate" DATE
);

CREATE TABLE "T-shirtNumber" (
	"Id" INTEGER PRIMARY KEY,
	"T-ShirtNumber" INTEGER,
	"CreatedBy" TEXT,
	"CreatedOn" DATETIME,
	"UpdatedBy" TEXT,
	"UpdatedOn" DATETIME,
	"DeletedBy" TEXT,
	"DeletedOn" DATETIME
);

CREATE TABLE "WearingSize" (
	"Id" INTEGER PRIMARY KEY,
	"WearingSizeName" TEXT,
	"CreatedBy" TEXT,
	"CreatedOn" DATETIME,
	"UpdatedBy" TEXT,
	"UpdatedOn" DATETIME,
	"DeletedBy" TEXT,
	"DeletedOn" DATETIME
);

-- الجداول التي تحتوي على Foreign Keys

CREATE TABLE "Guardian" (
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

CREATE TABLE "Player" (
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

CREATE TABLE "PlayerEquipment" (
	"id" INTEGER PRIMARY KEY,
	"Playerid" INTEGER,
	"Eqid" INTEGER,
	FOREIGN KEY ("Eqid") REFERENCES "Equipment" ("Id"),
	FOREIGN KEY ("Playerid") REFERENCES "Player" ("Id")
);

CREATE TABLE "PlayerGuradian" (
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

CREATE TABLE "Team" (
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

CREATE TABLE "PlayerTeamSubscribtion" (
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

CREATE TABLE "TournamentTable" (
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
	"Role" TEXT NOT NULL, -- SUPER_ADMIN, CLUB_ADMIN
	"ClubId" INTEGER,
	FOREIGN KEY ("ClubId") REFERENCES "Club" ("Id")
);
INSERT OR IGNORE INTO "BloodType" ("Id", "BloodTypeNameAR", "BloodTypeNameEN") VALUES
(1, 'A موجب', 'A+'),
(2, 'A سالب', 'A-'),
(3, 'B موجب', 'B+'),
(4, 'B سالب', 'B-'),
(5, 'AB موجب', 'AB+'),
(6, 'AB سالب', 'AB-'),
(7, 'O موجب', 'O+'),
(8, 'O سالب', 'O-');

INSERT OR IGNORE INTO "EducationLevel" ("Id", "EducationLevelNameAR", "EducationLevelNameEN") VALUES
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

INSERT OR IGNORE INTO "MedicalReportState" ("Id", "MedicalReportStateNameAR", "MedicalReportStateNameEN") VALUES
(1, 'لم يتم الفحص', 'Not Examined'),
(2, 'قيد الفحص', 'Under Examination'),
(3, 'لائق طبيًا', 'Medically Fit'),
(4, 'لائق مع متابعة', 'Fit with Follow-up'),
(5, 'يحتاج إعادة فحص', 'Requires Re-examination'),
(6, 'غير لائق طبيًا', 'Medically Unfit'),
(7, 'التقرير منتهي', 'Report Expired');

INSERT OR IGNORE INTO "MembershipStatus" ("Id", "MembershipStatusNameAR", "MembershipStatusNameEN") VALUES
(1, 'نشطة', 'Active'),
(2, 'معلقة', 'Suspended'),
(3, 'منتهية', 'Expired'),
(4, 'ملغاة', 'Cancelled'),
(5, 'قيد التجديد', 'Renewal Pending'),
(6, 'غير نشطة', 'Inactive');

INSERT OR IGNORE INTO "MembershipType" ("Id", "MembershipTypeNameAR", "MembershipTypeNameEN") VALUES
(1, 'لاعب', 'Player'),
(2, 'لاعب أكاديمية', 'Academy Player'),
(3, 'لاعب ناشئين', 'Youth Player'),
(4, 'عضو عامل', 'Active Member'),
(5, 'عضو منتسب', 'Associate Member');

INSERT OR IGNORE INTO "Nationality" ("Id", "NationalityNameAR", "NationalityNameEN") VALUES
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

INSERT OR IGNORE INTO "Religion" ("Id", "ReligionNameAR", "ReligionNameEN") VALUES
(1, 'مسلم', 'Muslim'),
(2, 'مسيحي', 'Christian'),
(3, 'يهودي', 'Jewish'),
(4, 'ديانة أخرى', 'Other'),
(5, 'غير محدد', 'Not Specified');

INSERT OR IGNORE INTO "WearingSize" ("Id", "WearingSizeName") VALUES
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
INSERT OR IGNORE INTO "TeamCategory" ("Id", "TeamCategoryNameAR", "TeamCategoryNameEN") VALUES
(1, 'الفريق الأول', 'First Team'),
(2, 'فريق الشباب', 'Youth Team'),
(3, 'فريق الناشئين', 'Junior Team'),
(4, 'فريق البراعم', 'Junior Academy'),
(5, 'فريق الأكاديمية', 'Academy Team'),
(6, 'فريق السيدات', 'Women''s Team'),
(7, 'فريق الرجال', 'Men''s Team');

INSERT OR IGNORE INTO "Sport" ("Id", "SportNameAR", "SportNameEN") VALUES
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
