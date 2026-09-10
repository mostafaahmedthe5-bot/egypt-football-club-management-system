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
        "SELECT Id, ClubNameAR, ClubNameEN FROM Club WHERE Id = ?",
        (club_id,)
    )

    if not club:
        ui.notify('النادي غير موجود', color='negative')
        ui.navigate.to('/select_club')
        return

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

            .medical-page {
                min-height: 100vh;
                background:
                    radial-gradient(
                        circle at top right,
                        rgba(16,185,129,.08),
                        transparent 28%
                    ),
                    radial-gradient(
                        circle at bottom left,
                        rgba(30,58,138,.06),
                        transparent 30%
                    ),
                    #f8fafc;
            }

            .page-card {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 22px;
                box-shadow: 0 8px 25px rgba(15,23,42,.05);
            }

            .page-title {
                color: #0f172a;
                font-size: 28px;
                font-weight: 900;
            }

            .stat-card {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
                box-shadow: 0 8px 25px rgba(15,23,42,.05);
                transition: .2s ease;
            }

            .stat-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 15px 35px rgba(15,23,42,.09);
            }

            .stat-icon {
                width: 50px;
                height: 50px;
                border-radius: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .player-row {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 18px;
                transition: .2s ease;
            }

            .player-row:hover {
                background: #f8fafc;
                border-color: #cbd5e1;
            }

        </style>
        '''
    )

    # =========================================================
    # الصفحة
    # =========================================================

    with ui.column().classes(
        'medical-page w-full p-4 md:p-6 lg:p-8 gap-6'
    ):

        # =====================================================
        # Header
        # =====================================================

        with ui.row().classes(
            'w-full items-center justify-between'
        ):

            with ui.column().classes('gap-1'):

                ui.label(
                    '🩺 الكشف الطبي'
                ).classes(
                    'page-title'
                )

                ui.label(
                    club['ClubNameAR'] or 'النادي'
                ).classes(
                    'text-emerald-700 text-lg font-bold'
                )

                ui.label(
                    'إدارة حالة الكشف الطبي للاعبين'
                ).classes(
                    'text-slate-500 text-sm'
                )

            with ui.element('div').classes(
                'bg-emerald-50 text-emerald-700 '
                'px-4 py-2 rounded-full font-bold'
            ):
                ui.label('MedicalReportState')

        # =====================================================
        # Statistics
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
            'w-full grid grid-cols-1 sm:grid-cols-2 '
            'lg:grid-cols-4 gap-4'
        ):

            with ui.card().classes(
                'stat-card w-full p-5'
            ):

                with ui.row().classes(
                    'w-full items-center justify-between'
                ):

                    with ui.element('div').classes(
                        'stat-icon bg-blue-50'
                    ):
                        ui.icon('groups').classes(
                            'text-2xl text-blue-600'
                        )

                    ui.label(
                        str(players_count)
                    ).classes(
                        'text-3xl font-black text-slate-900'
                    )

                ui.label(
                    'إجمالي اللاعبين'
                ).classes(
                    'text-slate-500 font-bold mt-4'
                )

            for state in state_counts[:3]:

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
                    'stat-card w-full p-5'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):

                        with ui.element('div').classes(
                            'stat-icon bg-emerald-50'
                        ):
                            ui.icon(
                                'health_and_safety'
                            ).classes(
                                'text-2xl text-emerald-600'
                            )

                        ui.label(
                            str(state_count)
                        ).classes(
                            'text-3xl font-black text-slate-900'
                        )

                    ui.label(
                        state_name
                    ).classes(
                        'text-slate-500 font-bold mt-4'
                    )

        # =====================================================
        # Search
        # =====================================================

        with ui.card().classes(
            'page-card w-full p-4'
        ):

            with ui.row().classes(
                'w-full items-center gap-3'
            ):

                ui.icon(
                    'search'
                ).classes(
                    'text-xl text-slate-500'
                )

                search = ui.input(
                    placeholder='ابحث باسم اللاعب...'
                ).props(
                    'outlined rounded clearable'
                ).classes(
                    'flex-1'
                )

                refresh_button = ui.button(
                    'تحديث',
                    icon='refresh'
                ).props(
                    'flat no-caps'
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
                'w-[450px] max-w-[95vw] p-6 rounded-2xl'
            ):

                ui.label(
                    'تحديث الكشف الطبي'
                ).classes(
                    'text-2xl font-black text-slate-900 mb-2'
                )

                edit_player_id = ui.number(
                    'Id'
                ).props(
                    'readonly'
                ).classes(
                    'w-full mb-3'
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
                    label='MedicalReportState'
                ).props(
                    'outlined rounded clearable'
                ).classes(
                    'w-full mb-5'
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
                        'حفظ',
                        icon='save'
                    ).props(
                        'unelevated no-caps'
                    ).classes(
                        'bg-emerald-600 text-white'
                    )

        # =====================================================
        # Refresh
        # =====================================================

        def refresh_players():

            players_container.clear()

            search_value = (
                search.value or ''
            ).strip()

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

            params = [club_id]

            if search_value:

                query += """
                    AND (
                        p.PlayerNameAR LIKE ?
                        OR p.PlayerNameEN LIKE ?
                    )
                """

                params.extend([
                    f'%{search_value}%',
                    f'%{search_value}%'
                ])

            query += """
                ORDER BY p.Id DESC
            """

            players = db.fetch_all(
                query,
                tuple(params)
            )

            with players_container:

                with ui.card().classes(
                    'page-card w-full p-5 md:p-6'
                ):

                    with ui.row().classes(
                        'w-full items-center justify-between mb-5'
                    ):

                        ui.label(
                            'قائمة اللاعبين'
                        ).classes(
                            'text-xl font-black text-slate-900'
                        )

                        ui.label(
                            f'{len(players)} لاعب'
                        ).classes(
                            'bg-emerald-50 text-emerald-700 '
                            'px-3 py-1 rounded-full text-xs font-bold'
                        )

                    if not players:

                        with ui.column().classes(
                            'w-full items-center py-12'
                        ):

                            ui.icon(
                                'person_search'
                            ).classes(
                                'text-6xl text-slate-300'
                            )

                            ui.label(
                                'لا توجد بيانات'
                            ).classes(
                                'text-slate-500 font-bold mt-4'
                            )

                        return

                    with ui.column().classes(
                        'w-full gap-3'
                    ):

                        for player in players:

                            player_name = (
                                player['PlayerNameAR']
                                or player['PlayerNameEN']
                                or 'بدون اسم'
                            )

                            medical_name = (
                                player['MedicalReportStateNameAR']
                                or player['MedicalReportStateNameEN']
                                or 'غير محدد'
                            )

                            with ui.element(
                                'div'
                            ).classes(
                                'player-row w-full p-4'
                            ):

                                with ui.row().classes(
                                    'w-full items-center '
                                    'justify-between gap-4'
                                ):

                                    with ui.row().classes(
                                        'items-center gap-4'
                                    ):

                                        with ui.element(
                                            'div'
                                        ).classes(
                                            'w-11 h-11 rounded-xl '
                                            'bg-emerald-50 '
                                            'flex items-center '
                                            'justify-center'
                                        ):
                                            ui.icon(
                                                'person'
                                            ).classes(
                                                'text-xl '
                                                'text-emerald-600'
                                            )

                                        with ui.column().classes(
                                            'gap-0'
                                        ):

                                            ui.label(
                                                player_name
                                            ).classes(
                                                'font-black '
                                                'text-slate-800'
                                            )

                                            ui.label(
                                                f'Id: {player["Id"]}'
                                            ).classes(
                                                'text-xs '
                                                'text-slate-400 mt-1'
                                            )

                                    with ui.row().classes(
                                        'items-center gap-3'
                                    ):

                                        ui.label(
                                            medical_name
                                        ).classes(
                                            'bg-slate-100 '
                                            'text-slate-700 '
                                            'px-3 py-1 rounded-full '
                                            'text-xs font-bold'
                                        )

                                        def open_edit(
                                            player_data=player
                                        ):

                                            edit_player_id.value = (
                                                player_data['Id']
                                            )

                                            edit_player_name.value = (
                                                player_data['PlayerNameAR']
                                                or player_data['PlayerNameEN']
                                                or ''
                                            )

                                            edit_medical_state.value = (
                                                player_data[
                                                    'MedicalReportStatueId'
                                                ]
                                            )

                                            edit_dialog.open()

                                        ui.button(
                                            icon='edit',
                                            on_click=open_edit
                                        ).props(
                                            'flat round'
                                        ).tooltip(
                                            'تعديل الكشف'
                                        )

        # =====================================================
        # Events
        # =====================================================

        def update_medical():

            if not edit_player_id.value:
                return

            try:

                db.execute_query(
                    """
                    UPDATE Player
                    SET MedicalReportStatueId = ?
                    WHERE Id = ?
                    AND ClubId = ?
                    """,
                    (
                        edit_medical_state.value,
                        int(edit_player_id.value),
                        club_id
                    )
                )

                ui.notify(
                    'تم تحديث حالة الكشف الطبي بنجاح',
                    color='positive'
                )

                edit_dialog.close()
                refresh_players()

            except Exception as e:

                ui.notify(
                    'حدث خطأ أثناء تحديث الكشف الطبي',
                    color='negative'
                )

                print(
                    f'[MEDICAL ERROR] {type(e).__name__}: {e}'
                )

        update_button.on(
            'click',
            update_medical
        )

        search.on(
            'update:model-value',
            lambda e: refresh_players()
        )

        refresh_button.on(
            'click',
            refresh_players
        )

        refresh_players()