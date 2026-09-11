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
        'سيراميكا كليوباترا': 'https://assets.footylogos.com/logos/ceramica-cleopatra-fc/ceramica-cleopatra-fc-logo-footylogos.png',
        'الجونة': 'https://assets.footylogos.com/logos/el-gouna-fc/el-gouna-fc-logo-footylogos.png',
        'طلائع الجيش': 'https://assets.footylogos.com/logos/talaea-el-geish/talaea-el-geish-logo-footylogos.png',
        'مودرن سبورت': 'https://assets.footylogos.com/logos/modern-sport/modern-sport-logo-footylogos.png',
        'زد': 'https://assets.footylogos.com/logos/zed-fc/zed-fc-logo-footylogos.png',
        'المقاولون العرب': 'https://assets.footylogos.com/logos/el-mokawloon/el-mokawloon-logo-footylogos.png',
        'وادي دجلة': 'https://assets.footylogos.com/logos/wadi-degla-sc/wadi-degla-sc-logo-footylogos.png',
        'غزل المحلة': 'https://assets.footylogos.com/logos/ghazl-el-mahalla/ghazl-el-mahalla-logo-footylogos.png',
        'فاركو': 'https://assets.footylogos.com/logos/pharco-fc/pharco-fc-logo-footylogos.png',
        'حرس الحدود': 'https://assets.footylogos.com/logos/harras-hodoud/harras-hodoud-logo-footylogos.png',
        'بتروجيت': 'https://assets.footylogos.com/logos/petrojet-fc/petrojet-fc-logo-footylogos.png',
        'كهرباء الإسماعيلية': None,
    }
    return logos.get((club_name or '').strip())


def content(club_id=None):

    # =========================================================
    # جلب الأندية
    # =========================================================
    clubs = db.fetch_all(
        """
        SELECT
            c.Id,
            c.ClubNameAR,
            c.ClubNameEN
        FROM Club c
        ORDER BY c.Id
        """
    )

    # =========================================================
    # CSS
    # =========================================================
    ui.add_head_html(
        '''
        <style>
            .clubs-page {
    min-height: 100vh;
    width: 100%;
    background:
        radial-gradient(
            circle at top right,
            rgba(184,159,122,.14),
            transparent 28%
        ),
        radial-gradient(
            circle at bottom left,
            rgba(232,220,200,.28),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #F7F3EC 0%,
            #E8DCC8 100%
        );
}

            .hero {
                width: 100%;
                background:
                    linear-gradient(
                        135deg,
                        #0f172a 0%,
                        #1e293b 55%,
                        #1e3a8a 100%
                    );
                border-radius: 28px;
                box-shadow: 0 20px 45px rgba(15,23,42,.15);
                position: relative;
                overflow: hidden;
            }

            .hero::before {
                content: "";
                position: absolute;
                width: 260px;
                height: 260px;
                border-radius: 50%;
                right: -90px;
                top: -120px;
                background: rgba(255,255,255,.06);
            }

            .hero::after {
                content: "";
                position: absolute;
                width: 190px;
                height: 190px;
                border-radius: 50%;
                left: 25%;
                bottom: -120px;
                background: rgba(245,158,11,.08);
            }

            .club-card {
                width: 300px;
                min-height: 385px;
                background: rgba(255,255,255,.98);
                border: 1px solid #e2e8f0;
                border-radius: 24px;
                box-shadow: 0 8px 25px rgba(15,23,42,.06);
                position: relative;
                overflow: hidden;
            }

            .club-card::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 5px;
                background:
                    linear-gradient(
                        90deg,
                        #0f172a,
                        #1e3a8a,
                        #f59e0b
                    );
            }

            .club-logo {
                width: 92px;
                height: 92px;
                border-radius: 26px;
                background:
                    linear-gradient(
                        135deg,
                        #0f172a,
                        #1e293b
                    );
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 10px 25px rgba(15,23,42,.16);
                overflow: hidden;
            }

            .club-logo img {
                width: 76px;
                height: 76px;
                object-fit: contain;
            }

            .club-name {
                color: #0f172a;
                font-size: 20px;
                font-weight: 900;
                text-align: center;
                line-height: 1.5;
            }

            .club-name-en {
                color: #94a3b8;
                font-size: 11px;
                font-weight: 650;
                text-align: center;
            }

            .club-id {
                color: #cbd5e1;
                font-size: 9px;
                font-weight: 700;
            }

            .stats-grid {
                width: 100%;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 8px;
            }

            .stat-box {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 13px;
                padding: 9px 10px;
                width: 100%;
            }

            .stat-number {
                color: #0f172a;
                font-size: 17px;
                font-weight: 950;
                line-height: 1;
            }

            .stat-label {
                color: #94a3b8;
                font-size: 9px;
                font-weight: 750;
                margin-top: 4px;
            }

            .stat-icon {
                width: 29px;
                height: 29px;
                border-radius: 9px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .view-only {
                width: 100%;
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 9px;
            }

            .summary-card {
                width: 100%;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
                padding: 17px 20px;
                box-shadow: 0 6px 18px rgba(15,23,42,.04);
            }

            .summary-number {
                color: #0f172a;
                font-size: 22px;
                font-weight: 950;
            }

            .summary-label {
                color: #64748b;
                font-size: 11px;
                font-weight: 750;
            }

            .section-title {
                color: #0f172a;
                font-size: 21px;
                font-weight: 900;
            }

            .empty-card {
                width: 100%;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 24px;
                box-shadow: 0 8px 25px rgba(15,23,42,.05);
            }

            @media (max-width: 700px) {
                .hero {
                    padding: 22px !important;
                    border-radius: 21px;
                }
                .hero-title {
                    font-size: 25px !important;
                }
                .club-card {
                    width: 100%;
                    max-width: 350px;
                }
            }
        </style>
        '''
    )

    # =========================================================
    # إجماليات النظام
    # =========================================================
    total_teams_row = db.fetch_one("SELECT COUNT(*) AS Count FROM Team")
    total_players_row = db.fetch_one("SELECT COUNT(*) AS Count FROM Player")
    total_tournaments_row = db.fetch_one(
        "SELECT COUNT(*) AS Count FROM Tournament"
    )

    total_teams = total_teams_row['Count'] if total_teams_row else 0
    total_players = total_players_row['Count'] if total_players_row else 0
    total_tournaments = (
        total_tournaments_row['Count'] if total_tournaments_row else 0
    )

    # =========================================================
    # PAGE
    # =========================================================
    with ui.column().classes('clubs-page w-full p-4 md:p-6 lg:p-8 gap-6'):

        with ui.column().classes('w-full max-w-[1550px] mx-auto gap-6'):

            # =================================================
            # HERO
            # =================================================
            with ui.element('div').classes('hero w-full p-6 md:p-8'):
                with ui.row().classes(
                    'w-full items-center justify-between relative z-10 gap-5 flex-wrap'
                ):
                    with ui.column().classes('gap-1'):
                        ui.label('جميع الأندية').classes(
                            'text-3xl md:text-4xl font-black text-white'
                        )
                        ui.label(
                            'نظرة عامة على الأندية الموجودة في النظام'
                        ).classes('text-white/75 text-base md:text-lg mt-1')
                        ui.label('Egypt Football Club Management System').classes(
                            'text-white/45 text-xs mt-2'
                        )

                    with ui.row().classes('items-center gap-2'):
                        with ui.element('div').classes(
                            'bg-white/10 border border-white/15 rounded-full px-4 py-2'
                        ):
                            ui.label(f'{len(clubs)} نادي').classes(
                                'text-white text-xs font-black'
                            )

            # =================================================
            # SUMMARY
            # =================================================
            with ui.row().classes(
                'w-full grid grid-cols-2 md:grid-cols-4 gap-4'
            ):
                summary_data = [
                    (
                        len(clubs),
                        'الأندية',
                        'account_balance',
                        'bg-blue-50',
                        'text-blue-600',
                    ),
                    (
                        total_teams,
                        'الفرق',
                        'groups',
                        'bg-emerald-50',
                        'text-emerald-600',
                    ),
                    (
                        total_players,
                        'اللاعبين',
                        'person',
                        'bg-amber-50',
                        'text-amber-600',
                    ),
                    (
                        total_tournaments,
                        'البطولات',
                        'emoji_events',
                        'bg-purple-50',
                        'text-purple-600',
                    ),
                ]

                for (
                    number,
                    label,
                    icon,
                    bg_color,
                    text_color,
                ) in summary_data:
                    with ui.element('div').classes('summary-card'):
                        with ui.row().classes(
                            'w-full items-center justify-between'
                        ):
                            with ui.element('div').classes(
                                f'w-10 h-10 rounded-xl {bg_color} flex items-center justify-center'
                            ):
                                ui.icon(icon).classes(
                                    f'{text_color} text-lg'
                                )

                            with ui.column().classes('items-end gap-0'):
                                ui.label(str(number)).classes(
                                    'summary-number'
                                )
                                ui.label(label).classes('summary-label')

            # =================================================
            # SECTION HEADER
            # =================================================
            with ui.row().classes(
                'w-full items-center justify-between flex-wrap gap-3'
            ):
                with ui.row().classes('items-center gap-3'):
                    with ui.element('div').classes(
                        'w-11 h-11 rounded-xl bg-blue-50 flex items-center justify-center'
                    ):
                        ui.icon('groups').classes('text-xl text-blue-700')

                    with ui.column().classes('gap-0'):
                        ui.label('الأندية الموجودة').classes('section-title')
                        ui.label('معلومات وإحصائيات كل نادي').classes(
                            'text-xs text-slate-400 font-semibold'
                        )

                ui.label(f'{len(clubs)} نادي').classes(
                    'bg-white border border-slate-200 px-4 py-2 rounded-full text-xs font-black text-slate-600'
                )

            # =================================================
            # CLUBS
            # =================================================
            if not clubs:
                with ui.column().classes(
                    'empty-card items-center justify-center p-14'
                ):
                    ui.icon('sports_soccer').classes('text-7xl text-slate-300')
                    ui.label('لا توجد أندية').classes(
                        'text-2xl font-black text-slate-600 mt-5'
                    )
                    ui.label('لا توجد بيانات في جدول Club').classes(
                        'text-slate-400 text-sm mt-2'
                    )
            else:
                with ui.row().classes('w-full justify-center flex-wrap gap-6'):
                    for club in clubs:
                        club_id_value = club['Id']
                        club_name_ar = club['ClubNameAR'] or 'بدون اسم'
                        club_name_en = club['ClubNameEN'] or ''
                        logo_url = get_club_logo_url(club_name_ar)

                        # =====================================
                        # Club statistics
                        # =====================================
                        team_row = db.fetch_one(
                            """
                            SELECT COUNT(*) AS Count
                            FROM Team
                            WHERE Clubid = ?
                            """,
                            (club_id_value,),
                        )

                        player_row = db.fetch_one(
                            """
                            SELECT COUNT(*) AS Count
                            FROM Player
                            WHERE ClubId = ?
                            """,
                            (club_id_value,),
                        )

                        sport_row = db.fetch_one(
                            """
                            SELECT COUNT(DISTINCT Sportid) AS Count
                            FROM Team
                            WHERE Clubid = ?
                            """,
                            (club_id_value,),
                        )

                        tournament_row = db.fetch_one(
                            """
                            SELECT COUNT(DISTINCT tt.TournamentId) AS Count
                            FROM TournamentTable tt
                            INNER JOIN Team t
                                ON t.Id = tt.Teamid
                            WHERE t.Clubid = ?
                            """,
                            (club_id_value,),
                        )

                        team_count = team_row['Count'] if team_row else 0
                        player_count = player_row['Count'] if player_row else 0
                        sport_count = sport_row['Count'] if sport_row else 0
                        tournament_count = (
                            tournament_row['Count'] if tournament_row else 0
                        )

                        # =====================================
                        # Card
                        # =====================================
                        with ui.element('div').classes('club-card'):
                            with ui.column().classes(
                                'w-full h-full items-center p-6'
                            ):

                                # =============================
                                # Logo
                                # =============================
                                with ui.element('div').classes('club-logo'):
                                    if logo_url:
                                        ui.image(logo_url).props(
                                            'fit=contain'
                                        ).classes('w-[76px] h-[76px]')
                                    else:
                                        ui.icon('sports_soccer').classes(
                                            'text-4xl text-slate-400'
                                        )

                                # =============================
                                # Name
                                # =============================
                                ui.label(club_name_ar).classes('club-name mt-4')

                                if club_name_en:
                                    ui.label(club_name_en).classes(
                                        'club-name-en mt-1'
                                    )

                                ui.label(f'Club ID: {club_id_value}').classes(
                                    'club-id mt-2'
                                )

                                # =============================
                                # Statistics
                                # =============================
                                with ui.element('div').classes(
                                    'stats-grid mt-5'
                                ):

                                    # Teams
                                    with ui.element('div').classes('stat-box'):
                                        with ui.row().classes(
                                            'items-center justify-between'
                                        ):
                                            with ui.element('div').classes(
                                                'stat-icon bg-blue-50'
                                            ):
                                                ui.icon('groups').classes(
                                                    'text-blue-600 text-sm'
                                                )
                                            ui.label(str(team_count)).classes(
                                                'stat-number'
                                            )
                                        ui.label('الفرق').classes('stat-label')

                                    # Players
                                    with ui.element('div').classes('stat-box'):
                                        with ui.row().classes(
                                            'items-center justify-between'
                                        ):
                                            with ui.element('div').classes(
                                                'stat-icon bg-emerald-50'
                                            ):
                                                ui.icon('person').classes(
                                                    'text-emerald-600 text-sm'
                                                )
                                            ui.label(str(player_count)).classes(
                                                'stat-number'
                                            )
                                        ui.label('اللاعبين').classes(
                                            'stat-label'
                                        )

                                    # Sports
                                    with ui.element('div').classes('stat-box'):
                                        with ui.row().classes(
                                            'items-center justify-between'
                                        ):
                                            with ui.element('div').classes(
                                                'stat-icon bg-amber-50'
                                            ):
                                                ui.icon('sports').classes(
                                                    'text-amber-600 text-sm'
                                                )
                                            ui.label(str(sport_count)).classes(
                                                'stat-number'
                                            )
                                        ui.label('الرياضات').classes(
                                            'stat-label'
                                        )

                                    # Tournaments
                                    with ui.element('div').classes('stat-box'):
                                        with ui.row().classes(
                                            'items-center justify-between'
                                        ):
                                            with ui.element('div').classes(
                                                'stat-icon bg-purple-50'
                                            ):
                                                ui.icon(
                                                    'emoji_events'
                                                ).classes(
                                                    'text-purple-600 text-sm'
                                                )
                                            ui.label(
                                                str(tournament_count)
                                            ).classes('stat-number')
                                        ui.label('البطولات').classes(
                                            'stat-label'
                                        )

                                # =============================
                                # Status
                                # =============================
                               