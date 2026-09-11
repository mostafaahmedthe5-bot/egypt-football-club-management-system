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
    # البيانات المساعدة
    # =========================================================

    categories = db.fetch_all(
        """
        SELECT
            Id,
            TeamCategoryNameAR,
            TeamCategoryNameEN
        FROM TeamCategory
        ORDER BY Id
        """
    )

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

            /* =================================================
               GLOBAL
               ================================================= */

            .teams-page {
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

            .teams-wrapper {
                width: 100%;
                max-width: 1500px;
                margin: 0 auto;
            }

            /* =================================================
               HEADER
               ================================================= */

            .teams-header {
                width: 100%;

                position: relative;
                overflow: hidden;

                border-radius: 24px;

                padding: 28px 30px;

                background:
                    linear-gradient(
                        135deg,
                        #0f172a 0%,
                        #172554 55%,
                        #1e3a8a 100%
                    );

                border:
                    1px solid
                    rgba(255,255,255,.08);

                box-shadow:
                    0 14px 35px
                    rgba(15,23,42,.13);
            }

            .teams-header::before {
                content: "";

                position: absolute;

                width: 280px;
                height: 280px;

                top: -170px;
                left: -80px;

                border-radius: 50%;

                background:
                    rgba(255,255,255,.035);
            }

            .teams-header::after {
                content: "";

                position: absolute;

                width: 280px;
                height: 280px;

                bottom: -180px;
                right: -90px;

                border-radius: 50%;

                background:
                    rgba(56,189,248,.05);
            }

            .teams-header-content {
                position: relative;
                z-index: 2;
            }

            .teams-header-icon {
                width: 62px;
                height: 62px;

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

            .teams-header-title {
                color: white;

                font-size: 29px;

                font-weight: 900;

                line-height: 1.3;
            }

            .teams-header-club {
                color: #67e8f9;

                font-size: 19px;

                font-weight: 800;
            }

            .teams-header-en {
                color: #94a3b8;

                font-size: 10px;

                font-weight: 700;

                letter-spacing: 2px;
            }

            .teams-header-description {
                color: #cbd5e1;

                font-size: 13px;

                line-height: 1.8;
            }

            .teams-header-badge {
                display: inline-flex;

                align-items: center;

                gap: 8px;

                padding:
                    8px 14px;

                border-radius: 999px;

                background:
                    rgba(59,130,246,.10);

                border:
                    1px solid
                    rgba(96,165,250,.18);

                color: #dbeafe;

                font-size: 11px;

                font-weight: 800;
            }

            .teams-header-dot {
                width: 7px;
                height: 7px;

                border-radius: 50%;

                background: #60a5fa;
            }

            /* =================================================
               MAIN CARDS
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
               CARD HEADER
               ================================================= */

            .card-heading-icon {
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

            /* =================================================
               FIELD
               ================================================= */

            .field-label {
                color: #475569;

                font-size: 11px;

                font-weight: 850;
            }

            .team-field .q-field__control {
                min-height: 50px !important;

                border-radius: 13px !important;
            }

            .team-field input {
                font-size: 13px !important;

                font-weight: 650 !important;
            }

            /* =================================================
               SAVE BUTTON
               ================================================= */

            .save-team-button {
                min-height: 50px !important;

                border-radius: 13px !important;

                background:
                    #1d4ed8 !important;

                color: white !important;

                font-weight: 850 !important;

                padding:
                    0 24px !important;
            }

            /* =================================================
               LIST HEADER
               ================================================= */

            .teams-list-card {
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

            .teams-list-header {
                background: #f8fafc;

                border-bottom:
                    1px solid #e2e8f0;
            }

            .teams-count {
                min-width: 75px;

                text-align: center;

                background:
                    #eff6ff;

                color:
                    #1d4ed8;

                border:
                    1px solid #dbeafe;

                padding:
                    6px 11px;

                border-radius:
                    999px;

                font-size: 11px;

                font-weight: 850;
            }

            /* =================================================
               TEAM ROW
               ================================================= */

            .team-row {
                width: 100%;

                min-height: 82px;

                background: white;

                border-bottom:
                    1px solid #f1f5f9;

                padding:
                    14px 18px;
            }

            .team-row:last-child {
                border-bottom: none;
            }

            .team-avatar {
                width: 50px;
                height: 50px;

                flex-shrink: 0;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 15px;

                background:
                    linear-gradient(
                        135deg,
                        #0f172a,
                        #1e3a8a
                    );

                color: white;
            }

            .team-name {
                color: #0f172a;

                font-size: 14px;

                font-weight: 900;
            }

            .team-name-en {
                color: #94a3b8;

                font-size: 10px;

                font-weight: 600;
            }

            .team-meta {
                display: inline-flex;

                align-items: center;

                gap: 6px;

                background:
                    #f8fafc;

                border:
                    1px solid #e2e8f0;

                color:
                    #475569;

                padding:
                    6px 10px;

                border-radius:
                    9px;

                font-size: 10px;

                font-weight: 750;
            }

            .team-meta.sport {
                background:
                    #eff6ff;

                border-color:
                    #dbeafe;

                color:
                    #1d4ed8;
            }

            .team-meta.category {
                background:
                    #f0fdf4;

                border-color:
                    #dcfce7;

                color:
                    #15803d;
            }

            .team-id {
                color: #94a3b8;

                font-size: 9px;

                font-weight: 650;
            }

            .team-action {
                width: 38px !important;
                height: 38px !important;

                border-radius: 10px !important;

                color: #475569 !important;
            }

            .team-delete-action {
                color: #dc2626 !important;
            }

            /* =================================================
               EMPTY STATE
               ================================================= */

            .empty-state {
                min-height: 330px;
            }

            .empty-icon-box {
                width: 82px;
                height: 82px;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 22px;

                background:
                    #f8fafc;

                border:
                    1px solid #e2e8f0;
            }

            /* =================================================
               DIALOG
               ================================================= */

            .dialog-card {
                width: 500px;

                max-width: 95vw;

                border-radius: 22px;

                overflow: hidden;

                background: white;

                box-shadow:
                    0 20px 60px
                    rgba(15,23,42,.18);
            }

            .dialog-header {
                padding:
                    22px 24px;

                background:
                    linear-gradient(
                        135deg,
                        #0f172a,
                        #172554
                    );
            }

            .dialog-header-icon {
                width: 48px;
                height: 48px;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 14px;

                background:
                    rgba(255,255,255,.08);

                border:
                    1px solid
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

                font-weight: 600;
            }

            .dialog-body {
                padding:
                    24px;
            }

            .dialog-save {
                background:
                    #1d4ed8 !important;

                color: white !important;

                border-radius:
                    11px !important;

                font-weight:
                    850 !important;
            }

            /* =================================================
               DELETE DIALOG
               ================================================= */

            .delete-dialog {
                width: 420px;

                max-width: 95vw;

                border-radius: 21px;

                padding: 26px;
            }

            .delete-icon-box {
                width: 70px;
                height: 70px;

                display: flex;
                align-items: center;
                justify-content: center;

                margin: 0 auto;

                border-radius: 20px;

                background:
                    #fef2f2;

                border:
                    1px solid #fecaca;
            }

            .delete-title {
                color: #0f172a;

                font-size: 21px;

                font-weight: 900;
            }

            .delete-team-name {
                color: #1d4ed8;

                font-size: 15px;

                font-weight: 850;
            }

            .delete-warning {
                color: #64748b;

                font-size: 12px;

                line-height: 1.8;

                background:
                    #f8fafc;

                border:
                    1px solid #e2e8f0;

                border-radius: 13px;

                padding:
                    12px;
            }

            .delete-button {
                background:
                    #dc2626 !important;

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

                .teams-header {
                    padding: 24px;
                }

                .teams-header-title {
                    font-size: 25px;
                }

                .teams-header-club {
                    font-size: 17px;
                }
            }

            @media (max-width: 700px) {

                .team-row {
                    padding:
                        13px 12px;
                }

                .team-meta {
                    font-size: 9px;
                    padding:
                        5px 8px;
                }

                .team-avatar {
                    width: 44px;
                    height: 44px;
                }
            }

            @media (max-width: 600px) {

                .teams-page {
                    padding: 12px !important;
                }

                .teams-header {
                    padding: 20px;
                    border-radius: 18px;
                }

                .teams-header-title {
                    font-size: 22px;
                }

                .teams-header-description {
                    font-size: 11px;
                }

                .teams-list-card,
                .main-card {
                    border-radius: 17px;
                }

                .team-row {
                    min-height: 76px;
                }
            }

        </style>
        '''
    )

    # =========================================================
    # الصفحة
    # =========================================================

    with ui.column().classes(
        'teams-page w-full p-4 md:p-6 lg:p-8'
    ):

        with ui.column().classes(
            'teams-wrapper gap-6'
        ):

            # =================================================
            # HEADER
            # =================================================

            with ui.element(
                'div'
            ).classes(
                'teams-header'
            ):

                with ui.row().classes(
                    'teams-header-content w-full items-center justify-between flex-wrap gap-6'
                ):

                    with ui.row().classes(
                        'items-center gap-4'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'teams-header-icon'
                        ):

                            ui.icon(
                                'groups'
                            ).classes(
                                'text-3xl text-white'
                            )

                        with ui.column().classes(
                            'gap-1'
                        ):

                            ui.label(
                                'إدارة فرق النادي'
                            ).classes(
                                'teams-header-title'
                            )

                            ui.label(
                                club_name_ar
                            ).classes(
                                'teams-header-club'
                            )

                            if club_name_en:

                                ui.label(
                                    club_name_en
                                ).classes(
                                    'teams-header-en'
                                )

                            ui.label(
                                'إنشاء وإدارة فرق النادي وربط كل فريق بالفئة والرياضة المناسبة.'
                            ).classes(
                                'teams-header-description mt-2'
                            )

                    with ui.element(
                        'div'
                    ).classes(
                        'teams-header-badge'
                    ):

                        ui.element(
                            'span'
                        ).classes(
                            'teams-header-dot'
                        )

                        ui.label(
                            'Team Management'
                        )

            # =================================================
            # ADD TEAM
            # =================================================

            with ui.card().classes(
                'main-card p-5 md:p-6'
            ):

                with ui.row().classes(
                    'items-center gap-3 mb-6'
                ):

                    with ui.element(
                        'div'
                    ).classes(
                        'card-heading-icon bg-blue-50 text-blue-600'
                    ):

                        ui.icon(
                            'add_circle'
                        ).classes(
                            'text-xl'
                        )

                    with ui.column().classes(
                        'gap-0'
                    ):

                        ui.label(
                            'إضافة فريق جديد'
                        ).classes(
                            'card-title'
                        )

                        ui.label(
                            'أدخل بيانات الفريق وحدد الرياضة والفئة'
                        ).classes(
                            'card-subtitle mt-1'
                        )

                with ui.row().classes(
                    'w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4'
                ):

                    # =========================================
                    # Team Arabic
                    # =========================================

                    with ui.column().classes(
                        'w-full gap-2'
                    ):

                        ui.label(
                            'اسم الفريق بالعربي'
                        ).classes(
                            'field-label'
                        )

                        team_ar = ui.input(
                            placeholder='مثال: الفريق الأول'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'team-field w-full'
                        )

                    # =========================================
                    # Team English
                    # =========================================

                    with ui.column().classes(
                        'w-full gap-2'
                    ):

                        ui.label(
                            'اسم الفريق بالإنجليزي'
                        ).classes(
                            'field-label'
                        )

                        team_en = ui.input(
                            placeholder='Example: First Team'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'team-field w-full'
                        )

                    # =========================================
                    # Category
                    # =========================================

                    with ui.column().classes(
                        'w-full gap-2'
                    ):

                        ui.label(
                            'فئة الفريق'
                        ).classes(
                            'field-label'
                        )

                        team_category = ui.select(
                            category_options,
                            label='اختر فئة الفريق'
                        ).props(
                            'outlined rounded clearable'
                        ).classes(
                            'team-field w-full'
                        )

                    # =========================================
                    # Sport
                    # =========================================

                    with ui.column().classes(
                        'w-full gap-2'
                    ):

                        ui.label(
                            'الرياضة'
                        ).classes(
                            'field-label'
                        )

                        sport = ui.select(
                            sport_options,
                            label='اختر الرياضة'
                        ).props(
                            'outlined rounded clearable'
                        ).classes(
                            'team-field w-full'
                        )

                with ui.row().classes(
                    'w-full justify-end mt-6'
                ):

                    save_button = ui.button(
                        'حفظ الفريق',
                        icon='save'
                    ).props(
                        'unelevated no-caps'
                    ).classes(
                        'save-team-button'
                    )

            # =================================================
            # TEAMS CONTAINER
            # =================================================

            teams_container = ui.column().classes(
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

                    # =========================================
                    # Header
                    # =========================================

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
                                'dialog-header-icon'
                            ):

                                ui.icon(
                                    'edit'
                                ).classes(
                                    'text-xl text-white'
                                )

                            with ui.column().classes(
                                'gap-0'
                            ):

                                ui.label(
                                    'تعديل الفريق'
                                ).classes(
                                    'dialog-title'
                                )

                                ui.label(
                                    'تعديل بيانات الفريق الحالية'
                                ).classes(
                                    'dialog-subtitle mt-1'
                                )

                    # =========================================
                    # Body
                    # =========================================

                    with ui.column().classes(
                        'dialog-body'
                    ):

                        edit_id = ui.number(
                            'رقم الفريق'
                        ).props(
                            'outlined rounded readonly'
                        ).classes(
                            'w-full mb-3'
                        )

                        edit_team_ar = ui.input(
                            'اسم الفريق بالعربي'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'w-full mb-3'
                        )

                        edit_team_en = ui.input(
                            'اسم الفريق بالإنجليزي'
                        ).props(
                            'outlined rounded'
                        ).classes(
                            'w-full mb-3'
                        )

                        edit_category = ui.select(
                            category_options,
                            label='فئة الفريق'
                        ).props(
                            'outlined rounded clearable'
                        ).classes(
                            'w-full mb-3'
                        )

                        edit_sport = ui.select(
                            sport_options,
                            label='الرياضة'
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

            # =================================================
            # DELETE DIALOG
            # =================================================

            delete_dialog = ui.dialog()

            with delete_dialog:

                with ui.card().classes(
                    'delete-dialog'
                ):

                    with ui.element(
                        'div'
                    ).classes(
                        'delete-icon-box'
                    ):

                        ui.icon(
                            'delete_forever'
                        ).classes(
                            'text-3xl text-red-600'
                        )

                    ui.label(
                        'حذف الفريق'
                    ).classes(
                        'delete-title text-center mt-4'
                    )

                    delete_team_name = ui.label(
                        ''
                    ).classes(
                        'delete-team-name text-center mt-2'
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
                        'text-center text-slate-700 font-bold mt-4'
                    )

                    ui.label(
                        'سيتم حذف سجل الفريق من النادي. تأكد من عدم وجود بيانات مرتبطة تمنع الحذف.'
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

                        delete_button = ui.button(
                            'تأكيد الحذف',
                            icon='delete'
                        ).props(
                            'unelevated no-caps'
                        ).classes(
                            'delete-button'
                        )

            # =================================================
            # REFRESH TABLE
            # =================================================

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
                        'teams-list-card'
                    ):

                        # =====================================
                        # LIST HEADER
                        # =====================================

                        with ui.row().classes(
                            'teams-list-header w-full items-center justify-between p-5'
                        ):

                            with ui.row().classes(
                                'items-center gap-3'
                            ):

                                with ui.element(
                                    'div'
                                ).classes(
                                    'card-heading-icon bg-emerald-50 text-emerald-600'
                                ):

                                    ui.icon(
                                        'groups'
                                    ).classes(
                                        'text-xl'
                                    )

                                with ui.column().classes(
                                    'gap-0'
                                ):

                                    ui.label(
                                        'الفرق المسجلة'
                                    ).classes(
                                        'card-title'
                                    )

                                    ui.label(
                                        'جميع الفرق التابعة للنادي'
                                    ).classes(
                                        'card-subtitle mt-1'
                                    )

                            ui.label(
                                f'{len(teams)} فريق'
                            ).classes(
                                'teams-count'
                            )

                        # =====================================
                        # EMPTY STATE
                        # =====================================

                        if not teams:

                            with ui.column().classes(
                                'empty-state w-full items-center justify-center'
                            ):

                                with ui.element(
                                    'div'
                                ).classes(
                                    'empty-icon-box'
                                ):

                                    ui.icon(
                                        'groups'
                                    ).classes(
                                        'text-4xl text-slate-300'
                                    )

                                ui.label(
                                    'لا توجد فرق مسجلة'
                                ).classes(
                                    'text-slate-600 font-black text-lg mt-4'
                                )

                                ui.label(
                                    'يمكنك إضافة أول فريق من النموذج الموجود بالأعلى'
                                ).classes(
                                    'text-slate-400 text-sm mt-1'
                                )

                            return

                        # =====================================
                        # COLUMN HEADER
                        # =====================================

                        with ui.row().classes(
                            'w-full items-center px-5 py-3 bg-white border-b border-slate-100'
                        ):

                            ui.label(
                                'بيانات الفريق'
                            ).classes(
                                'text-xs font-black text-slate-400 flex-1'
                            )

                            ui.label(
                                'الفئة والرياضة'
                            ).classes(
                                'text-xs font-black text-slate-400 w-64 text-center'
                            )

                            ui.label(
                                'الإجراءات'
                            ).classes(
                                'text-xs font-black text-slate-400 w-24 text-center'
                            )

                        # =====================================
                        # TEAM ROWS
                        # =====================================

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

                            with ui.row().classes(
                                'team-row items-center gap-4'
                            ):

                                # =================================
                                # Team information
                                # =================================

                                with ui.row().classes(
                                    'items-center gap-4 flex-1 min-w-0'
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
                                        'gap-0 min-w-0'
                                    ):

                                        ui.label(
                                            team_name_ar
                                        ).classes(
                                            'team-name'
                                        )

                                        if team_name_en:

                                            ui.label(
                                                team_name_en
                                            ).classes(
                                                'team-name-en mt-1'
                                            )

                                        ui.label(
                                            f'ID: {team_id}'
                                        ).classes(
                                            'team-id mt-1'
                                        )

                                # =================================
                                # Category + Sport
                                # =================================

                                with ui.row().classes(
                                    'w-64 justify-center items-center gap-2 flex-wrap'
                                ):

                                    with ui.element(
                                        'div'
                                    ).classes(
                                        'team-meta category'
                                    ):

                                        ui.icon(
                                            'category'
                                        ).classes(
                                            'text-xs'
                                        )

                                        ui.label(
                                            category_name
                                        )

                                    with ui.element(
                                        'div'
                                    ).classes(
                                        'team-meta sport'
                                    ):

                                        ui.icon(
                                            'sports'
                                        ).classes(
                                            'text-xs'
                                        )

                                        ui.label(
                                            sport_name
                                        )

                                # =================================
                                # Actions
                                # =================================

                                with ui.row().classes(
                                    'w-24 justify-center items-center gap-1'
                                ):

                                    def open_edit(
                                        team_data=team
                                    ):

                                        edit_id.value = (
                                            team_data['Id']
                                        )

                                        edit_team_ar.value = (
                                            team_data['TeamAR']
                                            or ''
                                        )

                                        edit_team_en.value = (
                                            team_data['TeamEN']
                                            or ''
                                        )

                                        edit_category.value = (
                                            team_data[
                                                'Teamcatgoryid'
                                            ]
                                        )

                                        edit_sport.value = (
                                            team_data[
                                                'Sportid'
                                            ]
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
                                            or team_data['TeamEN']
                                            or 'هذا الفريق'
                                        )

                                        delete_dialog.open()

                                    ui.button(
                                        icon='edit',
                                        on_click=open_edit
                                    ).props(
                                        'flat round'
                                    ).classes(
                                        'team-action'
                                    ).tooltip(
                                        'تعديل الفريق'
                                    )

                                    ui.button(
                                        icon='delete',
                                        on_click=open_delete
                                    ).props(
                                        'flat round'
                                    ).classes(
                                        'team-action team-delete-action'
                                    ).tooltip(
                                        'حذف الفريق'
                                    )

            # =================================================
            # ADD TEAM
            # =================================================

            def add_team():

                team_ar_value = (
                    team_ar.value or ''
                ).strip()

                team_en_value = (
                    team_en.value or ''
                ).strip()

                if not team_ar_value:

                    ui.notify(
                        'من فضلك أدخل اسم الفريق بالعربي',
                        color='warning'
                    )

                    team_ar.run_method(
                        'focus'
                    )

                    return

                if not team_category.value:

                    ui.notify(
                        'من فضلك اختر فئة الفريق',
                        color='warning'
                    )

                    return

                if not sport.value:

                    ui.notify(
                        'من فضلك اختر الرياضة',
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
                        'تمت إضافة الفريق بنجاح',
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

            # =================================================
            # UPDATE TEAM
            # =================================================

            def update_team():

                if not edit_id.value:

                    ui.notify(
                        'لم يتم تحديد الفريق',
                        color='warning'
                    )

                    return

                team_ar_value = (
                    edit_team_ar.value or ''
                ).strip()

                team_en_value = (
                    edit_team_en.value or ''
                ).strip()

                if not team_ar_value:

                    ui.notify(
                        'من فضلك أدخل اسم الفريق بالعربي',
                        color='warning'
                    )

                    return

                if not edit_category.value:

                    ui.notify(
                        'من فضلك اختر فئة الفريق',
                        color='warning'
                    )

                    return

                if not edit_sport.value:

                    ui.notify(
                        'من فضلك اختر الرياضة',
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
                        'تم تعديل الفريق بنجاح',
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

            # =================================================
            # DELETE TEAM
            # =================================================

            def delete_team():

                if not delete_team_id.value:

                    ui.notify(
                        'لم يتم تحديد الفريق',
                        color='warning'
                    )

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
                        'تم حذف الفريق بنجاح',
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

            # =================================================
            # INITIAL LOAD
            # =================================================

            refresh_teams_table()