from nicegui import ui, app
import database as db


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

    club_name_ar = club['ClubNameAR'] or 'النادي'
    club_name_en = club['ClubNameEN'] or ''

    # =========================================================
    # MedicalReportState
    # =========================================================

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

    medical_options = {
        row['Id']:
            (
                row['MedicalReportStateNameAR']
                or row['MedicalReportStateNameEN']
                or str(row['Id'])
            )
        for row in medical_states
    }

    # =========================================================
    # CSS
    # =========================================================

    ui.add_head_html(
        '''
        <style>

            /* =================================================
               GLOBAL
               ================================================= */

            .medical-page {
                direction: rtl;

                min-height: 100vh;
                width: 100%;

                background:
                    linear-gradient(
                        180deg,
                        #f8fafc 0%,
                        #f1f5f9 100%
                    );
            }

            .medical-wrapper {
                width: 100%;
                max-width: 1500px;
                margin: 0 auto;
            }

            /* =================================================
               HEADER
               ================================================= */

            .medical-header {
                width: 100%;

                background:#6F9C8A;
                    

                border-radius: 24px;

                padding: 28px 30px;

                overflow: hidden;

                position: relative;

                box-shadow:
                    0 14px 35px
                    rgba(15,23,42,.13);
            }

            .medical-header::before {
                content: "";

                position: absolute;

                width: 250px;
                height: 250px;

                top: -140px;
                left: -70px;

                border-radius: 50%;

                background:
                    rgba(255,255,255,.035);
            }

            .medical-header::after {
                content: "";

                position: absolute;

                width: 260px;
                height: 260px;

                bottom: -170px;
                right: -80px;

                border-radius: 50%;

                background:
                    rgba(56,189,248,.05);
            }

            .medical-header-content {
                position: relative;
                z-index: 2;
            }

            .medical-header-icon {
                width: 60px;
                height: 60px;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 17px;

                background:
                    rgba(255,255,255,.08);

                border:
                    1px solid
                    rgba(255,255,255,.12);
            }

            .medical-header-title {
                color: white;

                font-size: 29px;

                font-weight: 900;

                line-height: 1.3;
            }

            .medical-header-club {
                color: #67e8f9;

                font-size: 19px;

                font-weight: 800;
            }

            .medical-header-en {
                color: #94a3b8;

                font-size: 10px;

                font-weight: 700;

                letter-spacing: 2px;
            }

            .medical-header-description {
                color: #cbd5e1;

                font-size: 13px;

                line-height: 1.8;
            }

            .medical-header-badge {
                display: inline-flex;

                align-items: center;

                gap: 8px;

                padding:
                    8px 13px;

                border-radius: 999px;

                color: #d1fae5;

                background:
                    rgba(16,185,129,.10);

                border:
                    1px solid
                    rgba(16,185,129,.18);

                font-size: 11px;

                font-weight: 800;
            }

            .medical-header-badge-dot {
                width: 7px;
                height: 7px;

                border-radius: 50%;

                background: #10b981;
            }

            /* =================================================
               MAIN CARD
               ================================================= */

            .main-card {
                width: 100%;

                background: white;

                border:
                    1px solid #e2e8f0;

                border-radius: 21px;

                box-shadow:
                    0 7px 22px
                    rgba(15,23,42,.045);
            }

            /* =================================================
               STATISTICS
               ================================================= */

            .stat-card {
                width: 100%;

                min-height: 145px;

                background: white;

                border:
                    1px solid #e2e8f0;

                border-radius: 19px;

                box-shadow:
                    0 7px 22px
                    rgba(15,23,42,.045);

                position: relative;

                overflow: hidden;
            }

            .stat-card::before {
                content: "";

                position: absolute;

                top: 0;
                right: 0;
                left: 0;

                height: 4px;

                background: #e2e8f0;
            }

            .stat-card.total::before {
                background: #2563eb;
            }

            .stat-card.medical::before {
                background: #059669;
            }

            .stat-icon {
                width: 52px;
                height: 52px;

                border-radius: 15px;

                display: flex;
                align-items: center;
                justify-content: center;
            }

            .stat-label {
                color: #64748b;

                font-size: 12px;

                font-weight: 750;
            }

            .stat-number {
                color: #0f172a;

                font-size: 34px;

                line-height: 1;

                font-weight: 950;
            }

            .stat-description {
                color: #94a3b8;

                font-size: 10px;

                font-weight: 600;
            }

            /* =================================================
               FILTER AREA
               ================================================= */

            .filter-card {
                width: 100%;

                background: white;

                border:
                    1px solid #e2e8f0;

                border-radius: 19px;

                box-shadow:
                    0 6px 18px
                    rgba(15,23,42,.035);
            }

            .filter-label {
                color: #475569;

                font-size: 11px;

                font-weight: 800;
            }

            .filter-input .q-field__control {
                min-height: 50px !important;

                background: #f8fafc;

                border-radius: 13px !important;
            }

            .filter-select .q-field__control {
                min-height: 50px !important;

                border-radius: 13px !important;
            }

            .refresh-button {
                min-height: 50px !important;

                border-radius: 13px !important;

                font-weight: 800 !important;
            }

            /* =================================================
               TABLE HEADER
               ================================================= */

            .table-card {
                width: 100%;

                background: white;

                border:
                    1px solid #e2e8f0;

                border-radius: 21px;

                overflow: hidden;

                box-shadow:
                    0 7px 22px
                    rgba(15,23,42,.045);
            }

            .table-header {
                background:
                    #f8fafc;

                border-bottom:
                    1px solid #e2e8f0;
            }

            .table-column-title {
                color: #64748b;

                font-size: 11px;

                font-weight: 850;
            }

            /* =================================================
               PLAYER ROW
               ================================================= */

            .player-row {
                width: 100%;

                min-height: 72px;

                background: white;

                border-bottom:
                    1px solid #f1f5f9;
            }

            .player-row:last-child {
                border-bottom: none;
            }

            .player-avatar {
                width: 46px;
                height: 46px;

                flex-shrink: 0;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 13px;

                background:
                    #ecfdf5;

                border:
                    1px solid #d1fae5;
            }

            .player-name {
                color: #0f172a;

                font-size: 13px;

                font-weight: 850;
            }

            .player-id {
                color: #94a3b8;

                font-size: 10px;

                font-weight: 600;
            }

            .medical-status {
                display: inline-flex;

                align-items: center;

                justify-content: center;

                min-width: 110px;

                min-height: 32px;

                padding:
                    5px 12px;

                border-radius: 999px;

                background:
                    #f8fafc;

                border:
                    1px solid #e2e8f0;

                color: #475569;

                font-size: 11px;

                font-weight: 800;
            }

            .edit-button {
                width: 38px !important;
                height: 38px !important;

                border-radius: 10px !important;

                color: #475569 !important;
            }

            /* =================================================
               EMPTY
               ================================================= */

            .empty-state {
                min-height: 320px;
            }

            .empty-state-icon {
                width: 78px;
                height: 78px;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 22px;

                background: #f8fafc;

                border:
                    1px solid #e2e8f0;
            }

            /* =================================================
               DIALOG
               ================================================= */

            .medical-dialog {
                width: 470px;

                max-width: 95vw;

                border-radius: 22px;

                background: white;

                overflow: hidden;

                box-shadow:
                    0 20px 60px
                    rgba(15,23,42,.18);
            }

            .dialog-header {
                padding: 22px 24px;

                background:
                    linear-gradient(
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

                background:
                    rgba(255,255,255,.08);
            }

            .dialog-title {
                color: white;

                font-size: 19px;

                font-weight: 900;
            }

            .dialog-subtitle {
                color: #94a3b8;

                font-size: 11px;
            }

            .dialog-body {
                padding: 24px;
            }

            .dialog-save {
                background:
                    #059669 !important;

                color: white !important;

                border-radius:
                    11px !important;

                font-weight:
                    850 !important;
            }

            /* =================================================
               SCROLLBAR
               ================================================= */

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

            /* =================================================
               RESPONSIVE
               ================================================= */

            @media (max-width: 900px) {

                .medical-header {
                    padding: 24px;
                }

                .medical-header-title {
                    font-size: 25px;
                }

                .medical-header-club {
                    font-size: 17px;
                }
            }

            @media (max-width: 600px) {

                .medical-page {
                    padding: 12px !important;
                }

                .medical-header {
                    border-radius: 18px;
                    padding: 20px;
                }

                .medical-header-title {
                    font-size: 22px;
                }

                .medical-header-description {
                    font-size: 12px;
                }

                .stat-card {
                    min-height: 132px;
                    border-radius: 16px;
                }

                .main-card,
                .filter-card,
                .table-card {
                    border-radius: 17px;
                }

                .player-row {
                    padding:
                        10px 8px;
                }

                .medical-status {
                    min-width: auto;

                    font-size: 10px;

                    padding:
                        5px 9px;
                }
            }

        </style>
        '''
    )

    # =========================================================
    # الصفحة
    # =========================================================

    with ui.column().classes(
        'medical-page w-full p-4 md:p-6 lg:p-8'
    ):

        with ui.column().classes(
            'medical-wrapper gap-6'
        ):

            # =====================================================
            # HEADER
            # =====================================================

            with ui.element(
                'div'
            ).classes(
                'medical-header'
            ):

                with ui.row().classes(
                    'medical-header-content w-full items-center justify-between flex-wrap gap-6'
                ):

                    with ui.row().classes(
                        'items-center gap-4'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'medical-header-icon'
                        ):

                            ui.icon(
                                'medical_information'
                            ).classes(
                                'text-3xl text-white'
                            )

                        with ui.column().classes(
                            'gap-1'
                        ):

                            ui.label(
                                'إدارة الكشف الطبي'
                            ).classes(
                                'medical-header-title'
                            )

                            ui.label(
                                club_name_ar
                            ).classes(
                                'medical-header-club'
                            )

                            

                            

                    with ui.element(
                        'div'
                    ).classes(
                        'medical-header-badge'
                    ):

                        ui.element(
                            'span'
                        ).classes(
                            'medical-header-badge-dot'
                        )

                        

            # =====================================================
            # STATISTICS
            # =====================================================

            players_count = len(
                db.fetch_all(
                    """
                    SELECT Id
                    FROM Player
                    WHERE ClubId = ?
                    """,
                    (club_id,)
                )
            )

            state_counts = db.fetch_all(
                """
                SELECT
                    mrs.Id,
                    mrs.MedicalReportStateNameAR,
                    mrs.MedicalReportStateNameEN,
                    COUNT(p.Id) AS PlayerCount
                FROM MedicalReportState mrs
                LEFT JOIN Player p
                    ON p.MedicalReportStatueId = mrs.Id
                    AND p.ClubId = ?
                GROUP BY
                    mrs.Id,
                    mrs.MedicalReportStateNameAR,
                    mrs.MedicalReportStateNameEN
                ORDER BY mrs.Id
                """,
                (club_id,)
            )

            with ui.row().classes(
                'w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4'
            ):

                # =================================================
                # Total
                # =================================================

                with ui.card().classes(
                    'stat-card total p-5'
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
                                str(players_count)
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
                        'جميع اللاعبين المسجلين بالنادي'
                    ).classes(
                        'stat-description mt-4'
                    )

                # =================================================
                # Medical States
                # =================================================

                for index, state in enumerate(
                    state_counts[:3]
                ):

                    state_name = (
                        state['MedicalReportStateNameAR']
                        or state['MedicalReportStateNameEN']
                        or 'غير محدد'
                    )

                    state_count = (
                        state['PlayerCount']
                        or 0
                    )

                    with ui.card().classes(
                        'stat-card medical p-5'
                    ):

                        with ui.row().classes(
                            'w-full items-center justify-between'
                        ):

                            with ui.column().classes(
                                'gap-2'
                            ):

                                ui.label(
                                    state_name
                                ).classes(
                                    'stat-label'
                                )

                                ui.label(
                                    str(state_count)
                                ).classes(
                                    'stat-number'
                                )

                            with ui.element(
                                'div'
                            ).classes(
                                'stat-icon bg-emerald-50'
                            ):

                                ui.icon(
                                    'health_and_safety'
                                ).classes(
                                    'text-2xl text-emerald-600'
                                )

                        ui.label(
                            'لاعب'
                        ).classes(
                            'stat-description mt-4'
                        )

            # =====================================================
            # FILTER
            # =====================================================

            with ui.card().classes(
                'filter-card p-5'
            ):

                with ui.row().classes(
                    'w-full items-end gap-4 flex-wrap'
                ):

                    with ui.column().classes(
                        'gap-2 flex-1 min-w-[220px]'
                    ):

                        ui.label(
                            'البحث'
                        ).classes(
                            'filter-label'
                        )

                        with ui.row().classes(
                            'w-full items-center'
                        ):

                            ui.icon(
                                'search'
                            ).classes(
                                'text-lg text-slate-400 mr-2'
                            )

                            search = ui.input(
                                placeholder='ابحث باسم اللاعب...'
                            ).props(
                                'outlined rounded clearable'
                            ).classes(
                                'filter-input w-full'
                            )

                    with ui.column().classes(
                        'gap-2 min-w-[220px]'
                    ):

                        ui.label(
                            'الحالة الطبية'
                        ).classes(
                            'filter-label'
                        )

                        status_filter_options = {
                            'all': 'كل الحالات'
                        }

                        for state in medical_states:

                            status_filter_options[
                                state['Id']
                            ] = (
                                state['MedicalReportStateNameAR']
                                or state['MedicalReportStateNameEN']
                                or str(state['Id'])
                            )

                        status_filter = ui.select(
                            status_filter_options,
                            value='all'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'filter-select w-full'
                        )

                    refresh_button = ui.button(
                        'تحديث البيانات',
                        icon='refresh'
                    ).props(
                        'unelevated no-caps'
                    ).classes(
                        'refresh-button bg-slate-800 text-white'
                    )

            # =====================================================
            # Players Container
            # =====================================================

            players_container = ui.column().classes(
                'w-full'
            )

            # =====================================================
            # Edit Dialog
            # =====================================================

            edit_dialog = ui.dialog()

            with edit_dialog:

                with ui.card().classes(
                    'medical-dialog'
                ):

                    # =============================================
                    # Dialog Header
                    # =============================================

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
                                    'medical_information'
                                ).classes(
                                    'text-2xl text-white'
                                )

                            with ui.column().classes(
                                'gap-0'
                            ):

                                ui.label(
                                    'تحديث الكشف الطبي'
                                ).classes(
                                    'dialog-title'
                                )

                                ui.label(
                                    'تعديل الحالة الطبية للاعب'
                                ).classes(
                                    'dialog-subtitle mt-1'
                                )

                    # =============================================
                    # Dialog Body
                    # =============================================

                    with ui.column().classes(
                        'dialog-body'
                    ):

                        edit_player_id = ui.number(
                            'رقم اللاعب'
                        ).props(
                            'readonly outlined'
                        ).classes(
                            'w-full mb-4'
                        )

                        edit_player_name = ui.input(
                            'اسم اللاعب'
                        ).props(
                            'readonly outlined rounded'
                        ).classes(
                            'w-full mb-4'
                        )

                        edit_medical_state = ui.select(
                            medical_options,
                            label='الحالة الطبية'
                        ).props(
                            'outlined rounded clearable'
                        ).classes(
                            'w-full mb-6'
                        )

                        with ui.row().classes(
                            'w-full justify-end gap-2'
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

            # =====================================================
            # Actions & Handlers
            # =====================================================

            def save_medical_state():
                player_id = edit_player_id.value
                new_state = edit_medical_state.value

                if not player_id:
                    ui.notify('لم يتم تحديد اللاعب', color='negative')
                    return

                db.execute(
                    """
                    UPDATE Player
                    SET MedicalReportStatueId = ?
                    WHERE Id = ? AND ClubId = ?
                    """,
                    (new_state, player_id, club_id)
                )

                ui.notify('تم تحديث الحالة الطبية بنجاح', color='positive')
                edit_dialog.close()
                refresh_players()

            update_button.on_click(save_medical_state)

            # =====================================================
            # Refresh Players
            # =====================================================

            def refresh_players():

                players_container.clear()

                search_value = (
                    search.value or ''
                ).strip()

                selected_status = (
                    status_filter.value
                )

                query = """
                    SELECT
                        p.Id,
                        p.PlayerNameAR,
                        p.PlayerNameEN,
                        p.MedicalReportStatueId,
                        mrs.MedicalReportStateNameAR,
                        mrs.MedicalReportStateNameEN
                    FROM Player p
                    LEFT JOIN MedicalReportState mrs
                        ON mrs.Id = p.MedicalReportStatueId
                    WHERE p.ClubId = ?
                """

                params = [
                    club_id
                ]

                # Search Filter
                if search_value:
                    query += """
                        AND (
                            p.PlayerNameAR LIKE ?
                            OR p.PlayerNameEN LIKE ?
                        )
                    """
                    params.extend([f'%{search_value}%', f'%{search_value}%'])

                # Status Filter
                if selected_status and selected_status != 'all':
                    query += " AND p.MedicalReportStatueId = ?"
                    params.append(selected_status)

                query += " ORDER BY p.Id DESC"

                players = db.fetch_all(query, tuple(params))

                with players_container:
                    if not players:
                        with ui.card().classes(
                            'main-card empty-state flex flex-col items-center justify-center p-8 text-center'
                        ):
                            with ui.element('div').classes('empty-state-icon mb-4'):
                                ui.icon('search_off').classes('text-4xl text-slate-400')

                            ui.label('لم يتم العثور على أي لاعبين').classes(
                                'text-lg font-bold text-slate-700'
                            )
                            ui.label('جرب تغيير خيارات البحث أو التصفية').classes(
                                'text-xs text-slate-400 mt-1'
                            )
                    else:
                        with ui.card().classes('table-card w-full p-0'):
                            # Table Header
                            with ui.row().classes(
                                'table-header w-full items-center px-6 py-4 grid grid-cols-12 gap-2'
                            ):
                                ui.label('اللاعب').classes('table-column-title col-span-5 md:col-span-6')
                                ui.label('الحالة الطبية').classes('table-column-title col-span-5 md:col-span-4 text-center')
                                ui.label('إجراء').classes('table-column-title col-span-2 text-center')

                            # Player Rows
                            for player in players:
                                p_id = player['Id']
                                p_name = (
                                    player['PlayerNameAR']
                                    or player['PlayerNameEN']
                                    or f'لاعب #{p_id}'
                                )
                                p_status = (
                                    player['MedicalReportStateNameAR']
                                    or player['MedicalReportStateNameEN']
                                    or 'غير محدد'
                                )

                                with ui.row().classes(
                                    'player-row w-full items-center px-6 py-3 grid grid-cols-12 gap-2'
                                ):
                                    with ui.row().classes('col-span-5 md:col-span-6 items-center gap-3'):
                                        with ui.element('div').classes('player-avatar'):
                                            ui.icon('person').classes('text-xl text-emerald-600')

                                        with ui.column().classes('gap-0'):
                                            ui.label(p_name).classes('player-name')
                                            ui.label(f'#{p_id}').classes('player-id')

                                    with ui.row().classes('col-span-5 md:col-span-4 justify-center items-center'):
                                        ui.label(p_status).classes('medical-status')

                                    with ui.row().classes('col-span-2 justify-center items-center'):
                                        def open_edit(p=player):
                                            edit_player_id.value = p['Id']
                                            edit_player_name.value = p['PlayerNameAR'] or p['PlayerNameEN'] or ''
                                            edit_medical_state.value = p['MedicalReportStatueId']
                                            edit_dialog.open()

                                        ui.button(
                                            icon='edit',
                                            on_click=open_edit
                                        ).props('flat round size=sm').classes('edit-button')

            # =====================================================
            # Event Bindings & Initial Refresh
            # =====================================================

            refresh_button.on_click(refresh_players)
            search.on_value_change(refresh_players)
            status_filter.on_value_change(refresh_players)

            refresh_players()