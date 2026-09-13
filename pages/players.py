from nicegui import ui, app
import database as db

# =========================================================
# Club Images
# =========================================================

CLUB_LOGOS = {
    'الأهلي': 'https://assets.footylogos.com/logos/al-ahly-sc/al-ahly-sc-logo-footylogos.png',
    'الزمالك': 'https://assets.footylogos.com/logos/zamalek-sc/zamalek-sc-logo-footylogos.png',
}

CLUB_TEAM_PHOTOS = {
    'الأهلي': 'https://mediaaws-live.almasryalyoum.com/almasryalyoum/uploads/images/2026/02/28/thumbs/600x600/1652556.jpg',
}

# =========================================================
# Player Photos
#
# IMPORTANT:
# Do not put invented URLs here.
# Add verified direct image URLs only.
# If a player has no image, the page automatically
# falls back to the player's initials.
# =========================================================

PLAYER_PHOTOS = {

    # -----------------------------------------------------
    # Emam Ashour
    # Direct image source currently available
    # -----------------------------------------------------
    'emam ashour':
        'https://www.cairo24.com/Upload/libfiles/107/8/710.jfif',

    'إمام عاشور':
        'https://www.cairo24.com/Upload/libfiles/107/8/710.jfif',

    # -----------------------------------------------------
    # You can add more verified direct image URLs here.
    #
    # Example:
    #
    # 'mohamed el shenawy':
    #     'DIRECT_IMAGE_URL',
    #
    # 'محمد الشناوي':
    #     'DIRECT_IMAGE_URL',
    # -----------------------------------------------------
}


# =========================================================
# Helpers
# =========================================================

def safe_text(value, fallback='غير محدد'):
    if value is None:
        return fallback

    value = str(value).strip()

    return value if value else fallback


def safe_id(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def option_label(row, ar_key, en_key=None, fallback_key='Id'):
    if not row:
        return ''

    ar_value = row.get(ar_key)

    if ar_value:
        return str(ar_value)

    if en_key:
        en_value = row.get(en_key)

        if en_value:
            return str(en_value)

    return str(row.get(fallback_key, ''))


def get_status_color(status):
    text = safe_text(status, '').lower()

    positive_words = [
        'سليم',
        'ناجح',
        'صالح',
        'فعال',
        'مقبول',
        'لائق',
        'نشطة',
        'نشط',
        'passed',
        'active',
        'valid',
        'approved',
        'fit',
    ]

    negative_words = [
        'راسب',
        'غير صالح',
        'مرفوض',
        'غير فعال',
        'غير لائق',
        'منتهية',
        'ملغاة',
        'expired',
        'failed',
        'inactive',
        'rejected',
        'unfit',
    ]

    warning_words = [
        'انتظار',
        'معلق',
        'معلقة',
        'قيد',
        'متابعة',
        'pending',
        'waiting',
        'review',
    ]

    if any(word in text for word in positive_words):
        return 'positive'

    if any(word in text for word in negative_words):
        return 'negative'

    if any(word in text for word in warning_words):
        return 'warning'

    return 'neutral'


def status_classes(status):
    color = get_status_color(status)

    if color == 'positive':
        return 'bg-emerald-50 text-emerald-700 border border-emerald-200'

    if color == 'negative':
        return 'bg-red-50 text-red-700 border border-red-200'

    if color == 'warning':
        return 'bg-amber-50 text-amber-700 border border-amber-200'

    return 'bg-slate-50 text-slate-600 border border-slate-200'


def get_initials(name):
    name = safe_text(name, '')

    if not name:
        return '؟'

    parts = [
        part.strip()
        for part in name.split()
        if part.strip()
    ]

    if len(parts) >= 2:
        return parts[0][0] + parts[1][0]

    return parts[0][0]


def get_avatar_classes(player_id):
    try:
        value = int(player_id)
    except (TypeError, ValueError):
        value = 0

    classes = [
        'avatar-navy',
        'avatar-blue',
        'avatar-indigo',
        'avatar-slate',
        'avatar-cyan',
        'avatar-teal',
    ]

    return classes[value % len(classes)]


# =========================================================
# Name normalization
# =========================================================

def normalize_player_name(name):
    if not name:
        return ''

    name = str(name).strip().lower()

    replacements = {
        'أ': 'ا',
        'إ': 'ا',
        'آ': 'ا',
        'ى': 'ي',
        'ة': 'ه',
        'ـ': '',
        '"': '',
        "'": '',
        '’': '',
        '“': '',
        '”': '',
        '«': '',
        '»': '',
        '-': ' ',
        '_': ' ',
    }

    for old, new in replacements.items():
        name = name.replace(old, new)

    return ' '.join(name.split())


# =========================================================
# Get player photo
# =========================================================

def get_player_photo(player):
    if not player:
        return None

    player_name_ar = normalize_player_name(
        player.get('PlayerNameAR')
    )

    player_name_en = normalize_player_name(
        player.get('PlayerNameEN')
    )

    # -----------------------------------------------------
    # Arabic lookup
    # -----------------------------------------------------

    for name, url in PLAYER_PHOTOS.items():

        normalized_key = normalize_player_name(name)

        if normalized_key == player_name_ar:
            return url

    # -----------------------------------------------------
    # English lookup
    # -----------------------------------------------------

    for name, url in PLAYER_PHOTOS.items():

        normalized_key = normalize_player_name(name)

        if normalized_key == player_name_en:
            return url

    # -----------------------------------------------------
    # Partial English matching
    # -----------------------------------------------------

    if player_name_en:

        for name, url in PLAYER_PHOTOS.items():

            normalized_key = normalize_player_name(name)

            if (
                normalized_key in player_name_en
                or player_name_en in normalized_key
            ):
                return url

    return None


# =========================================================
# Get club logo
# =========================================================

def get_club_logo_url(club_name):
    if not club_name:
        return None

    club_name = str(club_name).strip()

    return CLUB_LOGOS.get(club_name)


# =========================================================
# Get club team photo
# =========================================================

def get_club_team_photo_url(club_name):
    if not club_name:
        return None

    club_name = str(club_name).strip()

    return CLUB_TEAM_PHOTOS.get(club_name)


# =========================================================
# Main page
# =========================================================

def content(club_id=None):

    # =====================================================
    # Current club
    # =====================================================

    if club_id is None:
        club_id = app.storage.user.get('club_id')

    if not club_id:
        ui.navigate.to('/select_club')
        return

    club_id = safe_id(club_id)

    if not club_id:
        ui.navigate.to('/select_club')
        return

    # =====================================================
    # Club information
    # =====================================================

    club = db.fetch_one(
        """
        SELECT
            Id,
            ClubNameAR,
            ClubNameEN
        FROM Club
        WHERE Id = ?
        """,
        (club_id,)
    )

    if not club:
        ui.notify(
            'النادي غير موجود',
            color='negative'
        )

        ui.navigate.to('/select_club')
        return

    club_name = safe_text(
        club['ClubNameAR'],
        'النادي'
    )

    club_name_en = safe_text(
        club['ClubNameEN'],
        ''
    )

    club_logo_url = get_club_logo_url(
        club_name
    )

    club_team_photo_url = get_club_team_photo_url(
        club_name
    )

    # =====================================================
    # Hero background
    # =====================================================

    if club_team_photo_url:

        hero_background = f"""
            background-image:
                linear-gradient(
                    90deg,
                    rgba(5, 15, 12, .94) 0%,
                    rgba(15, 23, 42, .78) 48%,
                    rgba(15, 23, 42, .34) 100%
                ),
                url("{club_team_photo_url}");
            background-size: cover;
            background-position: center 35%;
            background-repeat: no-repeat;
        """

    else:

        hero_background = """
            background:
                linear-gradient(
                    135deg,
                    #0f172a 0%,
                    #172554 55%,
                    #1e3a8a 100%
                );
        """

    # =====================================================
    # CSS
    # =====================================================

    ui.add_head_html(
        """
        <style>

            /* =================================================
               Page
               ================================================= */

            .players-page {
                min-height: calc(100vh - 20px);
                width: 100%;

                background:
                    radial-gradient(
                        circle at 90% 0%,
                        rgba(245,158,11,.08),
                        transparent 24%
                    ),
                    radial-gradient(
                        circle at 0% 80%,
                        rgba(30,58,138,.06),
                        transparent 30%
                    ),
                    linear-gradient(
                        135deg,
                        #f8fafc 0%,
                        #f1f5f9 100%
                    );
            }


            /* =================================================
               Hero
               ================================================= */

            .players-hero {
                width: 100%;
                min-height: 270px;

                border-radius: 28px;
                padding: 30px;

                position: relative;
                overflow: hidden;

                box-shadow:
                    0 22px 55px rgba(15,23,42,.22);

                border:
                    1px solid rgba(255,255,255,.12);
            }


            .players-hero::before {
                content: "";

                position: absolute;

                width: 360px;
                height: 360px;

                border-radius: 50%;

                background:
                    rgba(220,38,38,.13);

                top: -210px;
                left: -100px;
            }


            .players-hero::after {
                content: "";

                position: absolute;

                width: 420px;
                height: 420px;

                border-radius: 50%;

                background:
                    rgba(245,158,11,.09);

                bottom: -290px;
                right: -120px;
            }


            .hero-content {
                position: relative;
                z-index: 3;
            }


            .hero-icon {
                width: 70px;
                height: 70px;

                border-radius: 21px;

                background:
                    rgba(255,255,255,.96);

                border:
                    2px solid rgba(255,255,255,.8);

                display: flex;
                align-items: center;
                justify-content: center;

                box-shadow:
                    0 14px 30px rgba(0,0,0,.20);

                overflow: hidden;
            }


            .hero-club-logo {
                width: 82px;
                height: 82px;

                border-radius: 24px;

                background:
                    rgba(255,255,255,.96);

                display: flex;
                align-items: center;
                justify-content: center;

                padding: 10px;

                box-shadow:
                    0 14px 30px rgba(0,0,0,.22);

                border:
                    2px solid rgba(255,255,255,.75);

                overflow: hidden;
            }


            .hero-title {
                color: white;

                font-size: 31px;
                font-weight: 900;

                line-height: 1.2;

                text-shadow:
                    0 3px 15px rgba(0,0,0,.30);
            }


            .hero-subtitle {
                color:
                    rgba(255,255,255,.78);

                font-size: 14px;
                font-weight: 600;
            }


            .hero-football-label {
                display: inline-flex;
                align-items: center;
                gap: 7px;

                background:
                    rgba(220,38,38,.22);

                border:
                    1px solid rgba(248,113,113,.28);

                color:
                    #fecaca;

                border-radius: 999px;

                padding:
                    7px 13px;

                font-size: 11px;
                font-weight: 900;
            }


            .club-badge {
                background:
                    rgba(245,158,11,.16);

                border:
                    1px solid rgba(245,158,11,.34);

                color:
                    #fbbf24;

                border-radius: 999px;

                padding:
                    8px 14px;

                font-size: 13px;
                font-weight: 800;
            }


            /* =================================================
               Statistics
               ================================================= */

            .stats-grid {
                display: grid;

                grid-template-columns:
                    repeat(4, minmax(0, 1fr));

                gap: 16px;

                width: 100%;
            }


            .stat-card {
                background:
                    white;

                border:
                    1px solid #e2e8f0;

                border-radius:
                    22px;

                padding:
                    20px;

                box-shadow:
                    0 8px 25px rgba(15,23,42,.045);

                transition:
                    transform .2s ease,
                    box-shadow .2s ease;
            }


            .stat-card:hover {
                transform:
                    translateY(-3px);

                box-shadow:
                    0 15px 35px rgba(15,23,42,.08);
            }


            .stat-icon {
                width: 46px;
                height: 46px;

                border-radius: 15px;

                display: flex;
                align-items: center;
                justify-content: center;
            }


            .stat-number {
                color:
                    #0f172a;

                font-size:
                    28px;

                font-weight:
                    900;

                line-height:
                    1;
            }


            .stat-label {
                color:
                    #64748b;

                font-size:
                    12px;

                font-weight:
                    800;
            }


            /* =================================================
               Filters
               ================================================= */

            .filter-card {
                width: 100%;

                background:
                    white;

                border:
                    1px solid #e2e8f0;

                border-radius:
                    24px;

                padding:
                    20px;

                box-shadow:
                    0 8px 25px rgba(15,23,42,.045);
            }


            .filter-title {
                color:
                    #0f172a;

                font-size:
                    18px;

                font-weight:
                    900;
            }


            .filter-label {
                color:
                    #475569;

                font-size:
                    12px;

                font-weight:
                    800;

                margin-bottom:
                    5px;
            }


            .filter-grid {
                display: grid;

                grid-template-columns:
                    2fr 1fr 1fr 1fr auto;

                gap:
                    12px;

                width:
                    100%;
            }


            /* =================================================
               Player list
               ================================================= */

            .players-card {
                width: 100%;

                background:
                    white;

                border:
                    1px solid #e2e8f0;

                border-radius:
                    24px;

                padding:
                    20px;

                box-shadow:
                    0 8px 25px rgba(15,23,42,.045);
            }


            .players-card-header {
                padding-bottom:
                    16px;

                border-bottom:
                    1px solid #f1f5f9;
            }


            .player-row {
                width: 100%;

                background:
                    white;

                border:
                    1px solid #e2e8f0;

                border-radius:
                    20px;

                padding:
                    15px;

                transition:
                    transform .18s ease,
                    border-color .18s ease,
                    box-shadow .18s ease;
            }


            .player-row:hover {
                transform:
                    translateY(-2px);

                border-color:
                    #cbd5e1;

                box-shadow:
                    0 10px 25px rgba(15,23,42,.06);
            }


            .player-main {
                min-width:
                    260px;
            }


            .player-avatar {
                width:
                    64px;

                height:
                    64px;

                min-width:
                    64px;

                border-radius:
                    18px;

                display:
                    flex;

                align-items:
                    center;

                justify-content:
                    center;

                color:
                    white;

                font-size:
                    17px;

                font-weight:
                    900;

                box-shadow:
                    0 8px 18px rgba(15,23,42,.14);

                overflow:
                    hidden;

                position:
                    relative;
            }


            .player-avatar-image {
                width:
                    100%;

                height:
                    100%;

                object-fit:
                    cover;

                object-position:
                    center top;

                display:
                    block;
            }


            .player-avatar-fallback {
                width:
                    100%;

                height:
                    100%;

                display:
                    flex;

                align-items:
                    center;

                justify-content:
                    center;
            }


            .avatar-navy {
                background:
                    linear-gradient(
                        135deg,
                        #0f172a,
                        #334155
                    );
            }


            .avatar-blue {
                background:
                    linear-gradient(
                        135deg,
                        #1d4ed8,
                        #3b82f6
                    );
            }


            .avatar-indigo {
                background:
                    linear-gradient(
                        135deg,
                        #3730a3,
                        #6366f1
                    );
            }


            .avatar-slate {
                background:
                    linear-gradient(
                        135deg,
                        #334155,
                        #64748b
                    );
            }


            .avatar-cyan {
                background:
                    linear-gradient(
                        135deg,
                        #0e7490,
                        #06b6d4
                    );
            }


            .avatar-teal {
                background:
                    linear-gradient(
                        135deg,
                        #0f766e,
                        #14b8a6
                    );
            }


            .player-name {
                color:
                    #0f172a;

                font-size:
                    17px;

                font-weight:
                    900;
            }


            .player-name-en {
                color:
                    #94a3b8;

                font-size:
                    11px;

                font-weight:
                    600;
            }


            .player-id {
                color:
                    #94a3b8;

                font-size:
                    10px;

                font-weight:
                    700;
            }


            .chips-container {
                display:
                    flex;

                align-items:
                    center;

                flex-wrap:
                    wrap;

                gap:
                    6px;
            }


            .info-chip {
                display:
                    inline-flex;

                align-items:
                    center;

                gap:
                    5px;

                border-radius:
                    999px;

                padding:
                    6px 10px;

                font-size:
                    11px;

                font-weight:
                    800;

                white-space:
                    nowrap;
            }


            .action-button {
                width:
                    38px;

                height:
                    38px;

                border-radius:
                    12px;
            }


            /* =================================================
               Dialog
               ================================================= */

            .dialog-card {
                width:
                    980px;

                max-width:
                    96vw;

                max-height:
                    90vh;

                overflow-y:
                    auto;

                background:
                    white;

                border-radius:
                    26px;

                padding:
                    24px;
            }


            .dialog-header {
                padding-bottom:
                    18px;

                border-bottom:
                    1px solid #f1f5f9;

                margin-bottom:
                    20px;
            }


            .dialog-title {
                color:
                    #0f172a;

                font-size:
                    22px;

                font-weight:
                    900;
            }


            .section-title {
                color:
                    #0f172a;

                font-size:
                    14px;

                font-weight:
                    900;
            }


            .section-description {
                color:
                    #94a3b8;

                font-size:
                    11px;

                font-weight:
                    600;
            }


            .section-icon {
                width:
                    38px;

                height:
                    38px;

                border-radius:
                    12px;

                background:
                    #eff6ff;

                display:
                    flex;

                align-items:
                    center;

                justify-content:
                    center;
            }


            .field-label {
                color:
                    #475569;

                font-size:
                    12px;

                font-weight:
                    800;

                margin-bottom:
                    5px;
            }


            /* =================================================
               Empty
               ================================================= */

            .empty-state {
                width:
                    100%;

                padding:
                    65px 20px;

                display:
                    flex;

                align-items:
                    center;

                justify-content:
                    center;

                flex-direction:
                    column;
            }


            .empty-icon {
                width:
                    76px;

                height:
                    76px;

                border-radius:
                    24px;

                background:
                    #f8fafc;

                border:
                    1px solid #e2e8f0;

                display:
                    flex;

                align-items:
                    center;

                justify-content:
                    center;
            }


            /* =================================================
               Responsive
               ================================================= */

            @media (max-width: 1100px) {

                .stats-grid {
                    grid-template-columns:
                        repeat(2, minmax(0, 1fr));
                }

                .filter-grid {
                    grid-template-columns:
                        1fr 1fr;
                }
            }


            @media (max-width: 800px) {

                .players-hero {
                    padding:
                        22px;

                    border-radius:
                        22px;

                    min-height:
                        240px;
                }


                .hero-title {
                    font-size:
                        24px;
                }


                .hero-club-logo {
                    width:
                        64px;

                    height:
                        64px;

                    border-radius:
                        18px;
                }


                .hero-icon {
                    width:
                        60px;

                    height:
                        60px;

                    border-radius:
                        18px;
                }


                .player-row {
                    padding:
                        13px;
                }


                .player-main {
                    min-width:
                        0;

                    width:
                        100%;
                }
            }


            @media (max-width: 600px) {

                .stats-grid {
                    grid-template-columns:
                        1fr 1fr;

                    gap:
                        10px;
                }


                .stat-card {
                    padding:
                        15px;

                    border-radius:
                        18px;
                }


                .stat-number {
                    font-size:
                        23px;
                }


                .filter-grid {
                    grid-template-columns:
                        1fr;
                }


                .players-card {
                    padding:
                        14px;

                    border-radius:
                        20px;
                }


                .player-row {
                    border-radius:
                        17px;
                }


                .player-avatar {
                    width:
                        52px;

                    height:
                        52px;

                    min-width:
                        52px;

                    border-radius:
                        15px;
                }


                .dialog-card {
                    padding:
                        17px;

                    border-radius:
                        20px;
                }
            }

        </style>
        """
    )

    # =========================================================
    # Lookup data
    # =========================================================

    teams = db.fetch_all(
        """
        SELECT
            Id,
            TeamAR,
            TeamEN
        FROM Team
        WHERE Clubid = ?
        ORDER BY Id
        """,
        (club_id,)
    )

    nationalities = db.fetch_all(
        """
        SELECT
            Id,
            NationalityNameAR,
            NationalityNameEN
        FROM Nationality
        ORDER BY Id
        """
    )

    wearing_sizes = db.fetch_all(
        """
        SELECT
            Id,
            WearingSizeName
        FROM WearingSize
        ORDER BY Id
        """
    )

    education_levels = db.fetch_all(
        """
        SELECT
            Id,
            EducationLevelNameAR,
            EducationLevelNameEN
        FROM EducationLevel
        ORDER BY Id
        """
    )

    medical_states = db.fetch_all(
        """
        SELECT
            Id,
            MedicalReportStateNameAR,
            MedicalReportStateNameEN
        FROM MedicalReportState
        ORDER BY Id
        """
    )

    blood_types = db.fetch_all(
        """
        SELECT
            Id,
            BloodTypeNameAR,
            BloodTypeNameEN
        FROM BloodType
        ORDER BY Id
        """
    )

    membership_statuses = db.fetch_all(
        """
        SELECT
            Id,
            MembershipStatusNameAR,
            MembershipStatusNameEN
        FROM MembershipStatus
        ORDER BY Id
        """
    )

    membership_types = db.fetch_all(
        """
        SELECT
            Id,
            MembershipTypeNameAR,
            MembershipTypeNameEN
        FROM MembershipType
        ORDER BY Id
        """
    )

    religions = db.fetch_all(
        """
        SELECT
            Id,
            ReligionNameAR,
            ReligionNameEN
        FROM Religion
        ORDER BY Id
        """
    )

    # =========================================================
    # Options
    # =========================================================

    team_options = {
        row['Id']:
            option_label(
                row,
                'TeamAR',
                'TeamEN'
            )
        for row in teams
    }

    nationality_options = {
        row['Id']:
            option_label(
                row,
                'NationalityNameAR',
                'NationalityNameEN'
            )
        for row in nationalities
    }

    wearing_size_options = {
        row['Id']:
            safe_text(
                row['WearingSizeName'],
                str(row['Id'])
            )
        for row in wearing_sizes
    }

    education_options = {
        row['Id']:
            option_label(
                row,
                'EducationLevelNameAR',
                'EducationLevelNameEN'
            )
        for row in education_levels
    }

    medical_options = {
        row['Id']:
            option_label(
                row,
                'MedicalReportStateNameAR',
                'MedicalReportStateNameEN'
            )
        for row in medical_states
    }

    blood_options = {
        row['Id']:
            option_label(
                row,
                'BloodTypeNameAR',
                'BloodTypeNameEN'
            )
        for row in blood_types
    }

    membership_status_options = {
        row['Id']:
            option_label(
                row,
                'MembershipStatusNameAR',
                'MembershipStatusNameEN'
            )
        for row in membership_statuses
    }

    membership_type_options = {
        row['Id']:
            option_label(
                row,
                'MembershipTypeNameAR',
                'MembershipTypeNameEN'
            )
        for row in membership_types
    }

    religion_options = {
        row['Id']:
            option_label(
                row,
                'ReligionNameAR',
                'ReligionNameEN'
            )
        for row in religions
    }

    # =========================================================
    # Page
    # =========================================================

    with ui.column().classes(
        'players-page w-full p-4 md:p-6 lg:p-8 gap-5'
    ):

        # =====================================================
        # Hero
        # =====================================================

        with ui.element('div').classes(
            'players-hero'
        ).style(hero_background):

            with ui.column().classes(
                'hero-content w-full gap-5'
            ):

                with ui.row().classes(
                    'w-full items-center justify-between gap-5 flex-wrap'
                ):

                    with ui.row().classes(
                        'items-center gap-4'
                    ):

                        # -------------------------------------------------
                        # Club logo
                        # -------------------------------------------------

                        if club_logo_url:

                            with ui.element(
                                'div'
                            ).classes(
                                'hero-club-logo'
                            ):

                                ui.image(
                                    club_logo_url
                                ).classes(
                                    'w-full h-full object-contain'
                                )

                        else:

                            with ui.element(
                                'div'
                            ).classes(
                                'hero-icon'
                            ):

                                ui.icon(
                                    'sports_soccer'
                                ).classes(
                                    'text-3xl text-red-600'
                                )

                        # -------------------------------------------------
                        # Title
                        # -------------------------------------------------

                        with ui.column().classes(
                            'gap-2'
                        ):

                            with ui.row().classes(
                                'items-center gap-2'
                            ):

                                ui.label(
                                    'إدارة اللاعبين'
                                ).classes(
                                    'hero-title'
                                )

                            ui.label(
                                'إدارة ومتابعة بيانات لاعبي النادي'
                            ).classes(
                                'hero-subtitle'
                            )

                            with ui.row().classes(
                                'items-center gap-2'
                            ):

                                with ui.element(
                                    'div'
                                ).classes(
                                    'hero-football-label'
                                ):

                                    ui.icon(
                                        'sports_soccer'
                                    ).classes(
                                        'text-sm'
                                    )

                                    ui.label(
                                        'Football Club Management'
                                    )

                    # -----------------------------------------------------
                    # Club badge
                    # -----------------------------------------------------

                    with ui.row().classes(
                        'items-center gap-2'
                    ):

                        ui.label(
                            club_name
                        ).classes(
                            'club-badge'
                        )

                        ui.icon(
                            'verified'
                        ).classes(
                            'text-amber-400'
                        )

                # ---------------------------------------------------------
                # Hero bottom information
                # ---------------------------------------------------------

                with ui.row().classes(
                    'items-center gap-3 flex-wrap'
                ):

                    with ui.element(
                        'div'
                    ).classes(
                        'bg-white/10 border border-white/10 rounded-2xl px-4 py-3'
                    ):

                        with ui.row().classes(
                            'items-center gap-2'
                        ):

                            ui.icon(
                                'groups'
                            ).classes(
                                'text-red-300'
                            )

                            ui.label(
                                'الفريق الأول والقطاعات الرياضية'
                            ).classes(
                                'text-white text-xs font-bold'
                            )

                    with ui.element(
                        'div'
                    ).classes(
                        'bg-white/10 border border-white/10 rounded-2xl px-4 py-3'
                    ):

                        with ui.row().classes(
                            'items-center gap-2'
                        ):

                            ui.icon(
                                'verified_user'
                            ).classes(
                                'text-amber-300'
                            )

                            ui.label(
                                'بيانات اللاعبين والعضويات'
                            ).classes(
                                'text-white text-xs font-bold'
                            )

        # =====================================================
        # Statistics
        # =====================================================

        stats_container = ui.element(
            'div'
        ).classes(
            'stats-grid'
        )

        # =====================================================
        # Add dialog
        # =====================================================

        add_dialog = ui.dialog()

        with add_dialog:

            with ui.card().classes(
                'dialog-card'
            ):

                with ui.row().classes(
                    'dialog-header w-full items-center justify-between'
                ):

                    with ui.row().classes(
                        'items-center gap-3'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'section-icon'
                        ):

                            ui.icon(
                                'person_add'
                            ).classes(
                                'text-blue-600 text-xl'
                            )

                        with ui.column().classes(
                            'gap-0'
                        ):

                            ui.label(
                                'تسجيل لاعب جديد'
                            ).classes(
                                'dialog-title'
                            )

                            ui.label(
                                'أدخل البيانات الأساسية للاعب'
                            ).classes(
                                'section-description'
                            )

                    ui.button(
                        icon='close',
                        on_click=add_dialog.close
                    ).props(
                        'flat round'
                    )

                # =====================================================
                # Basic information
                # =====================================================

                with ui.column().classes(
                    'w-full gap-4'
                ):

                    with ui.row().classes(
                        'items-center gap-3'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'section-icon'
                        ):

                            ui.icon(
                                'person'
                            ).classes(
                                'text-blue-600'
                            )

                        with ui.column().classes(
                            'gap-0'
                        ):

                            ui.label(
                                'البيانات الأساسية'
                            ).classes(
                                'section-title'
                            )

                            ui.label(
                                'بيانات تعريف اللاعب'
                            ).classes(
                                'section-description'
                            )

                    with ui.row().classes(
                        'w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'
                    ):

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'اسم اللاعب بالعربي'
                            ).classes(
                                'field-label'
                            )

                            name_ar = ui.input(
                                placeholder='مثال: أحمد محمد'
                            ).props(
                                'outlined rounded'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'اسم اللاعب بالإنجليزي'
                            ).classes(
                                'field-label'
                            )

                            name_en = ui.input(
                                placeholder='Example: Ahmed Mohamed'
                            ).props(
                                'outlined rounded'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'الجنسية'
                            ).classes(
                                'field-label'
                            )

                            nationality = ui.select(
                                nationality_options,
                                label='اختر الجنسية'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                    # =================================================
                    # Membership
                    # =================================================

                    with ui.row().classes(
                        'items-center gap-3 mt-3'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'section-icon'
                        ):

                            ui.icon(
                                'sports'
                            ).classes(
                                'text-blue-600'
                            )

                        with ui.column().classes(
                            'gap-0'
                        ):

                            ui.label(
                                'بيانات العضوية'
                            ).classes(
                                'section-title'
                            )

                            ui.label(
                                'العضوية والتصنيف'
                            ).classes(
                                'section-description'
                            )

                    with ui.row().classes(
                        'w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'
                    ):

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'حالة العضوية'
                            ).classes(
                                'field-label'
                            )

                            membership_status = ui.select(
                                membership_status_options,
                                label='اختر حالة العضوية'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'نوع العضوية'
                            ).classes(
                                'field-label'
                            )

                            membership_type = ui.select(
                                membership_type_options,
                                label='اختر نوع العضوية'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'الفريق'
                            ).classes(
                                'field-label'
                            )

                            add_team = ui.select(
                                team_options,
                                label='اختر الفريق'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                    # =================================================
                    # Personal details
                    # =================================================

                    with ui.row().classes(
                        'items-center gap-3 mt-3'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'section-icon'
                        ):

                            ui.icon(
                                'badge'
                            ).classes(
                                'text-blue-600'
                            )

                        with ui.column().classes(
                            'gap-0'
                        ):

                            ui.label(
                                'البيانات الشخصية'
                            ).classes(
                                'section-title'
                            )

                            ui.label(
                                'الملابس والتعليم والديانة'
                            ).classes(
                                'section-description'
                            )

                    with ui.row().classes(
                        'w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'
                    ):

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'مقاس الملابس'
                            ).classes(
                                'field-label'
                            )

                            wearing_size = ui.select(
                                wearing_size_options,
                                label='اختر المقاس'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'المؤهل الدراسي'
                            ).classes(
                                'field-label'
                            )

                            education = ui.select(
                                education_options,
                                label='اختر المؤهل'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'الديانة'
                            ).classes(
                                'field-label'
                            )

                            religion = ui.select(
                                religion_options,
                                label='اختر الديانة'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                    # =================================================
                    # Medical information
                    # =================================================

                    with ui.row().classes(
                        'items-center gap-3 mt-3'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'section-icon'
                        ):

                            ui.icon(
                                'medical_services'
                            ).classes(
                                'text-blue-600'
                            )

                        with ui.column().classes(
                            'gap-0'
                        ):

                            ui.label(
                                'البيانات الطبية'
                            ).classes(
                                'section-title'
                            )

                            ui.label(
                                'الحالة الطبية وفصيلة الدم'
                            ).classes(
                                'section-description'
                            )

                    with ui.row().classes(
                        'w-full grid grid-cols-1 md:grid-cols-2 gap-4'
                    ):

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'الحالة الطبية'
                            ).classes(
                                'field-label'
                            )

                            medical_state = ui.select(
                                medical_options,
                                label='اختر الحالة الطبية'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'فصيلة الدم'
                            ).classes(
                                'field-label'
                            )

                            blood_type = ui.select(
                                blood_options,
                                label='اختر فصيلة الدم'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                # =====================================================
                # Add actions
                # =====================================================

                with ui.row().classes(
                    'w-full justify-end items-center gap-2 mt-7 pt-5 border-t border-slate-100'
                ):

                    ui.button(
                        'إلغاء',
                        on_click=add_dialog.close
                    ).props(
                        'flat no-caps'
                    )

                    save_button = ui.button(
                        'تسجيل اللاعب',
                        icon='person_add'
                    ).props(
                        'unelevated no-caps'
                    ).classes(
                        'bg-blue-700 text-white rounded-xl px-7 py-3 font-bold'
                    )

        # =====================================================
        # Add player action
        # =====================================================

        with ui.row().classes(
            'w-full justify-end'
        ):

            ui.button(
                'تسجيل لاعب جديد',
                icon='person_add',
                on_click=add_dialog.open
            ).props(
                'unelevated no-caps'
            ).classes(
                'bg-blue-700 text-white rounded-xl px-7 py-3 font-bold'
            )

        # =====================================================
        # Filters
        # =====================================================

        with ui.card().classes(
            'filter-card'
        ):

            with ui.row().classes(
                'w-full items-center justify-between gap-4 mb-5 flex-wrap'
            ):

                with ui.row().classes(
                    'items-center gap-3'
                ):

                    with ui.element(
                        'div'
                    ).classes(
                        'w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center'
                    ):

                        ui.icon(
                            'tune'
                        ).classes(
                            'text-slate-600'
                        )

                    with ui.column().classes(
                        'gap-0'
                    ):

                        ui.label(
                            'البحث والتصفية'
                        ).classes(
                            'filter-title'
                        )

                        ui.label(
                            'اعثر على اللاعب المطلوب بسرعة'
                        ).classes(
                            'section-description'
                        )

                clear_filters_button = ui.button(
                    'مسح الفلاتر',
                    icon='filter_alt_off'
                ).props(
                    'flat no-caps'
                )

            with ui.element(
                'div'
            ).classes(
                'filter-grid'
            ):

                with ui.column().classes(
                    'w-full'
                ):

                    ui.label(
                        'البحث'
                    ).classes(
                        'filter-label'
                    )

                    search = ui.input(
                        placeholder='ابحث باسم اللاعب...'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

                with ui.column().classes(
                    'w-full'
                ):

                    ui.label(
                        'الفريق'
                    ).classes(
                        'filter-label'
                    )

                    team_filter = ui.select(
                        team_options,
                        label='كل الفرق'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

                with ui.column().classes(
                    'w-full'
                ):

                    ui.label(
                        'الحالة الطبية'
                    ).classes(
                        'filter-label'
                    )

                    medical_filter = ui.select(
                        medical_options,
                        label='كل الحالات'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

                with ui.column().classes(
                    'w-full'
                ):

                    ui.label(
                        'العضوية'
                    ).classes(
                        'filter-label'
                    )

                    membership_filter = ui.select(
                        membership_status_options,
                        label='كل الحالات'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

                with ui.column().classes(
                    'w-full'
                ):

                    ui.label(
                        'الترتيب'
                    ).classes(
                        'filter-label'
                    )

                    sort_select = ui.select(
                        {
                            'newest': 'الأحدث أولًا',
                            'oldest': 'الأقدم أولًا',
                            'name_ar': 'الاسم بالعربي',
                            'name_en': 'الاسم بالإنجليزي',
                        },
                        value='newest',
                        label='ترتيب اللاعبين'
                    ).props(
                        'outlined rounded'
                    ).classes(
                        'w-full'
                    )

        # =====================================================
        # Players container
        # =====================================================

        players_container = ui.column().classes(
            'w-full'
        )

        # =====================================================
        # Edit dialog
        # =====================================================

        edit_dialog = ui.dialog()

        with edit_dialog:

            with ui.card().classes(
                'dialog-card'
            ):

                with ui.row().classes(
                    'dialog-header w-full items-center justify-between'
                ):

                    with ui.row().classes(
                        'items-center gap-3'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'section-icon'
                        ):

                            ui.icon(
                                'edit'
                            ).classes(
                                'text-blue-600 text-xl'
                            )

                        with ui.column().classes(
                            'gap-0'
                        ):

                            ui.label(
                                'تعديل بيانات اللاعب'
                            ).classes(
                                'dialog-title'
                            )

                            ui.label(
                                'قم بتعديل بيانات اللاعب ثم احفظ التغييرات'
                            ).classes(
                                'section-description'
                            )

                    ui.button(
                        icon='close',
                        on_click=edit_dialog.close
                    ).props(
                        'flat round'
                    )

                edit_id = ui.number(
                    'Id'
                ).props(
                    'outlined rounded readonly'
                ).classes(
                    'hidden'
                )

                with ui.column().classes(
                    'w-full gap-4'
                ):

                    with ui.row().classes(
                        'items-center gap-3'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'section-icon'
                        ):

                            ui.icon(
                                'person'
                            ).classes(
                                'text-blue-600'
                            )

                        ui.label(
                            'البيانات الأساسية'
                        ).classes(
                            'section-title'
                        )

                    with ui.row().classes(
                        'w-full grid grid-cols-1 md:grid-cols-2 gap-4'
                    ):

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'اسم اللاعب بالعربي'
                            ).classes(
                                'field-label'
                            )

                            edit_name_ar = ui.input().props(
                                'outlined rounded'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'اسم اللاعب بالإنجليزي'
                            ).classes(
                                'field-label'
                            )

                            edit_name_en = ui.input().props(
                                'outlined rounded'
                            ).classes(
                                'w-full'
                            )

                    with ui.row().classes(
                        'w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'
                    ):

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'الجنسية'
                            ).classes(
                                'field-label'
                            )

                            edit_nationality = ui.select(
                                nationality_options,
                                label='الجنسية'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'الفريق'
                            ).classes(
                                'field-label'
                            )

                            edit_team = ui.select(
                                team_options,
                                label='الفريق'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'مقاس الملابس'
                            ).classes(
                                'field-label'
                            )

                            edit_wearing_size = ui.select(
                                wearing_size_options,
                                label='مقاس الملابس'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                    with ui.row().classes(
                        'w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'
                    ):

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'المؤهل الدراسي'
                            ).classes(
                                'field-label'
                            )

                            edit_education = ui.select(
                                education_options,
                                label='المؤهل الدراسي'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'الديانة'
                            ).classes(
                                'field-label'
                            )

                            edit_religion = ui.select(
                                religion_options,
                                label='الديانة'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'نوع العضوية'
                            ).classes(
                                'field-label'
                            )

                            edit_membership_type = ui.select(
                                membership_type_options,
                                label='نوع العضوية'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                    with ui.row().classes(
                        'w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'
                    ):

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'الحالة الطبية'
                            ).classes(
                                'field-label'
                            )

                            edit_medical_state = ui.select(
                                medical_options,
                                label='الحالة الطبية'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'فصيلة الدم'
                            ).classes(
                                'field-label'
                            )

                            edit_blood_type = ui.select(
                                blood_options,
                                label='فصيلة الدم'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                        with ui.column().classes(
                            'w-full'
                        ):

                            ui.label(
                                'حالة العضوية'
                            ).classes(
                                'field-label'
                            )

                            edit_membership_status = ui.select(
                                membership_status_options,
                                label='حالة العضوية'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'w-full'
                            )

                with ui.row().classes(
                    'w-full justify-end gap-2 mt-7 pt-5 border-t border-slate-100'
                ):

                    ui.button(
                        'إلغاء',
                        on_click=edit_dialog.close
                    ).props(
                        'flat no-caps'
                    )

                    update_button = ui.button(
                        'حفظ التعديل',
                        icon='save'
                    ).props(
                        'unelevated no-caps'
                    ).classes(
                        'bg-blue-700 text-white rounded-xl px-7 py-3 font-bold'
                    )

        # =====================================================
        # Delete dialog
        # =====================================================

        delete_dialog = ui.dialog()

        with delete_dialog:

            with ui.card().classes(
                'w-[430px] max-w-[94vw] p-7 rounded-3xl'
            ):

                with ui.column().classes(
                    'w-full items-center'
                ):

                    with ui.element(
                        'div'
                    ).classes(
                        'w-16 h-16 rounded-2xl bg-red-50 flex items-center justify-center'
                    ):

                        ui.icon(
                            'delete_forever'
                        ).classes(
                            'text-3xl text-red-600'
                        )

                    ui.label(
                        'حذف اللاعب'
                    ).classes(
                        'text-2xl font-black text-slate-900 mt-4'
                    )

                    delete_player_name = ui.label(
                        ''
                    ).classes(
                        'text-lg font-black text-red-600 mt-3 text-center'
                    )

                    ui.label(
                        'هل أنت متأكد أنك تريد حذف هذا اللاعب؟'
                    ).classes(
                        'text-sm text-slate-500 text-center mt-2'
                    )

                    ui.label(
                        'لا يمكن التراجع عن هذا الإجراء.'
                    ).classes(
                        'text-xs text-slate-400 text-center mt-1'
                    )

                    delete_player_id = ui.number(
                        'Id'
                    ).props(
                        'readonly'
                    ).classes(
                        'hidden'
                    )

                    with ui.row().classes(
                        'w-full justify-center gap-3 mt-7'
                    ):

                        ui.button(
                            'إلغاء',
                            on_click=delete_dialog.close
                        ).props(
                            'flat no-caps'
                        )

                        delete_button = ui.button(
                            'حذف اللاعب',
                            icon='delete'
                        ).props(
                            'unelevated no-caps'
                        ).classes(
                            'bg-red-600 text-white rounded-xl px-6 py-3 font-bold'
                        )

        # =====================================================
        # Statistics refresh
        # =====================================================

        def refresh_statistics(players):

            stats_container.clear()

            total_players = len(players)

            medical_passed = 0
            medical_failed = 0
            active_members = 0

            for player in players:

                medical_status = safe_text(
                    player.get(
                        'MedicalReportStateNameAR'
                    ),
                    ''
                ).lower()

                membership_status = safe_text(
                    player.get(
                        'MembershipStatusNameAR'
                    ),
                    ''
                ).lower()

                if get_status_color(
                    medical_status
                ) == 'positive':

                    medical_passed += 1

                if get_status_color(
                    medical_status
                ) == 'negative':

                    medical_failed += 1

                if get_status_color(
                    membership_status
                ) == 'positive':

                    active_members += 1

            with stats_container:

                # -------------------------------------------------
                # Total
                # -------------------------------------------------

                with ui.element(
                    'div'
                ).classes(
                    'stat-card'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'stat-icon bg-blue-50'
                        ):

                            ui.icon(
                                'groups'
                            ).classes(
                                'text-blue-600 text-xl'
                            )

                        ui.label(
                            str(total_players)
                        ).classes(
                            'stat-number'
                        )

                    ui.label(
                        'إجمالي اللاعبين'
                    ).classes(
                        'stat-label mt-3'
                    )

                # -------------------------------------------------
                # Medical passed
                # -------------------------------------------------

                with ui.element(
                    'div'
                ).classes(
                    'stat-card'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'stat-icon bg-emerald-50'
                        ):

                            ui.icon(
                                'health_and_safety'
                            ).classes(
                                'text-emerald-600 text-xl'
                            )

                        ui.label(
                            str(medical_passed)
                        ).classes(
                            'stat-number'
                        )

                    ui.label(
                        'الحالات الطبية السليمة'
                    ).classes(
                        'stat-label mt-3'
                    )

                # -------------------------------------------------
                # Medical failed
                # -------------------------------------------------

                with ui.element(
                    'div'
                ).classes(
                    'stat-card'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'stat-icon bg-red-50'
                        ):

                            ui.icon(
                                'medical_information'
                            ).classes(
                                'text-red-600 text-xl'
                            )

                        ui.label(
                            str(medical_failed)
                        ).classes(
                            'stat-number'
                        )

                    ui.label(
                        'الحالات الطبية غير السليمة'
                    ).classes(
                        'stat-label mt-3'
                    )

                # -------------------------------------------------
                # Membership
                # -------------------------------------------------

                with ui.element(
                    'div'
                ).classes(
                    'stat-card'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'stat-icon bg-amber-50'
                        ):

                            ui.icon(
                                'verified_user'
                            ).classes(
                                'text-amber-600 text-xl'
                            )

                        ui.label(
                            str(active_members)
                        ).classes(
                            'stat-number'
                        )

                    ui.label(
                        'الأعضاء النشطون'
                    ).classes(
                        'stat-label mt-3'
                    )

        # =====================================================
        # Query players
        # =====================================================

        def fetch_players():

            search_value = (
                search.value or ''
            ).strip()

            team_value = team_filter.value
            medical_value = medical_filter.value
            membership_value = membership_filter.value

            query = """
                SELECT
                    p.Id,
                    p.PlayerNameAR,
                    p.PlayerNameEN,
                    p.ClubId,
                    p.NationalityId,
                    p.WearingSizeId,
                    p.EducationLevelId,
                    p.MedicalReportStatueId,
                    p.BloodTypeId,
                    p.MembershipStatueId,
                    p.MembershipTypeId,
                    p.ReligionId,

                    n.NationalityNameAR,
                    n.NationalityNameEN,

                    ws.WearingSizeName,

                    e.EducationLevelNameAR,
                    e.EducationLevelNameEN,

                    mrs.MedicalReportStateNameAR,
                    mrs.MedicalReportStateNameEN,

                    bt.BloodTypeNameAR,
                    bt.BloodTypeNameEN,

                    ms.MembershipStatusNameAR,
                    ms.MembershipStatusNameEN,

                    mt.MembershipTypeNameAR,
                    mt.MembershipTypeNameEN,

                    r.ReligionNameAR,
                    r.ReligionNameEN,

                    pts.TeamId,

                    t.TeamAR,
                    t.TeamEN

                FROM Player p

                LEFT JOIN Nationality n
                    ON n.Id = p.NationalityId

                LEFT JOIN WearingSize ws
                    ON ws.Id = p.WearingSizeId

                LEFT JOIN EducationLevel e
                    ON e.Id = p.EducationLevelId

                LEFT JOIN MedicalReportState mrs
                    ON mrs.Id = p.MedicalReportStatueId

                LEFT JOIN BloodType bt
                    ON bt.Id = p.BloodTypeId

                LEFT JOIN MembershipStatus ms
                    ON ms.Id = p.MembershipStatueId

                LEFT JOIN MembershipType mt
                    ON mt.Id = p.MembershipTypeId

                LEFT JOIN Religion r
                    ON r.Id = p.ReligionId

                LEFT JOIN PlayerTeamSubscribtion pts
                    ON pts.PlayerId = p.Id

                LEFT JOIN Team t
                    ON t.Id = pts.TeamId

                WHERE p.ClubId = ?
            """

            params = [
                club_id
            ]

            if search_value:

                query += """
                    AND (
                        p.PlayerNameAR LIKE ?
                        OR p.PlayerNameEN LIKE ?
                    )
                """

                search_pattern = (
                    f'%{search_value}%'
                )

                params.extend([
                    search_pattern,
                    search_pattern
                ])

            if team_value:

                query += """
                    AND pts.TeamId = ?
                """

                params.append(
                    team_value
                )

            if medical_value:

                query += """
                    AND p.MedicalReportStatueId = ?
                """

                params.append(
                    medical_value
                )

            if membership_value:

                query += """
                    AND p.MembershipStatueId = ?
                """

                params.append(
                    membership_value
                )

            sort_value = (
                sort_select.value
                or 'newest'
            )

            if sort_value == 'oldest':

                query += """
                    ORDER BY p.Id ASC
                """

            elif sort_value == 'name_ar':

                query += """
                    ORDER BY
                        p.PlayerNameAR
                        COLLATE NOCASE ASC
                """

            elif sort_value == 'name_en':

                query += """
                    ORDER BY
                        p.PlayerNameEN
                        COLLATE NOCASE ASC
                """

            else:

                query += """
                    ORDER BY p.Id DESC
                """

            try:

                return db.fetch_all(
                    query,
                    tuple(params)
                )

            except Exception as e:

                print(
                    f'[FETCH PLAYERS ERROR] '
                    f'{type(e).__name__}: {e}'
                )

                ui.notify(
                    'تعذر تحميل اللاعبين',
                    color='negative'
                )

                return []

        # =====================================================
        # Open edit
        # =====================================================

        def open_edit(player_data):

            edit_id.value = player_data['Id']

            edit_name_ar.value = (
                player_data['PlayerNameAR']
                or ''
            )

            edit_name_en.value = (
                player_data['PlayerNameEN']
                or ''
            )

            edit_nationality.value = (
                player_data.get(
                    'NationalityId'
                )
            )

            edit_team.value = (
                player_data.get(
                    'TeamId'
                )
            )

            edit_wearing_size.value = (
                player_data.get(
                    'WearingSizeId'
                )
            )

            edit_education.value = (
                player_data.get(
                    'EducationLevelId'
                )
            )

            edit_medical_state.value = (
                player_data.get(
                    'MedicalReportStatueId'
                )
            )

            edit_blood_type.value = (
                player_data.get(
                    'BloodTypeId'
                )
            )

            edit_membership_status.value = (
                player_data.get(
                    'MembershipStatueId'
                )
            )

            edit_membership_type.value = (
                player_data.get(
                    'MembershipTypeId'
                )
            )

            edit_religion.value = (
                player_data.get(
                    'ReligionId'
                )
            )

            edit_dialog.open()

        # =====================================================
        # Open delete
        # =====================================================

        def open_delete(player_data):

            delete_player_id.value = (
                player_data['Id']
            )

            delete_player_name.text = (
                player_data['PlayerNameAR']
                or 'هذا اللاعب'
            )

            delete_dialog.open()

        # =====================================================
        # Render player
        # =====================================================

        def render_player(player):

            player_id = player['Id']

            player_name_ar = safe_text(
                player['PlayerNameAR'],
                'بدون اسم'
            )

            player_name_en = (
                player['PlayerNameEN']
                or ''
            )

            nationality_name = option_label(
                player,
                'NationalityNameAR',
                'NationalityNameEN'
            )

            if not nationality_name:
                nationality_name = 'غير محدد'

            medical_name = option_label(
                player,
                'MedicalReportStateNameAR',
                'MedicalReportStateNameEN'
            )

            if not medical_name:
                medical_name = 'غير محدد'

            membership_name = option_label(
                player,
                'MembershipStatusNameAR',
                'MembershipStatusNameEN'
            )

            if not membership_name:
                membership_name = 'غير محدد'

            membership_type_name = option_label(
                player,
                'MembershipTypeNameAR',
                'MembershipTypeNameEN'
            )

            if not membership_type_name:
                membership_type_name = 'غير محدد'

            team_name = option_label(
                player,
                'TeamAR',
                'TeamEN'
            )

            if not team_name:
                team_name = 'بدون فريق'

            blood_name = option_label(
                player,
                'BloodTypeNameAR',
                'BloodTypeNameEN'
            )

            if not blood_name:
                blood_name = 'غير محدد'

            player_photo_url = get_player_photo(
                player
            )

            with ui.element(
                'div'
            ).classes(
                'player-row'
            ):

                with ui.row().classes(
                    'w-full items-center justify-between gap-4 flex-wrap'
                ):

                    # =================================================
                    # Main information
                    # =================================================

                    with ui.row().classes(
                        'player-main items-center gap-3'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'player-avatar '
                            + get_avatar_classes(
                                player_id
                            )
                        ):

                            if player_photo_url:

                                ui.image(
                                    player_photo_url
                                ).classes(
                                    'player-avatar-image'
                                )

                            else:

                                with ui.element(
                                    'div'
                                ).classes(
                                    'player-avatar-fallback'
                                ):

                                    ui.label(
                                        get_initials(
                                            player_name_ar
                                        )
                                    )

                        with ui.column().classes(
                            'gap-0'
                        ):

                            ui.label(
                                player_name_ar
                            ).classes(
                                'player-name'
                            )

                            if player_name_en:

                                ui.label(
                                    player_name_en
                                ).classes(
                                    'player-name-en mt-1'
                                )

                            ui.label(
                                f'ID: {player_id}'
                            ).classes(
                                'player-id mt-1'
                            )

                    # =================================================
                    # Information chips
                    # =================================================

                    with ui.row().classes(
                        'chips-container flex-1'
                    ):

                        ui.label(
                            team_name
                        ).classes(
                            'info-chip bg-indigo-50 '
                            'text-indigo-700 '
                            'border border-indigo-100'
                        )

                        ui.label(
                            nationality_name
                        ).classes(
                            'info-chip bg-slate-50 '
                            'text-slate-600 '
                            'border border-slate-200'
                        )

                        ui.label(
                            medical_name
                        ).classes(
                            'info-chip '
                            + status_classes(
                                medical_name
                            )
                        )

                        ui.label(
                            membership_name
                        ).classes(
                            'info-chip '
                            + status_classes(
                                membership_name
                            )
                        )

                        if membership_type_name != 'غير محدد':

                            ui.label(
                                membership_type_name
                            ).classes(
                                'info-chip bg-amber-50 '
                                'text-amber-700 '
                                'border border-amber-100'
                            )

                        if blood_name != 'غير محدد':

                            ui.label(
                                blood_name
                            ).classes(
                                'info-chip bg-red-50 '
                                'text-red-700 '
                                'border border-red-100'
                            )

                    # =================================================
                    # Actions
                    # =================================================

                    with ui.row().classes(
                        'items-center gap-1'
                    ):

                        ui.button(
                            icon='edit',
                            on_click=lambda p=player:
                                open_edit(p)
                        ).props(
                            'flat round'
                        ).classes(
                            'action-button text-blue-600'
                        ).tooltip(
                            'تعديل بيانات اللاعب'
                        )

                        ui.button(
                            icon='delete',
                            on_click=lambda p=player:
                                open_delete(p)
                        ).props(
                            'flat round'
                        ).classes(
                            'action-button text-red-600'
                        ).tooltip(
                            'حذف اللاعب'
                        )

        # =====================================================
        # Refresh players
        # =====================================================

        def refresh_players():

            players_container.clear()

            players = fetch_players()

            refresh_statistics(
                players
            )

            with players_container:

                with ui.card().classes(
                    'players-card'
                ):

                    # =================================================
                    # Header
                    # =================================================

                    with ui.row().classes(
                        'players-card-header '
                        'w-full items-center '
                        'justify-between '
                        'gap-4 flex-wrap'
                    ):

                        with ui.row().classes(
                            'items-center gap-3'
                        ):

                            with ui.element(
                                'div'
                            ).classes(
                                'w-11 h-11 rounded-xl '
                                'bg-red-50 '
                                'flex items-center '
                                'justify-center'
                            ):

                                ui.icon(
                                    'sports_soccer'
                                ).classes(
                                    'text-xl text-red-600'
                                )

                            with ui.column().classes(
                                'gap-0'
                            ):

                                ui.label(
                                    'قائمة اللاعبين'
                                ).classes(
                                    'text-xl font-black text-slate-900'
                                )

                                ui.label(
                                    'اللاعبون التابعون للنادي'
                                ).classes(
                                    'text-xs text-slate-400 font-semibold'
                                )

                        with ui.row().classes(
                            'items-center gap-2'
                        ):

                            ui.label(
                                f'{len(players)} لاعب'
                            ).classes(
                                'bg-red-50 text-red-700 '
                                'px-4 py-2 rounded-full '
                                'text-xs font-black'
                            )

                            refresh_button = ui.button(
                                icon='refresh'
                            ).props(
                                'flat round'
                            ).classes(
                                'text-slate-500'
                            ).tooltip(
                                'تحديث القائمة'
                            )

                            refresh_button.on(
                                'click',
                                refresh_players
                            )

                    # =================================================
                    # List
                    # =================================================

                    if not players:

                        with ui.column().classes(
                            'empty-state'
                        ):

                            with ui.element(
                                'div'
                            ).classes(
                                'empty-icon'
                            ):

                                ui.icon(
                                    'person_search'
                                ).classes(
                                    'text-4xl text-slate-300'
                                )

                            if (
                                search.value
                                or team_filter.value
                                or medical_filter.value
                                or membership_filter.value
                            ):

                                ui.label(
                                    'لا توجد نتائج مطابقة'
                                ).classes(
                                    'text-xl font-black text-slate-600 mt-5'
                                )

                                ui.label(
                                    'جرّب تغيير معايير البحث أو مسح الفلاتر'
                                ).classes(
                                    'text-sm text-slate-400 text-center mt-2'
                                )

                            else:

                                ui.label(
                                    'لا يوجد لاعبون مسجلون'
                                ).classes(
                                    'text-xl font-black text-slate-600 mt-5'
                                )

                                ui.label(
                                    'ابدأ بتسجيل أول لاعب في النادي'
                                ).classes(
                                    'text-sm text-slate-400 text-center mt-2'
                                )

                    else:

                        with ui.column().classes(
                            'w-full gap-3 mt-5'
                        ):

                            for player in players:

                                render_player(
                                    player
                                )

        # =====================================================
        # Save player
        # =====================================================

        def save_player():

            player_name_ar = (
                name_ar.value or ''
            ).strip()

            player_name_en = (
                name_en.value or ''
            ).strip()

            if not player_name_ar:

                ui.notify(
                    'من فضلك أدخل اسم اللاعب بالعربي',
                    color='warning'
                )

                return

            try:

                db.execute_query(
                    """
                    INSERT INTO Player
                    (
                        PlayerNameAR,
                        PlayerNameEN,
                        ClubId,
                        NationalityId,
                        WearingSizeId,
                        EducationLevelId,
                        MedicalReportStatueId,
                        BloodTypeId,
                        MembershipStatueId,
                        MembershipTypeId,
                        ReligionId
                    )
                    VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        player_name_ar,
                        player_name_en,
                        club_id,
                        nationality.value,
                        wearing_size.value,
                        education.value,
                        medical_state.value,
                        blood_type.value,
                        membership_status.value,
                        membership_type.value,
                        religion.value
                    )
                )

                # =================================================
                # Get inserted player
                # =================================================

                inserted_player = db.fetch_one(
                    """
                    SELECT
                        Id
                    FROM Player
                    WHERE ClubId = ?
                    ORDER BY Id DESC
                    LIMIT 1
                    """,
                    (club_id,)
                )

                # =================================================
                # Team subscription
                # =================================================

                if (
                    add_team.value
                    and inserted_player
                ):

                    try:

                        db.execute_query(
                            """
                            INSERT INTO
                                PlayerTeamSubscribtion
                            (
                                PlayerId,
                                TeamId
                            )
                            VALUES (?, ?)
                            """,
                            (
                                inserted_player['Id'],
                                add_team.value
                            )
                        )

                    except Exception as team_error:

                        print(
                            '[PLAYER TEAM LINK ERROR] '
                            f'{type(team_error).__name__}: '
                            f'{team_error}'
                        )

                ui.notify(
                    'تم تسجيل اللاعب بنجاح',
                    color='positive'
                )

                # =================================================
                # Reset
                # =================================================

                name_ar.value = ''
                name_en.value = ''

                nationality.value = None
                wearing_size.value = None
                education.value = None
                medical_state.value = None
                blood_type.value = None
                membership_status.value = None
                membership_type.value = None
                religion.value = None
                add_team.value = None

                add_dialog.close()

                refresh_players()

            except Exception as e:

                ui.notify(
                    'حدث خطأ أثناء تسجيل اللاعب',
                    color='negative'
                )

                print(
                    '[SAVE PLAYER ERROR] '
                    f'{type(e).__name__}: {e}'
                )

        # =====================================================
        # Update player
        # =====================================================

        def update_player():

            player_id = safe_id(
                edit_id.value
            )

            if not player_id:

                ui.notify(
                    'بيانات اللاعب غير صحيحة',
                    color='warning'
                )

                return

            player_name_ar = (
                edit_name_ar.value or ''
            ).strip()

            player_name_en = (
                edit_name_en.value or ''
            ).strip()

            if not player_name_ar:

                ui.notify(
                    'من فضلك أدخل اسم اللاعب بالعربي',
                    color='warning'
                )

                return

            try:

                db.execute_query(
                    """
                    UPDATE Player
                    SET
                        PlayerNameAR = ?,
                        PlayerNameEN = ?,
                        NationalityId = ?,
                        WearingSizeId = ?,
                        EducationLevelId = ?,
                        MedicalReportStatueId = ?,
                        BloodTypeId = ?,
                        MembershipStatueId = ?,
                        MembershipTypeId = ?,
                        ReligionId = ?
                    WHERE
                        Id = ?
                        AND ClubId = ?
                    """,
                    (
                        player_name_ar,
                        player_name_en,
                        edit_nationality.value,
                        edit_wearing_size.value,
                        edit_education.value,
                        edit_medical_state.value,
                        edit_blood_type.value,
                        edit_membership_status.value,
                        edit_membership_type.value,
                        edit_religion.value,
                        player_id,
                        club_id
                    )
                )

                # =================================================
                # Team relation
                # =================================================

                if edit_team.value:

                    try:

                        existing_relation = db.fetch_one(
                            """
                            SELECT
                                Id
                            FROM PlayerTeamSubscribtion
                            WHERE PlayerId = ?
                            LIMIT 1
                            """,
                            (player_id,)
                        )

                        if existing_relation:

                            db.execute_query(
                                """
                                UPDATE
                                    PlayerTeamSubscribtion
                                SET
                                    TeamId = ?
                                WHERE
                                    PlayerId = ?
                                """,
                                (
                                    edit_team.value,
                                    player_id
                                )
                            )

                        else:

                            db.execute_query(
                                """
                                INSERT INTO
                                    PlayerTeamSubscribtion
                                (
                                    PlayerId,
                                    TeamId
                                )
                                VALUES (?, ?)
                                """,
                                (
                                    player_id,
                                    edit_team.value
                                )
                            )

                    except Exception as team_error:

                        print(
                            '[UPDATE TEAM LINK ERROR] '
                            f'{type(team_error).__name__}: '
                            f'{team_error}'
                        )

                else:

                    try:

                        db.execute_query(
                            """
                            DELETE FROM
                                PlayerTeamSubscribtion
                            WHERE
                                PlayerId = ?
                            """,
                            (player_id,)
                        )

                    except Exception as team_error:

                        print(
                            '[REMOVE TEAM LINK ERROR] '
                            f'{type(team_error).__name__}: '
                            f'{team_error}'
                        )

                ui.notify(
                    'تم تعديل بيانات اللاعب بنجاح',
                    color='positive'
                )

                edit_dialog.close()

                refresh_players()

            except Exception as e:

                ui.notify(
                    'حدث خطأ أثناء تعديل اللاعب',
                    color='negative'
                )

                print(
                    '[UPDATE PLAYER ERROR] '
                    f'{type(e).__name__}: {e}'
                )

        # =====================================================
        # Delete player
        # =====================================================

        def delete_player():

            player_id = safe_id(
                delete_player_id.value
            )

            if not player_id:

                ui.notify(
                    'بيانات اللاعب غير صحيحة',
                    color='warning'
                )

                return

            try:

                # =================================================
                # Delete team relation
                # =================================================

                try:

                    db.execute_query(
                        """
                        DELETE FROM
                            PlayerTeamSubscribtion
                        WHERE
                            PlayerId = ?
                        """,
                        (player_id,)
                    )

                except Exception as relation_error:

                    print(
                        '[DELETE TEAM RELATION ERROR] '
                        f'{type(relation_error).__name__}: '
                        f'{relation_error}'
                    )

                # =================================================
                # Delete player
                # =================================================

                db.execute_query(
                    """
                    DELETE FROM Player
                    WHERE
                        Id = ?
                        AND ClubId = ?
                    """,
                    (
                        player_id,
                        club_id
                    )
                )

                ui.notify(
                    'تم حذف اللاعب بنجاح',
                    color='positive'
                )

                delete_dialog.close()

                refresh_players()

            except Exception as e:

                ui.notify(
                    'لا يمكن حذف اللاعب لأنه مرتبط ببيانات أخرى',
                    color='negative'
                )

                print(
                    '[DELETE PLAYER ERROR] '
                    f'{type(e).__name__}: {e}'
                )

        # =====================================================
        # Clear filters
        # =====================================================

        def clear_filters():

            search.value = ''

            team_filter.value = None

            medical_filter.value = None

            membership_filter.value = None

            sort_select.value = 'newest'

            refresh_players()

        # =====================================================
        # Events
        # =====================================================

        save_button.on(
            'click',
            save_player
        )

        update_button.on(
            'click',
            update_player
        )

        delete_button.on(
            'click',
            delete_player
        )

        clear_filters_button.on(
            'click',
            clear_filters
        )

        search.on(
            'update:model-value',
            lambda e: refresh_players()
        )

        team_filter.on(
            'update:model-value',
            lambda e: refresh_players()
        )

        medical_filter.on(
            'update:model-value',
            lambda e: refresh_players()
        )

        membership_filter.on(
            'update:model-value',
            lambda e: refresh_players()
        )

        sort_select.on(
            'update:model-value',
            lambda e: refresh_players()
        )

        # =====================================================
        # Initial render
        # =====================================================

        refresh_players()