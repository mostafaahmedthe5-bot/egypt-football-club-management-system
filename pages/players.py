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
        ui.notify(
            'النادي غير موجود',
            color='negative'
        )
        ui.navigate.to('/select_club')
        return

    club_name = club['ClubNameAR'] or 'النادي'

    # =========================================================
    # CSS
    # =========================================================

    ui.add_head_html(
        '''
        <style>

            .players-page {
                min-height: 100vh;
                background:
                    radial-gradient(
                        circle at top right,
                        rgba(245,158,11,.07),
                        transparent 25%
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

            .field-label {
                color: #475569;
                font-size: 13px;
                font-weight: 800;
                margin-bottom: 5px;
            }

            .player-row {
                border: 1px solid #e2e8f0;
                border-radius: 18px;
                background: white;
                transition: .2s ease;
            }

            .player-row:hover {
                background: #f8fafc;
                border-color: #cbd5e1;
                transform: translateY(-1px);
            }

            .player-avatar {
                width: 52px;
                height: 52px;
                border-radius: 16px;
                background:
                    linear-gradient(
                        135deg,
                        #0f172a,
                        #1e3a8a
                    );
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .filter-card {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 18px;
            }

            .info-chip {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                color: #475569;
                border-radius: 999px;
                padding: 5px 10px;
                font-size: 12px;
                font-weight: 700;
            }

        </style>
        '''
    )

    # =========================================================
    # Load lookup data
    # =========================================================

    teams = db.fetch_all(
        """
        SELECT Id, TeamAR, TeamEN
        FROM Team
        WHERE Clubid = ?
        ORDER BY Id
        """,
        (club_id,)
    )

    nationalities = db.fetch_all(
        """
        SELECT Id, NationalityNameAR, NationalityNameEN
        FROM Nationality
        ORDER BY Id
        """
    )

    wearing_sizes = db.fetch_all(
        """
        SELECT Id, WearingSizeName
        FROM WearingSize
        ORDER BY Id
        """
    )

    education_levels = db.fetch_all(
        """
        SELECT Id, EducationLevelNameAR, EducationLevelNameEN
        FROM EducationLevel
        ORDER BY Id
        """
    )

    medical_states = db.fetch_all(
        """
        SELECT Id, MedicalReportStateNameAR, MedicalReportStateNameEN
        FROM MedicalReportState
        ORDER BY Id
        """
    )

    blood_types = db.fetch_all(
        """
        SELECT Id, BloodTypeNameAR, BloodTypeNameEN
        FROM BloodType
        ORDER BY Id
        """
    )

    membership_statuses = db.fetch_all(
        """
        SELECT Id, MembershipStatusNameAR, MembershipStatusNameEN
        FROM MembershipStatus
        ORDER BY Id
        """
    )

    membership_types = db.fetch_all(
        """
        SELECT Id, MembershipTypeNameAR, MembershipTypeNameEN
        FROM MembershipType
        ORDER BY Id
        """
    )

    religions = db.fetch_all(
        """
        SELECT Id, ReligionNameAR, ReligionNameEN
        FROM Religion
        ORDER BY Id
        """
    )

    team_options = {
        row['Id']:
            (
                row['TeamAR']
                or row['TeamEN']
                or str(row['Id'])
            )
        for row in teams
    }

    nationality_options = {
        row['Id']:
            (
                row['NationalityNameAR']
                or row['NationalityNameEN']
                or str(row['Id'])
            )
        for row in nationalities
    }

    wearing_size_options = {
        row['Id']:
            (
                row['WearingSizeName']
                or str(row['Id'])
            )
        for row in wearing_sizes
    }

    education_options = {
        row['Id']:
            (
                row['EducationLevelNameAR']
                or row['EducationLevelNameEN']
                or str(row['Id'])
            )
        for row in education_levels
    }

    medical_options = {
        row['Id']:
            (
                row['MedicalReportStateNameAR']
                or row['MedicalReportStateNameEN']
                or str(row['Id'])
            )
        for row in medical_states
    }

    blood_options = {
        row['Id']:
            (
                row['BloodTypeNameAR']
                or row['BloodTypeNameEN']
                or str(row['Id'])
            )
        for row in blood_types
    }

    membership_status_options = {
        row['Id']:
            (
                row['MembershipStatusNameAR']
                or row['MembershipStatusNameEN']
                or str(row['Id'])
            )
        for row in membership_statuses
    }

    membership_type_options = {
        row['Id']:
            (
                row['MembershipTypeNameAR']
                or row['MembershipTypeNameEN']
                or str(row['Id'])
            )
        for row in membership_types
    }

    religion_options = {
        row['Id']:
            (
                row['ReligionNameAR']
                or row['ReligionNameEN']
                or str(row['Id'])
            )
        for row in religions
    }

    # =========================================================
    # Header
    # =========================================================

    with ui.column().classes(
        'players-page w-full p-4 md:p-6 lg:p-8 gap-6'
    ):

        with ui.row().classes(
            'w-full items-center justify-between'
        ):

            with ui.column().classes('gap-1'):

                ui.label(
                    '🏃‍♂️ قائمة وإدارة اللاعبين'
                ).classes(
                    'page-title'
                )

                ui.label(
                    club_name
                ).classes(
                    'text-blue-800 text-lg font-bold'
                )

                ui.label(
                    'إدارة بيانات اللاعبين داخل النادي'
                ).classes(
                    'text-sm text-slate-500'
                )

            with ui.element('div').classes(
                'bg-blue-50 text-blue-700 '
                'px-4 py-2 rounded-full font-bold'
            ):
                ui.label('Player')

        # =========================================================
        # Add player card
        # =========================================================

        with ui.card().classes(
            'page-card w-full p-5 md:p-6'
        ):

            with ui.row().classes(
                'items-center gap-3 mb-5'
            ):

                with ui.element('div').classes(
                    'w-11 h-11 rounded-xl bg-blue-50 '
                    'flex items-center justify-center'
                ):
                    ui.icon('person_add').classes(
                        'text-xl text-blue-600'
                    )

                ui.label(
                    'تسجيل لاعب جديد'
                ).classes(
                    'text-xl font-black text-slate-900'
                )

            with ui.row().classes(
                'w-full grid grid-cols-1 md:grid-cols-2 '
                'lg:grid-cols-4 gap-4'
            ):

                # PlayerNameAR
                with ui.column().classes('w-full'):
                    ui.label(
                        'اسم اللاعب بالعربي'
                    ).classes('field-label')

                    name_ar = ui.input(
                        placeholder='مثال: أحمد محمد'
                    ).props(
                        'outlined rounded'
                    ).classes(
                        'w-full'
                    )

                # PlayerNameEN
                with ui.column().classes('w-full'):
                    ui.label(
                        'اسم اللاعب بالإنجليزي'
                    ).classes('field-label')

                    name_en = ui.input(
                        placeholder='Example: Ahmed Mohamed'
                    ).props(
                        'outlined rounded'
                    ).classes(
                        'w-full'
                    )

                # NationalityId
                with ui.column().classes('w-full'):
                    ui.label(
                        'Nationality'
                    ).classes('field-label')

                    nationality = ui.select(
                        nationality_options,
                        label='اختر Nationality'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

                # WearingSizeId
                with ui.column().classes('w-full'):
                    ui.label(
                        'WearingSize'
                    ).classes('field-label')

                    wearing_size = ui.select(
                        wearing_size_options,
                        label='اختر WearingSize'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

                # EducationLevelId
                with ui.column().classes('w-full'):
                    ui.label(
                        'EducationLevel'
                    ).classes('field-label')

                    education = ui.select(
                        education_options,
                        label='اختر EducationLevel'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

                # MedicalReportStatueId
                with ui.column().classes('w-full'):
                    ui.label(
                        'MedicalReportState'
                    ).classes('field-label')

                    medical_state = ui.select(
                        medical_options,
                        label='اختر MedicalReportState'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

                # BloodTypeId
                with ui.column().classes('w-full'):
                    ui.label(
                        'BloodType'
                    ).classes('field-label')

                    blood_type = ui.select(
                        blood_options,
                        label='اختر BloodType'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

                # MembershipStatueId
                with ui.column().classes('w-full'):
                    ui.label(
                        'MembershipStatus'
                    ).classes('field-label')

                    membership_status = ui.select(
                        membership_status_options,
                        label='اختر MembershipStatus'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

                # MembershipTypeId
                with ui.column().classes('w-full'):
                    ui.label(
                        'MembershipType'
                    ).classes('field-label')

                    membership_type = ui.select(
                        membership_type_options,
                        label='اختر MembershipType'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

                # ReligionId
                with ui.column().classes('w-full'):
                    ui.label(
                        'Religion'
                    ).classes('field-label')

                    religion = ui.select(
                        religion_options,
                        label='اختر Religion'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

            with ui.row().classes(
                'w-full justify-end mt-5'
            ):

                save_button = ui.button(
                    'تسجيل اللاعب',
                    icon='person_add'
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'bg-green-600 text-white '
                    'rounded-xl px-7 py-3 font-bold'
                )

        # =========================================================
        # Filter
        # =========================================================

        with ui.card().classes(
            'filter-card w-full p-4'
        ):

            with ui.row().classes(
                'w-full items-center gap-3'
            ):

                ui.icon('search').classes(
                    'text-xl text-slate-500'
                )

                search = ui.input(
                    placeholder='ابحث باسم اللاعب بالعربي أو الإنجليزي...'
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

        # =========================================================
        # Players container
        # =========================================================

        players_container = ui.column().classes(
            'w-full'
        )

        # =========================================================
        # Edit dialog
        # =========================================================

        edit_dialog = ui.dialog()

        with edit_dialog:
            with ui.card().classes(
                'w-[650px] max-w-[96vw] p-6 rounded-2xl'
            ):

                ui.label(
                    'تعديل بيانات اللاعب'
                ).classes(
                    'text-2xl font-black text-slate-900 mb-5'
                )

                edit_id = ui.number(
                    'Id'
                ).props(
                    'outlined rounded readonly'
                ).classes(
                    'w-full mb-3'
                )

                edit_name_ar = ui.input(
                    'اسم اللاعب بالعربي'
                ).props(
                    'outlined rounded'
                ).classes(
                    'w-full mb-3'
                )

                edit_name_en = ui.input(
                    'اسم اللاعب بالإنجليزي'
                ).props(
                    'outlined rounded'
                ).classes(
                    'w-full mb-3'
                )

                edit_nationality = ui.select(
                    nationality_options,
                    label='Nationality'
                ).props(
                    'outlined rounded clearable'
                ).classes(
                    'w-full mb-3'
                )

                edit_wearing_size = ui.select(
                    wearing_size_options,
                    label='WearingSize'
                ).props(
                    'outlined rounded clearable'
                ).classes(
                    'w-full mb-3'
                )

                edit_education = ui.select(
                    education_options,
                    label='EducationLevel'
                ).props(
                    'outlined rounded clearable'
                ).classes(
                    'w-full mb-3'
                )

                edit_medical_state = ui.select(
                    medical_options,
                    label='MedicalReportState'
                ).props(
                    'outlined rounded clearable'
                ).classes(
                    'w-full mb-3'
                )

                edit_blood_type = ui.select(
                    blood_options,
                    label='BloodType'
                ).props(
                    'outlined rounded clearable'
                ).classes(
                    'w-full mb-3'
                )

                edit_membership_status = ui.select(
                    membership_status_options,
                    label='MembershipStatus'
                ).props(
                    'outlined rounded clearable'
                ).classes(
                    'w-full mb-3'
                )

                edit_membership_type = ui.select(
                    membership_type_options,
                    label='MembershipType'
                ).props(
                    'outlined rounded clearable'
                ).classes(
                    'w-full mb-3'
                )

                edit_religion = ui.select(
                    religion_options,
                    label='Religion'
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
                        'حفظ التعديل',
                        icon='save'
                    ).props(
                        'unelevated no-caps'
                    ).classes(
                        'bg-blue-700 text-white'
                    )

        # =========================================================
        # Delete dialog
        # =========================================================

        delete_dialog = ui.dialog()

        with delete_dialog:
            with ui.card().classes(
                'w-[400px] max-w-[95vw] p-6 rounded-2xl'
            ):

                ui.icon(
                    'warning'
                ).classes(
                    'text-5xl text-red-500 self-center'
                )

                ui.label(
                    'حذف اللاعب'
                ).classes(
                    'text-2xl font-black text-center mt-3'
                )

                delete_player_name = ui.label(
                    ''
                ).classes(
                    'text-slate-700 font-bold text-center mt-3'
                )

                delete_player_id = ui.number(
                    'Id'
                ).props(
                    'readonly'
                ).classes(
                    'hidden'
                )

                ui.label(
                    'هل أنت متأكد من حذف هذا اللاعب؟'
                ).classes(
                    'text-slate-500 text-center mt-2'
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

                    delete_button = ui.button(
                        'حذف',
                        icon='delete'
                    ).props(
                        'unelevated no-caps'
                    ).classes(
                        'bg-red-600 text-white'
                    )

        # =========================================================
        # Refresh players
        # =========================================================

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
                    r.ReligionNameEN
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

                        with ui.row().classes(
                            'items-center gap-3'
                        ):

                            with ui.element('div').classes(
                                'w-11 h-11 rounded-xl bg-blue-50 '
                                'flex items-center justify-center'
                            ):
                                ui.icon('groups').classes(
                                    'text-xl text-blue-600'
                                )

                            ui.label(
                                'اللاعبون المسجلون'
                            ).classes(
                                'text-xl font-black text-slate-900'
                            )

                        ui.label(
                            f'{len(players)} لاعب'
                        ).classes(
                            'bg-blue-50 text-blue-700 '
                            'px-3 py-1 rounded-full '
                            'text-xs font-bold'
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

                            if search_value:
                                ui.label(
                                    'لا توجد نتائج للبحث'
                                ).classes(
                                    'text-slate-500 font-bold text-lg mt-4'
                                )
                            else:
                                ui.label(
                                    'لا يوجد لاعبون'
                                ).classes(
                                    'text-slate-500 font-bold text-lg mt-4'
                                )

                    else:

                        with ui.column().classes(
                            'w-full gap-3'
                        ):

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

                                nationality_name = (
                                    player['NationalityNameAR']
                                    or player['NationalityNameEN']
                                    or 'غير محدد'
                                )

                                medical_name = (
                                    player['MedicalReportStateNameAR']
                                    or player['MedicalReportStateNameEN']
                                    or 'غير محدد'
                                )

                                membership_name = (
                                    player['MembershipStatusNameAR']
                                    or player['MembershipStatusNameEN']
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

                                        # =================================
                                        # Player information
                                        # =================================

                                        with ui.row().classes(
                                            'items-center gap-4'
                                        ):

                                            with ui.element(
                                                'div'
                                            ).classes(
                                                'player-avatar'
                                            ):
                                                ui.icon(
                                                    'person'
                                                ).classes(
                                                    'text-2xl'
                                                )

                                            with ui.column().classes(
                                                'gap-0'
                                            ):

                                                ui.label(
                                                    player_name_ar
                                                ).classes(
                                                    'text-lg font-black '
                                                    'text-slate-800'
                                                )

                                                if player_name_en:
                                                    ui.label(
                                                        player_name_en
                                                    ).classes(
                                                        'text-xs '
                                                        'text-slate-400 '
                                                        'mt-1'
                                                    )

                                                ui.label(
                                                    f'Id: {player_id}'
                                                ).classes(
                                                    'text-xs '
                                                    'text-slate-400 '
                                                    'mt-1'
                                                )

                                        # =================================
                                        # Status
                                        # =================================

                                        with ui.row().classes(
                                            'items-center gap-2 flex-wrap'
                                        ):

                                            ui.label(
                                                nationality_name
                                            ).classes(
                                                'info-chip'
                                            )

                                            ui.label(
                                                medical_name
                                            ).classes(
                                                'info-chip'
                                            )

                                            ui.label(
                                                membership_name
                                            ).classes(
                                                'info-chip'
                                            )

                                        # =================================
                                        # Actions
                                        # =================================

                                        with ui.row().classes(
                                            'items-center gap-1'
                                        ):

                                            def open_edit(
                                                player_data=player
                                            ):

                                                edit_id.value = (
                                                    player_data['Id']
                                                )

                                                edit_name_ar.value = (
                                                    player_data['PlayerNameAR']
                                                    or ''
                                                )

                                                edit_name_en.value = (
                                                    player_data['PlayerNameEN']
                                                    or ''
                                                )

                                                edit_nationality.value = (
                                                    player_data['NationalityId']
                                                )

                                                edit_wearing_size.value = (
                                                    player_data['WearingSizeId']
                                                )

                                                edit_education.value = (
                                                    player_data['EducationLevelId']
                                                )

                                                edit_medical_state.value = (
                                                    player_data['MedicalReportStatueId']
                                                )

                                                edit_blood_type.value = (
                                                    player_data['BloodTypeId']
                                                )

                                                edit_membership_status.value = (
                                                    player_data['MembershipStatueId']
                                                )

                                                edit_membership_type.value = (
                                                    player_data['MembershipTypeId']
                                                )

                                                edit_religion.value = (
                                                    player_data['ReligionId']
                                                )

                                                edit_dialog.open()

                                            def open_delete(
                                                player_data=player
                                            ):

                                                delete_player_id.value = (
                                                    player_data['Id']
                                                )

                                                delete_player_name.text = (
                                                    player_data['PlayerNameAR']
                                                    or 'هذا اللاعب'
                                                )

                                                delete_dialog.open()

                                            ui.button(
                                                icon='edit',
                                                on_click=open_edit
                                            ).props(
                                                'flat round'
                                            ).tooltip(
                                                'تعديل'
                                            )

                                            ui.button(
                                                icon='delete',
                                                on_click=open_delete
                                            ).props(
                                                'flat round'
                                            ).classes(
                                                'text-red-600'
                                            ).tooltip(
                                                'حذف'
                                            )

        # =========================================================
        # Add player
        # =========================================================

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
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

                ui.notify(
                    'تم حفظ اللاعب بنجاح',
                    color='positive'
                )

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

                refresh_players()

            except Exception as e:

                ui.notify(
                    'حدث خطأ أثناء حفظ اللاعب',
                    color='negative'
                )

                print(
                    f'[SAVE PLAYER ERROR] {type(e).__name__}: {e}'
                )

        save_button.on(
            'click',
            save_player
        )

        # =========================================================
        # Update player
        # =========================================================

        def update_player():

            if not edit_id.value:
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
                    WHERE Id = ?
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
                        int(edit_id.value),
                        club_id
                    )
                )

                ui.notify(
                    'تم تعديل اللاعب بنجاح',
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
                    f'[UPDATE PLAYER ERROR] {type(e).__name__}: {e}'
                )

        update_button.on(
            'click',
            update_player
        )

        # =========================================================
        # Delete player
        # =========================================================

        def delete_player():

            if not delete_player_id.value:
                return

            try:

                db.execute_query(
                    """
                    DELETE FROM Player
                    WHERE Id = ?
                    AND ClubId = ?
                    """,
                    (
                        int(delete_player_id.value),
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
                    f'[DELETE PLAYER ERROR] {type(e).__name__}: {e}'
                )

        delete_button.on(
            'click',
            delete_player
        )

        # =========================================================
        # Search
        # =========================================================

        search.on(
            'update:model-value',
            lambda e: refresh_players()
        )

        refresh_button.on(
            'click',
            refresh_players
        )

        # =========================================================
        # Initial load
        # =========================================================

        refresh_players()