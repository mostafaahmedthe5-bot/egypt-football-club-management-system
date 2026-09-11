from nicegui import ui, app
import database as db


def content():
    # =========================================================
    # جلب الأندية
    # =========================================================

    clubs = db.fetch_all(
        """
        SELECT
            Id,
            ClubNameAR,
            ClubNameEN
        FROM Club
        ORDER BY Id
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
                background: #f8fafc;
                direction: rtl;
            }

            .clubs-wrapper {
                width: 100%;
                max-width: 1550px;
                margin: 0 auto;
            }

            .hero {
                width: 100%;
                background: #B8755D;
                border-radius: 28px;
                padding: 30px;
                box-shadow: 0 14px 35px rgba(15,23,42,.12);
                position: relative;
                overflow: hidden;
            }

            .hero-title {
                color: white;
                font-size: 32px;
                font-weight: 950;
            }

            .hero-subtitle {
                color: rgba(255,255,255,.78);
                font-size: 14px;
                font-weight: 650;
            }

            .hero-season {
                color: #fff7ed;
                font-size: 13px;
                font-weight: 850;
            }

            .hero-icon {
                width: 82px;
                height: 82px;
                border-radius: 24px;
                background: rgba(255,255,255,.12);
                border: 1px solid rgba(255,255,255,.18);
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .hero-badge {
                display: inline-flex;
                align-items: center;
                gap: 7px;
                padding: 9px 14px;
                border-radius: 999px;
                background: rgba(255,255,255,.10);
                border: 1px solid rgba(255,255,255,.15);
                color: white;
                font-size: 11px;
                font-weight: 800;
            }

            .section-title {
                color: #0f172a;
                font-size: 21px;
                font-weight: 950;
            }

            .section-subtitle {
                color: #94a3b8;
                font-size: 11px;
                font-weight: 650;
            }

            .summary-card {
                width: 100%;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
                padding: 18px 20px;
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

            .club-card {
                width: 310px;
                min-height: 320px;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 24px;
                box-shadow: 0 8px 25px rgba(15,23,42,.055);
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }

            .club-card-top {
                width: 100%;
                height: 6px;
                background: #B8755D;
            }

            .club-logo {
                width: 82px;
                height: 82px;
                border-radius: 22px;
                background: #0f172a;
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .club-name {
                color: #0f172a;
                font-size: 20px;
                font-weight: 950;
                text-align: center;
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

            .club-stat {
                width: 112px;
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 13px;
                padding: 9px 10px;
            }

            .club-stat-number {
                color: #0f172a;
                font-size: 17px;
                font-weight: 950;
            }

            .club-stat-label {
                color: #94a3b8;
                font-size: 9px;
                font-weight: 750;
            }

            .club-stat-icon {
                width: 30px;
                height: 30px;
                border-radius: 9px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .login-line {
                width: 100%;
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 13px;
                padding: 10px 13px;
            }

            .empty-card {
                width: 100%;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 24px;
                padding: 60px;
            }

            @media (max-width: 700px) {

                .hero {
                    padding: 22px;
                    border-radius: 21px;
                }

                .hero-title {
                    font-size: 24px;
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
    # إحصائيات عامة
    # =========================================================

    total_clubs = len(clubs)

    total_teams_row = db.fetch_one(
        """
        SELECT COUNT(*) AS Count
        FROM Team
        """
    )

    total_players_row = db.fetch_one(
        """
        SELECT COUNT(*) AS Count
        FROM Player
        """
    )

    total_tournaments_row = db.fetch_one(
        """
        SELECT COUNT(*) AS Count
        FROM Tournament
        """
    )

    total_teams = (
        total_teams_row['Count']
        if total_teams_row
        else 0
    )

    total_players = (
        total_players_row['Count']
        if total_players_row
        else 0
    )

    total_tournaments = (
        total_tournaments_row['Count']
        if total_tournaments_row
        else 0
    )

    # =========================================================
    # PAGE
    # =========================================================

    with ui.column().classes(
        'clubs-page w-full p-4 md:p-6 lg:p-8'
    ):

        with ui.column().classes(
            'clubs-wrapper gap-6'
        ):

            # =================================================
            # HERO
            # =================================================

            with ui.element('div').classes(
                'hero'
            ):

                with ui.row().classes(
                    'w-full items-center justify-between gap-5 flex-wrap'
                ):

                    with ui.row().classes(
                        'items-center gap-4'
                    ):

                        with ui.element('div').classes(
                            'hero-icon'
                        ):

                            ui.icon(
                                'sports_soccer'
                            ).classes(
                                'text-4xl text-white'
                            )

                        with ui.column().classes(
                            'gap-1'
                        ):

                            ui.label(
                                'أندية كرة القدم'
                            ).classes(
                                'hero-title'
                            )

                            ui.label(
                                'اختر النادي للوصول إلى صفحة تسجيل الدخول'
                            ).classes(
                                'hero-subtitle'
                            )

                            ui.label(
                                'الموسم الرياضي 2026 / 2027'
                            ).classes(
                                'hero-season'
                            )

                    with ui.row().classes(
                        'items-center gap-2'
                    ):

                        with ui.element('div').classes(
                            'hero-badge'
                        ):

                            ui.icon(
                                'groups'
                            )

                            ui.label(
                                f'{total_clubs} نادي'
                            )

            # =================================================
            # SUMMARY
            # =================================================

            with ui.row().classes(
                'w-full grid grid-cols-2 md:grid-cols-4 gap-4'
            ):

                summary_items = [
                    (
                        total_clubs,
                        'الأندية',
                        'sports_soccer',
                        'bg-blue-50',
                        'text-blue-600'
                    ),
                    (
                        total_teams,
                        'الفرق',
                        'groups',
                        'bg-emerald-50',
                        'text-emerald-600'
                    ),
                    (
                        total_players,
                        'اللاعبين',
                        'person',
                        'bg-amber-50',
                        'text-amber-600'
                    ),
                    (
                        total_tournaments,
                        'البطولات',
                        'emoji_events',
                        'bg-purple-50',
                        'text-purple-600'
                    )
                ]

                for number, label, icon, bg_class, text_class in summary_items:

                    with ui.element('div').classes(
                        'summary-card'
                    ):

                        with ui.row().classes(
                            'items-center justify-between'
                        ):

                            with ui.element('div').classes(
                                f'w-10 h-10 rounded-xl {bg_class} flex items-center justify-center'
                            ):

                                ui.icon(
                                    icon
                                ).classes(
                                    f'{text_class} text-lg'
                                )

                            with ui.column().classes(
                                'items-end gap-0'
                            ):

                                ui.label(
                                    str(number)
                                ).classes(
                                    'summary-number'
                                )

                                ui.label(
                                    label
                                ).classes(
                                    'summary-label'
                                )

            # =================================================
            # SECTION
            # =================================================

            with ui.row().classes(
                'w-full items-center justify-between flex-wrap gap-3'
            ):

                with ui.row().classes(
                    'items-center gap-3'
                ):

                    with ui.element('div').classes(
                        'w-11 h-11 rounded-xl bg-blue-50 flex items-center justify-center'
                    ):

                        ui.icon(
                            'account_balance'
                        ).classes(
                            'text-xl text-blue-700'
                        )

                    with ui.column().classes(
                        'gap-0'
                    ):

                        ui.label(
                            'اختيار النادي'
                        ).classes(
                            'section-title'
                        )

                        ui.label(
                            'اختر النادي الذي تريد الدخول إليه'
                        ).classes(
                            'section-subtitle'
                        )

                ui.label(
                    f'{total_clubs} نادي متاح'
                ).classes(
                    'bg-white border border-slate-200 px-4 py-2 rounded-full text-xs font-black text-slate-600'
                )

            # =================================================
            # CLUBS
            # =================================================

            if not clubs:

                with ui.column().classes(
                    'empty-card items-center justify-center'
                ):

                    ui.icon(
                        'sports_soccer'
                    ).classes(
                        'text-6xl text-slate-300'
                    )

                    ui.label(
                        'لا توجد أندية'
                    ).classes(
                        'text-2xl font-black text-slate-600 mt-5'
                    )

                    ui.label(
                        'لم يتم تسجيل أي نادي في قاعدة البيانات'
                    ).classes(
                        'text-sm text-slate-400 mt-2'
                    )

            else:

                with ui.row().classes(
                    'w-full justify-center flex-wrap gap-6'
                ):

                    for club in clubs:

                        club_id = club['Id']

                        club_name_ar = (
                            club['ClubNameAR']
                            or 'بدون اسم'
                        )

                        club_name_en = (
                            club['ClubNameEN']
                            or ''
                        )

                        # =====================================
                        # إحصائيات النادي
                        # =====================================

                        team_row = db.fetch_one(
                            """
                            SELECT COUNT(*) AS Count
                            FROM Team
                            WHERE Clubid = ?
                            """,
                            (club_id,)
                        )

                        player_row = db.fetch_one(
                            """
                            SELECT COUNT(*) AS Count
                            FROM Player
                            WHERE ClubId = ?
                            """,
                            (club_id,)
                        )

                        sport_row = db.fetch_one(
                            """
                            SELECT COUNT(DISTINCT Sportid) AS Count
                            FROM Team
                            WHERE Clubid = ?
                            """,
                            (club_id,)
                        )

                        tournament_row = db.fetch_one(
                            """
                            SELECT COUNT(DISTINCT tt.TournamentId) AS Count
                            FROM TournamentTable tt
                            INNER JOIN Team t
                                ON t.Id = tt.Teamid
                            WHERE t.Clubid = ?
                            """,
                            (club_id,)
                        )

                        team_count = (
                            team_row['Count']
                            if team_row
                            else 0
                        )

                        player_count = (
                            player_row['Count']
                            if player_row
                            else 0
                        )

                        sport_count = (
                            sport_row['Count']
                            if sport_row
                            else 0
                        )

                        tournament_count = (
                            tournament_row['Count']
                            if tournament_row
                            else 0
                        )

                        def select_club(
                            selected_club_id=club_id
                        ):

                            app.storage.user.update({
                                'selected_club_id': selected_club_id
                            })

                            ui.navigate.to('/login')

                        # =====================================
                        # CLUB CARD
                        # =====================================

                        with ui.element('div').classes(
                            'club-card'
                        ).on(
                            'click',
                            select_club
                        ):

                            ui.element(
                                'div'
                            ).classes(
                                'club-card-top'
                            )

                            with ui.column().classes(
                                'w-full items-center p-6'
                            ):

                                # Logo

                                with ui.element('div').classes(
                                    'club-logo'
                                ):

                                    ui.icon(
                                        'sports_soccer'
                                    ).classes(
                                        'text-4xl'
                                    )

                                # Name

                                ui.label(
                                    club_name_ar
                                ).classes(
                                    'club-name mt-4'
                                )

                                if club_name_en:

                                    ui.label(
                                        club_name_en
                                    ).classes(
                                        'club-name-en mt-1'
                                    )

                                ui.label(
                                    f'Club ID: {club_id}'
                                ).classes(
                                    'club-id mt-2'
                                )

                                # Stats

                                with ui.row().classes(
                                    'w-full justify-center flex-wrap gap-2 mt-5'
                                ):

                                    # Teams

                                    with ui.element('div').classes(
                                        'club-stat'
                                    ):

                                        with ui.row().classes(
                                            'items-center justify-between'
                                        ):

                                            with ui.element('div').classes(
                                                'club-stat-icon bg-blue-50'
                                            ):

                                                ui.icon(
                                                    'groups'
                                                ).classes(
                                                    'text-blue-600 text-sm'
                                                )

                                            ui.label(
                                                str(team_count)
                                            ).classes(
                                                'club-stat-number'
                                            )

                                        ui.label(
                                            'الفرق'
                                        ).classes(
                                            'club-stat-label'
                                        )

                                    # Players

                                    with ui.element('div').classes(
                                        'club-stat'
                                    ):

                                        with ui.row().classes(
                                            'items-center justify-between'
                                        ):

                                            with ui.element('div').classes(
                                                'club-stat-icon bg-emerald-50'
                                            ):

                                                ui.icon(
                                                    'person'
                                                ).classes(
                                                    'text-emerald-600 text-sm'
                                                )

                                            ui.label(
                                                str(player_count)
                                            ).classes(
                                                'club-stat-number'
                                            )

                                        ui.label(
                                            'اللاعبين'
                                        ).classes(
                                            'club-stat-label'
                                        )

                                    # Sports

                                    with ui.element('div').classes(
                                        'club-stat'
                                    ):

                                        with ui.row().classes(
                                            'items-center justify-between'
                                        ):

                                            with ui.element('div').classes(
                                                'club-stat-icon bg-amber-50'
                                            ):

                                                ui.icon(
                                                    'sports'
                                                ).classes(
                                                    'text-amber-600 text-sm'
                                                )

                                            ui.label(
                                                str(sport_count)
                                            ).classes(
                                                'club-stat-number'
                                            )

                                        ui.label(
                                            'الرياضات'
                                        ).classes(
                                            'club-stat-label'
                                        )

                                    # Tournaments

                                    with ui.element('div').classes(
                                        'club-stat'
                                    ):

                                        with ui.row().classes(
                                            'items-center justify-between'
                                        ):

                                            with ui.element('div').classes(
                                                'club-stat-icon bg-purple-50'
                                            ):

                                                ui.icon(
                                                    'emoji_events'
                                                ).classes(
                                                    'text-purple-600 text-sm'
                                                )

                                            ui.label(
                                                str(tournament_count)
                                            ).classes(
                                                'club-stat-number'
                                            )

                                        ui.label(
                                            'البطولات'
                                        ).classes(
                                            'club-stat-label'
                                        )

                                # Login

                                with ui.row().classes(
                                    'login-line items-center justify-center gap-2 mt-5'
                                ):

                                    ui.icon(
                                        'login'
                                    ).classes(
                                        'text-blue-600 text-sm'
                                    )

                                    ui.label(
                                        'اضغط للدخول إلى النادي'
                                    ).classes(
                                        'text-slate-600 text-xs font-black'
                                    )

            # =================================================
            # FOOTER
            # =================================================

            with ui.column().classes(
                'w-full items-center pt-4'
            ):

                ui.label(
                    'Egypt Football Club Management System'
                ).classes(
                    'text-slate-500 text-sm font-bold'
                )

                ui.label(
                    'نظام إدارة أندية كرة القدم'
                ).classes(
                    'text-slate-400 text-xs mt-1'
                )