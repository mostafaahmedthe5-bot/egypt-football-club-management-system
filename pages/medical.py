from nicegui import app, ui
import database as db

GRASS_BACKGROUND = "https://imgs.search.brave.com/sJbzVVnKH_yP_2G9TeAfuOc7BqdkM9hIYavynKjmqHk/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudmVjdG9yZWV6eXkuY29tL3N5c3RlbS9yZXNvdXJjZXMvdGh1/bWJuYWlscy8wMDgvNDU5Lzc3Ni9zbWFs/bC9ncmVlbi1uYXR1/cmFsLW9yZ2FuaWMtZ3Jhc3MtYmFja2dyb3VuZC1hbmQtdGV4/dHVyZS12ZWN0b3Iu/anBn"


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
        'بتروجيت': 'https://assets.footylogos.com/logos/petrojet-fc/petrojet-logo-footylogos.png',
        'كهرباء الإسماعيلية': None,
    }
    return logos.get(club_name)


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
        (club_id,),
    )

    if not club:
        ui.notify('النادي غير موجود', color='negative')
        ui.navigate.to('/select_club')
        return

    club_name_ar = club['ClubNameAR'] or 'النادي'
    club_name_en = club['ClubNameEN'] or ''
    club_logo = get_club_logo_url(club_name_ar)

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
        row['Id']: (
            row['MedicalReportStateNameAR']
            or row['MedicalReportStateNameEN']
            or str(row['Id'])
        )
        for row in medical_states
    }

    # =========================================================
    # CSS
    # =========================================================
    ui.add_head_html(f'''
        <style>
            /* GLOBAL */
            .medical-page {{
                direction: rtl;
                min-height: 100vh;
                width: 100%;
                background: linear-gradient(180deg, #f0fdf4 0%, #f8fafc 42%, #f1f5f9 100%);
            }}
            .medical-wrapper {{
                width: 100%;
                max-width: 1500px;
                margin: 0 auto;
            }}

            /* FOOTBALL GRASS CARDS */
            .main-card, .stat-card, .filter-card, .table-card {{
                background-image: linear-gradient(rgba(255,255,255,.88), rgba(255,255,255,.88)), url("{GRASS_BACKGROUND}");
                background-size: cover;
                background-position: center;
                background-repeat: repeat;
                border: 1px solid rgba(22,163,74,.18);
                box-shadow: 0 10px 28px rgba(15,23,42,.055);
            }}

            /* FOOTBALL PITCH EFFECT */
            .football-card {{
                position: relative;
                overflow: hidden;
            }}
            .football-card::before {{
                content: "";
                position: absolute;
                width: 180px;
                height: 180px;
                border: 2px solid rgba(22,163,74,.12);
                border-radius: 50%;
                left: -75px;
                bottom: -90px;
                pointer-events: none;
            }}
            .football-card::after {{
                content: "";
                position: absolute;
                width: 260px;
                height: 90px;
                border: 2px solid rgba(22,163,74,.10);
                border-radius: 50%;
                right: -100px;
                top: -45px;
                transform: rotate(-8deg);
                pointer-events: none;
            }}
            .football-card > * {{
                position: relative;
                z-index: 2;
            }}

            /* HEADER */
            .medical-header {{
                width: 100%;
                background: linear-gradient(135deg, #064e3b 0%, #065f46 45%, #0f766e 100%);
                border-radius: 24px;
                padding: 28px 30px;
                overflow: hidden;
                position: relative;
                box-shadow: 0 16px 38px rgba(6,78,59,.22);
            }}
            .medical-header::before {{
                content: "";
                position: absolute;
                width: 340px;
                height: 340px;
                top: -220px;
                left: -80px;
                border: 2px solid rgba(255,255,255,.07);
                border-radius: 50%;
            }}
            .medical-header::after {{
                content: "";
                position: absolute;
                width: 280px;
                height: 280px;
                bottom: -190px;
                right: -90px;
                border: 2px solid rgba(255,255,255,.07);
                border-radius: 50%;
            }}
            .pitch-line {{
                position: absolute;
                width: 180px;
                height: 180px;
                border: 2px solid rgba(255,255,255,.06);
                border-radius: 50%;
                right: 18%;
                top: -115px;
                pointer-events: none;
            }}
            .medical-header-content {{
                position: relative;
                z-index: 3;
            }}
            .medical-header-icon {{
                width: 64px;
                height: 64px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 18px;
                background: rgba(255,255,255,.10);
                border: 1px solid rgba(255,255,255,.15);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,.03);
                padding: 6px;
            }}
            .medical-header-title {{
                color: white;
                font-size: 29px;
                font-weight: 900;
                line-height: 1.3;
            }}
            .medical-header-club {{
                color: #bbf7d0;
                font-size: 19px;
                font-weight: 850;
            }}
            .medical-header-en {{
                color: #a7f3d0;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 2px;
            }}
            .medical-header-description {{
                color: #d1fae5;
                font-size: 13px;
                line-height: 1.8;
            }}
            .medical-header-badge {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 9px 15px;
                border-radius: 999px;
                color: #dcfce7;
                background: rgba(255,255,255,.08);
                border: 1px solid rgba(255,255,255,.15);
                font-size: 11px;
                font-weight: 850;
                backdrop-filter: blur(5px);
            }}
            .medical-header-badge-dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #4ade80;
                box-shadow: 0 0 0 5px rgba(74,222,128,.12);
            }}

            /* FOOTBALL DECORATION */
            .football-decoration {{
                width: 72px;
                height: 72px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                background: rgba(255,255,255,.07);
                border: 1px solid rgba(255,255,255,.12);
                margin-left: 8px;
            }}
            .football-decoration .q-icon {{
                font-size: 38px;
                color: white;
            }}

            /* STATISTICS */
            .stat-card {{
                width: 100%;
                min-height: 145px;
                border-radius: 19px;
                position: relative;
                overflow: hidden;
                transition: transform .2s ease, box-shadow .2s ease;
            }}
            .stat-card:hover {{
                transform: translateY(-3px);
                box-shadow: 0 14px 30px rgba(15,23,42,.10);
            }}
            .stat-card-stripe {{
                position: absolute;
                top: 0; right: 0; left: 0;
                height: 5px;
                background: #16a34a;
                z-index: 4;
            }}
            .stat-card.total .stat-card-stripe {{ background: linear-gradient(90deg, #166534, #22c55e); }}
            .stat-card.medical .stat-card-stripe {{ background: linear-gradient(90deg, #059669, #34d399); }}
            
            .stat-icon {{
                width: 54px;
                height: 54px;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: rgba(220,252,231,.88);
                border: 1px solid #bbf7d0;
            }}
            .stat-label {{ color: #475569; font-size: 12px; font-weight: 800; }}
            .stat-number {{ color: #064e3b; font-size: 34px; line-height: 1; font-weight: 950; }}
            .stat-description {{ color: #64748b; font-size: 10px; font-weight: 650; }}

            /* FILTER */
            .filter-card {{ width: 100%; border-radius: 19px; position: relative; overflow: hidden; }}
            .filter-label {{ color: #166534; font-size: 11px; font-weight: 850; }}
            .filter-input .q-field__control, .filter-select .q-field__control {{
                min-height: 50px !important;
                background: rgba(248,250,252,.92);
                border-radius: 13px !important;
            }}
            .filter-input .q-field__native, .filter-select .q-field__native {{ font-weight: 650; }}
            .refresh-button {{
                min-height: 50px !important;
                border-radius: 13px !important;
                font-weight: 850 !important;
                background: #166534 !important;
                box-shadow: 0 6px 14px rgba(22,101,52,.20);
            }}
            .refresh-button:hover {{ background: #14532d !important; }}

            /* TABLE */
            .table-card {{ width: 100%; border-radius: 21px; overflow: hidden; position: relative; }}
            .table-header {{
                background: rgba(220,252,231,.88);
                border-bottom: 1px solid rgba(22,101,52,.14);
                min-height: 58px;
            }}
            .table-column-title {{ color: #166534; font-size: 11px; font-weight: 900; }}

            /* PLAYER ROW */
            .player-row {{
                width: 100%;
                min-height: 76px;
                background: rgba(255,255,255,.78);
                border-bottom: 1px solid rgba(22,163,74,.10);
                transition: background .18s ease, transform .18s ease;
            }}
            .player-row:hover {{
                background: rgba(240,253,244,.94);
                transform: translateX(-2px);
            }}
            .player-row:last-child {{ border-bottom: none; }}
            .player-avatar {{
                width: 48px;
                height: 48px;
                flex-shrink: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                background: linear-gradient(145deg, #dcfce7, #bbf7d0);
                border: 2px solid rgba(22,163,74,.18);
                box-shadow: 0 4px 10px rgba(22,101,52,.10);
            }}
            .player-name {{ color: #0f172a; font-size: 13px; font-weight: 900; }}
            .player-id {{ color: #64748b; font-size: 10px; font-weight: 650; }}
            .medical-status {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-width: 110px;
                min-height: 32px;
                padding: 5px 12px;
                border-radius: 999px;
                background: rgba(240,253,244,.94);
                border: 1px solid #bbf7d0;
                color: #166534;
                font-size: 11px;
                font-weight: 850;
                box-shadow: 0 3px 8px rgba(22,101,52,.06);
            }}
            .edit-button {{
                width: 38px !important;
                height: 38px !important;
                border-radius: 11px !important;
                color: #166534 !important;
                background: rgba(220,252,231,.70) !important;
            }}
            .edit-button:hover {{ background: #dcfce7 !important; }}

            /* EMPTY */
            .empty-state {{ min-height: 320px; position: relative; overflow: hidden; }}
            .empty-state-icon {{
                width: 82px;
                height: 82px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                background: rgba(220,252,231,.90);
                border: 2px solid #bbf7d0;
            }}

            /* DIALOG */
            .medical-dialog {{
                width: 470px;
                max-width: 95vw;
                border-radius: 22px;
                background: white;
                overflow: hidden;
                box-shadow: 0 25px 70px rgba(15,23,42,.22);
            }}
            .dialog-header {{
                padding: 22px 24px;
                background: linear-gradient(135deg, #064e3b, #166534);
                position: relative;
                overflow: hidden;
            }}
            .dialog-header::after {{
                content: "";
                position: absolute;
                width: 130px;
                height: 130px;
                border: 2px solid rgba(255,255,255,.07);
                border-radius: 50%;
                left: -55px;
                top: -55px;
            }}
            .dialog-icon {{
                width: 48px;
                height: 48px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 14px;
                background: rgba(255,255,255,.10);
                border: 1px solid rgba(255,255,255,.14);
            }}
            .dialog-title {{ color: white; font-size: 19px; font-weight: 900; }}
            .dialog-subtitle {{ color: #bbf7d0; font-size: 11px; }}
            .dialog-body {{ padding: 24px; }}
            .dialog-save {{
                background: #15803d !important;
                color: white !important;
                border-radius: 11px !important;
                font-weight: 850 !important;
            }}

            /* FOOTBALL STRIP */
            .football-strip {{
                height: 5px;
                width: 100%;
                background: repeating-linear-gradient(90deg, #166534 0px, #166534 45px, #22c55e 45px, #22c55e 90px);
                border-radius: 999px;
            }}

            /* SCROLLBAR */
            ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
            ::-webkit-scrollbar-track {{ background: transparent; }}
            ::-webkit-scrollbar-thumb {{ background: #86efac; border-radius: 999px; }}

            /* RESPONSIVE */
            @media (max-width: 900px) {{
                .medical-header {{ padding: 24px; }}
                .medical-header-title {{ font-size: 25px; }}
                .medical-header-club {{ font-size: 17px; }}
            }}
            @media (max-width: 600px) {{
                .medical-page {{ padding: 12px !important; }}
                .medical-header {{ border-radius: 18px; padding: 20px; }}
                .medical-header-title {{ font-size: 22px; }}
                .medical-header-description {{ font-size: 12px; }}
                .stat-card {{ min-height: 132px; border-radius: 16px; }}
                .main-card, .filter-card, .table-card {{ border-radius: 17px; }}
                .player-row {{ padding: 10px 8px; }}
                .medical-status {{ min-width: auto; font-size: 10px; padding: 5px 9px; }}
                .player-avatar {{ width: 42px; height: 42px; }}
            }}
        </style>
    ''')

    # =========================================================
    # الصفحة
    # =========================================================
    with ui.column().classes('medical-page w-full p-4 md:p-6 lg:p-8'):
        with ui.column().classes('medical-wrapper gap-6'):

            # =====================================================
            # HEADER
            # =====================================================
            with ui.element('div').classes('medical-header'):
                ui.element('div').classes('pitch-line')
                with ui.row().classes(
                    'medical-header-content w-full items-center justify-between flex-wrap gap-6'
                ):
                    with ui.row().classes('items-center gap-4'):
                        with ui.element('div').classes('medical-header-icon'):
                            if club_logo:
                                ui.image(club_logo).classes(
                                    'w-full h-full object-contain'
                                )
                            else:
                                ui.icon('sports_soccer').classes(
                                    'text-3xl text-white'
                                )
                        with ui.column().classes('gap-1'):
                            ui.label('الإدارة الطبية للاعبين').classes(
                                'medical-header-title'
                            )
                            ui.label(club_name_ar).classes(
                                'medical-header-club'
                            )
                            if club_name_en:
                                ui.label(club_name_en.upper()).classes(
                                    'medical-header-en'
                                )
                            ui.label(
                                'متابعة الحالة الطبية والجاهزية الصحية لفريق النادي'
                            ).classes('medical-header-description')

                    with ui.row().classes('items-center gap-3'):
                        with ui.element('div').classes('football-decoration'):
                            ui.icon('sports_soccer')
                        with ui.element('div').classes('medical-header-badge'):
                            ui.element('span').classes(
                                'medical-header-badge-dot'
                            )
                            ui.label('النظام الطبي للفريق')

            # =====================================================
            # FOOTBALL STRIP
            # =====================================================
            ui.element('div').classes('football-strip')

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
                    (club_id,),
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
                (club_id,),
            )

            with ui.row().classes(
                'w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4'
            ):
                # Total
                with ui.card().classes('stat-card football-card total p-5'):
                    ui.element('div').classes('stat-card-stripe')
                    with ui.row().classes(
                        'w-full items-center justify-between'
                    ):
                        with ui.column().classes('gap-2'):
                            ui.label('إجمالي اللاعبين').classes('stat-label')
                            ui.label(str(players_count)).classes('stat-number')
                        with ui.element('div').classes('stat-icon'):
                            ui.icon('groups').classes('text-2xl text-green-700')
                    ui.label('جميع لاعبي الفريق المسجلين بالنادي').classes(
                        'stat-description mt-4'
                    )

                # Medical States
                for state in state_counts[:3]:
                    state_name = (
                        state['MedicalReportStateNameAR']
                        or state['MedicalReportStateNameEN']
                        or 'غير محدد'
                    )
                    state_count = state['PlayerCount'] or 0

                    with ui.card().classes(
                        'stat-card football-card medical p-5'
                    ):
                        ui.element('div').classes('stat-card-stripe')
                        with ui.row().classes(
                            'w-full items-center justify-between'
                        ):
                            with ui.column().classes('gap-2'):
                                ui.label(state_name).classes('stat-label')
                                ui.label(str(state_count)).classes(
                                    'stat-number'
                                )
                            with ui.element('div').classes('stat-icon'):
                                ui.icon('health_and_safety').classes(
                                    'text-2xl text-green-700'
                                )
                        ui.label('لاعب').classes('stat-description mt-4')

            # =====================================================
            # FILTER
            # =====================================================
            with ui.card().classes('filter-card football-card p-5'):
                with ui.row().classes('w-full items-end gap-4 flex-wrap'):
                    with ui.column().classes('gap-2 flex-1 min-w-[220px]'):
                        ui.label('البحث عن لاعب').classes('filter-label')
                        with ui.row().classes('w-full items-center'):
                            ui.icon('search').classes(
                                'text-lg text-green-700 mr-2'
                            )
                            search = (
                                ui.input(placeholder='ابحث باسم اللاعب...')
                                .props('outlined rounded clearable')
                                .classes('filter-input w-full')
                            )

                    with ui.column().classes('gap-2 min-w-[220px]'):
                        ui.label('الحالة الطبية').classes('filter-label')
                        status_filter_options = {'all': 'كل الحالات'}
                        for state in medical_states:
                            status_filter_options[state['Id']] = (
                                state['MedicalReportStateNameAR']
                                or state['MedicalReportStateNameEN']
                                or str(state['Id'])
                            )

                        status_filter = (
                            ui.select(status_filter_options, value='all')
                            .props('outlined rounded')
                            .classes('filter-select w-full')
                        )

                    refresh_button = (
                        ui.button('تحديث البيانات', icon='refresh')
                        .props('unelevated no-caps')
                        .classes('refresh-button text-white')
                    )

            # =====================================================
            # Players Container & Logic
            # =====================================================
            players_container = ui.column().classes('w-full')

            # State for dialog handling
            current_player_id = {'value': None}

            # =====================================================
            # Edit Dialog
            # =====================================================
            edit_dialog = ui.dialog()
            with edit_dialog:
                with ui.card().classes('medical-dialog p-0'):
                    with ui.element('div').classes('dialog-header'):
                        with ui.row().classes('items-center gap-3'):
                            with ui.element('div').classes('dialog-icon'):
                                ui.icon('edit_note').classes(
                                    'text-2xl text-white'
                                )
                            with ui.column().classes('gap-0'):
                                ui.label('تعديل الحالة الطبية').classes(
                                    'dialog-title'
                                )
                                player_dialog_name = ui.label('').classes(
                                    'dialog-subtitle'
                                )

                    with ui.column().classes('dialog-body gap-4 w-full'):
                        dialog_status_select = (
                            ui.select(medical_options, label='الحالة الطبية')
                            .props('outlined rounded')
                            .classes('w-full')
                        )

                        def save_medical_status():
                            if (
                                current_player_id['value']
                                and dialog_status_select.value
                            ):
                                db.execute(
                                    """
                                    UPDATE Player 
                                    SET MedicalReportStatueId = ? 
                                    WHERE Id = ? AND ClubId = ?
                                    """,
                                    (
                                        dialog_status_select.value,
                                        current_player_id['value'],
                                        club_id,
                                    ),
                                )
                                ui.notify(
                                    'تم تحديث الحالة الطبية بنجاح',
                                    color='positive',
                                )
                                edit_dialog.close()
                                render_players()

                        with ui.row().classes('w-full justify-end gap-2 mt-2'):
                            ui.button(
                                'إلغاء', on_click=edit_dialog.close
                            ).props('flat')
                            ui.button(
                                'حفظ', on_click=save_medical_status
                            ).classes('dialog-save')

            def open_edit(player):
                current_player_id['value'] = player['Id']
                player_dialog_name.text = (
                    player['PlayerNameAR']
                    or player['PlayerNameEN']
                    or 'اسم اللاعب'
                )
                dialog_status_select.value = player['MedicalReportStatueId']
                edit_dialog.open()

            def render_players():
                players_container.clear()

                query = """
                    SELECT 
                        p.Id,
                        p.PlayerNameAR,
                        p.PlayerNameEN,
                        p.MedicalReportStatueId,
                        mrs.MedicalReportStateNameAR,
                        mrs.MedicalReportStateNameEN
                    FROM Player p
                    LEFT JOIN MedicalReportState mrs ON mrs.Id = p.MedicalReportStatueId
                    WHERE p.ClubId = ?
                """
                params = [club_id]

                if search.value:
                    query += """
                        AND (
                            p.PlayerNameAR LIKE ? 
                            OR p.PlayerNameEN LIKE ?
                        )
                    """
                    params.extend(
                        [f"%{search.value}%", f"%{search.value}%"]
                    )

                if status_filter.value != 'all':
                    query += " AND p.MedicalReportStatueId = ?"
                    params.append(status_filter.value)

                query += " ORDER BY p.Id DESC"

                players = db.fetch_all(query, tuple(params))

                with players_container:
                    with ui.card().classes('table-card football-card p-0'):
                        # Table Header
                        with ui.row().classes(
                            'table-header w-full items-center px-6 py-3'
                        ):
                            ui.label('اللاعب').classes(
                                'table-column-title flex-1'
                            )
                            ui.label('الحالة الطبية').classes(
                                'table-column-title w-40 text-center'
                            )
                            ui.label('إجراءات').classes(
                                'table-column-title w-20 text-center'
                            )

                        if not players:
                            with ui.column().classes(
                                'empty-state w-full items-center justify-center p-8 gap-3 text-center'
                            ):
                                with ui.element('div').classes(
                                    'empty-state-icon'
                                ):
                                    ui.icon('sports_soccer').classes(
                                        'text-4xl text-green-700'
                                    )
                                ui.label(
                                    'لا توجد نتائج تطابق البحث'
                                ).classes('text-base font-bold text-slate-700')
                        else:
                            for p in players:
                                p_name = (
                                    p['PlayerNameAR']
                                    or p['PlayerNameEN']
                                    or 'لاعب'
                                )
                                p_status = (
                                    p['MedicalReportStateNameAR']
                                    or p['MedicalReportStateNameEN']
                                    or 'غير محدد'
                                )

                                with ui.row().classes(
                                    'player-row w-full items-center px-6 py-3'
                                ):
                                    with ui.row().classes(
                                        'items-center gap-3 flex-1'
                                    ):
                                        with ui.element('div').classes(
                                            'player-avatar'
                                        ):
                                            ui.icon('sports_soccer').classes(
                                                'text-xl text-green-800'
                                            )
                                        with ui.column().classes('gap-0'):
                                            ui.label(p_name).classes(
                                                'player-name'
                                            )
                                            ui.label(
                                                f"معرف: #{p['Id']}"
                                            ).classes('player-id')

                                    with ui.element('div').classes(
                                        'w-40 text-center'
                                    ):
                                        ui.label(p_status).classes(
                                            'medical-status'
                                        )

                                    with ui.element('div').classes(
                                        'w-20 text-center'
                                    ):
                                        ui.button(
                                            icon='edit',
                                            on_click=lambda p_item=p: open_edit(
                                                p_item
                                            ),
                                        ).props('flat round dense').classes(
                                            'edit-button'
                                        )

            # Bind events
            search.on('update:model-value', render_players)
            status_filter.on('update:model-value', render_players)
            refresh_button.on_click(render_players)

            # Initial render
            render_players()