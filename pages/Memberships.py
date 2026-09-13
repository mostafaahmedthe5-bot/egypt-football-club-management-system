from nicegui import ui, app
import database as db


# =========================================================
# CLUB LOGOS
# =========================================================

def get_club_logo_url(club_name):
    logos = {
        'الأهلي': 'https://assets.footylogos.com/logos/al-ahly-sc/al-ahly-sc-logo-footylogos.png',
        'الزمالك': 'https://assets.footylogos.com/logos/zamalek-sc/zamalek-sc-logo-footylogos.png',
        'بيراميدز': 'https://assets.footylogos.com/logos/pyramids-fc/pyramids-fc-logo-footylogos.png',
        'المصري': 'https://assets.footylogos.com/logos/al-masry-sc/al-masry-sc-logo-footylogos.png',
        'الإسماعيلي': 'https://assets.footylogos.com/logos/ismaily-sc/ismaily-sc-logo-footylogos.png',
        'الاتحاد السكندري': 'https://assets.footylogos.com/logos/ittihad-alexandria/ittihad-alexandria-logo-footylogos.png',
        'سموحة': 'https://assets.footylogos.com/logos/smouha/smouha-logo-footylogos.png',
        'إنبي': 'https://assets.footylogos.com/logos/enppi-sc/enppi-sc-logo-footylogos.png',
        'البنك الأهلي': 'https://assets.footylogos.com/logos/bank-el-ahly/bank-el-ahly-logo-footylogos.png',
        'سيراميكا كليوباترا': 'https://assets.footylogos.com/logos/ceramica-cleopatra-fc/ceramica-cleopatra-logo-footylogos.png',
        'الجونة': 'https://assets.footylogos.com/logos/el-gouna-fc/el-gouna-logo-footylogos.png',
        'طلائع الجيش': 'https://assets.footylogos.com/logos/talaea-el-geish/talaea-el-geish-logo-footylogos.png',
        'مودرن سبورت': 'https://assets.footylogos.com/logos/modern-sport/modern-sport-logo-footylogos.png',
        'زد': 'https://assets.footylogos.com/logos/zed-fc/zed-fc-logo-footylogos.png',
        'المقاولون العرب': 'https://assets.footylogos.com/logos/el-mokawloon/el-mokawloon-logo-footylogos.png',
        'وادي دجلة': 'https://assets.footylogos.com/logos/wadi-degla-sc/wadi-degla-logo-footylogos.png',
        'غزل المحلة': 'https://assets.footylogos.com/logos/ghazl-el-mahalla/ghazl-el-mahalla-logo-footylogos.png',
        'فاركو': 'https://assets.footylogos.com/logos/pharco-fc/pharco-fc-logo-footylogos.png',
        'حرس الحدود': 'https://assets.footylogos.com/logos/harras-hodoud/harras-hodoud-logo-footylogos.png',
        'بتروجيت': 'https://assets.footylogos.com/logos/petrojet-fc/petrojet-fc-logo-footylogos.png',
        'كهرباء الإسماعيلية': None,
    }

    return logos.get(club_name)


# =========================================================
# CLUB TEAM PHOTOS
# =========================================================

def get_club_team_photo_url(club_name):
    team_photos = {
        'الأهلي': 'https://mediaaws-live.almasryalyoum.com/almasryalyoum/uploads/images/2026/02/28/thumbs/600x600/1652556.jpg',
        'الزمالك': 'https://img.btolat.com/2026/8/26/news/408598/large.jpg',
        'بيراميدز': 'https://assets.kooora.com/images/v3/getty-2241502137/crop/MM5DINJWHA5DENJXGA5G433XMU5DAORVGQZQ%3D%3D%3D%3D/GettyImages-2241502137.jpg?upscale=true&width=1400',
        'المصري': 'https://cdn.footballkitarchive.com/2025/08/16/SJ9EsdhLqv00LYu.jpg',
        'الإسماعيلي': 'https://gate.ahram.org.eg/Media/News/2026/2/22/19_2026-639073872925408457-540.jpg',
        'الاتحاد السكندري': 'https://media.egypttelegraph.com/2024/5/large/2816857328732202405140838433843.jpg',
        'سموحة': 'https://gate.ahram.org.eg/Media/News/2021/3/12/19_2021-637511660578110818-811.jpg',
        'إنبي': None,
        'البنك الأهلي': 'https://sportcdn.elwatannews.com/sport/537x389/6296324251755267957.jpg',
        'سيراميكا كليوباترا': None,
        'الجونة': 'https://assets.kooora.com/images/v3/kooora_816777_1/koo_110409.jpg?auto=webp&format=pjpg&quality=60&width=1320',
        'طلائع الجيش': 'https://img.btolat.com/2022/8/17/news/292086/large.jpg',
        'مودرن سبورت': 'https://gate.ahram.org.eg/Media/News/2025/8/9/19_2025-638903754105204016-520.jpeg',
        'زد': 'https://cdn.korabia.net/images/1200x667/2023/%D9%81%D8%B1%D9%8A%D9%82-%D8%B2%D8%AF1701348086.webp',
        'المقاولون العرب': 'https://aws-br-images.s3.us-east-2.amazonaws.com/upload/iblock/0bb/0bb3375257da9d00dc55d9d48a74843d.jpg',
        'وادي دجلة': 'https://koraplus.com/images/2025/8/large/1644140042104202508160520342034.jpg',
        'غزل المحلة': 'https://mediaaws-live.almasryalyoum.com/AMAYLivePictures/portalimages/news/original/2025/08/10/2742503_0.jpg',
        'فاركو': 'https://media.egypttelegraph.com/2024/7/large/28243251869320240708090941941.jpg',
        'حرس الحدود': 'https://media.elbalad.news/2024/10/large/838/5/181.jpg',
        'بتروجيت': 'https://cdn.dailysports.net/dailysports/20260223/82dcfee5426da77f59ff6044a60b5b0cb80409300cd5fe08dfc95f890c5b098f-1200-675.webp',
        'كهرباء الإسماعيلية': 'https://img.btolat.com/2026/5/4/news/399815/large.jpg',
    }

    return team_photos.get(club_name)


# =========================================================
# HELPERS
# =========================================================

def _table_columns(table_name):
    rows = db.fetch_all(
        f'PRAGMA table_info("{table_name}")'
    )

    return [
        row['name']
        for row in rows
    ]


def _first_existing_column(table_name, candidates):
    columns = _table_columns(table_name)

    for candidate in candidates:
        if candidate in columns:
            return candidate

    return None


def now_string():
    from datetime import datetime

    return datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S'
    )


def get_membership_status_column():
    return _first_existing_column(
        'MembershipStatus',
        [
            'MembershipStatusAR',
            'StatusAR',
            'NameAR',
            'Name',
            'MembershipStatus'
        ]
    )


def get_membership_type_column():
    return _first_existing_column(
        'MembershipType',
        [
            'MembershipTypeAR',
            'TypeAR',
            'NameAR',
            'Name',
            'MembershipType'
        ]
    )


def get_statuses():
    name_column = get_membership_status_column()

    if not name_column:
        return []

    rows = db.fetch_all(
        f'''
        SELECT
            Id,
            "{name_column}" AS Name
        FROM MembershipStatus
        ORDER BY Id
        '''
    )

    return rows


def get_membership_types():
    name_column = get_membership_type_column()

    if not name_column:
        return []

    rows = db.fetch_all(
        f'''
        SELECT
            Id,
            "{name_column}" AS Name
        FROM MembershipType
        ORDER BY Id
        '''
    )

    return rows


def get_players(
    club_id,
    search_value='',
    status_id='all',
    type_id='all'
):
    status_name_column = get_membership_status_column()
    type_name_column = get_membership_type_column()

    if not status_name_column:
        status_name_sql = "''"
    else:
        status_name_sql = (
            f's."{status_name_column}"'
        )

    if not type_name_column:
        type_name_sql = "''"
    else:
        type_name_sql = (
            f'mt."{type_name_column}"'
        )

    query = f'''
        SELECT
            p.Id,
            p.PlayerNameAR,
            p.PlayerNameEN,
            p.MembershipStatueId,
            p.MembershipTypeId,
            {status_name_sql} AS MembershipStatusName,
            {type_name_sql} AS MembershipTypeName,
            t.TeamAR,
            t.TeamEN
        FROM Player p

        LEFT JOIN MembershipStatus s
            ON s.Id = p.MembershipStatueId

        LEFT JOIN MembershipType mt
            ON mt.Id = p.MembershipTypeId

        LEFT JOIN PlayerTeamSubscribtion pts
            ON pts.Playerid = p.Id

        LEFT JOIN Team t
            ON t.Id = pts.Teamid

        WHERE p.ClubId = ?
    '''

    params = [club_id]

    if search_value:
        query += '''
            AND (
                p.PlayerNameAR LIKE ?
                OR p.PlayerNameEN LIKE ?
                OR CAST(p.Id AS TEXT) LIKE ?
            )
        '''

        search_pattern = (
            f'%{search_value}%'
        )

        params.extend([
            search_pattern,
            search_pattern,
            search_pattern
        ])

    if status_id not in (
        None,
        '',
        'all'
    ):
        query += '''
            AND p.MembershipStatueId = ?
        '''

        params.append(
            int(status_id)
        )

    if type_id not in (
        None,
        '',
        'all'
    ):
        query += '''
            AND p.MembershipTypeId = ?
        '''

        params.append(
            int(type_id)
        )

    query += '''
        ORDER BY
            p.Id DESC
    '''

    return db.fetch_all(
        query,
        tuple(params)
    )


def get_membership_statistics(club_id):
    total = db.fetch_one(
        '''
        SELECT COUNT(*) AS Count
        FROM Player
        WHERE ClubId = ?
        ''',
        (club_id,)
    )

    active = db.fetch_one(
        '''
        SELECT COUNT(*) AS Count
        FROM Player
        WHERE ClubId = ?
        AND MembershipStatueId = 1
        ''',
        (club_id,)
    )

    suspended = db.fetch_one(
        '''
        SELECT COUNT(*) AS Count
        FROM Player
        WHERE ClubId = ?
        AND MembershipStatueId = 2
        ''',
        (club_id,)
    )

    expired = db.fetch_one(
        '''
        SELECT COUNT(*) AS Count
        FROM Player
        WHERE ClubId = ?
        AND MembershipStatueId = 3
        ''',
        (club_id,)
    )

    return {
        'total': (
            total['Count']
            if total else 0
        ),
        'active': (
            active['Count']
            if active else 0
        ),
        'suspended': (
            suspended['Count']
            if suspended else 0
        ),
        'expired': (
            expired['Count']
            if expired else 0
        ),
    }


# =========================================================
# PAGE
# =========================================================

def content(club_id=None):

    if club_id is None:
        club_id = app.storage.user.get(
            'club_id'
        )

    if not club_id:
        ui.navigate.to(
            '/select_club'
        )
        return

    club = db.fetch_one(
        '''
        SELECT
            Id,
            ClubNameAR,
            ClubNameEN
        FROM Club
        WHERE Id = ?
        ''',
        (club_id,)
    )

    if not club:
        ui.notify(
            'النادي غير موجود',
            color='negative'
        )

        ui.navigate.to(
            '/select_club'
        )
        return

    club_name_ar = (
        club['ClubNameAR']
        or 'النادي'
    )

    club_name_en = (
        club['ClubNameEN']
        or ''
    )

    club_logo_url = (
        get_club_logo_url(
            club_name_ar
        )
    )

    team_photo_url = (
        get_club_team_photo_url(
            club_name_ar
        )
    )

    statuses = get_statuses()

    membership_types = (
        get_membership_types()
    )

    # =====================================================
    # HERO BACKGROUND
    # =====================================================

    hero_style = ''

    if team_photo_url:

        hero_style = f'''
            background-image:
                linear-gradient(
                    90deg,
                    rgba(15, 23, 42, 0.90),
                    rgba(15, 23, 42, 0.70),
                    rgba(15, 23, 42, 0.38)
                ),
                url("{team_photo_url}");
            background-size: cover;
            background-position: center 35%;
            background-repeat: no-repeat;
        '''

    # =====================================================
    # CSS
    # =====================================================

    ui.add_head_html(
        '''
        <style>

            .memberships-page {
                direction: rtl;
                width: 100%;
                min-height: 100vh;
                background: #f8fafc;
            }

            .memberships-wrapper {
                width: 100%;
                max-width: 1550px;
                margin: 0 auto;
            }

            /* ============================================
               FOOTBALL HEADER
               ============================================ */

            .memberships-header {
                width: 100%;
                min-height: 245px;
                padding: 30px;
                position: relative;
                overflow: hidden;
                border-radius: 24px;
                background-color: #0f172a;
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                border: 1px solid rgba(255,255,255,.10);
                box-shadow:
                    0 18px 45px
                    rgba(15,23,42,.20);
            }

            .memberships-header::after {
                content: "";
                position: absolute;
                inset: 0;
                pointer-events: none;
                background:
                    radial-gradient(
                        circle at 85% 20%,
                        rgba(245,158,11,.16),
                        transparent 28%
                    );
            }

            .memberships-header-content {
                position: relative;
                z-index: 2;
            }

            .memberships-header-icon {
                width: 64px;
                height: 64px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 18px;
                background: rgba(255,255,255,.10);
                border: 1px solid rgba(255,255,255,.18);
                backdrop-filter: blur(8px);
                box-shadow:
                    0 10px 25px
                    rgba(0,0,0,.18);
            }

            .memberships-club-logo {
                width: 88px;
                height: 88px;
                padding: 10px;
                flex-shrink: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 23px;
                background: rgba(255,255,255,.96);
                border: 2px solid
                    rgba(255,255,255,.55);
                box-shadow:
                    0 14px 35px
                    rgba(0,0,0,.28);
                backdrop-filter: blur(8px);
            }

            .memberships-club-logo img {
                width: 100%;
                height: 100%;
                object-fit: contain;
            }

            .memberships-title {
                color: white;
                font-size: 30px;
                font-weight: 900;
                line-height: 1.3;
                text-shadow:
                    0 3px 12px
                    rgba(0,0,0,.30);
            }

            .memberships-club {
                color: white;
                font-size: 20px;
                font-weight: 900;
                text-shadow:
                    0 2px 10px
                    rgba(0,0,0,.30);
            }

            .memberships-en {
                color: rgba(255,255,255,.65);
                font-size: 10px;
                letter-spacing: 2px;
                font-weight: 700;
            }

            .memberships-description {
                color: rgba(255,255,255,.82);
                font-size: 13px;
                line-height: 1.8;
            }

            .memberships-badge {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 9px 15px;
                border-radius: 999px;
                background: rgba(15,23,42,.58);
                border: 1px solid
                    rgba(255,255,255,.16);
                color: #fef3c7;
                font-size: 11px;
                font-weight: 800;
                backdrop-filter: blur(8px);
                position: relative;
                z-index: 3;
            }

            .memberships-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #fbbf24;
                box-shadow:
                    0 0 10px
                    rgba(251,191,36,.65);
            }

            .football-label {
                display: inline-flex;
                align-items: center;
                gap: 7px;
                color: rgba(255,255,255,.72);
                font-size: 11px;
                font-weight: 750;
            }

            /* ============================================
               STATISTICS
               ============================================ */

            .stat-card {
                width: 100%;
                min-height: 145px;
                position: relative;
                overflow: hidden;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 19px;
                box-shadow:
                    0 6px 20px
                    rgba(15,23,42,.04);
            }

            .stat-card::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
            }

            .stat-blue::before {
                background: #2563eb;
            }

            .stat-green::before {
                background: #059669;
            }

            .stat-amber::before {
                background: #d97706;
            }

            .stat-red::before {
                background: #dc2626;
            }

            .stat-label {
                color: #64748b;
                font-size: 11px;
                font-weight: 800;
            }

            .stat-number {
                color: #0f172a;
                font-size: 32px;
                font-weight: 950;
                line-height: 1;
            }

            .stat-description {
                color: #94a3b8;
                font-size: 10px;
                font-weight: 600;
            }

            .stat-icon {
                width: 50px;
                height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 14px;
            }

            /* ============================================
               FILTERS
               ============================================ */

            .filter-card {
                width: 100%;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 19px;
                box-shadow:
                    0 6px 18px
                    rgba(15,23,42,.035);
            }

            .field-label {
                color: #475569;
                font-size: 11px;
                font-weight: 850;
            }

            .filter-field .q-field__control {
                min-height: 49px !important;
                border-radius: 13px !important;
            }

            .refresh-button {
                min-height: 49px !important;
                border-radius: 13px !important;
                background: #0f172a !important;
                color: white !important;
                font-weight: 800 !important;
            }

            /* ============================================
               TABLE
               ============================================ */

            .table-card {
                width: 100%;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 21px;
                overflow: hidden;
                box-shadow:
                    0 7px 22px
                    rgba(15,23,42,.045);
            }

            .table-header {
                background: #f8fafc;
                border-bottom: 1px solid #e2e8f0;
            }

            .table-row {
                width: 100%;
                min-height: 84px;
                padding: 13px 18px;
                background: white;
                border-bottom: 1px solid #f1f5f9;
                transition:
                    background .18s ease,
                    transform .18s ease;
            }

            .table-row:hover {
                background: #f8fafc;
            }

            .table-row:last-child {
                border-bottom: none;
            }

            .player-avatar {
                width: 48px;
                height: 48px;
                flex-shrink: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 14px;
                background: #eff6ff;
                border: 1px solid #dbeafe;
            }

            .player-name {
                color: #0f172a;
                font-size: 13px;
                font-weight: 900;
            }

            .player-en {
                color: #94a3b8;
                font-size: 10px;
                font-weight: 600;
            }

            .player-id {
                color: #94a3b8;
                font-size: 9px;
                font-weight: 650;
            }

            .membership-chip {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-height: 31px;
                padding: 5px 11px;
                border-radius: 999px;
                font-size: 10px;
                font-weight: 800;
                border: 1px solid;
            }

            .chip-green {
                background: #f0fdf4;
                color: #15803d;
                border-color: #dcfce7;
            }

            .chip-amber {
                background: #fffbeb;
                color: #b45309;
                border-color: #fef3c7;
            }

            .chip-red {
                background: #fef2f2;
                color: #b91c1c;
                border-color: #fecaca;
            }

            .chip-blue {
                background: #eff6ff;
                color: #1d4ed8;
                border-color: #dbeafe;
            }

            .chip-slate {
                background: #f8fafc;
                color: #475569;
                border-color: #e2e8f0;
            }

            .edit-button {
                width: 38px !important;
                height: 38px !important;
                border-radius: 10px !important;
                color: #2563eb !important;
            }

            /* ============================================
               EMPTY STATE
               ============================================ */

            .empty-state {
                min-height: 280px;
            }

            .empty-icon {
                width: 80px;
                height: 80px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 22px;
                background: #f8fafc;
                border: 1px solid #e2e8f0;
            }

            /* ============================================
               DIALOG
               ============================================ */

            .dialog-card {
                width: 560px;
                max-width: 95vw;
                border-radius: 22px;
                overflow: hidden;
                background: white;
            }

            .dialog-header {
                padding: 22px 24px;
                background: linear-gradient(
                    135deg,
                    #0f172a,
                    #172554
                );
            }

            .dialog-icon {
                width: 48px;
                height: 48px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 14px;
                background: rgba(255,255,255,.08);
                border: 1px solid
                    rgba(255,255,255,.10);
            }

            .dialog-title {
                color: white;
                font-size: 19px;
                font-weight: 900;
            }

            .dialog-subtitle {
                color: #94a3b8;
                font-size: 10px;
            }

            .dialog-body {
                padding: 24px;
            }

            .dialog-save {
                background: #1d4ed8 !important;
                color: white !important;
                border-radius: 11px !important;
                font-weight: 850 !important;
            }

            /* ============================================
               RESPONSIVE
               ============================================ */

            @media (max-width: 900px) {

                .memberships-header {
                    padding: 24px;
                    min-height: 220px;
                }

                .memberships-title {
                    font-size: 25px;
                }

                .memberships-club-logo {
                    width: 72px;
                    height: 72px;
                }

                .table-row {
                    padding: 12px;
                }
            }

            @media (max-width: 650px) {

                .memberships-header {
                    padding: 20px;
                    border-radius: 18px;
                    min-height: 250px;
                }

                .memberships-title {
                    font-size: 22px;
                }

                .memberships-club {
                    font-size: 17px;
                }

                .memberships-description {
                    font-size: 11px;
                }

                .memberships-club-logo {
                    width: 62px;
                    height: 62px;
                    border-radius: 17px;
                }

                .table-row {
                    min-height: auto;
                    margin-bottom: 8px;
                    border: 1px solid #e2e8f0;
                    border-radius: 14px;
                }
            }

        </style>
        '''
    )

    stats = get_membership_statistics(
        club_id
    )

    status_options = {
        'all': 'كل الحالات'
    }

    for row in statuses:

        status_options[
            str(row['Id'])
        ] = (
            row['Name']
            or f"الحالة {row['Id']}"
        )

    type_options = {
        'all': 'كل الأنواع'
    }

    for row in membership_types:

        type_options[
            str(row['Id'])
        ] = (
            row['Name']
            or f"النوع {row['Id']}"
        )

    # =====================================================
    # PAGE
    # =====================================================

    with ui.column().classes(
        'memberships-page w-full p-4 md:p-6 lg:p-8'
    ):

        with ui.column().classes(
            'memberships-wrapper gap-6'
        ):

            # =================================================
            # HEADER
            # =================================================

            with ui.element(
                'div'
            ).classes(
                'memberships-header'
            ).style(
                hero_style
            ):

                with ui.column().classes(
                    'memberships-header-content w-full gap-5'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between flex-wrap gap-6'
                    ):

                        with ui.row().classes(
                            'items-center gap-4'
                        ):

                            # ---------------------------------
                            # CLUB LOGO
                            # ---------------------------------

                            if club_logo_url:

                                with ui.element(
                                    'div'
                                ).classes(
                                    'memberships-club-logo'
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
                                    'memberships-header-icon'
                                ):

                                    ui.icon(
                                        'sports_soccer'
                                    ).classes(
                                        'text-3xl text-white'
                                    )

                            # ---------------------------------
                            # TITLE
                            # ---------------------------------

                            with ui.column().classes(
                                'gap-1'
                            ):

                                ui.label(
                                    'إدارة العضويات'
                                ).classes(
                                    'memberships-title'
                                )

                                ui.label(
                                    club_name_ar
                                ).classes(
                                    'memberships-club'
                                )

                                if club_name_en:

                                    ui.label(
                                        club_name_en
                                    ).classes(
                                        'memberships-en'
                                    )

                        # -------------------------------------
                        # BADGE
                        # -------------------------------------

                        with ui.element(
                            'div'
                        ).classes(
                            'memberships-badge'
                        ):

                            ui.element(
                                'span'
                            ).classes(
                                'memberships-dot'
                            )

                            ui.icon(
                                'sports_soccer'
                            ).classes(
                                'text-sm text-amber-300'
                            )

                            ui.label(
                                'Football Club Management'
                            )

                    # -----------------------------------------
                    # DESCRIPTION
                    # -----------------------------------------

                    with ui.row().classes(
                        'items-center gap-3'
                    ):

                        ui.icon(
                            'groups'
                        ).classes(
                            'text-lg text-amber-300'
                        )

                        ui.label(
                            'إدارة ومتابعة عضويات لاعبي النادي والفرق الرياضية'
                        ).classes(
                            'memberships-description'
                        )

            # =================================================
            # STATISTICS
            # =================================================

            with ui.row().classes(
                'w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4'
            ):

                # ---------------------------------------------
                # TOTAL
                # ---------------------------------------------

                with ui.card().classes(
                    'stat-card stat-blue p-5'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):

                        with ui.column().classes(
                            'gap-2'
                        ):

                            ui.label(
                                'إجمالي اللاعبين'
                            ).classes(
                                'stat-label'
                            )

                            ui.label(
                                str(stats['total'])
                            ).classes(
                                'stat-number'
                            )

                        with ui.element(
                            'div'
                        ).classes(
                            'stat-icon bg-blue-50'
                        ):

                            ui.icon(
                                'groups'
                            ).classes(
                                'text-2xl text-blue-600'
                            )

                    ui.label(
                        'إجمالي لاعبي النادي'
                    ).classes(
                        'stat-description mt-4'
                    )

                # ---------------------------------------------
                # ACTIVE
                # ---------------------------------------------

                with ui.card().classes(
                    'stat-card stat-green p-5'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):

                        with ui.column().classes(
                            'gap-2'
                        ):

                            ui.label(
                                'عضويات نشطة'
                            ).classes(
                                'stat-label'
                            )

                            ui.label(
                                str(stats['active'])
                            ).classes(
                                'stat-number'
                            )

                        with ui.element(
                            'div'
                        ).classes(
                            'stat-icon bg-emerald-50'
                        ):

                            ui.icon(
                                'verified'
                            ).classes(
                                'text-2xl text-emerald-600'
                            )

                    ui.label(
                        'حالة العضوية رقم 1'
                    ).classes(
                        'stat-description mt-4'
                    )

                # ---------------------------------------------
                # SUSPENDED
                # ---------------------------------------------

                with ui.card().classes(
                    'stat-card stat-amber p-5'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):

                        with ui.column().classes(
                            'gap-2'
                        ):

                            ui.label(
                                'عضويات معلقة'
                            ).classes(
                                'stat-label'
                            )

                            ui.label(
                                str(stats['suspended'])
                            ).classes(
                                'stat-number'
                            )

                        with ui.element(
                            'div'
                        ).classes(
                            'stat-icon bg-amber-50'
                        ):

                            ui.icon(
                                'pause_circle'
                            ).classes(
                                'text-2xl text-amber-600'
                            )

                    ui.label(
                        'حالة العضوية رقم 2'
                    ).classes(
                        'stat-description mt-4'
                    )

                # ---------------------------------------------
                # EXPIRED
                # ---------------------------------------------

                with ui.card().classes(
                    'stat-card stat-red p-5'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):

                        with ui.column().classes(
                            'gap-2'
                        ):

                            ui.label(
                                'عضويات منتهية'
                            ).classes(
                                'stat-label'
                            )

                            ui.label(
                                str(stats['expired'])
                            ).classes(
                                'stat-number'
                            )

                        with ui.element(
                            'div'
                        ).classes(
                            'stat-icon bg-red-50'
                        ):

                            ui.icon(
                                'event_busy'
                            ).classes(
                                'text-2xl text-red-600'
                            )

                    ui.label(
                        'حالة العضوية رقم 3'
                    ).classes(
                        'stat-description mt-4'
                    )

            # =================================================
            # FILTERS
            # =================================================

            with ui.card().classes(
                'filter-card p-5'
            ):

                with ui.row().classes(
                    'w-full items-end gap-4 flex-wrap'
                ):

                    with ui.column().classes(
                        'flex-1 min-w-[260px] gap-2'
                    ):

                        ui.label(
                            'البحث'
                        ).classes(
                            'field-label'
                        )

                        search = ui.input(
                            placeholder='ابحث باسم اللاعب أو الرقم...'
                        ).props(
                            'outlined rounded clearable'
                        ).classes(
                            'filter-field w-full'
                        )

                    with ui.column().classes(
                        'min-w-[190px] gap-2'
                    ):

                        ui.label(
                            'حالة العضوية'
                        ).classes(
                            'field-label'
                        )

                        status_filter = ui.select(
                            status_options,
                            value='all'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'filter-field w-full'
                        )

                    with ui.column().classes(
                        'min-w-[190px] gap-2'
                    ):

                        ui.label(
                            'نوع العضوية'
                        ).classes(
                            'field-label'
                        )

                        type_filter = ui.select(
                            type_options,
                            value='all'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'filter-field w-full'
                        )

                    refresh_button = ui.button(
                        'تحديث',
                        icon='refresh'
                    ).props(
                        'unelevated no-caps'
                    ).classes(
                        'refresh-button'
                    )

            # =================================================
            # TABLE CONTAINER
            # =================================================

            table_container = ui.column().classes(
                'w-full'
            )

            # =================================================
            # EDIT DIALOG
            # =================================================

            edit_dialog = ui.dialog()

            with edit_dialog:

                with ui.card().classes(
                    'dialog-card'
                ):

                    with ui.element(
                        'div'
                    ).classes(
                        'dialog-header'
                    ):

                        with ui.row().classes(
                            'items-center gap-3'
                        ):

                            with ui.element(
                                'div'
                            ).classes(
                                'dialog-icon'
                            ):

                                ui.icon(
                                    'card_membership'
                                ).classes(
                                    'text-xl text-white'
                                )

                            with ui.column().classes(
                                'gap-0'
                            ):

                                ui.label(
                                    'تعديل العضوية'
                                ).classes(
                                    'dialog-title'
                                )

                                ui.label(
                                    'تحديث حالة ونوع عضوية اللاعب'
                                ).classes(
                                    'dialog-subtitle mt-1'
                                )

                    with ui.column().classes(
                        'dialog-body gap-4'
                    ):

                        edit_player_id = ui.number(
                            'رقم اللاعب'
                        ).props(
                            'outlined rounded readonly'
                        ).classes(
                            'w-full'
                        )

                        edit_player_name = ui.input(
                            'اسم اللاعب'
                        ).props(
                            'outlined rounded readonly'
                        ).classes(
                            'w-full'
                        )

                        edit_status = ui.select(
                            status_options,
                            label='حالة العضوية'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'w-full'
                        )

                        edit_type = ui.select(
                            type_options,
                            label='نوع العضوية'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'w-full'
                        )

                        with ui.row().classes(
                            'w-full justify-end gap-2 mt-2'
                        ):

                            ui.button(
                                'إلغاء',
                                on_click=edit_dialog.close
                            ).props(
                                'flat no-caps'
                            )

                            save_edit_button = ui.button(
                                'حفظ التعديل',
                                icon='save'
                            ).props(
                                'unelevated no-caps'
                            ).classes(
                                'dialog-save'
                            )

            # =================================================
            # REFRESH TABLE
            # =================================================

            def refresh_table():

                table_container.clear()

                search_value = (
                    search.value or ''
                ).strip()

                selected_status = (
                    status_filter.value
                )

                selected_type = (
                    type_filter.value
                )

                players = get_players(
                    club_id,
                    search_value,
                    selected_status,
                    selected_type
                )

                with table_container:

                    with ui.card().classes(
                        'table-card'
                    ):

                        # -------------------------------------
                        # TABLE HEADER
                        # -------------------------------------

                        with ui.row().classes(
                            'table-header w-full items-center justify-between p-5'
                        ):

                            with ui.row().classes(
                                'items-center gap-3'
                            ):

                                with ui.element(
                                    'div'
                                ).classes(
                                    'w-11 h-11 rounded-xl bg-blue-50 flex items-center justify-center'
                                ):

                                    ui.icon(
                                        'groups'
                                    ).classes(
                                        'text-xl text-blue-600'
                                    )

                                with ui.column().classes(
                                    'gap-0'
                                ):

                                    ui.label(
                                        'عضويات اللاعبين'
                                    ).classes(
                                        'text-lg font-black text-slate-900'
                                    )

                                    ui.label(
                                        'قائمة العضويات الحالية للاعبي النادي'
                                    ).classes(
                                        'text-[11px] text-slate-400 mt-1'
                                    )

                            ui.label(
                                f'{len(players)} لاعب'
                            ).classes(
                                'px-3 py-1.5 rounded-full bg-blue-50 text-blue-700 border border-blue-100 text-[11px] font-black'
                            )

                        # -------------------------------------
                        # EMPTY
                        # -------------------------------------

                        if not players:

                            with ui.column().classes(
                                'empty-state w-full items-center justify-center'
                            ):

                                with ui.element(
                                    'div'
                                ).classes(
                                    'empty-icon'
                                ):

                                    ui.icon(
                                        'card_membership'
                                    ).classes(
                                        'text-4xl text-slate-300'
                                    )

                                ui.label(
                                    'لا توجد نتائج'
                                ).classes(
                                    'text-lg font-black text-slate-600 mt-4'
                                )

                                ui.label(
                                    'غيّر البحث أو الفلاتر وحاول مرة أخرى.'
                                ).classes(
                                    'text-sm text-slate-400 mt-1'
                                )

                            return

                        # -------------------------------------
                        # TABLE HEADERS
                        # -------------------------------------

                        with ui.row().classes(
                            'w-full items-center px-5 py-3 bg-white border-b border-slate-100'
                        ):

                            ui.label(
                                'اللاعب'
                            ).classes(
                                'flex-1 text-xs font-black text-slate-400'
                            )

                            ui.label(
                                'الفريق'
                            ).classes(
                                'w-48 text-center text-xs font-black text-slate-400'
                            )

                            ui.label(
                                'حالة العضوية'
                            ).classes(
                                'w-40 text-center text-xs font-black text-slate-400'
                            )

                            ui.label(
                                'نوع العضوية'
                            ).classes(
                                'w-44 text-center text-xs font-black text-slate-400'
                            )

                            ui.label(
                                'إجراء'
                            ).classes(
                                'w-24 text-center text-xs font-black text-slate-400'
                            )

                        # -------------------------------------
                        # ROWS
                        # -------------------------------------

                        for player in players:

                            player_id = player['Id']

                            player_name_ar = (
                                player['PlayerNameAR']
                                or 'بدون اسم'
                            )

                            player_name_en = (
                                player['PlayerNameEN']
                                or ''
                            )

                            team_name = (
                                player['TeamAR']
                                or player['TeamEN']
                                or 'غير مرتبط بفريق'
                            )

                            status_name = (
                                player['MembershipStatusName']
                                or 'غير محددة'
                            )

                            type_name = (
                                player['MembershipTypeName']
                                or 'غير محدد'
                            )

                            status_id = (
                                player[
                                    'MembershipStatueId'
                                ]
                            )

                            # ---------------------------------
                            # STATUS COLOR
                            # ---------------------------------

                            if status_id == 1:

                                status_class = (
                                    'membership-chip chip-green'
                                )

                            elif status_id == 2:

                                status_class = (
                                    'membership-chip chip-amber'
                                )

                            elif status_id in (
                                3,
                                4,
                                6
                            ):

                                status_class = (
                                    'membership-chip chip-red'
                                )

                            elif status_id == 5:

                                status_class = (
                                    'membership-chip chip-blue'
                                )

                            else:

                                status_class = (
                                    'membership-chip chip-slate'
                                )

                            # ---------------------------------
                            # ROW
                            # ---------------------------------

                            with ui.row().classes(
                                'table-row items-center gap-4'
                            ):

                                # =============================
                                # PLAYER
                                # =============================

                                with ui.row().classes(
                                    'flex-1 min-w-0 items-center gap-3'
                                ):

                                    with ui.element(
                                        'div'
                                    ).classes(
                                        'player-avatar'
                                    ):

                                        ui.icon(
                                            'person'
                                        ).classes(
                                            'text-xl text-blue-600'
                                        )

                                    with ui.column().classes(
                                        'gap-0 min-w-0'
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
                                                'player-en mt-1'
                                            )

                                        ui.label(
                                            f'ID: {player_id}'
                                        ).classes(
                                            'player-id mt-1'
                                        )

                                # =============================
                                # TEAM
                                # =============================

                                with ui.row().classes(
                                    'w-48 justify-center'
                                ):

                                    ui.label(
                                        team_name
                                    ).classes(
                                        'text-xs font-bold text-slate-600 text-center'
                                    )

                                # =============================
                                # STATUS
                                # =============================

                                with ui.row().classes(
                                    'w-40 justify-center'
                                ):

                                    ui.label(
                                        status_name
                                    ).classes(
                                        status_class
                                    )

                                # =============================
                                # TYPE
                                # =============================

                                with ui.row().classes(
                                    'w-44 justify-center'
                                ):

                                    ui.label(
                                        type_name
                                    ).classes(
                                        'membership-chip chip-blue'
                                    )

                                # =============================
                                # ACTION
                                # =============================

                                with ui.row().classes(
                                    'w-24 justify-center'
                                ):

                                    def open_edit(
                                        player_data=player
                                    ):

                                        edit_player_id.value = (
                                            player_data['Id']
                                        )

                                        edit_player_name.value = (
                                            player_data[
                                                'PlayerNameAR'
                                            ]
                                            or player_data[
                                                'PlayerNameEN'
                                            ]
                                            or ''
                                        )

                                        edit_status.value = (
                                            str(
                                                player_data[
                                                    'MembershipStatueId'
                                                ]
                                            )
                                            if player_data[
                                                'MembershipStatueId'
                                            ] is not None
                                            else None
                                        )

                                        edit_type.value = (
                                            str(
                                                player_data[
                                                    'MembershipTypeId'
                                                ]
                                            )
                                            if player_data[
                                                'MembershipTypeId'
                                            ] is not None
                                            else None
                                        )

                                        edit_dialog.open()

                                    ui.button(
                                        icon='edit',
                                        on_click=open_edit
                                    ).props(
                                        'flat round'
                                    ).classes(
                                        'edit-button'
                                    ).tooltip(
                                        'تعديل العضوية'
                                    )

            # =================================================
            # SAVE EDIT
            # =================================================

            def save_membership_edit():

                if not edit_player_id.value:

                    ui.notify(
                        'لم يتم تحديد اللاعب',
                        color='warning'
                    )

                    return

                player_id = int(
                    edit_player_id.value
                )

                status_value = (
                    edit_status.value
                )

                type_value = (
                    edit_type.value
                )

                if status_value in (
                    None,
                    '',
                    'all'
                ):

                    ui.notify(
                        'اختر حالة العضوية',
                        color='warning'
                    )

                    return

                if type_value in (
                    None,
                    '',
                    'all'
                ):

                    ui.notify(
                        'اختر نوع العضوية',
                        color='warning'
                    )

                    return

                try:

                    db.execute_query(
                        '''
                        UPDATE Player
                        SET
                            MembershipStatueId = ?,
                            MembershipTypeId = ?,
                            UpdatedBy = ?,
                            UpdatedOn = ?
                        WHERE Id = ?
                        AND ClubId = ?
                        ''',
                        (
                            int(status_value),
                            int(type_value),
                            app.storage.user.get(
                                'username',
                                'SYSTEM'
                            ),
                            now_string(),
                            player_id,
                            club_id
                        )
                    )

                    ui.notify(
                        'تم تحديث العضوية بنجاح',
                        color='positive'
                    )

                    edit_dialog.close()

                    refresh_table()

                except Exception as e:

                    ui.notify(
                        'حدث خطأ أثناء تحديث العضوية',
                        color='negative'
                    )

                    print(
                        f'[MEMBERSHIP UPDATE ERROR] '
                        f'{type(e).__name__}: {e}'
                    )

            save_edit_button.on(
                'click',
                save_membership_edit
            )

            # =================================================
            # EVENTS
            # =================================================

            search.on(
                'update:model-value',
                lambda e: refresh_table()
            )

            status_filter.on(
                'update:model-value',
                lambda e: refresh_table()
            )

            type_filter.on(
                'update:model-value',
                lambda e: refresh_table()
            )

            refresh_button.on(
                'click',
                refresh_table
            )

            # =================================================
            # INITIAL LOAD
            # =================================================

            refresh_table()