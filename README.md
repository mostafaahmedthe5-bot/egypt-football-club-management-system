# ⚽ Egypt Football Club Management System

A comprehensive multi-tenant football club management system designed for football clubs in Egypt.

The system provides each club with an independent management environment for handling players, teams, academies, coaches, medical records, registrations, memberships, contracts, salaries, equipment, and statistics.

At the same time, a central **Super Admin** can manage and monitor all clubs from a single platform.

---

## 📌 Project Overview

The **Egypt Football Club Management System** is designed to digitize and centralize the administrative and sporting operations of football clubs.

The platform follows a **Multi-Tenant Architecture**, where every club has its own isolated data.

Each club can manage:

* Club information
* Teams
* Players
* Academies
* Coaches
* Technical staff
* Medical staff
* Medical examinations
* Injuries
* Player registrations
* Memberships
* Contracts
* Salaries
* Bonuses
* Player measurements
* Equipment
* Statistics

The platform also provides a centralized dashboard for the **Super Admin** to monitor all registered clubs and their overall statistics.

---

# 🎯 Main Objectives

The main goals of the system are:

* Digitize football club management.
* Centralize player and club information.
* Separate every club's data securely.
* Simplify player registration and management.
* Track player medical eligibility.
* Manage contracts and salaries.
* Manage teams and age categories.
* Manage football academies.
* Track coaches and technical staff.
* Track equipment and player measurements.
* Provide detailed statistics and dashboards.
* Provide centralized monitoring for the platform administrator.

---

# 🏗️ System Architecture

The system follows a multi-tenant structure:

```text
Central Platform
│
├── Super Admin
│
├── Club 1
│   ├── Users
│   ├── Teams
│   ├── Players
│   ├── Academies
│   ├── Coaches
│   ├── Medical Records
│   ├── Contracts
│   ├── Registrations
│   ├── Memberships
│   └── Equipment
│
├── Club 2
│   ├── Users
│   ├── Teams
│   ├── Players
│   ├── Academies
│   ├── Coaches
│   ├── Medical Records
│   ├── Contracts
│   ├── Registrations
│   ├── Memberships
│   └── Equipment
│
└── Club N
    ├── Users
    ├── Teams
    ├── Players
    ├── Academies
    ├── Coaches
    ├── Medical Records
    ├── Contracts
    ├── Registrations
    ├── Memberships
    └── Equipment
```

---

# 🔐 Multi-Tenant Data Isolation

One of the most important requirements of the system is **strict data isolation between clubs**.

Every club-related record is associated with a `club_id`.

For example:

```text
Club
 ├── Users
 ├── Teams
 ├── Players
 ├── Academies
 ├── Coaches
 ├── Medical Records
 ├── Contracts
 ├── Registrations
 ├── Memberships
 └── Equipment
```

If a user belongs to:

```text
club_id = 5
```

their queries must only access data belonging to that club.

Conceptually:

```sql
SELECT *
FROM players
WHERE club_id = 5;
```

The isolation must be implemented at the **database/business-logic level**, not only by hiding records in the user interface.

---

# 👥 User Roles

The system supports multiple user roles.

## SUPER_ADMIN

The central platform administrator.

Permissions include:

* Add clubs
* Edit clubs
* Delete clubs
* Activate or deactivate clubs
* Create club user accounts
* View all clubs
* Access club data
* View centralized statistics
* Monitor overall platform activity

---

## CLUB_ADMIN

The administrator of a specific football club.

Permissions include:

* Manage club information
* Manage teams
* Manage players
* Manage academies
* Manage coaches
* Manage registrations
* Manage memberships
* Manage medical records
* Manage contracts
* Manage equipment
* View club statistics

A `CLUB_ADMIN` can only access their own club's data.

---

## COACH

Access is focused on sporting operations.

Possible permissions include:

* View assigned teams
* View players
* View player sporting information
* Manage team-related information
* View player positions
* View player performance-related data

---

## MEDICAL

Access is focused on medical information.

Permissions include:

* Medical examinations
* Injuries
* Health status
* Physical measurements
* Medical notes
* Medical eligibility

---

## FINANCE

Access is focused on financial information.

Permissions include:

* Player contracts
* Salaries
* Bonuses
* Incentives
* Contract status

---

# ⚽ Club Management

Each registered football club has its own management environment.

Club information includes:

* Club name
* Club logo
* Club information
* Teams
* Players
* Academies
* Coaches
* Technical staff
* Medical staff
* Contracts
* Registrations
* Equipment
* Statistics

Each club should feel like it has its own dedicated management platform while remaining part of the central system.

---

# 🏆 Team Management

The system supports different football teams and age categories.

Examples:

```text
First Team
U23
U21
U19
U18
U17
U16
U15
U14
U13
U12
U10
```

Additional age categories can be added.

Each team contains:

* Team name
* Age category
* Sports season
* Player count
* Maximum roster size
* Head coach
* Assistant coaches
* Team status

---

# 🏫 Football Academies

A club can have one or more football academies.

Each academy can contain:

* Academy name
* Branch
* Age category
* Coach
* Number of players
* Capacity
* Subscription status
* Player information

Academies are not restricted by the same roster limitations as senior or competitive teams.

---

# 👤 Player Management

The player module contains the complete profile of every player.

## Personal Information

* Full name
* National ID
* Date of birth
* Automatically calculated age
* Gender
* Phone number
* Email
* Marital status
* Address

---

## Sporting Information

* Club
* Current team
* Age category
* Position
* Preferred foot
* Player level
* Years of experience
* Club joining date
* Player status

### Preferred Foot

```text
Right
Left
Both
```

### Football Positions

Examples:

```text
Goalkeeper
Center Back
Right Back
Left Back
Defensive Midfielder
Midfielder
Right Winger
Left Winger
Striker
```

---

# 📋 Player Classification

Players can be classified into different categories:

```text
First Team
Youth Team
Academy
Practitioner
Amateur
```

A player can move from one category to another while maintaining a historical record of their transfers.

Example:

```text
Academy
   ↓
U15
   ↓
U17
   ↓
U21
   ↓
First Team
```

---

# 📝 Registration & Membership

The system tracks the administrative status of every player.

## Registration Status

```text
Registered
Not Registered
Pending
Suspended
Expired
```

## Membership Status

```text
Active
Expired
Suspended
Pending
```

## General Player Status

```text
Active
Injured
Suspended
Transferred
Retired
```

---

# 🩺 Medical Management

Each player can have independent medical records.

Medical information includes:

* Examination date
* Examination type
* Examination result
* Health status
* Injuries
* Physical measurements
* Medical notes
* Responsible doctor
* Medical status

## Medical Status

```text
Passed
Failed
Pending
```

---

# ✅ Player Eligibility

The system calculates whether a player is eligible to participate.

Example:

```text
Player: Ahmed Mohamed

Registration: ✓ Registered
Membership: ✓ Active
Medical Examination: ✓ Passed

Eligibility: Eligible
```

If the medical examination is invalid:

```text
Player: Ahmed Mohamed

Registration: ✓ Registered
Membership: ✓ Active
Medical Examination: ✗ Failed

Eligibility: Not Eligible

Reason:
Failed medical examination
```

Player eligibility should be calculated based on the player's administrative and medical status.

---

# 📄 Contracts & Salaries

The system manages player contracts and financial information.

Each player can have:

* Contract type
* Contract start date
* Contract end date
* Monthly salary
* Annual salary
* Maximum salary
* Bonuses
* Incentives
* Contract status

Example:

```text
Mohamed Ahmed | First Team | 50,000 EGP
Ali Hassan    | U21        | 15,000 EGP
Ahmed Samir   | Academy    | No Salary
```

---

# 👕 Player Measurements

The system stores player measurements for equipment and sportswear management.

Measurements include:

* Shirt size
* Shorts size
* Jacket size
* Shoe size
* Height
* Weight
* Body measurements
* Other sportswear measurements

---

# 🎒 Equipment Management

The equipment module tracks equipment assigned to players.

Each equipment record can contain:

* Equipment name
* Equipment type
* Quantity
* Delivery date
* Return date
* Equipment condition

Example:

```text
2 × Match Shirt
1 × Football Boots
1 × Training Suit
2 × Shorts
```

---

# 🧑‍🏫 Coaches & Technical Staff

Each club can manage its coaching and technical staff.

Examples include:

* Head Coach
* Assistant Coach
* Goalkeeper Coach
* Fitness Coach
* Performance Analyst
* Medical Staff

Coaches can be associated with the teams they work with.

---

# 📊 Club Dashboard

Every `CLUB_ADMIN` has a dashboard containing statistics for their own club.

Dashboard metrics include:

* Total players
* First-team players
* Youth players
* Academy players
* Practitioners
* Number of teams
* Number of coaches
* Registered players
* Active memberships
* Players who passed medical examinations
* Ineligible players
* Injured players
* Total monthly salaries
* Total annual salaries

---

# ⚽ Football Statistics

The club dashboard can display:

* Goalkeepers
* Defenders
* Midfielders
* Wingers
* Strikers
* Players by age category
* Players by team
* Players by position

---

# 🌍 Central Super Admin Dashboard

The `SUPER_ADMIN` dashboard provides a centralized view of the entire platform.

It includes:

* Total clubs
* Total football players
* Total teams
* Total academies
* Total coaches
* Players by club
* Players by age category
* Players by position
* Registered players
* Unregistered players
* Medical examination statistics
* Total salaries
* Average salaries

---

# 📋 Players Table

The main players page provides a professional searchable and filterable table.

Example:

| Player        | Age | Team       | Position   | Registration | Membership | Medical | Eligibility | Salary |
| ------------- | --: | ---------- | ---------- | ------------ | ---------- | ------- | ----------- | -----: |
| Ahmed Mohamed |  24 | First Team | Striker    | Registered   | Active     | Passed  | Eligible    | 50,000 |
| Ali Hassan    |  19 | U21        | Midfielder | Registered   | Active     | Passed  | Eligible    | 15,000 |

---

# 🔎 Player Search & Filters

The player list supports:

* Search by name
* Search by National ID
* Filter by team
* Filter by age
* Filter by position
* Filter by registration status
* Filter by membership status
* Filter by medical status
* Filter by eligibility

---

# 🛡️ Security Requirements

Security is a major part of the project.

The system must ensure that:

1. Users can only access data allowed by their role.
2. Club administrators cannot access another club's data.
3. Club-related records are associated with `club_id`.
4. Data isolation is enforced in database queries and business logic.
5. Sensitive credentials should not be hardcoded.
6. Passwords should be securely hashed.
7. Database access should use parameterized queries.
8. Administrative operations should validate permissions before execution.

---

# 🗄️ Data Model

The system is based around the following core entities:

```text
Clubs
Users
Teams
Players
Academies
Coaches
Medical Records
Contracts
Registrations
Memberships
Equipment
Player Equipment
Player Transfers
```

Basic relationship structure:

```text
Club
 │
 ├── Users
 │
 ├── Teams
 │    └── Players
 │
 ├── Academies
 │    └── Players
 │
 ├── Coaches
 │
 ├── Medical Records
 │    └── Players
 │
 ├── Contracts
 │    └── Players
 │
 ├── Registrations
 │    └── Players
 │
 ├── Memberships
 │    └── Players
 │
 └── Equipment
      └── Players
```

---

# 🖥️ Technology Stack

The project is designed around:

* **Python**
* **NiceGUI**
* **SQLite**
* **HTML/CSS**
* **SQL**
* **Git**
* **GitHub**

The interface is designed for Arabic users with:

* RTL layout
* Arabic language support
* Modern dashboard UI
* Responsive components
* Professional tables
* Statistics cards
* Search and filtering

---

# 🌐 User Experience

The system is designed so that every club feels like it has its own dedicated environment.

For example:

```text
Al Ahly
│
├── Dashboard
├── Teams
├── Players
├── Academy
├── Coaches
├── Medical
├── Contracts & Salaries
├── Registration & Membership
├── Equipment
└── Statistics
```

When another club logs in:

```text
Zamalek
│
├── Dashboard
├── Teams
├── Players
├── Academy
├── Coaches
├── Medical
├── Contracts & Salaries
├── Registration & Membership
├── Equipment
└── Statistics
```

The interface structure remains consistent while the data belongs exclusively to the logged-in club.

---

# 📁 Project Structure

The project is organized into separate modules for database management, business logic, UI components, and pages.

Example structure:

```text
egypt-football-club-management/
│
├── main.py
├── database.py
├── business_logic.py
├── theme.py
├── requirements.txt
├── README.md
├── .gitignore
├── run.bat
│
├── components/
│   ├── __init__.py
│   ├── cards.py
│   ├── layout.py
│   └── tables.py
│
└── pages/
    ├── __init__.py
    ├── landing.py
    ├── login_page.py
    ├── dashboard_page.py
    ├── clubs_page.py
    ├── teams_page.py
    ├── players_page.py
    ├── academies_page.py
    ├── coaches_page.py
    ├── medical_page.py
    ├── contracts_page.py
    ├── registrations_page.py
    ├── equipment_page.py
    └── statistics_page.py
```

The structure may evolve as development continues.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/egypt-football-club-management.git
```

```bash
cd egypt-football-club-management
```

---

## 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
python main.py
```

The application will normally be available at:

```text
http://localhost:8080
```

---

# ⚙️ Configuration

Sensitive configuration values should be stored outside the source code.

Recommended environment variables include:

```text
DATABASE_URL
SECRET_KEY
STORAGE_SECRET
```

Do not commit real credentials or production secrets to GitHub.

---

# 🧪 Development Status

The project is currently under active development.

### Planned / Developing Modules

* [x] Authentication
* [x] Multi-tenant concept
* [x] Club management
* [x] Dashboard concept
* [x] Team management
* [ ] Complete player management
* [ ] Academy management
* [ ] Coach management
* [ ] Medical management
* [ ] Contract management
* [ ] Registration management
* [ ] Membership management
* [ ] Equipment management
* [ ] Advanced statistics
* [ ] Complete role-based permissions
* [ ] Audit logging
* [ ] Production deployment

---

# 🔮 Future Improvements

Possible future features include:

* Advanced player performance analytics
* Player transfer history
* Contract expiration notifications
* Medical examination expiration alerts
* Injury history
* Attendance tracking
* Training management
* Match management
* Player statistics
* Goals and assists
* Cards
* Minutes played
* Performance ratings
* Scouting system
* Player reports
* PDF reports
* Excel exports
* Notifications
* Audit logs
* Advanced role permissions
* Cloud deployment
* REST API
* Mobile application

---

# 📈 Long-Term Vision

The long-term goal is to build a centralized digital platform for football club management in Egypt.

The platform can eventually support:

```text
Football Clubs
      │
      ├── First Teams
      ├── Youth Teams
      ├── Academies
      ├── Coaches
      ├── Medical Staff
      ├── Players
      ├── Contracts
      ├── Registrations
      └── Statistics
```

while maintaining strict data isolation between clubs.

The central administration can then monitor the overall football ecosystem through aggregated statistics without compromising individual club data.

---

# 🤝 Contribution

Contributions, suggestions, and improvements are welcome.

For major changes, please open an issue first to discuss the proposed changes before submitting a pull request.

---

# 📄 License

This project is currently intended for development and educational purposes.

A formal open-source license may be added in the future.

---

# 👨‍💻 Project

**Egypt Football Club Management System**

A centralized, multi-tenant platform for managing football clubs, players, teams, academies, coaches, medical records, contracts, registrations, equipment, and statistics.

---

## ⭐ Core Concept

> **One platform. Multiple clubs. Completely isolated data.**

Each football club gets its own management environment while the central administration maintains a complete overview of the platform.

---
