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