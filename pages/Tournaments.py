from nicegui import ui, app
import database as db
import sqlite3


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

    club_name_ar = (
        club['ClubNameAR']
        or 'النادي'
    )

    club_name_en = (
        club['ClubNameEN']
        or ''
    )

    # =========================================================
    # CSS
    # =========================================================

    ui.add_head_html(
        '''
        <style>

            .tournaments-page {
                direction: rtl;
                min-height: 100vh;
                width: 100%;
                background: #f8fafc;
            }

            .tournaments-wrapper {
                width: 100%;
                max-width: 1550px;
                margin: 0 auto;
            }

            .tournaments-header {
                width: 100%;
                position: relative;
                overflow: hidden;
                border-radius: 24px;
                padding: 28px 30px;
                background: #B49A5A;
                border: 1px solid rgba(255,255,255,.08);
                box-shadow: 0 14px 35px rgba(15,23,42,.13);
            }

            .tournaments-header::before {
                content: "";
                position: absolute;
                width: 280px;
                height: 280px;
                top: -170px;
                left: -80px;
                border-radius: 50%;
                background: rgba(255,255,255,.035);
            }

            .tournaments-header::after {
                content: "";
                position: absolute;
                width: 300px;
                height: 300px;
                bottom: -200px;
                right: -100px;
                border-radius: 50%;
                background: rgba(56,189,248,.05);
            }

            .tournaments-header-content {
                position: relative;
                z-index: 2;
            }

            .tournaments-header-icon {
                width: 62px;
                height: 62px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 17px;
                background: rgba(255,255,255,.08);
                border: 1px solid rgba(255,255,255,.12);
            }

            .tournaments-header-title {
                color: white;
                font-size: 29px;
                font-weight: 900;
                line-height: 1.3;
            }

            .tournaments-header-club {
                color: #fff7ed;
                font-size: 19px;
                font-weight: 800;
            }

            .tournaments-header-en {
                color: #94a3b8;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            .tournaments-header-description {
                color: #cbd5e1;
                font-size: 13px;
                line-height: 1.8;
            }

            .tournaments-header-badge {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 8px 14px;
                border-radius: 999px;
                background: rgba(245,158,11,.10);
                border: 1px solid rgba(245,158,11,.18);
                color: #fef3c7;
                font-size: 11px;
                font-weight: 800;
            }

            .tournaments-header-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #fbbf24;
            }

            .tournaments-card {
                width: 100%;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 21px;
                box-shadow: 0 7px 22px rgba(15,23,42,.045);
            }

            .card-icon {
                width: 44px;
                height: 44px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 13px;
            }

            .card-title {
                color: #0f172a;
                font-size: 18px;
                font-weight: 900;
            }

            .card-subtitle {
                color: #94a3b8;
                font-size: 11px;
                font-weight: 600;
            }

            .field-label {
                color: #475569;
                font-size: 11px;
                font-weight: 850;
            }

            .tournament-field .q-field__control {
                min-height: 50px !important;
                border-radius: 13px !important;
            }

            .tournament-field input {
                font-size: 13px !important;
                font-weight: 650 !important;
            }

            .save-button {
                min-height: 51px !important;
                border-radius: 13px !important;
                background: #1d4ed8 !important;
                color: white !important;
                font-weight: 850 !important;
                padding: 0 25px !important;
            }

            .stats-grid {
                width: 100%;
            }

            .stat-card {
                width: 100%;
                min-height: 140px;
                position: relative;
                overflow: hidden;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 18px;
                box-shadow: 0 6px 20px rgba(15,23,42,.04);
            }

            .stat-card::before {
                content: "";
                position: absolute;
                top: 0;
                right: 0;
                left: 0;
                height: 3px;
                background: #e2e8f0;
            }

            .stat-blue::before {
                background: #2563eb;
            }

            .stat-emerald::before {
                background: #059669;
            }

            .stat-amber::before {
                background: #d97706;
            }

            .stat-slate::before {
                background: #475569;
            }

            .stat-icon {
                width: 50px;
                height: 50px;
                border-radius: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .stat-label {
                color: #64748b;
                font-size: 11px;
                font-weight: 800;
            }

            .stat-number {
                color: #0f172a;
                font-size: 32px;
                line-height: 1;
                font-weight: 950;
            }

            .stat-description {
                color: #94a3b8;
                font-size: 10px;
                font-weight: 600;
            }

            .filter-card {
                width: 100%;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 19px;
                box-shadow: 0 6px 18px rgba(15,23,42,.035);
            }

            .filter-field .q-field__control {
                min-height: 49px !important;
                border-radius: 13px !important;
            }

            .filter-button {
                min-height: 49px !important;
                border-radius: 13px !important;
                font-weight: 800 !important;
            }

            .list-card {
                width: 100%;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 21px;
                overflow: hidden;
                box-shadow: 0 7px 22px rgba(15,23,42,.045);
            }

            .list-header {
                background: #f8fafc;
                border-bottom: 1px solid #e2e8f0;
            }

            .count-badge {
                min-width: 75px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 6px 11px;
                border-radius: 999px;
                background: #eff6ff;
                color: #1d4ed8;
                border: 1px solid #dbeafe;
                font-size: 11px;
                font-weight: 850;
            }

            .tournament-row {
                width: 100%;
                min-height: 96px;
                background: white;
                border-bottom: 1px solid #f1f5f9;
                padding: 14px 18px;
            }

            .tournament-row:last-child {
                border-bottom: none;
            }

            .tournament-avatar {
                width: 52px;
                height: 52px;
                flex-shrink: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 15px;
                background: #0f172a;
                color: white;
            }

            .tournament-name {
                color: #0f172a;
                font-size: 14px;
                font-weight: 900;
            }

            .tournament-name-en {
                color: #94a3b8;
                font-size: 10px;
                font-weight: 600;
            }

            .tournament-id {
                color: #94a3b8;
                font-size: 9px;
                font-weight: 650;
            }

            .meta-chip {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                min-height: 31px;
                padding: 5px 10px;
                border-radius: 9px;
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                color: #475569;
                font-size: 10px;
                font-weight: 750;
            }

            .meta-chip.date {
                background: #eff6ff;
                border-color: #dbeafe;
                color: #1d4ed8;
            }

            .meta-chip.teams {
                background: #f0fdf4;
                border-color: #dcfce7;
                color: #15803d;
            }

            .meta-chip.type {
                background: #fffbeb;
                border-color: #fef3c7;
                color: #b45309;
            }

            .meta-chip.sport {
                background: #f5f3ff;
                border-color: #ede9fe;
                color: #6d28d9;
            }

            .action-button {
                width: 38px !important;
                height: 38px !important;
                border-radius: 10px !important;
                color: #475569 !important;
            }

            .delete-button {
                color: #dc2626 !important;
            }

            .team-selection-box {
                width: 100%;
                border: 1px solid #e2e8f0;
                border-radius: 15px;
                background: #f8fafc;
                padding: 12px;
            }

            .team-selection-title {
                color: #334155;
                font-size: 12px;
                font-weight: 850;
            }

            .empty-state {
                min-height: 320px;
            }

            .empty-icon-box {
                width: 84px;
                height: 84px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 23px;
                background: #f8fafc;
                border: 1px solid #e2e8f0;
            }

            .dialog-card {
                width: 760px;
                max-width: 96vw;
                border-radius: 22px;
                overflow: hidden;
                background: white;
                box-shadow: 0 20px 60px rgba(15,23,42,.18);
            }

            .dialog-header {
                padding: 22px 24px;
                background: #0f172a;
            }

            .dialog-icon {
                width: 48px;
                height: 48px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 14px;
                background: rgba(255,255,255,.08);
                border: 1px solid rgba(255,255,255,.10);
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

            .delete-dialog {
                width: 430px;
                max-width: 95vw;
                border-radius: 21px;
                padding: 26px;
            }

            .delete-icon-box {
                width: 72px;
                height: 72px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto;
                border-radius: 20px;
                background: #fef2f2;
                border: 1px solid #fecaca;
            }

            .delete-title {
                color: #0f172a;
                font-size: 21px;
                font-weight: 900;
            }

            .delete-name {
                color: #1d4ed8;
                font-size: 15px;
                font-weight: 850;
            }

            .delete-warning {
                color: #64748b;
                font-size: 11px;
                line-height: 1.8;
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 13px;
                padding: 12px;
            }

            .delete-confirm {
                background: #dc2626 !important;
                color: white !important;
                border-radius: 11px !important;
                font-weight: 850 !important;
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

            @media (max-width: 900px) {

                .tournaments-header {
                    padding: 24px;
                }

                .tournaments-header-title {
                    font-size: 25px;
                }

                .tournaments-header-club {
                    font-size: 17px;
                }

                .tournament-row {
                    padding: 14px 12px;
                }
            }

            @media (max-width: 650px) {

                .tournaments-page {
                    padding: 12px !important;
                }

                .tournaments-header {
                    padding: 20px;
                    border-radius: 18px;
                }

                .tournaments-header-title {
                    font-size: 22px;
                }

                .tournaments-header-description {
                    font-size: 11px;
                }

                .tournaments-card,
                .filter-card,
                .list-card {
                    border-radius: 17px;
                }

                .tournament-row {
                    min-height: auto;
                    border: 1px solid #e2e8f0;
                    border-radius: 14px;
                    margin-bottom: 8px;
                }

                .tournament-row:last-child {
                    border: 1px solid #e2e8f0;
                }
            }

        </style>
        '''
    )

    # =========================================================
    # PAGE
    # =========================================================

    with ui.column().classes(
        'tournaments-page w-full p-4 md:p-6 lg:p-8'
    ):

        with ui.column().classes(
            'tournaments-wrapper gap-6'
        ):

            # =================================================
            # HEADER
            # =================================================

            with ui.element('div').classes(
                'tournaments-header'
            ):

                with ui.row().classes(
                    'tournaments-header-content w-full items-center justify-between flex-wrap gap-6'
                ):

                    with ui.row().classes(
                        'items-center gap-4'
                    ):

                        with ui.element('div').classes(
                            'tournaments-header-icon'
                        ):

                            ui.icon(
                                'emoji_events'
                            ).classes(
                                'text-3xl text-white'
                            )

                        with ui.column().classes('gap-1'):

                            ui.label(
                                'إدارة البطولات'
                            ).classes(
                                'tournaments-header-title'
                            )

                            ui.label(
                                club_name_ar
                            ).classes(
                                'tournaments-header-club'
                            )

                    with ui.element('div').classes(
                        'tournaments-header-badge'
                    ):

                        ui.element('span').classes(
                            'tournaments-header-dot'
                        )

                        ui.label(
                            'Tournament Management'
                        )

            # =================================================
            # STATISTICS
            # =================================================

            tournament_stats = db.fetch_one(
                """
                SELECT
                    COUNT(DISTINCT t.Id) AS TournamentCount,
                    COUNT(DISTINCT tt.Teamid) AS TeamParticipationCount
                FROM Tournament t
                INNER JOIN TournamentTable tt
                    ON tt.TournamentId = t.Id
                INNER JOIN Team tm
                    ON tm.Id = tt.Teamid
                WHERE tm.Clubid = ?
                """,
                (club_id,)
            )

            total_tournaments = db.fetch_one(
                """
                SELECT
                    COUNT(DISTINCT t.Id) AS Count
                FROM Tournament t
                WHERE EXISTS (
                    SELECT 1
                    FROM TournamentTable tt
                    INNER JOIN Team tm
                        ON tm.Id = tt.Teamid
                    WHERE tt.TournamentId = t.Id
                    AND tm.Clubid = ?
                )
                """,
                (club_id,)
            )

            tournaments_count = (
                total_tournaments['Count']
                if total_tournaments
                else 0
            )

            participation_count = (
                tournament_stats['TeamParticipationCount']
                if tournament_stats
                else 0
            )

            team_count_row = db.fetch_one(
                """
                SELECT
                    COUNT(*) AS Count
                FROM Team
                WHERE Clubid = ?
                """,
                (club_id,)
            )

            club_teams_count = (
                team_count_row['Count']
                if team_count_row
                else 0
            )

            current_year = datetime_year()

            with ui.row().classes(
                'w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 stats-grid'
            ):

                with ui.card().classes(
                    'stat-card stat-blue p-5'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):

                        with ui.column().classes('gap-2'):

                            ui.label(
                                'البطولات'
                            ).classes(
                                'stat-label'
                            )

                            ui.label(
                                str(tournaments_count)
                            ).classes(
                                'stat-number'
                            )

                        with ui.element('div').classes(
                            'stat-icon bg-blue-50'
                        ):

                            ui.icon(
                                'emoji_events'
                            ).classes(
                                'text-2xl text-blue-600'
                            )

                    ui.label(
                        'البطولات المرتبطة بالنادي'
                    ).classes(
                        'stat-description mt-4'
                    )

                with ui.card().classes(
                    'stat-card stat-emerald p-5'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):

                        with ui.column().classes('gap-2'):

                            ui.label(
                                'مشاركات الفرق'
                            ).classes(
                                'stat-label'
                            )

                            ui.label(
                                str(participation_count)
                            ).classes(
                                'stat-number'
                            )

                        with ui.element('div').classes(
                            'stat-icon bg-emerald-50'
                        ):

                            ui.icon(
                                'groups'
                            ).classes(
                                'text-2xl text-emerald-600'
                            )

                    ui.label(
                        'عدد مشاركات الفرق'
                    ).classes(
                        'stat-description mt-4'
                    )

                with ui.card().classes(
                    'stat-card stat-amber p-5'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):

                        with ui.column().classes('gap-2'):

                            ui.label(
                                'فرق النادي'
                            ).classes(
                                'stat-label'
                            )

                            ui.label(
                                str(club_teams_count)
                            ).classes(
                                'stat-number'
                            )

                        with ui.element('div').classes(
                            'stat-icon bg-amber-50'
                        ):

                            ui.icon(
                                'account_tree'
                            ).classes(
                                'text-2xl text-amber-600'
                            )

                    ui.label(
                        'الفرق المتاحة للمشاركة'
                    ).classes(
                        'stat-description mt-4'
                    )

                with ui.card().classes(
                    'stat-card stat-slate p-5'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):

                        with ui.column().classes('gap-2'):

                            ui.label(
                                'السنة الحالية'
                            ).classes(
                                'stat-label'
                            )

                            ui.label(
                                str(current_year)
                            ).classes(
                                'stat-number'
                            )

                        with ui.element('div').classes(
                            'stat-icon bg-slate-100'
                        ):

                            ui.icon(
                                'calendar_month'
                            ).classes(
                                'text-2xl text-slate-600'
                            )

                    ui.label(
                        'العام الحالي'
                    ).classes(
                        'stat-description mt-4'
                    )

            # =================================================
            # ADD TOURNAMENT
            # =================================================

            sports = db.fetch_all(
                """
                SELECT
                    Id,
                    SportNameAR,
                    SportNameEN
                FROM Sport
                ORDER BY Id
                """
            )

            sport_options = {}

            for sport in sports:
                sport_options[sport['Id']] = (
                    sport['SportNameAR']
                    or sport['SportNameEN']
                    or 'رياضة'
                )

            tournament_types = {
                'محلية': 'محلية',
                'إفريقية': 'إفريقية',
                'عربية': 'عربية',
                'دولية': 'دولية'
            }

            with ui.card().classes(
                'tournaments-card p-5 md:p-6'
            ):

                with ui.row().classes(
                    'items-center gap-3 mb-6'
                ):

                    with ui.element('div').classes(
                        'card-icon bg-amber-50 text-amber-600'
                    ):

                        ui.icon(
                            'add_circle'
                        ).classes(
                            'text-xl'
                        )

                    with ui.column().classes('gap-0'):

                        ui.label(
                            'إضافة بطولة جديدة'
                        ).classes(
                            'card-title'
                        )

                        ui.label(
                            'أدخل بيانات البطولة ثم حدد الفرق المشاركة'
                        ).classes(
                            'card-subtitle mt-1'
                        )

                with ui.row().classes(
                    'w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'
                ):

                    with ui.column().classes('gap-2'):

                        ui.label(
                            'اسم البطولة بالعربي *'
                        ).classes(
                            'field-label'
                        )

                        tournament_name_ar = ui.input(
                            placeholder='مثال: الدوري المصري الممتاز'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'tournament-field w-full'
                        )

                    with ui.column().classes('gap-2'):

                        ui.label(
                            'اسم البطولة بالإنجليزي'
                        ).classes(
                            'field-label'
                        )

                        tournament_name_en = ui.input(
                            placeholder='Example: Egyptian Premier League'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'tournament-field w-full'
                        )

                    with ui.column().classes('gap-2'):

                        ui.label(
                            'الرياضة *'
                        ).classes(
                            'field-label'
                        )

                        tournament_sport = ui.select(
                            sport_options,
                            label='اختر الرياضة'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'tournament-field w-full'
                        )

                with ui.row().classes(
                    'w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4'
                ):

                    with ui.column().classes('gap-2'):

                        ui.label(
                            'تاريخ البداية *'
                        ).classes(
                            'field-label'
                        )

                        tournament_start_date = ui.input(
                            placeholder='YYYY-MM-DD'
                        ).props(
                            'outlined rounded type=date'
                        ).classes(
                            'tournament-field w-full'
                        )

                    with ui.column().classes('gap-2'):

                        ui.label(
                            'تاريخ النهاية *'
                        ).classes(
                            'field-label'
                        )

                        tournament_end_date = ui.input(
                            placeholder='YYYY-MM-DD'
                        ).props(
                            'outlined rounded type=date'
                        ).classes(
                            'tournament-field w-full'
                        )

                    with ui.column().classes('gap-2'):

                        ui.label(
                            'نوع البطولة *'
                        ).classes(
                            'field-label'
                        )

                        tournament_type = ui.select(
                            tournament_types,
                            label='اختر نوع البطولة'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'tournament-field w-full'
                        )

                with ui.row().classes(
                    'w-full grid grid-cols-1 md:grid-cols-2 gap-4 mt-4'
                ):

                    with ui.column().classes('gap-2'):

                        ui.label(
                            'مكان البطولة'
                        ).classes(
                            'field-label'
                        )

                        tournament_location = ui.input(
                            placeholder='مثال: استاد القاهرة'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'tournament-field w-full'
                        )

                    with ui.column().classes('gap-2'):

                        ui.label(
                            'الدولة / المدينة'
                        ).classes(
                            'field-label'
                        )

                        tournament_country_city = ui.input(
                            placeholder='مثال: مصر - القاهرة'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'tournament-field w-full'
                        )

                

                with ui.row().classes(
                    'w-full justify-end mt-6'
                ):

                    save_button = ui.button(
                        'حفظ البطولة',
                        icon='save'
                    ).props(
                        'unelevated no-caps'
                    ).classes(
                        'save-button'
                    )

            # =================================================
            # FILTER
            # =================================================

            with ui.card().classes(
                'filter-card p-5'
            ):

                with ui.row().classes(
                    'w-full items-end gap-4 flex-wrap'
                ):

                    with ui.column().classes(
                        'flex-1 min-w-[250px] gap-2'
                    ):

                        ui.label(
                            'البحث عن بطولة'
                        ).classes(
                            'field-label'
                        )

                        search = ui.input(
                            placeholder='ابحث باسم البطولة...'
                        ).props(
                            'outlined rounded clearable'
                        ).classes(
                            'filter-field w-full'
                        )

                    with ui.column().classes(
                        'min-w-[180px] gap-2'
                    ):

                        ui.label(
                            'السنة'
                        ).classes(
                            'field-label'
                        )

                        year_filter = ui.select(
                            {
                                'all': 'كل السنوات'
                            },
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
                        'filter-button bg-slate-800 text-white'
                    )

            tournaments_container = ui.column().classes(
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

                    with ui.element('div').classes(
                        'dialog-header'
                    ):

                        with ui.row().classes(
                            'items-center gap-3'
                        ):

                            with ui.element('div').classes(
                                'dialog-icon'
                            ):

                                ui.icon(
                                    'edit'
                                ).classes(
                                    'text-xl text-white'
                                )

                            with ui.column().classes('gap-0'):

                                ui.label(
                                    'تعديل البطولة'
                                ).classes(
                                    'dialog-title'
                                )

                                ui.label(
                                    'تعديل بيانات البطولة والفرق المشاركة'
                                ).classes(
                                    'dialog-subtitle mt-1'
                                )

                    with ui.column().classes(
                        'dialog-body'
                    ):

                        edit_id = ui.number(
                            'رقم البطولة'
                        ).props(
                            'outlined rounded readonly'
                        ).classes(
                            'w-full mb-3'
                        )

                        with ui.row().classes(
                            'w-full grid grid-cols-1 md:grid-cols-2 gap-3'
                        ):

                            edit_name_ar = ui.input(
                                'اسم البطولة بالعربي'
                            ).props(
                                'outlined rounded'
                            ).classes(
                                'w-full'
                            )

                            edit_name_en = ui.input(
                                'اسم البطولة بالإنجليزي'
                            ).props(
                                'outlined rounded'
                            ).classes(
                                'w-full'
                            )

                        with ui.row().classes(
                            'w-full grid grid-cols-1 md:grid-cols-2 gap-3 mt-3'
                        ):

                            edit_sport = ui.select(
                                sport_options,
                                label='الرياضة'
                            ).props(
                                'outlined rounded'
                            ).classes(
                                'w-full'
                            )

                            edit_type = ui.select(
                                tournament_types,
                                label='نوع البطولة'
                            ).props(
                                'outlined rounded'
                            ).classes(
                                'w-full'
                            )

                        with ui.row().classes(
                            'w-full grid grid-cols-1 md:grid-cols-2 gap-3 mt-3'
                        ):

                            edit_start_date = ui.input(
                                'تاريخ البداية'
                            ).props(
                                'outlined rounded type=date'
                            ).classes(
                                'w-full'
                            )

                            edit_end_date = ui.input(
                                'تاريخ النهاية'
                            ).props(
                                'outlined rounded type=date'
                            ).classes(
                                'w-full'
                            )

                        with ui.row().classes(
                            'w-full grid grid-cols-1 md:grid-cols-2 gap-3 mt-3'
                        ):

                            edit_location = ui.input(
                                'مكان البطولة'
                            ).props(
                                'outlined rounded'
                            ).classes(
                                'w-full'
                            )

                            edit_country_city = ui.input(
                                'الدولة / المدينة'
                            ).props(
                                'outlined rounded'
                            ).classes(
                                'w-full'
                            )

                        ui.label(
                            'الفرق المشاركة'
                        ).classes(
                            'field-label mt-4'
                        )

                        edit_team_selection = ui.select(
                            team_options_for_club(club_id),
                            multiple=True,
                            label='اختر الفرق'
                        ).props(
                            'outlined rounded use-chips'
                        ).classes(
                            'w-full mt-2'
                        )

                        with ui.row().classes(
                            'w-full justify-end gap-2 mt-6'
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
                                'dialog-save'
                            )

            # =================================================
            # DELETE DIALOG
            # =================================================

            delete_dialog = ui.dialog()

            with delete_dialog:

                with ui.card().classes(
                    'delete-dialog'
                ):

                    with ui.element('div').classes(
                        'delete-icon-box'
                    ):

                        ui.icon(
                            'delete_forever'
                        ).classes(
                            'text-3xl text-red-600'
                        )

                    ui.label(
                        'حذف البطولة'
                    ).classes(
                        'delete-title text-center mt-4'
                    )

                    delete_tournament_name = ui.label(
                        ''
                    ).classes(
                        'delete-name text-center mt-2'
                    )

                    delete_tournament_id = ui.number(
                        'Id'
                    ).props(
                        'readonly'
                    ).classes(
                        'hidden'
                    )

                    ui.label(
                        'هل أنت متأكد من حذف هذه البطولة؟'
                    ).classes(
                        'text-center text-slate-700 font-bold mt-4'
                    )

                    ui.label(
                        'لا يمكن حذف البطولة لأنها مرتبطة بفرق من خلال TournamentTable. افصل الفرق أولاً ثم احذف البطولة.'
                    ).classes(
                        'delete-warning text-center mt-4'
                    )

                    with ui.row().classes(
                        'w-full justify-center gap-3 mt-6'
                    ):

                        ui.button(
                            'إلغاء',
                            on_click=delete_dialog.close
                        ).props(
                            'flat no-caps'
                        )

                        delete_confirm_button = ui.button(
                            'تأكيد الحذف',
                            icon='delete'
                        ).props(
                            'unelevated no-caps'
                        ).classes(
                            'delete-confirm'
                        )

            # =================================================
            # TEAM MANAGEMENT DIALOG
            # =================================================

            teams_dialog = ui.dialog()

            with teams_dialog:

                with ui.card().classes(
                    'dialog-card'
                ):

                    with ui.element('div').classes(
                        'dialog-header'
                    ):

                        with ui.row().classes(
                            'items-center gap-3'
                        ):

                            with ui.element('div').classes(
                                'dialog-icon'
                            ):

                                ui.icon(
                                    'groups'
                                ).classes(
                                    'text-xl text-white'
                                )

                            with ui.column().classes('gap-0'):

                                ui.label(
                                    'فرق البطولة'
                                ).classes(
                                    'dialog-title'
                                )

                                ui.label(
                                    'إدارة الفرق ونتائجها في البطولة'
                                ).classes(
                                    'dialog-subtitle mt-1'
                                )

                    with ui.column().classes(
                        'dialog-body'
                    ):

                        manage_tournament_id = ui.number(
                            'Tournament Id'
                        ).props(
                            'readonly'
                        ).classes(
                            'hidden'
                        )

                        manage_tournament_name = ui.label(
                            ''
                        ).classes(
                            'text-slate-800 text-lg font-black mb-4'
                        )

                        manage_team_selection = ui.select(
                            team_options_for_club(club_id),
                            multiple=True,
                            label='الفرق المشاركة'
                        ).props(
                            'outlined rounded use-chips'
                        ).classes(
                            'w-full'
                        )

                        ui.label(
                            'بيانات الفرق المشاركة'
                        ).classes(
                            'field-label mt-5'
                        )

                        manage_team_results_container = ui.column().classes(
                            'w-full mt-3'
                        )

                        with ui.element('div').classes(
                            'team-selection-box mt-4'
                        ):

                            ui.label(
                                'ملاحظة'
                            ).classes(
                                'team-selection-title'
                            )

                            ui.label(
                                'المركز ومرحلة الوصول يتم حفظهما لكل فريق داخل البطولة.'
                            ).classes(
                                'text-xs text-slate-500 mt-1'
                            )

                        with ui.row().classes(
                            'w-full justify-end gap-2 mt-6'
                        ):

                            ui.button(
                                'إلغاء',
                                on_click=teams_dialog.close
                            ).props(
                                'flat no-caps'
                            )

                            save_teams_button = ui.button(
                                'حفظ الفرق',
                                icon='save'
                            ).props(
                                'unelevated no-caps'
                            ).classes(
                                'dialog-save'
                            )

            # =================================================
            # LOAD YEARS
            # =================================================

            def refresh_years():

                rows = db.fetch_all(
                    """
                    SELECT DISTINCT
                        substr(
                            COALESCE(
                                TournamentStartDate,
                                TournamentEndDate
                            ),
                            1,
                            4
                        ) AS YearValue
                    FROM Tournament
                    WHERE COALESCE(
                        TournamentStartDate,
                        TournamentEndDate
                    ) IS NOT NULL
                    AND COALESCE(
                        TournamentStartDate,
                        TournamentEndDate
                    ) <> ''
                    ORDER BY YearValue DESC
                    """
                )

                options = {
                    'all': 'كل السنوات'
                }

                for row in rows:

                    year_value = row['YearValue']

                    if year_value:
                        options[str(year_value)] = str(year_value)

                current_value = year_filter.value

                year_filter.options = options

                if current_value in options:
                    year_filter.value = current_value
                else:
                    year_filter.value = 'all'

            # =================================================
            # LOAD TOURNAMENTS
            # =================================================

            def refresh_tournaments():

                tournaments_container.clear()

                search_value = (
                    search.value or ''
                ).strip()

                selected_year = year_filter.value

                query = """
                    SELECT
                        t.Id,
                        t.TournamentNameAR,
                        t.TournamentNameEN,
                        t.TournamentStartDate,
                        t.TournamentEndDate,
                        t.TournamentLocation,
                        t.TournamentCountryCity,
                        t.TournamentType,
                        t.SportId,
                        s.SportNameAR,
                        s.SportNameEN,
                        COUNT(
                            DISTINCT CASE
                                WHEN tm.Clubid = ?
                                THEN tt.Teamid
                            END
                        ) AS TeamCount
                    FROM Tournament t
                    LEFT JOIN Sport s
                        ON s.Id = t.SportId
                    LEFT JOIN TournamentTable tt
                        ON tt.TournamentId = t.Id
                    LEFT JOIN Team tm
                        ON tm.Id = tt.Teamid
                    WHERE 1 = 1
                """

                params = [club_id]

                if search_value:

                    query += """
                        AND (
                            t.TournamentNameAR LIKE ?
                            OR t.TournamentNameEN LIKE ?
                            OR t.TournamentLocation LIKE ?
                            OR t.TournamentCountryCity LIKE ?
                            OR t.TournamentType LIKE ?
                        )
                    """

                    params.extend([
                        f'%{search_value}%',
                        f'%{search_value}%',
                        f'%{search_value}%',
                        f'%{search_value}%',
                        f'%{search_value}%'
                    ])

                if (
                    selected_year
                    and selected_year != 'all'
                ):

                    query += """
                        AND substr(
                            COALESCE(
                                t.TournamentStartDate,
                                t.TournamentEndDate
                            ),
                            1,
                            4
                        ) = ?
                    """

                    params.append(
                        str(selected_year)
                    )

                query += """
                    AND EXISTS (
                        SELECT 1
                        FROM TournamentTable tt2
                        INNER JOIN Team tm2
                            ON tm2.Id = tt2.Teamid
                        WHERE tt2.TournamentId = t.Id
                        AND tm2.Clubid = ?
                    )
                """

                params.append(club_id)

                query += """
                    GROUP BY
                        t.Id,
                        t.TournamentNameAR,
                        t.TournamentNameEN,
                        t.TournamentStartDate,
                        t.TournamentEndDate,
                        t.TournamentLocation,
                        t.TournamentCountryCity,
                        t.TournamentType,
                        t.SportId,
                        s.SportNameAR,
                        s.SportNameEN
                    ORDER BY
                        COALESCE(
                            t.TournamentStartDate,
                            t.TournamentEndDate
                        ) DESC,
                        t.Id DESC
                """

                tournaments = db.fetch_all(
                    query,
                    tuple(params)
                )

                with tournaments_container:

                    with ui.card().classes(
                        'list-card'
                    ):

                        with ui.row().classes(
                            'list-header w-full items-center justify-between p-5'
                        ):

                            with ui.row().classes(
                                'items-center gap-3'
                            ):

                                with ui.element('div').classes(
                                    'card-icon bg-blue-50 text-blue-600'
                                ):

                                    ui.icon(
                                        'emoji_events'
                                    ).classes(
                                        'text-xl'
                                    )

                                with ui.column().classes('gap-0'):

                                    ui.label(
                                        'البطولات المسجلة'
                                    ).classes(
                                        'card-title'
                                    )

                                    ui.label(
                                        'البطولات المرتبطة بفرق النادي'
                                    ).classes(
                                        'card-subtitle mt-1'
                                    )

                            ui.label(
                                f'{len(tournaments)} بطولة'
                            ).classes(
                                'count-badge'
                            )

                        if not tournaments:

                            with ui.column().classes(
                                'empty-state w-full items-center justify-center'
                            ):

                                with ui.element('div').classes(
                                    'empty-icon-box'
                                ):

                                    ui.icon(
                                        'emoji_events'
                                    ).classes(
                                        'text-4xl text-slate-300'
                                    )

                                ui.label(
                                    'لا توجد بطولات'
                                ).classes(
                                    'text-slate-600 text-lg font-black mt-4'
                                )

                                ui.label(
                                    'أضف بطولة جديدة أو غيّر خيارات البحث.'
                                ).classes(
                                    'text-slate-400 text-sm mt-1'
                                )

                            return

                        with ui.row().classes(
                            'w-full items-center px-5 py-3 bg-white border-b border-slate-100'
                        ):

                            ui.label(
                                'البطولة'
                            ).classes(
                                'text-xs font-black text-slate-400 flex-1'
                            )

                            ui.label(
                                'الفترة'
                            ).classes(
                                'text-xs font-black text-slate-400 w-48 text-center'
                            )

                            ui.label(
                                'النوع'
                            ).classes(
                                'text-xs font-black text-slate-400 w-28 text-center'
                            )

                            ui.label(
                                'الفرق'
                            ).classes(
                                'text-xs font-black text-slate-400 w-28 text-center'
                            )

                            ui.label(
                                'الإجراءات'
                            ).classes(
                                'text-xs font-black text-slate-400 w-36 text-center'
                            )

                        for tournament in tournaments:

                            tournament_id = tournament['Id']

                            tournament_name_ar = (
                                tournament['TournamentNameAR']
                                or 'بدون اسم'
                            )

                            tournament_name_en = (
                                tournament['TournamentNameEN']
                                or ''
                            )

                            start_date = (
                                tournament['TournamentStartDate']
                                or ''
                            )

                            end_date = (
                                tournament['TournamentEndDate']
                                or ''
                            )

                            location = (
                                tournament['TournamentLocation']
                                or ''
                            )

                            country_city = (
                                tournament['TournamentCountryCity']
                                or ''
                            )

                            tournament_type = (
                                tournament['TournamentType']
                                or 'غير محدد'
                            )

                            sport_name = (
                                tournament['SportNameAR']
                                or tournament['SportNameEN']
                                or 'رياضة غير محددة'
                            )

                            tournament_team_count = (
                                tournament['TeamCount']
                                or 0
                            )

                            with ui.row().classes(
                                'tournament-row items-center gap-4'
                            ):

                                with ui.row().classes(
                                    'items-center gap-4 flex-1 min-w-0'
                                ):

                                    with ui.element('div').classes(
                                        'tournament-avatar'
                                    ):

                                        ui.icon(
                                            'emoji_events'
                                        ).classes(
                                            'text-2xl'
                                        )

                                    with ui.column().classes(
                                        'gap-0 min-w-0'
                                    ):

                                        ui.label(
                                            tournament_name_ar
                                        ).classes(
                                            'tournament-name'
                                        )

                                        if tournament_name_en:

                                            ui.label(
                                                tournament_name_en
                                            ).classes(
                                                'tournament-name-en mt-1'
                                            )

                                        ui.label(
                                            f'ID: {tournament_id}'
                                        ).classes(
                                            'tournament-id mt-1'
                                        )

                                        with ui.row().classes(
                                            'items-center gap-2 flex-wrap mt-2'
                                        ):

                                            with ui.element('div').classes(
                                                'meta-chip sport'
                                            ):

                                                ui.icon(
                                                    'sports'
                                                ).classes(
                                                    'text-xs'
                                                )

                                                ui.label(
                                                    sport_name
                                                )

                                            if location or country_city:

                                                with ui.element('div').classes(
                                                    'meta-chip'
                                                ):

                                                    ui.icon(
                                                        'location_on'
                                                    ).classes(
                                                        'text-xs'
                                                    )

                                                    ui.label(
                                                        (
                                                            f'{country_city} - {location}'
                                                            if country_city and location
                                                            else country_city or location
                                                        )
                                                    )

                                with ui.row().classes(
                                    'w-48 justify-center'
                                ):

                                    with ui.column().classes(
                                        'items-center gap-1'
                                    ):

                                        with ui.element('div').classes(
                                            'meta-chip date'
                                        ):

                                            ui.icon(
                                                'calendar_month'
                                            ).classes(
                                                'text-xs'
                                            )

                                            ui.label(
                                                f'{start_date or "غير محدد"}'
                                            )

                                        ui.label(
                                            f'إلى {end_date or "غير محدد"}'
                                        ).classes(
                                            'text-[10px] text-slate-400 font-bold'
                                        )

                                with ui.row().classes(
                                    'w-28 justify-center'
                                ):

                                    with ui.element('div').classes(
                                        'meta-chip type'
                                    ):

                                        ui.icon(
                                            'public'
                                        ).classes(
                                            'text-xs'
                                        )

                                        ui.label(
                                            tournament_type
                                        )

                                with ui.row().classes(
                                    'w-28 justify-center'
                                ):

                                    with ui.element('div').classes(
                                        'meta-chip teams'
                                    ):

                                        ui.icon(
                                            'groups'
                                        ).classes(
                                            'text-xs'
                                        )

                                        ui.label(
                                            f'{tournament_team_count} فريق'
                                        )

                                with ui.row().classes(
                                    'w-36 justify-center items-center gap-1'
                                ):

                                    def open_edit(
                                        tournament_data=tournament
                                    ):

                                        edit_id.value = (
                                            tournament_data['Id']
                                        )

                                        edit_name_ar.value = (
                                            tournament_data['TournamentNameAR']
                                            or ''
                                        )

                                        edit_name_en.value = (
                                            tournament_data['TournamentNameEN']
                                            or ''
                                        )

                                        edit_sport.value = (
                                            tournament_data['SportId']
                                        )

                                        edit_type.value = (
                                            tournament_data['TournamentType']
                                        )

                                        edit_start_date.value = (
                                            tournament_data['TournamentStartDate']
                                            or ''
                                        )

                                        edit_end_date.value = (
                                            tournament_data['TournamentEndDate']
                                            or ''
                                        )

                                        edit_location.value = (
                                            tournament_data['TournamentLocation']
                                            or ''
                                        )

                                        edit_country_city.value = (
                                            tournament_data['TournamentCountryCity']
                                            or ''
                                        )

                                        edit_team_selection.value = (
                                            get_tournament_team_ids(
                                                tournament_data['Id'],
                                                club_id
                                            )
                                        )

                                        edit_dialog.open()

                                    def open_teams_manager(
                                        tournament_data=tournament
                                    ):

                                        tournament_id_value = (
                                            tournament_data['Id']
                                        )

                                        manage_tournament_id.value = (
                                            tournament_id_value
                                        )

                                        manage_tournament_name.text = (
                                            tournament_data['TournamentNameAR']
                                            or tournament_data['TournamentNameEN']
                                            or 'البطولة'
                                        )

                                        manage_team_selection.value = (
                                            get_tournament_team_ids(
                                                tournament_id_value,
                                                club_id
                                            )
                                        )

                                        load_manage_team_results(
                                            tournament_id_value,
                                            club_id
                                        )

                                        teams_dialog.open()

                                    def open_delete(
                                        tournament_data=tournament
                                    ):

                                        delete_tournament_id.value = (
                                            tournament_data['Id']
                                        )

                                        delete_tournament_name.text = (
                                            tournament_data['TournamentNameAR']
                                            or tournament_data['TournamentNameEN']
                                            or 'هذه البطولة'
                                        )

                                        delete_dialog.open()

                                    ui.button(
                                        icon='edit',
                                        on_click=open_edit
                                    ).props(
                                        'flat round'
                                    ).classes(
                                        'action-button'
                                    ).tooltip(
                                        'تعديل البطولة'
                                    )

                                    ui.button(
                                        icon='groups',
                                        on_click=open_teams_manager
                                    ).props(
                                        'flat round'
                                    ).classes(
                                        'action-button text-emerald-600'
                                    ).tooltip(
                                        'إدارة الفرق'
                                    )

                                    ui.button(
                                        icon='delete',
                                        on_click=open_delete
                                    ).props(
                                        'flat round'
                                    ).classes(
                                        'action-button delete-button'
                                    ).tooltip(
                                        'حذف البطولة'
                                    )

            # =================================================
            # ADD TOURNAMENT
            # =================================================

            def add_tournament():

                name_ar = (
                    tournament_name_ar.value or ''
                ).strip()

                name_en = (
                    tournament_name_en.value or ''
                ).strip()

                sport_id = (
                    tournament_sport.value
                )

                tournament_start = (
                    tournament_start_date.value or ''
                ).strip()

                tournament_end = (
                    tournament_end_date.value or ''
                ).strip()

                location = (
                    tournament_location.value or ''
                ).strip()

                country_city = (
                    tournament_country_city.value or ''
                ).strip()

                tournament_type_value = (
                    tournament_type.value
                )

                selected_teams = (
                    add_team_selection.value or []
                )

                if not name_ar:

                    ui.notify(
                        'من فضلك أدخل اسم البطولة بالعربي',
                        color='warning'
                    )

                    tournament_name_ar.run_method(
                        'focus'
                    )

                    return

                if not sport_id:

                    ui.notify(
                        'من فضلك اختر الرياضة',
                        color='warning'
                    )

                    return

                if not tournament_type_value:

                    ui.notify(
                        'من فضلك اختر نوع البطولة',
                        color='warning'
                    )

                    return

                if not tournament_start:

                    ui.notify(
                        'من فضلك أدخل تاريخ بداية البطولة',
                        color='warning'
                    )

                    return

                if not tournament_end:

                    ui.notify(
                        'من فضلك أدخل تاريخ نهاية البطولة',
                        color='warning'
                    )

                    return

                if not valid_date(tournament_start):

                    ui.notify(
                        'صيغة تاريخ البداية يجب أن تكون YYYY-MM-DD',
                        color='warning'
                    )

                    return

                if not valid_date(tournament_end):

                    ui.notify(
                        'صيغة تاريخ النهاية يجب أن تكون YYYY-MM-DD',
                        color='warning'
                    )

                    return

                if tournament_end < tournament_start:

                    ui.notify(
                        'تاريخ النهاية يجب أن يكون بعد أو مساويًا لتاريخ البداية',
                        color='warning'
                    )

                    return

                try:

                    db.execute_query(
                        """
                        INSERT INTO Tournament
                        (
                            TournamentNameAR,
                            TournamentNameEN,
                            TournamentStartDate,
                            TournamentEndDate,
                            TournamentLocation,
                            TournamentCountryCity,
                            TournamentType,
                            SportId,
                            CreatedBy,
                            CreatedOn
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            name_ar,
                            name_en,
                            tournament_start,
                            tournament_end,
                            location or None,
                            country_city or None,
                            tournament_type_value,
                            int(sport_id),
                            'SYSTEM',
                            now_string()
                        )
                    )

                    tournament_row = db.fetch_one(
                        """
                        SELECT Id
                        FROM Tournament
                        ORDER BY Id DESC
                        LIMIT 1
                        """
                    )

                    if not tournament_row:
                        raise RuntimeError(
                            'تعذر الحصول على رقم البطولة الجديدة'
                        )

                    tournament_id = tournament_row['Id']

                    for team_id in selected_teams:

                        if team_belongs_to_club(
                            team_id,
                            club_id
                        ):

                            db.execute_query(
                                """
                                INSERT INTO TournamentTable
                                (
                                    TournamentId,
                                    Teamid,
                                    CreatedBy,
                                    CreatedOn
                                )
                                VALUES (?, ?, ?, ?)
                                """,
                                (
                                    tournament_id,
                                    int(team_id),
                                    'SYSTEM',
                                    now_string()
                                )
                            )

                    ui.notify(
                        'تمت إضافة البطولة بنجاح',
                        color='positive'
                    )

                    tournament_name_ar.value = ''
                    tournament_name_en.value = ''
                    tournament_sport.value = None
                    tournament_start_date.value = ''
                    tournament_end_date.value = ''
                    tournament_location.value = ''
                    tournament_country_city.value = ''
                    tournament_type.value = None
                    add_team_selection.value = []

                    refresh_years()
                    refresh_tournaments()

                except sqlite3.IntegrityError as e:

                    ui.notify(
                        'تعذر حفظ البطولة. تأكد من صحة الرياضة والبيانات.',
                        color='negative'
                    )

                    print(
                        f'[ADD TOURNAMENT INTEGRITY ERROR] {e}'
                    )

                except Exception as e:

                    ui.notify(
                        'حدث خطأ أثناء إضافة البطولة',
                        color='negative'
                    )

                    print(
                        f'[ADD TOURNAMENT ERROR] '
                        f'{type(e).__name__}: {e}'
                    )

            save_button.on(
                'click',
                add_tournament
            )

            # =================================================
            # UPDATE TOURNAMENT
            # =================================================

            def update_tournament():

                if not edit_id.value:

                    ui.notify(
                        'لم يتم تحديد البطولة',
                        color='warning'
                    )

                    return

                name_ar = (
                    edit_name_ar.value or ''
                ).strip()

                name_en = (
                    edit_name_en.value or ''
                ).strip()

                sport_id = edit_sport.value

                tournament_type_value = edit_type.value

                start_date = (
                    edit_start_date.value or ''
                ).strip()

                end_date = (
                    edit_end_date.value or ''
                ).strip()

                location = (
                    edit_location.value or ''
                ).strip()

                country_city = (
                    edit_country_city.value or ''
                ).strip()

                selected_teams = (
                    edit_team_selection.value or []
                )

                if not name_ar:

                    ui.notify(
                        'من فضلك أدخل اسم البطولة بالعربي',
                        color='warning'
                    )

                    return

                if not sport_id:

                    ui.notify(
                        'من فضلك اختر الرياضة',
                        color='warning'
                    )

                    return

                if not tournament_type_value:

                    ui.notify(
                        'من فضلك اختر نوع البطولة',
                        color='warning'
                    )

                    return

                if not start_date:

                    ui.notify(
                        'من فضلك أدخل تاريخ البداية',
                        color='warning'
                    )

                    return

                if not end_date:

                    ui.notify(
                        'من فضلك أدخل تاريخ النهاية',
                        color='warning'
                    )

                    return

                if not valid_date(start_date):

                    ui.notify(
                        'صيغة تاريخ البداية يجب أن تكون YYYY-MM-DD',
                        color='warning'
                    )

                    return

                if not valid_date(end_date):

                    ui.notify(
                        'صيغة تاريخ النهاية يجب أن تكون YYYY-MM-DD',
                        color='warning'
                    )

                    return

                if end_date < start_date:

                    ui.notify(
                        'تاريخ النهاية يجب أن يكون بعد أو مساويًا لتاريخ البداية',
                        color='warning'
                    )

                    return

                try:

                    tournament_id = int(
                        edit_id.value
                    )

                    db.execute_query(
                        """
                        UPDATE Tournament
                        SET
                            TournamentNameAR = ?,
                            TournamentNameEN = ?,
                            TournamentStartDate = ?,
                            TournamentEndDate = ?,
                            TournamentLocation = ?,
                            TournamentCountryCity = ?,
                            TournamentType = ?,
                            SportId = ?,
                            UpdatedBy = ?,
                            UpdatedOn = ?
                        WHERE Id = ?
                        """,
                        (
                            name_ar,
                            name_en,
                            start_date,
                            end_date,
                            location or None,
                            country_city or None,
                            tournament_type_value,
                            int(sport_id),
                            'SYSTEM',
                            now_string(),
                            tournament_id
                        )
                    )

                    db.execute_query(
                        """
                        DELETE FROM TournamentTable
                        WHERE TournamentId = ?
                        AND Teamid IN (
                            SELECT Id
                            FROM Team
                            WHERE Clubid = ?
                        )
                        """,
                        (
                            tournament_id,
                            club_id
                        )
                    )

                    for team_id in selected_teams:

                        if team_belongs_to_club(
                            team_id,
                            club_id
                        ):

                            already_exists = db.fetch_one(
                                """
                                SELECT id
                                FROM TournamentTable
                                WHERE TournamentId = ?
                                AND Teamid = ?
                                LIMIT 1
                                """,
                                (
                                    tournament_id,
                                    int(team_id)
                                )
                            )

                            if not already_exists:

                                db.execute_query(
                                    """
                                    INSERT INTO TournamentTable
                                    (
                                        TournamentId,
                                        Teamid,
                                        CreatedBy,
                                        CreatedOn
                                    )
                                    VALUES (?, ?, ?, ?)
                                    """,
                                    (
                                        tournament_id,
                                        int(team_id),
                                        'SYSTEM',
                                        now_string()
                                    )
                                )

                    ui.notify(
                        'تم تعديل البطولة بنجاح',
                        color='positive'
                    )

                    edit_dialog.close()

                    refresh_years()
                    refresh_tournaments()

                except sqlite3.IntegrityError as e:

                    ui.notify(
                        'تعذر تعديل البطولة. تأكد من صحة البيانات.',
                        color='negative'
                    )

                    print(
                        f'[UPDATE TOURNAMENT INTEGRITY ERROR] {e}'
                    )

                except Exception as e:

                    ui.notify(
                        'حدث خطأ أثناء تعديل البطولة',
                        color='negative'
                    )

                    print(
                        f'[UPDATE TOURNAMENT ERROR] '
                        f'{type(e).__name__}: {e}'
                    )

            update_button.on(
                'click',
                update_tournament
            )

            # =================================================
            # LOAD TEAM RESULTS
            # =================================================

            def load_manage_team_results(
                tournament_id,
                selected_club_id
            ):

                manage_team_results_container.clear()

                rows = db.fetch_all(
                    """
                    SELECT
                        tt.id,
                        tt.Teamid,
                        tt.TournamentPosition,
                        tt.TournamentStage,
                        t.TeamAR,
                        t.TeamEN,
                        s.SportNameAR,
                        s.SportNameEN
                    FROM TournamentTable tt
                    INNER JOIN Team t
                        ON t.Id = tt.Teamid
                    LEFT JOIN Sport s
                        ON s.Id = t.Sportid
                    WHERE tt.TournamentId = ?
                    AND t.Clubid = ?
                    ORDER BY tt.id
                    """,
                    (
                        tournament_id,
                        selected_club_id
                    )
                )

                with manage_team_results_container:

                    if not rows:

                        ui.label(
                            'اختر الفرق المشاركة أولاً، ثم افتح إدارة الفرق مرة أخرى لحفظ بياناتها.'
                        ).classes(
                            'text-xs text-slate-400'
                        )

                        return

                    for row in rows:

                        team_name = (
                            row['TeamAR']
                            or row['TeamEN']
                            or 'فريق'
                        )

                        with ui.card().classes(
                            'w-full border border-slate-200 shadow-none p-4 mb-3'
                        ):

                            with ui.row().classes(
                                'w-full items-center justify-between gap-3'
                            ):

                                with ui.column().classes(
                                    'gap-1 flex-1'
                                ):

                                    ui.label(
                                        team_name
                                    ).classes(
                                        'font-black text-slate-800'
                                    )

                                    sport_name = (
                                        row['SportNameAR']
                                        or row['SportNameEN']
                                        or ''
                                    )

                                    if sport_name:

                                        ui.label(
                                            sport_name
                                        ).classes(
                                            'text-xs text-slate-400'
                                        )

                                with ui.row().classes(
                                    'items-center gap-3'
                                ):

                                    position_input = ui.number(
                                        'المركز'
                                    ).props(
                                        'outlined rounded min=1'
                                    ).classes(
                                        'w-28'
                                    )

                                    stage_input = ui.input(
                                        'وصل لفين'
                                    ).props(
                                        'outlined rounded'
                                    ).classes(
                                        'w-40'
                                    )

                                    position_input.value = (
                                        row['TournamentPosition']
                                    )

                                    stage_input.value = (
                                        row['TournamentStage']
                                        or ''
                                    )

                                    row['_position_input'] = (
                                        position_input
                                    )

                                    row['_stage_input'] = (
                                        stage_input
                                    )

                manage_team_results_container._team_result_rows = rows

            # =================================================
            # MANAGE TEAMS
            # =================================================

            def save_tournament_teams():

                if not manage_tournament_id.value:

                    ui.notify(
                        'لم يتم تحديد البطولة',
                        color='warning'
                    )

                    return

                tournament_id = int(
                    manage_tournament_id.value
                )

                selected_teams = (
                    manage_team_selection.value or []
                )

                try:

                    db.execute_query(
                        """
                        DELETE FROM TournamentTable
                        WHERE TournamentId = ?
                        AND Teamid IN (
                            SELECT Id
                            FROM Team
                            WHERE Clubid = ?
                        )
                        """,
                        (
                            tournament_id,
                            club_id
                        )
                    )

                    for team_id in selected_teams:

                        if not team_belongs_to_club(
                            team_id,
                            club_id
                        ):
                            continue

                        db.execute_query(
                            """
                            INSERT INTO TournamentTable
                            (
                                TournamentId,
                                Teamid,
                                CreatedBy,
                                CreatedOn
                            )
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                tournament_id,
                                int(team_id),
                                'SYSTEM',
                                now_string()
                            )
                        )

                    ui.notify(
                        'تم تحديث فرق البطولة بنجاح',
                        color='positive'
                    )

                    load_manage_team_results(
                        tournament_id,
                        club_id
                    )

                except sqlite3.IntegrityError:

                    ui.notify(
                        'أحد الفرق مرتبط بالبطولة بالفعل',
                        color='warning'
                    )

                except Exception as e:

                    ui.notify(
                        'حدث خطأ أثناء تحديث فرق البطولة',
                        color='negative'
                    )

                    print(
                        f'[MANAGE TOURNAMENT TEAMS ERROR] '
                        f'{type(e).__name__}: {e}'
                    )

            save_teams_button.on(
                'click',
                save_tournament_teams
            )

            # =================================================
            # DELETE TOURNAMENT
            # =================================================

            def delete_tournament():

                if not delete_tournament_id.value:

                    ui.notify(
                        'لم يتم تحديد البطولة',
                        color='warning'
                    )

                    return

                tournament_id = int(
                    delete_tournament_id.value
                )

                try:

                    linked_rows = db.fetch_all(
                        """
                        SELECT id
                        FROM TournamentTable
                        WHERE TournamentId = ?
                        LIMIT 1
                        """,
                        (tournament_id,)
                    )

                    if linked_rows:

                        ui.notify(
                            'لا يمكن حذف البطولة لأنها مرتبطة بفرق. افصل الفرق أولاً.',
                            color='warning'
                        )

                        delete_dialog.close()

                        return

                    db.execute_query(
                        """
                        DELETE FROM Tournament
                        WHERE Id = ?
                        """,
                        (tournament_id,)
                    )

                    ui.notify(
                        'تم حذف البطولة بنجاح',
                        color='positive'
                    )

                    delete_dialog.close()

                    refresh_years()
                    refresh_tournaments()

                except Exception as e:

                    ui.notify(
                        'حدث خطأ أثناء حذف البطولة',
                        color='negative'
                    )

                    print(
                        f'[DELETE TOURNAMENT ERROR] '
                        f'{type(e).__name__}: {e}'
                    )

            delete_confirm_button.on(
                'click',
                delete_tournament
            )

            # =================================================
            # EVENTS
            # =================================================

            search.on(
                'update:model-value',
                lambda e: refresh_tournaments()
            )

            year_filter.on(
                'update:model-value',
                lambda e: refresh_tournaments()
            )

            refresh_button.on(
                'click',
                refresh_tournaments
            )

            # =================================================
            # INITIAL
            # =================================================

            refresh_years()
            refresh_tournaments()


# =============================================================
# HELPERS
# =============================================================

def now_string():
    from datetime import datetime

    return datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S'
    )


def datetime_year():
    from datetime import datetime

    return datetime.now().year


def valid_date(value):
    from datetime import datetime

    try:

        datetime.strptime(
            value,
            '%Y-%m-%d'
        )

        return True

    except ValueError:

        return False


def team_options_for_club(club_id):

    teams = db.fetch_all(
        """
        SELECT
            t.Id,
            t.TeamAR,
            t.TeamEN,
            s.SportNameAR,
            s.SportNameEN,
            tc.TeamCategoryNameAR,
            tc.TeamCategoryNameEN
        FROM Team t
        LEFT JOIN Sport s
            ON s.Id = t.Sportid
        LEFT JOIN TeamCategory tc
            ON tc.Id = t.Teamcatgoryid
        WHERE t.Clubid = ?
        ORDER BY t.Id DESC
        """,
        (club_id,)
    )

    options = {}

    for team in teams:

        team_name = (
            team['TeamAR']
            or team['TeamEN']
            or 'فريق'
        )

        sport_name = (
            team['SportNameAR']
            or team['SportNameEN']
            or 'رياضة غير محددة'
        )

        category_name = (
            team['TeamCategoryNameAR']
            or team['TeamCategoryNameEN']
            or 'فئة غير محددة'
        )

        options[team['Id']] = (
            f'{team_name} — '
            f'{sport_name} — '
            f'{category_name}'
        )

    return options


def team_belongs_to_club(
    team_id,
    club_id
):

    if team_id is None:
        return False

    row = db.fetch_one(
        """
        SELECT
            Id
        FROM Team
        WHERE Id = ?
        AND Clubid = ?
        """,
        (
            int(team_id),
            club_id
        )
    )

    return row is not None


def get_tournament_team_ids(
    tournament_id,
    club_id
):

    rows = db.fetch_all(
        """
        SELECT
            tt.Teamid
        FROM TournamentTable tt
        INNER JOIN Team t
            ON t.Id = tt.Teamid
        WHERE tt.TournamentId = ?
        AND t.Clubid = ?
        ORDER BY tt.Teamid
        """,
        (
            tournament_id,
            club_id
        )
    )

    return [
        row['Teamid']
        for row in rows
    ]