import base64
from nicegui import app, ui
import database as db


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


def content(club_id=None):

    # =========================================================
    # النادي الحالي
    # =========================================================
    if club_id is None:
        club_id = app.storage.user.get('club_id')

    if not club_id:
        ui.navigate.to('/select_club')
        return

    # =========================================================
    # بيانات النادي
    # =========================================================
    club = db.fetch_one(
        """
        SELECT Id, ClubNameAR, ClubNameEN, Logo
        FROM Club
        WHERE Id = ?
        """,
        (club_id,),
    )

    if not club:
        ui.notify('النادي غير موجود', color='negative')
        ui.navigate.to('/select_club')
        return

    club_name_ar = club['ClubNameAR'] or 'النادي'
    club_name_en = club['ClubNameEN'] or ''

    # =========================================================
    # معالجة لوجو النادي
    # =========================================================
    raw_logo = club.get('Logo')
    club_logo_src = None

    if raw_logo:
        if isinstance(raw_logo, bytes):
            encoded = base64.b64encode(raw_logo).decode('utf-8')
            club_logo_src = f'data:image/png;base64,{encoded}'
        elif isinstance(raw_logo, str) and raw_logo.strip():
            club_logo_src = raw_logo.strip()

    if not club_logo_src:
        club_logo_src = get_club_logo_url(club_name_ar)

    # =========================================================
    # صورة الفريق الجماعية
    # =========================================================
    team_photo_src = get_club_team_photo_url(club_name_ar)

    # =========================================================
    # الإحصائيات الأساسية
    # =========================================================
    players_count = len(
        db.fetch_all('SELECT Id FROM Player WHERE ClubId = ?', (club_id,))
    )

    teams_count = len(
        db.fetch_all('SELECT Id FROM Team WHERE Clubid = ?', (club_id,))
    )

    subscriptions_count = len(
        db.fetch_all(
            """
            SELECT pts.Id
            FROM PlayerTeamSubscribtion pts
            INNER JOIN Player p ON p.Id = pts.Playerid
            INNER JOIN Team t ON t.Id = pts.Teamid
            WHERE p.ClubId = ? AND t.Clubid = ?
            """,
            (club_id, club_id),
        )
    )

    tournaments_count = len(
        db.fetch_all(
            """
            SELECT DISTINCT tt.TournamentId
            FROM TournamentTable tt
            INNER JOIN Team t ON t.Id = tt.Teamid
            WHERE t.Clubid = ?
            """,
            (club_id,),
        )
    )

    # =========================================================
    # عدد الرياضات
    # =========================================================
    sports_count = len(
        db.fetch_all(
            """
            SELECT DISTINCT Sportid
            FROM Team
            WHERE Clubid = ? AND Sportid IS NOT NULL
            """,
            (club_id,),
        )
    )

    # =========================================================
    # الحالات الطبية
    # =========================================================
    medical_states = db.fetch_all(
        """
        SELECT
            mrs.MedicalReportStateNameAR,
            COUNT(p.Id) AS Count
        FROM Player p
        LEFT JOIN MedicalReportState mrs ON mrs.Id = p.MedicalReportStatueId
        WHERE p.ClubId = ?
        GROUP BY p.MedicalReportStatueId
        """,
        (club_id,),
    )

    # =========================================================
    # حالات العضوية
    # =========================================================
    membership_states = db.fetch_all(
        """
        SELECT
            ms.MembershipStatusNameAR,
            COUNT(p.Id) AS Count
        FROM Player p
        LEFT JOIN MembershipStatus ms ON ms.Id = p.MembershipStatueId
        WHERE p.ClubId = ?
        GROUP BY p.MembershipStatueId
        """,
        (club_id,),
    )

    # =========================================================
    # الفرق
    # =========================================================
    teams = db.fetch_all(
        """
        SELECT
            t.Id,
            t.TeamAR,
            t.TeamEN,
            tc.TeamCategoryNameAR,
            tc.TeamCategoryNameEN,
            s.SportNameAR,
            s.SportNameEN,
            COUNT(DISTINCT pts.Playerid) AS PlayerCount
        FROM Team t
        LEFT JOIN TeamCategory tc ON tc.Id = t.Teamcatgoryid
        LEFT JOIN Sport s ON s.Id = t.Sportid
        LEFT JOIN PlayerTeamSubscribtion pts ON pts.Teamid = t.Id
        WHERE t.Clubid = ?
        GROUP BY
            t.Id, t.TeamAR, t.TeamEN,
            tc.TeamCategoryNameAR, tc.TeamCategoryNameEN,
            s.SportNameAR, s.SportNameEN
        ORDER BY t.Id DESC
        """,
        (club_id,),
    )

    # =========================================================
    # أحدث اللاعبين
    # =========================================================
    latest_players = db.fetch_all(
        """
        SELECT
            p.Id,
            p.PlayerNameAR,
            ms.MembershipStatusNameAR,
            mrs.MedicalReportStateNameAR
        FROM Player p
        LEFT JOIN MembershipStatus ms ON ms.Id = p.MembershipStatueId
        LEFT JOIN MedicalReportState mrs ON mrs.Id = p.MedicalReportStatueId
        WHERE p.ClubId = ?
        ORDER BY p.Id DESC
        LIMIT 8
        """,
        (club_id,),
    )

    # =========================================================
    # CSS
    # =========================================================
    ui.add_head_html('''
        <style>
            html, body {
                margin: 0;
                padding: 0;
                min-height: 100%;
            }
            body {
                overflow-x: hidden;
                background: #f1f5f9;
            }
            .rtl-container {
                direction: rtl;
                width: 100%;
                max-width: 100% !important;
                min-height: 100vh;
                margin: 0;
                padding: 4px 4px 30px 4px;
            }
            .dashboard-content {
                width: 100%;
            }
            .hero-card {
                width: 100%;
                min-height: 240px;
                border-radius: 24px;
                padding: 32px 40px;
                position: relative;
                overflow: hidden;
                background-color: #527A91;
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                border: 1px solid rgba(255,255,255,.08);
                box-shadow: 0 14px 35px rgba(15,23,42,.16);
            }
            .hero-card::before {
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(
                    90deg,
                    rgba(15,23,42,.88) 0%,
                    rgba(15,23,42,.72) 42%,
                    rgba(15,23,42,.52) 72%,
                    rgba(15,23,42,.66) 100%
                );
                z-index: 1;
            }
            .hero-card::after {
                content: "";
                position: absolute;
                width: 280px;
                height: 280px;
                border-radius: 50%;
                bottom: -160px;
                left: 5%;
                background: radial-gradient(circle, rgba(245,158,11,.16), transparent 70%);
                z-index: 1;
                pointer-events: none;
            }
            .hero-content {
                position: relative;
                z-index: 2;
            }
            .hero-title {
                color: rgba(255,255,255,.85);
                font-size: 32px;
                font-weight: 900;
                line-height: 1.25;
            }
            .hero-club-name {
                color: #ffffff;
                font-size: 35px;
                font-weight: 900;
                line-height: 1.25;
                text-shadow: 0 3px 15px rgba(0,0,0,.25);
            }
            .hero-club-en {
                color: #e2e8f0;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 3px;
            }
            .hero-description {
                color: #e2e8f0;
                font-size: 14px;
                line-height: 1.8;
                max-width: 700px;
            }
            .hero-status {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                margin-top: 14px;
                padding: 7px 12px;
                border-radius: 999px;
                color: #d1fae5;
                background: rgba(16,185,129,.14);
                border: 1px solid rgba(16,185,129,.25);
                font-size: 11px;
                font-weight: 800;
                backdrop-filter: blur(6px);
            }
            .hero-status-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #10b981;
                box-shadow: 0 0 10px rgba(16,185,129,.7);
            }
            .hero-logo-wrapper {
                width: 150px;
                height: 150px;
                flex-shrink: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                background: rgba(255,255,255,.96);
                border-radius: 30px;
                padding: 18px;
                border: 1px solid rgba(255,255,255,.45);
                box-shadow: 0 20px 45px rgba(15,23,42,.35);
                position: relative;
                overflow: hidden;
            }
            .hero-logo-wrapper::before {
                content: "";
                position: absolute;
                top: 0;
                right: 0;
                left: 0;
                height: 4px;
                background: #f59e0b;
            }
            .hero-logo {
                width: 100%;
                height: 100%;
                object-fit: contain;
                position: relative;
                z-index: 2;
            }
            .hero-logo-fallback {
                color: #527A91 !important;
            }

            /* ---------------------------------------------------- */
            /* خلفية الكروت بصورة النجيل الأخضر المطلوبة */
            /* ---------------------------------------------------- */
            .stat-card, .section-card {
                min-height: 170px;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
                padding: 22px;
                box-shadow: 0 7px 20px rgba(15,23,42,.045);
                overflow: hidden;
                position: relative;
                background-image: 
                            linear-gradient(
            rgba(255, 255, 255, 0.58),
            rgba(255, 255, 255, 0.58)
        ),
                    url('https://imgs.search.brave.com/XNf_-WkrTa5HTcG0y0rxAaetpCRWAwPtmzJ-IncBhTw/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudmVjdGVlenku/Y29tL3N5c3RlbS9y/ZXNvdXJjZXMvdGh1/bWJuYWlscy8wNDMv/NDA3LzI0Ni9zbWFs/bC90ZXh0dXJlLW9m/LWdyZWVuLWdyYXNz/LW9uLXRoZS1sYXdu/LW5hdHVyYWwtYWJz/dHJhY3QtYmFja2dy/b3VuZC1waG90by5q/cGc') !important;
                background-size: cover !important;
                background-position: center !important;
            }

            .stat-card::before {
                content: "";
                position: absolute;
                width: 100%;
                height: 3px;
                top: 0;
                right: 0;
                background: #e2e8f0;
            }
            .stat-icon-wrapper {
                width: 58px;
                height: 58px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 16px;
            }
            .stat-label {
                color: #475569;
                font-size: 12px;
                font-weight: 750;
            }
            .stat-value {
                color: #0f172a;
                font-size: 40px;
                line-height: 1;
                font-weight: 950;
            }
            .stat-bottom-line {
                width: 100%;
                height: 3px;
                border-radius: 999px;
                background: rgba(0,0,0,0.05);
            }
            .section-title {
                color: #1e293b;
                font-size: 16px;
                font-weight: 850;
            }
            .section-subtitle {
                color: #64748b;
                font-size: 11px;
                font-weight: 600;
            }
            .section-icon {
                width: 42px;
                height: 42px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 12px;
            }
            .list-item {
                width: 100%;
                border-bottom: 1px solid rgba(0, 0, 0, 0.05);
                padding: 12px 10px;
            }
            .list-item:last-child {
                border-bottom: none;
            }
            .item-avatar {
                width: 48px;
                height: 48px;
                flex-shrink: 0;
                border-radius: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px solid #e2e8f0;
            }
            .number-badge {
                min-width: 42px;
                height: 29px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 0 10px;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.9);
                color: #334155;
                border: 1px solid #e2e8f0;
                font-size: 12px;
                font-weight: 900;
            }
            ::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }
            ::-webkit-scrollbar-track {
                background: transparent;
            }
            ::-webkit-scrollbar-thumb {
                background: #cbd5e1;
                border-radius: 999px;
            }
        </style>
    ''')

    # =========================================================
    # MAIN LAYOUT
    # =========================================================
    with ui.element('div').classes('rtl-container flex flex-col gap-6'):

        # HERO SECTION
        hero = ui.element('div').classes('hero-card')
        if team_photo_src:
            hero.style(f'background-image: url("{team_photo_src}");')

        with hero:
            with ui.row().classes(
                'hero-content w-full items-center justify-between flex-wrap gap-8'
            ):
                with ui.column().classes('gap-2 flex-1'):
                    ui.label('نادي').classes('hero-title')
                    ui.label(club_name_ar).classes('hero-club-name')

                    if club_name_en:
                        ui.label(club_name_en.upper()).classes('hero-club-en')

                    ui.label(
                        'إدارة شاملة لبيانات اللاعبين والفرق والبطولات والأنشطة الرياضية بالنادي.'
                    ).classes('hero-description mt-2')

                    with ui.element('div').classes('hero-status'):
                        ui.element('span').classes('hero-status-dot')
                        ui.label('النظام يعمل بشكل طبيعي')

                # LOGO
                with ui.element('div').classes('hero-logo-wrapper'):
                    if club_logo_src:
                        ui.image(club_logo_src).classes('hero-logo')
                    else:
                        ui.icon('sports_soccer', size='72px').classes(
                            'hero-logo-fallback'
                        )

        # STATISTICS SECTION
        with ui.row().classes(
            'w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5'
        ):

            # Players Stat
            with ui.card().classes('stat-card'):
                with ui.row().classes('w-full items-start justify-between'):
                    with ui.column().classes('gap-2'):
                        ui.label('إجمالي اللاعبين').classes('stat-label')
                        ui.label(str(players_count)).classes('stat-value')
                    with ui.element('div').classes(
                        'stat-icon-wrapper bg-sky-100 text-sky-600'
                    ):
                        ui.icon('groups').classes('text-3xl')
                ui.label('المسجلين بالنادي').classes(
                    'text-xs text-slate-500 mt-5'
                )
                ui.element('div').classes('stat-bottom-line mt-4')

            # Teams Stat
            with ui.card().classes('stat-card'):
                with ui.row().classes('w-full items-start justify-between'):
                    with ui.column().classes('gap-2'):
                        ui.label('إجمالي الفرق').classes('stat-label')
                        ui.label(str(teams_count)).classes('stat-value')
                    with ui.element('div').classes(
                        'stat-icon-wrapper bg-emerald-100 text-emerald-600'
                    ):
                        ui.icon('diversity_3').classes('text-3xl')
                ui.label('الفرق المسجلة').classes(
                    'text-xs text-slate-500 mt-5'
                )
                ui.element('div').classes('stat-bottom-line mt-4')

            # Subscriptions Stat
            with ui.card().classes('stat-card'):
                with ui.row().classes('w-full items-start justify-between'):
                    with ui.column().classes('gap-2'):
                        ui.label('اشتراكات اللاعبين').classes('stat-label')
                        ui.label(str(subscriptions_count)).classes(
                            'stat-value'
                        )
                    with ui.element('div').classes(
                        'stat-icon-wrapper bg-amber-100 text-amber-600'
                    ):
                        ui.icon('how_to_reg').classes('text-3xl')
                ui.label('الارتباطات الحالية').classes(
                    'text-xs text-slate-500 mt-5'
                )
                ui.element('div').classes('stat-bottom-line mt-4')

            # Tournaments Stat
            with ui.card().classes('stat-card'):
                with ui.row().classes('w-full items-start justify-between'):
                    with ui.column().classes('gap-2'):
                        ui.label('البطولات').classes('stat-label')
                        ui.label(str(tournaments_count)).classes('stat-value')
                    with ui.element('div').classes(
                        'stat-icon-wrapper bg-purple-100 text-purple-600'
                    ):
                        ui.icon('emoji_events').classes('text-3xl')
                ui.label('المشاركات الرسمية').classes(
                    'text-xs text-slate-500 mt-5'
                )
                ui.element('div').classes('stat-bottom-line mt-4')

        # SECONDARY STATS (Sports, Medical, Memberships)
        with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-3 gap-5'):

            # Sports
            with ui.card().classes(
                'section-card p-7 flex flex-col justify-center items-center text-center'
            ):
                with ui.element('div').classes(
                    'section-icon bg-blue-50 text-blue-600 mb-4'
                ):
                    ui.icon('sports').classes('text-2xl')
                ui.label('الرياضات المدرجة').classes('section-title')
                ui.label(str(sports_count)).classes(
                    'text-5xl font-black text-slate-800 mt-2'
                )
                ui.label('أنواع الرياضات المرتبطة بفرق النادي').classes(
                    'section-subtitle mt-2'
                )

            # Medical States
            with ui.card().classes('section-card p-6'):
                with ui.row().classes('items-center gap-3 mb-6'):
                    with ui.element('div').classes(
                        'section-icon bg-emerald-50 text-emerald-600'
                    ):
                        ui.icon('medical_information').classes('text-xl')
                    with ui.column().classes('gap-0'):
                        ui.label('الكشوفات الطبية').classes('section-title')
                        ui.label('الحالة الصحية للاعبين').classes(
                            'section-subtitle'
                        )

                if medical_states:
                    with ui.column().classes('w-full gap-1'):
                        for state in medical_states:
                            state_name = (
                                state['MedicalReportStateNameAR'] or 'غير محدد'
                            )
                            state_count = state['Count'] or 0
                            with ui.row().classes(
                                'w-full justify-between items-center px-2 py-2'
                            ):
                                ui.label(state_name).classes(
                                    'text-slate-700 font-medium text-sm'
                                )
                                ui.label(str(state_count)).classes(
                                    'number-badge'
                                )
                else:
                    with ui.column().classes(
                        'w-full items-center justify-center py-6'
                    ):
                        ui.icon('medical_information').classes(
                            'text-4xl text-slate-400'
                        )
                        ui.label('لا توجد بيانات طبية').classes(
                            'text-slate-500 text-sm mt-2'
                        )

            # Membership States
            with ui.card().classes('section-card p-6'):
                with ui.row().classes('items-center gap-3 mb-6'):
                    with ui.element('div').classes(
                        'section-icon bg-amber-50 text-amber-600'
                    ):
                        ui.icon('card_membership').classes('text-xl')
                    with ui.column().classes('gap-0'):
                        ui.label('حالة العضويات').classes('section-title')
                        ui.label('موقف العضويات الحالية').classes(
                            'section-subtitle'
                        )

                if membership_states:
                    with ui.column().classes('w-full gap-1'):
                        for state in membership_states:
                            state_name = (
                                state['MembershipStatusNameAR'] or 'غير محدد'
                            )
                            state_count = state['Count'] or 0
                            with ui.row().classes(
                                'w-full justify-between items-center px-2 py-2'
                            ):
                                ui.label(state_name).classes(
                                    'text-slate-700 font-medium text-sm'
                                )
                                ui.label(str(state_count)).classes(
                                    'number-badge'
                                )
                else:
                    with ui.column().classes(
                        'w-full items-center justify-center py-6'
                    ):
                        ui.icon('person_off').classes(
                            'text-4xl text-slate-400'
                        )
                        ui.label('لا توجد بيانات عضويات').classes(
                            'text-slate-500 text-sm mt-2'
                        )

        # TEAMS & PLAYERS LISTS
        with ui.row().classes('w-full grid grid-cols-1 lg:grid-cols-2 gap-5'):

            # Teams List
            with ui.card().classes('section-card p-0 overflow-hidden'):
                with ui.row().classes(
                    'w-full items-center justify-between p-5 bg-white/50 border-b border-slate-100'
                ):
                    with ui.row().classes('items-center gap-3'):
                        with ui.element('div').classes(
                            'section-icon bg-indigo-50 text-indigo-600'
                        ):
                            ui.icon('groups').classes('text-xl')
                        with ui.column().classes('gap-0'):
                            ui.label('قائمة الفرق').classes('section-title')
                            ui.label('الفرق التابعة للنادي').classes(
                                'section-subtitle'
                            )
                    ui.label(f'{teams_count} فريق').classes(
                        'bg-white text-slate-600 border border-slate-200 px-4 py-1 rounded-full text-xs font-bold'
                    )

                with ui.column().classes(
                    'w-full p-4 gap-1 h-96 overflow-y-auto'
                ):
                    if teams:
                        for team in teams:
                            team_name = (
                                team['TeamAR']
                                or team['TeamEN']
                                or 'فريق غير مسمى'
                            )
                            team_category = (
                                team['TeamCategoryNameAR'] or 'فئة غير محددة'
                            )
                            sport_name = (
                                team['SportNameAR'] or 'رياضة غير محددة'
                            )
                            player_count = team['PlayerCount'] or 0

                            with ui.row().classes(
                                'list-item items-center justify-between'
                            ):
                                with ui.row().classes('items-center gap-4'):
                                    with ui.element('div').classes(
                                        'item-avatar bg-indigo-50 text-indigo-500'
                                    ):
                                        ui.icon('sports_soccer').classes(
                                            'text-xl'
                                        )
                                    with ui.column().classes('gap-0'):
                                        ui.label(team_name).classes(
                                            'font-bold text-slate-800 text-sm'
                                        )
                                        ui.label(
                                            f'{sport_name} • {team_category}'
                                        ).classes(
                                            'text-xs text-slate-500 mt-1'
                                        )
                                with ui.column().classes('items-end gap-1'):
                                    ui.label(str(player_count)).classes(
                                        'font-black text-slate-700 text-lg'
                                    )
                                    ui.label('لاعب').classes(
                                        'text-xs text-slate-400'
                                    )
                    else:
                        with ui.column().classes(
                            'w-full h-full items-center justify-center py-12'
                        ):
                            ui.icon('groups').classes(
                                'text-5xl text-slate-300 mb-2'
                            )
                            ui.label('لا توجد فرق مسجلة').classes(
                                'text-slate-500 text-sm font-medium'
                            )

            # Latest Players List
            with ui.card().classes('section-card p-0 overflow-hidden'):
                with ui.row().classes(
                    'w-full items-center justify-between p-5 bg-white/50 border-b border-slate-100'
                ):
                    with ui.row().classes('items-center gap-3'):
                        with ui.element('div').classes(
                            'section-icon bg-sky-50 text-sky-600'
                        ):
                            ui.icon('person_add').classes('text-xl')
                        with ui.column().classes('gap-0'):
                            ui.label('أحدث اللاعبين').classes('section-title')
                            ui.label('آخر اللاعبين المضافين').classes(
                                'section-subtitle'
                            )
                    ui.label('أحدث 8').classes(
                        'bg-white text-slate-600 border border-slate-200 px-4 py-1 rounded-full text-xs font-bold'
                    )

                with ui.column().classes(
                    'w-full p-4 gap-1 h-96 overflow-y-auto'
                ):
                    if latest_players:
                        for player in latest_players:
                            player_name = (
                                player['PlayerNameAR'] or 'لاعب غير مسمى'
                            )
                            membership_status = (
                                player['MembershipStatusNameAR']
                                or 'عضوية غير محددة'
                            )
                            medical_status = (
                                player['MedicalReportStateNameAR']
                                or 'حالة طبية غير محددة'
                            )

                            with ui.row().classes(
                                'list-item items-center justify-between'
                            ):
                                with ui.row().classes('items-center gap-4'):
                                    with ui.element('div').classes(
                                        'item-avatar bg-sky-50 text-sky-500'
                                    ):
                                        ui.icon('person').classes('text-xl')
                                    with ui.column().classes('gap-0'):
                                        ui.label(player_name).classes(
                                            'font-bold text-slate-800 text-sm'
                                        )
                                        ui.label(
                                            f'{membership_status} • {medical_status}'
                                        ).classes(
                                            'text-xs text-slate-500 mt-1'
                                        )
                                ui.icon(
                                    'chevron_left', size='20px'
                                ).classes('text-slate-400')
                    else:
                        with ui.column().classes(
                            'w-full h-full items-center justify-center py-12'
                        ):
                            ui.icon('person_off').classes(
                                'text-5xl text-slate-300 mb-2'
                            )
                            ui.label('لا يوجد لاعبين مضافين مؤخراً').classes(
                                'text-slate-500 text-sm font-medium'
                            )