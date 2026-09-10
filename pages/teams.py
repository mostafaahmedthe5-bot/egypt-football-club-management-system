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
    # التحقق من النادي
    # =========================================================

    club = db.fetch_one(
        "SELECT Id, ClubNameAR FROM Club WHERE Id = ?",
        (club_id,)
    )

    if not club:
        ui.notify(
            'النادي غير موجود',
            color='negative'
        )
        ui.navigate.to('/select_club')
        return

    # =========================================================
    # البيانات المساعدة
    # =========================================================

    categories = db.fetch_all(
        """
        SELECT Id, TeamCategoryNameAR, TeamCategoryNameEN
        FROM TeamCategory
        ORDER BY Id
        """
    )

    sports = db.fetch_all(
        """
        SELECT Id, SportNameAR, SportNameEN
        FROM Sport
        ORDER BY Id
        """
    )

    category_options = {
        row['Id']: (
            row['TeamCategoryNameAR']
            or row['TeamCategoryNameEN']
            or str(row['Id'])
        )
        for row in categories
    }

    sport_options = {
        row['Id']: (
            row['SportNameAR']
            or row['SportNameEN']
            or str(row['Id'])
        )
        for row in sports
    }

    # =========================================================
    # CSS
    # =========================================================

    ui.add_head_html(
        '''
        <style>

            .teams-page {
                min-height: 100vh;
                background:
                    radial-gradient(
                        circle at top right,
                        rgba(245,158,11,.07),
                        transparent 25%
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

            .team-row {
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                transition: all .2s ease;
            }

            .team-row:hover {
                background: #f8fafc;
                border-color: #cbd5e1;
                transform: translateY(-1px);
            }

            .team-avatar {
                width: 48px;
                height: 48px;
                border-radius: 14px;
                background: linear-gradient(
                    135deg,
                    #0f172a,
                    #1e3a8a
                );
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
            }

        </style>
        '''
    )

    # =========================================================
    # الصفحة
    # =========================================================

    with ui.column().classes(
        'teams-page w-full p-4 md:p-6 lg:p-8 gap-6'
    ):

        # =====================================================
        # Header
        # =====================================================

        with ui.row().classes(
            'w-full items-center justify-between'
        ):

            with ui.column().classes('gap-1'):

                ui.label(
                    '⚽ إدارة الفرق الرياضية'
                ).classes(
                    'page-title'
                )

                ui.label(
                    club['ClubNameAR'] or 'النادي'
                ).classes(
                    'text-blue-800 font-bold text-lg'
                )

                ui.label(
                    'إدارة الفرق التابعة للنادي'
                ).classes(
                    'text-slate-500 text-sm'
                )

            with ui.element('div').classes(
                'bg-blue-50 text-blue-700 px-4 py-2 '
                'rounded-full font-bold'
            ):
                ui.label('Team')

        # =====================================================
        # Form
        # =====================================================

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
                    ui.icon('add_circle').classes(
                        'text-xl text-blue-600'
                    )

                ui.label(
                    'إضافة فريق جديد'
                ).classes(
                    'text-xl font-black text-slate-900'
                )

            with ui.row().classes(
                'w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4'
            ):

                with ui.column().classes('w-full'):
                    ui.label(
                        'اسم الفريق (عربي)'
                    ).classes(
                        'field-label'
                    )

                    team_ar = ui.input(
                        placeholder='مثال: الفريق الأول'
                    ).props(
                        'outlined rounded'
                    ).classes(
                        'w-full'
                    )

                with ui.column().classes('w-full'):
                    ui.label(
                        'اسم الفريق (إنجليزي)'
                    ).classes(
                        'field-label'
                    )

                    team_en = ui.input(
                        placeholder='Example: First Team'
                    ).props(
                        'outlined rounded'
                    ).classes(
                        'w-full'
                    )

                with ui.column().classes('w-full'):
                    ui.label(
                        'TeamCategory'
                    ).classes(
                        'field-label'
                    )

                    team_category = ui.select(
                        category_options,
                        label='اختر TeamCategory'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

                with ui.column().classes('w-full'):
                    ui.label(
                        'Sport'
                    ).classes(
                        'field-label'
                    )

                    sport = ui.select(
                        sport_options,
                        label='اختر Sport'
                    ).props(
                        'outlined rounded clearable'
                    ).classes(
                        'w-full'
                    )

            with ui.row().classes(
                'w-full justify-end mt-5'
            ):

                save_button = ui.button(
                    'حفظ الفريق',
                    icon='save'
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'bg-blue-700 text-white rounded-xl px-6 py-3 font-bold'
                )

        # =====================================================
        # Teams table container
        # =====================================================

        teams_container = ui.column().classes(
            'w-full'
        )

        # =====================================================
        # Dialog for edit
        # =====================================================

        edit_dialog = ui.dialog()

        with edit_dialog:
            with ui.card().classes(
                'w-[500px] max-w-[95vw] p-6 rounded-2xl'
            ):

                ui.label(
                    'تعديل الفريق'
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

                edit_team_ar = ui.input(
                    'اسم الفريق (عربي)'
                ).props(
                    'outlined rounded'
                ).classes(
                    'w-full mb-3'
                )

                edit_team_en = ui.input(
                    'اسم الفريق (إنجليزي)'
                ).props(
                    'outlined rounded'
                ).classes(
                    'w-full mb-3'
                )

                edit_category = ui.select(
                    category_options,
                    label='TeamCategory'
                ).props(
                    'outlined rounded clearable'
                ).classes(
                    'w-full mb-3'
                )

                edit_sport = ui.select(
                    sport_options,
                    label='Sport'
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

        # =====================================================
        # Delete Dialog
        # =====================================================

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
                    'حذف الفريق'
                ).classes(
                    'text-2xl font-black text-center mt-3'
                )

                delete_team_name = ui.label(
                    ''
                ).classes(
                    'text-slate-500 text-center mt-2'
                )

                delete_team_id = ui.number(
                    'Id'
                ).props(
                    'readonly'
                ).classes(
                    'hidden'
                )

                ui.label(
                    'هل أنت متأكد من حذف هذا الفريق؟'
                ).classes(
                    'text-center text-slate-600 mt-3'
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

        # =====================================================
        # Refresh table
        # =====================================================

        def refresh_teams_table():
            teams_container.clear()

            teams = db.fetch_all(
                """
                SELECT
                    t.Id,
                    t.TeamAR,
                    t.TeamEN,
                    t.Teamcatgoryid,
                    t.Sportid,
                    tc.TeamCategoryNameAR,
                    tc.TeamCategoryNameEN,
                    s.SportNameAR,
                    s.SportNameEN
                FROM Team t
                LEFT JOIN TeamCategory tc
                    ON tc.Id = t.Teamcatgoryid
                LEFT JOIN Sport s
                    ON s.Id = t.Sportid
                WHERE t.Clubid = ?
                ORDER BY t.Id DESC
                """,
                (club_id,)
            )

            with teams_container:

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
                                'w-11 h-11 rounded-xl bg-emerald-50 '
                                'flex items-center justify-center'
                            ):
                                ui.icon(
                                    'groups'
                                ).classes(
                                    'text-xl text-emerald-600'
                                )

                            ui.label(
                                'الفرق المسجلة'
                            ).classes(
                                'text-xl font-black text-slate-900'
                            )

                        ui.label(
                            f'{len(teams)} فريق'
                        ).classes(
                            'bg-slate-100 text-slate-600 '
                            'px-3 py-1 rounded-full text-xs font-bold'
                        )

                    if not teams:

                        with ui.column().classes(
                            'w-full items-center py-12'
                        ):

                            ui.icon(
                                'groups'
                            ).classes(
                                'text-6xl text-slate-300'
                            )

                            ui.label(
                                'لا توجد فرق مسجلة'
                            ).classes(
                                'text-slate-500 font-bold text-lg mt-4'
                            )

                            ui.label(
                                'يمكنك إضافة أول فريق من النموذج أعلاه'
                            ).classes(
                                'text-slate-400 text-sm mt-1'
                            )

                        return

                    with ui.column().classes(
                        'w-full gap-3'
                    ):

                        for team in teams:

                            team_id = team['Id']

                            team_name_ar = (
                                team['TeamAR']
                                or 'بدون اسم'
                            )

                            team_name_en = (
                                team['TeamEN']
                                or ''
                            )

                            category_name = (
                                team['TeamCategoryNameAR']
                                or team['TeamCategoryNameEN']
                                or 'غير محدد'
                            )

                            sport_name = (
                                team['SportNameAR']
                                or team['SportNameEN']
                                or 'غير محدد'
                            )

                            with ui.element('div').classes(
                                'team-row w-full p-4'
                            ):

                                with ui.row().classes(
                                    'w-full items-center '
                                    'justify-between gap-4'
                                ):

                                    # =================================
                                    # Team info
                                    # =================================

                                    with ui.row().classes(
                                        'items-center gap-4'
                                    ):

                                        with ui.element(
                                            'div'
                                        ).classes(
                                            'team-avatar'
                                        ):
                                            ui.icon(
                                                'sports_soccer'
                                            ).classes(
                                                'text-2xl'
                                            )

                                        with ui.column().classes(
                                            'gap-0'
                                        ):

                                            ui.label(
                                                team_name_ar
                                            ).classes(
                                                'text-lg font-black '
                                                'text-slate-800'
                                            )

                                            if team_name_en:
                                                ui.label(
                                                    team_name_en
                                                ).classes(
                                                    'text-xs text-slate-400 '
                                                    'mt-1'
                                                )

                                    # =================================
                                    # Details
                                    # =================================

                                    with ui.row().classes(
                                        'items-center gap-2 flex-wrap'
                                    ):

                                        ui.badge(
                                            category_name
                                        ).props(
                                            'outline'
                                        )

                                        ui.badge(
                                            sport_name
                                        ).props(
                                            'outline'
                                        )

                                    # =================================
                                    # Actions
                                    # =================================

                                    with ui.row().classes(
                                        'items-center gap-1'
                                    ):

                                        def open_edit(
                                            team_data=team
                                        ):

                                            edit_id.value = team_data['Id']
                                            edit_team_ar.value = (
                                                team_data['TeamAR']
                                                or ''
                                            )
                                            edit_team_en.value = (
                                                team_data['TeamEN']
                                                or ''
                                            )
                                            edit_category.value = (
                                                team_data['Teamcatgoryid']
                                            )
                                            edit_sport.value = (
                                                team_data['Sportid']
                                            )

                                            edit_dialog.open()

                                        def open_delete(
                                            team_data=team
                                        ):

                                            delete_team_id.value = (
                                                team_data['Id']
                                            )

                                            delete_team_name.text = (
                                                team_data['TeamAR']
                                                or 'هذا الفريق'
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
        # Add Team
        # =========================================================

        def add_team():

            team_ar_value = (
                team_ar.value or ''
            ).strip()

            team_en_value = (
                team_en.value or ''
            ).strip()

            if not team_ar_value:

                ui.notify(
                    'من فضلك أدخل اسم الفريق (عربي)',
                    color='warning'
                )
                return

            try:

                db.execute_query(
                    """
                    INSERT INTO Team
                    (
                        TeamAR,
                        TeamEN,
                        Clubid,
                        Teamcatgoryid,
                        Sportid
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        team_ar_value,
                        team_en_value,
                        club_id,
                        team_category.value,
                        sport.value
                    )
                )

                ui.notify(
                    'تمت إضافة الفريق بنجاح!',
                    color='positive'
                )

                team_ar.value = ''
                team_en.value = ''
                team_category.value = None
                sport.value = None

                refresh_teams_table()

            except Exception as e:

                ui.notify(
                    'حدث خطأ أثناء إضافة الفريق',
                    color='negative'
                )

                print(
                    f'[ADD TEAM ERROR] {type(e).__name__}: {e}'
                )

        save_button.on(
            'click',
            add_team
        )

        # =========================================================
        # Update Team
        # =========================================================

        def update_team():

            if not edit_id.value:
                return

            team_ar_value = (
                edit_team_ar.value or ''
            ).strip()

            team_en_value = (
                edit_team_en.value or ''
            ).strip()

            if not team_ar_value:

                ui.notify(
                    'من فضلك أدخل اسم الفريق (عربي)',
                    color='warning'
                )
                return

            try:

                db.execute_query(
                    """
                    UPDATE Team
                    SET
                        TeamAR = ?,
                        TeamEN = ?,
                        Teamcatgoryid = ?,
                        Sportid = ?
                    WHERE Id = ?
                    AND Clubid = ?
                    """,
                    (
                        team_ar_value,
                        team_en_value,
                        edit_category.value,
                        edit_sport.value,
                        int(edit_id.value),
                        club_id
                    )
                )

                ui.notify(
                    'تم تعديل الفريق بنجاح!',
                    color='positive'
                )

                edit_dialog.close()

                refresh_teams_table()

            except Exception as e:

                ui.notify(
                    'حدث خطأ أثناء تعديل الفريق',
                    color='negative'
                )

                print(
                    f'[UPDATE TEAM ERROR] {type(e).__name__}: {e}'
                )

        update_button.on(
            'click',
            update_team
        )

        # =========================================================
        # Delete Team
        # =========================================================

        def delete_team():

            if not delete_team_id.value:
                return

            try:

                db.execute_query(
                    """
                    DELETE FROM Team
                    WHERE Id = ?
                    AND Clubid = ?
                    """,
                    (
                        int(delete_team_id.value),
                        club_id
                    )
                )

                ui.notify(
                    'تم حذف الفريق بنجاح!',
                    color='positive'
                )

                delete_dialog.close()

                refresh_teams_table()

            except Exception as e:

                ui.notify(
                    'لا يمكن حذف الفريق حالياً',
                    color='negative'
                )

                print(
                    f'[DELETE TEAM ERROR] {type(e).__name__}: {e}'
                )

        delete_button.on(
            'click',
            delete_team
        )

        # =========================================================
        # Initial load
        # =========================================================

        refresh_teams_table()