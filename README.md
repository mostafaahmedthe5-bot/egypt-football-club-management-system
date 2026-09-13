# Egypt Football Club Management System

A modern multi-tenant football club management system built for football clubs in Egypt.

The platform provides clubs with a centralized digital environment to manage players, teams, academies, coaches, medical records, memberships, registrations, contracts, salaries, equipment, and football statistics.

The system is designed around a **Multi-Tenant Architecture**, allowing multiple football clubs to use the same platform while keeping their data completely isolated.

---

## Overview

Managing football clubs involves a large amount of administrative, sporting, medical, and financial data.

The Egypt Football Club Management System brings these operations together in one platform.

Each club has its own environment where authorized staff can manage:

* Players
* Teams
* Academies
* Coaches and technical staff
* Medical records
* Player registrations
* Memberships
* Contracts and salaries
* Equipment
* Player measurements
* Football statistics

A central **Super Admin** can manage the clubs registered on the platform and monitor aggregated platform statistics.

---

## Core Concept

The platform is built around one simple concept:

> **One platform. Multiple football clubs. Completely isolated data.**

For example:

```text
Central Platform
│
├── Super Admin
│
├── Al Ahly
│   ├── Teams
│   ├── Players
│   ├── Academy
│   ├── Coaches
│   ├── Medical
│   ├── Contracts
│   ├── Memberships
│   └── Equipment
│
├── Zamalek
│   ├── Teams
│   ├── Players
│   ├── Academy
│   ├── Coaches
│   ├── Medical
│   ├── Contracts
│   ├── Memberships
│   └── Equipment
│
└── Other Clubs
    └── Independent Club Data
```

The interface and platform remain centralized, while every club operates on its own isolated data.

---

# Multi-Tenant Architecture

Data isolation is one of the most important parts of the system.

Every club-related record is associated with its club.

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
 ├── Memberships
 └── Equipment
```

A club administrator can only access records belonging to their club.

The isolation is enforced through the application's database queries and business logic rather than relying only on the user interface.

This prevents users from accessing or modifying another club's data.

---

# User Roles

The system is designed to support different roles based on operational responsibilities.

## Super Admin

The central platform administrator.

Main responsibilities:

* Manage clubs
* Create and manage club accounts
* Activate or deactivate clubs
* Access platform-wide statistics
* Monitor registered clubs
* Manage platform-level settings

---

## Club Admin

The administrator of an individual football club.

Main responsibilities:

* Manage club information
* Manage teams
* Manage players
* Manage academies
* Manage coaches
* Manage memberships
* Manage registrations
* Manage medical information
* Manage contracts
* Manage equipment
* View club statistics

A Club Admin is restricted to their assigned club.

---

## Coach

Focused primarily on sporting operations.

Possible responsibilities:

* View assigned teams
* View players
* View sporting information
* Manage team information
* View player positions
* Monitor player performance

---

## Medical Staff

Focused on player medical information.

Possible responsibilities:

* Medical examinations
* Medical eligibility
* Injury records
* Physical measurements
* Medical notes
* Player health status

---

## Finance

Focused on financial operations.

Possible responsibilities:

* Player contracts
* Salaries
* Bonuses
* Incentives
* Contract status
* Contract expiration

---

# Club Management

Each club has its own management environment.

Club information can include:

* Arabic and English club name
* Club logo
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

The goal is for each club to feel like it has its own dedicated management system while still operating within the central platform.

---

# Team Management

The system supports different football teams and age categories.

Typical categories include:

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

Each team can contain:

* Team name
* Age category
* Season
* Player count
* Maximum roster size
* Head coach
* Assistant coaches
* Team status

The structure can also be extended with additional categories when required by a club.

---

# Football Academies

Clubs can manage multiple football academies and academy branches.

Academy information can include:

* Academy name
* Branch
* Age category
* Coach
* Player count
* Capacity
* Subscription status
* Player information

Academies are handled separately from competitive teams because their player capacity and management requirements can be different.

---

# Player Management

The player module is one of the core components of the platform.

Each player can have a complete profile containing personal, sporting, administrative, medical, and financial information.

## Personal Information

* Full name
* National ID
* Date of birth
* Calculated age
* Gender
* Phone number
* Email
* Address
* Marital status

## Sporting Information

* Club
* Team
* Age category
* Position
* Preferred foot
* Player level
* Years of experience
* Joining date
* Player status

### Preferred Foot

```text
Right
Left
Both
```

### Football Positions

```text
Goalkeeper
Center Back
Right Back
Left Back
Defensive Midfielder
Central Midfielder
Attacking Midfielder
Right Winger
Left Winger
Striker
```

---

# Player Classification

Players can be organized according to their sporting level and development stage.

Examples:

```text
First Team
Youth Team
Academy
Amateur
Practitioner
```

A player's progression can be tracked over time:

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

Historical team and registration records can be used to maintain the player's development history.

---

# Registration & Membership

The system tracks the administrative status of players.

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
Cancelled
```

## Player Status

```text
Active
Injured
Suspended
Transferred
Retired
```

These statuses can be used together to determine the player's current administrative and sporting situation.

---

# Medical Management

Medical information is maintained separately from general player information.

Medical records can include:

* Examination date
* Examination type
* Examination result
* Medical status
* Injuries
* Physical measurements
* Medical notes
* Responsible doctor
* Medical eligibility

Example medical states:

```text
Passed
Failed
Pending
```

---

# Player Eligibility

The system can calculate player eligibility using multiple conditions.

For example:

```text
Registration: Registered
Membership: Active
Medical Status: Passed

Eligibility: Eligible
```

If one of the required conditions is not satisfied:

```text
Registration: Registered
Membership: Active
Medical Status: Failed

Eligibility: Not Eligible
```

The system can also display the reason for the player's ineligibility.

---

# Contracts & Salaries

The financial module manages player contracts and compensation.

Contract information can include:

* Contract type
* Start date
* End date
* Monthly salary
* Annual salary
* Maximum salary
* Bonuses
* Incentives
* Contract status

Example:

```text
First Team Player    | 50,000 EGP / Month
U21 Player           | 15,000 EGP / Month
Academy Player       | No Salary
```

This information can also be used for financial statistics and reporting.

---

# Player Measurements

The system supports sportswear and physical measurement management.

Information can include:

* Shirt size
* Shorts size
* Jacket size
* Shoe size
* Height
* Weight
* Body measurements
* Other equipment measurements

This helps clubs manage player equipment more efficiently.

---

# Equipment Management

The equipment module tracks items assigned to players.

Equipment records can include:

* Equipment name
* Equipment type
* Quantity
* Delivery date
* Return date
* Condition

Example:

```text
2 × Match Shirts
1 × Football Boots
1 × Training Suit
2 × Shorts
```

The system can maintain the relationship between players and their assigned equipment.

---

# Coaches & Technical Staff

Clubs can manage coaching and technical staff across their teams.

Examples include:

* Head Coach
* Assistant Coach
* Goalkeeper Coach
* Fitness Coach
* Performance Analyst
* Medical Staff

Staff members can be associated with specific teams and responsibilities.

---

# Club Dashboard

Each club has a dedicated dashboard showing important operational statistics.

Examples include:

* Total players
* First-team players
* Youth players
* Academy players
* Number of teams
* Number of coaches
* Registered players
* Active memberships
* Medical examination statistics
* Eligible players
* Ineligible players
* Injured players
* Monthly salaries
* Annual salaries

---

# Football Statistics

The platform is designed to provide football-specific statistics such as:

* Players by position
* Players by team
* Players by age category
* Goalkeepers
* Defenders
* Midfielders
* Wingers
* Strikers
* Player distribution
* Team roster statistics

Future versions can expand this area into detailed performance analytics.

---

# Super Admin Dashboard

The Super Admin dashboard provides a centralized view of the platform.

It can include:

* Total clubs
* Total players
* Total teams
* Total academies
* Total coaches
* Players by club
* Players by age category
* Players by position
* Registration statistics
* Membership statistics
* Medical statistics
* Salary statistics
* Average salaries

The Super Admin can monitor the platform without compromising individual club data isolation.

---

# Search & Filtering

The player management interface supports advanced search and filtering.

Possible filters include:

* Player name
* National ID
* Team
* Age
* Position
* Registration status
* Membership status
* Medical status
* Eligibility

This allows club staff to quickly find the information they need.

---

# Security

Security and data isolation are core requirements of the system.

The application is designed to ensure that:

1. Users can only access data permitted by their role.
2. Club administrators cannot access another club's records.
3. Club-related data is associated with the correct club.
4. Database queries use parameterized values.
5. Permission checks are performed before administrative operations.
6. Sensitive credentials are not stored directly in source code.
7. Passwords are securely hashed.
8. Business logic enforces tenant isolation.

---

# Database

The project uses SQLite as its current database engine.

The database is organized around lookup tables and relational entities covering areas such as:

```text
Club
User
Player
Team
Sport
Team Category
Tournament
Membership
Medical
Guardian
Equipment
Contracts
Registrations
Player-Team Relationships
```

Foreign-key relationships are used to maintain data integrity between related entities.

---

# Technology Stack

The project is built with:

* Python
* NiceGUI
* SQLite
* SQL
* HTML/CSS
* Git
* GitHub

The interface is designed specifically for Arabic-speaking football organizations and uses:

* RTL layout
* Arabic interface
* Cairo font
* Responsive components
* Modern dashboards
* Searchable tables
* Statistics cards
* Football-oriented visual design

---

# Project Structure

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
    ├── memberships_page.py
    ├── equipment_page.py
    └── statistics_page.py
```

The structure may evolve as new modules are added.

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/egypt-football-club-management.git
cd egypt-football-club-management
```

## Create a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python main.py
```

The application runs by default on:

```text
http://localhost:8080
```

---

# Configuration

Production configuration should be stored outside the source code.

Recommended environment variables include:

```text
DATABASE_URL
SECRET_KEY
STORAGE_SECRET
```

Never commit production credentials, passwords, API keys, or secret keys to GitHub.

---

# Development Status

The project is currently under active development.

### Completed / In Progress

* [x] Authentication
* [x] Multi-tenant architecture concept
* [x] Club management
* [x] Dashboard
* [x] Team management
* [x] Player management foundation
* [x] Membership management
* [ ] Complete academy management
* [ ] Complete coach management
* [ ] Complete medical management
* [ ] Complete contract management
* [ ] Registration management
* [ ] Equipment management
* [ ] Advanced statistics
* [ ] Complete role-based permissions
* [ ] Audit logging
* [ ] Production deployment

---

# Roadmap

Future versions may include:

* Player transfer history
* Contract expiration notifications
* Medical examination alerts
* Injury history
* Attendance tracking
* Training management
* Match management
* Player performance statistics
* Goals and assists
* Minutes played
* Cards
* Performance ratings
* Scouting
* Player reports
* PDF reports
* Excel exports
* Notifications
* Audit logs
* Advanced permissions
* REST API
* Cloud deployment
* Mobile application

---

# Long-Term Vision

The long-term goal is to develop a complete digital infrastructure for football club management in Egypt.

The platform is intended to connect club administration, sporting operations, medical departments, financial management, academies, and player management in one centralized system.

The architecture allows the platform to grow from a club management application into a larger football management ecosystem while maintaining strict separation between clubs.

---

# License

This project is currently intended for development and educational purposes.

A formal open-source license may be added in a future release.

---

# Project

**Egypt Football Club Management System**

A multi-tenant football management platform designed to help Egyptian football clubs manage their players, teams, academies, staff, medical operations, memberships, contracts, equipment, and statistics from one centralized system.

**Core Principle:**

> One platform. Multiple clubs. Isolated data. Centralized management.
