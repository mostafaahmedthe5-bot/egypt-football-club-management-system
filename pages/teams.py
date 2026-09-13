import database as db
from nicegui import app, ui

GRASS_BACKGROUND = 'https://imgs.search.brave.com/sJbzVVnKH_yP_2G9TeAfuOc7BqdkM9hIYavynKjmqHk/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudmVjdGVlemku/Y29tL3N5c3RlbS9y/ZXNvdXJjZXMvdGh1/bWJuYWlscy8wMDgvNDU5Lzc3Ni9zbWFsbC9ncmVlbi1uYXR1/cmFsLW9yZ2FuaWMt/Z3Jhc3MtYmFja2dy/b3VuZC1hbmQtdGV4/dHVyZS12ZWN0b3IuanBn'


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
    if club_id is None:
        club_id = app.storage.user.get('club_id')
    if not club_id:
        ui.navigate.to('/select_club')
        return

    club = db.fetch_one(
        """
        SELECT Id, ClubNameAR, ClubNameEN 
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

    club_logo_url = get_club_logo_url(club_name_ar)
    team_photo_url = get_club_team_photo_url(club_name_ar)

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
        row['Id']: row['TeamCategoryNameAR']
        or row['TeamCategoryNameEN']
        or str(row['Id'])
        for row in categories
    }

    sport_options = {
        row['Id']: row['SportNameAR']
        or row['SportNameEN']
        or str(row['Id'])
        for row in sports
    }

    ui.add_head_html(f"""
        <style>
            .teams-page {{
                direction: rtl;
                min-height: 100vh;
                width: 100%;
                background: linear-gradient(180deg, #f0fdf4 0%, #f8fafc 38%, #eef2f7 100%);
            }}
            .teams-wrapper {{
                width: 100%;
                max-width: 1500px;
                margin: 0 auto;
            }}
            .football-hero {{
                position: relative;
                width: 100%;
                min-height: 310px;
                overflow: hidden;
                border-radius: 28px;
                background: #052e16;
                box-shadow: 0 20px 50px rgba(15,23,42,.18);
                isolation: isolate;
            }}
            .football-hero-bg {{
                position: absolute;
                inset: 0;
                z-index: -3;
                background-size: cover;
                background-position: center;
                transform: scale(1.02);
            }}
            .football-hero-overlay {{
                position: absolute;
                inset: 0;
                z-index: -2;
                background: linear-gradient(90deg, rgba(2,6,23,.94) 0%, rgba(2,6,23,.78) 40%, rgba(2,6,23,.45) 72%, rgba(2,6,23,.70) 100%);
            }}
            .football-hero-content {{
                position: relative;
                min-height: 310px;
                padding: 32px;
                z-index: 2;
            }}
            .hero-club-logo {{
                width: 90px;
                height: 90px;
                object-fit: contain;
                padding: 10px;
                border-radius: 23px;
                background: rgba(255,255,255,.95);
                box-shadow: 0 15px 35px rgba(0,0,0,.25);
            }}
            .hero-title {{
                color: white;
                font-size: 32px;
                font-weight: 950;
                line-height: 1.2;
            }}
            .main-card {{
                width: 100%;
                background: linear-gradient(rgba(255,255,255,.94), rgba(255,255,255,.94)), url("{GRASS_BACKGROUND}");
                background-size: cover;
                background-position: center;
                border: 1px solid #d1fae5;
                border-radius: 22px;
                box-shadow: 0 10px 30px rgba(15,23,42,.07);
            }}
            .card-heading-icon {{
                width: 46px;
                height: 46px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 14px;
                background: linear-gradient(145deg,#052e16,#16a34a);
                color: white;
                box-shadow: 0 8px 18px rgba(22,101,52,.18);
            }}
            .teams-list-card {{
                width: 100%;
                background: linear-gradient(rgba(255,255,255,.91), rgba(255,255,255,.91)), url("{GRASS_BACKGROUND}");
                background-size: cover;
                background-position: center;
                border: 1px solid #bbf7d0;
                border-radius: 24px;
                overflow: hidden;
            }}
            .teams-list-header {{
                background: linear-gradient(90deg, rgba(5,46,22,.96), rgba(21,128,61,.92));
                color: white;
            }}
            .teams-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 16px;
                padding: 20px;
            }}
            .team-card {{
                position: relative;
                min-height: 190px;
                border-radius: 20px;
                border: 1px solid rgba(187,247,208,.9);
                background: linear-gradient(rgba(2,44,20,.74), rgba(20,83,45,.84)), url("{GRASS_BACKGROUND}");
                background-size: cover;
                padding: 18px;
            }}
            .team-name {{ color: white; font-size: 16px; font-weight: 900; }}
            .team-meta {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 6px 12px;
                border-radius: 10px;
                font-size: 11px;
                font-weight: 700;
            }}
            .team-meta.category {{ color: #dcfce7; background: rgba(22,101,52,.60); }}
            .team-meta.sport {{ color: #dbeafe; background: rgba(30,64,175,.52); }}
            .team-actions {{ position: absolute; left: 14px; top: 14px; display: flex; gap: 5px; }}
        </style>
    """)

    with ui.element('div').classes('teams-page p-4 md:p-8'):
        with ui.element('div').classes('teams-wrapper space-y-6'):

            # Hero Section
            with ui.element('div').classes('football-hero'):
                if team_photo_url:
                    ui.element('div').classes('football-hero-bg').style(
                        f'background-image: url("{team_photo_url}")'
                    )
                ui.element('div').classes('football-hero-overlay')
                with ui.row().classes(
                    'football-hero-content items-center justify-between gap-6'
                ):
                    with ui.row().classes('items-center gap-4'):
                        if club_logo_url:
                            ui.image(club_logo_url).classes('hero-club-logo')
                        with ui.column().classes('gap-1'):
                            ui.label(club_name_ar).classes('hero-title')
                            ui.label(club_name_en).classes(
                                'text-slate-300 text-sm'
                            )

            # Add Team Form
            with ui.element('div').classes('main-card p-6'):
                with ui.row().classes('items-center gap-3 mb-4'):
                    with ui.element('div').classes('card-heading-icon'):
                        ui.icon('add').classes('text-xl')
                    ui.label('إضافة فريق جديد').classes(
                        'text-lg font-bold text-slate-800'
                    )

                with ui.row().classes('w-full gap-4 items-center flex-wrap'):
                    team_ar = (
                        ui.input(label='اسم الفريق (عربي)')
                        .classes('flex-1 min-w-[200px]')
                        .props('outlined dense')
                    )
                    team_en = (
                        ui.input(label='اسم الفريق (إنجليزي)')
                        .classes('flex-1 min-w-[200px]')
                        .props('outlined dense')
                    )
                    team_category = (
                        ui.select(
                            options=category_options, label='الفئة العمرية'
                        )
                        .classes('flex-1 min-w-[180px]')
                        .props('outlined dense')
                    )
                    sport = (
                        ui.select(options=sport_options, label='الرياضة')
                        .classes('flex-1 min-w-[180px]')
                        .props('outlined dense')
                    )

                    def save_new_team():
                        if not team_ar.value:
                            ui.notify(
                                'يرجى إدخال اسم الفريق بالعربية',
                                color='warning',
                            )
                            return
                        db.execute(
                            """
                            INSERT INTO Team (TeamAR, TeamEN, Teamcatgoryid, Sportid, Clubid)
                            VALUES (?, ?, ?, ?, ?)
                            """,
                            (
                                team_ar.value,
                                team_en.value,
                                team_category.value,
                                sport.value,
                                club_id,
                            ),
                        )
                        ui.notify('تمت إضافة الفريق بنجاح', color='positive')
                        team_ar.value = ''
                        team_en.value = ''
                        team_category.value = None
                        sport.value = None
                        refresh_teams()

                    ui.button(
                        'حفظ الفريق', icon='save', on_click=save_new_team
                    ).classes('bg-green-700 text-white px-6 py-2 rounded-lg')

            # Container for teams list
            teams_container = ui.element('div').classes('w-full')

            # Dialogs
            edit_dialog = ui.dialog()
            delete_dialog = ui.dialog()

            edit_id = {'value': None}
            delete_target_id = {'value': None}

            # State fields for edit
            edit_team_ar = None
            edit_team_en = None
            edit_category = None
            edit_sport = None

            # Setup Edit Dialog Content
            with edit_dialog, ui.card().classes('w-[500px] max-w-full p-6'):
                ui.label('تعديلبيانات الفريق').classes(
                    'text-xl font-bold mb-4'
                )
                edit_team_ar_input = ui.input(label='اسم الفريق (عربي)').props(
                    'outlined dense'
                )
                edit_team_en_input = ui.input(
                    label='اسم الفريق (إنجليزي)'
                ).props('outlined dense')
                edit_category_select = ui.select(
                    options=category_options, label='الفئة العمرية'
                ).props('outlined dense')
                edit_sport_select = ui.select(
                    options=sport_options, label='الرياضة'
                ).props('outlined dense')

                def update_team():
                    db.execute(
                        """
                        UPDATE Team 
                        SET TeamAR = ?, TeamEN = ?, Teamcatgoryid = ?, Sportid = ?
                        WHERE Id = ?
                        """,
                        (
                            edit_team_ar_input.value,
                            edit_team_en_input.value,
                            edit_category_select.value,
                            edit_sport_select.value,
                            edit_id['value'],
                        ),
                    )
                    ui.notify('تم تحديث البيانات بنجاح', color='positive')
                    edit_dialog.close()
                    refresh_teams()

                with ui.row().classes('justify-end gap-2 mt-4'):
                    ui.button(
                        'إلغاء', on_click=edit_dialog.close
                    ).props('flat')
                    ui.button(
                        'حفظ التعديلات', on_click=update_team
                    ).classes('bg-green-700 text-white')

            # Setup Delete Dialog Content
            with delete_dialog, ui.card().classes('w-[400px] max-w-full p-6'):
                ui.label('تأكيد الحذف').classes(
                    'text-xl font-bold text-red-600 mb-2'
                )
                ui.label(
                    'هل أنت تأكد من رغبتك في حذف هذا الفريق نهائياً؟'
                ).classes('text-sm text-slate-600 mb-4')

                def confirm_delete():
                    db.execute(
                        'DELETE FROM Team WHERE Id = ?',
                        (delete_target_id['value'],),
                    )
                    ui.notify('تم حذف الفريق', color='negative')
                    delete_dialog.close()
                    refresh_teams()

                with ui.row().classes('justify-end gap-2'):
                    ui.button(
                        'إلغاء', on_click=delete_dialog.close
                    ).props('flat')
                    ui.button('حذف', on_click=confirm_delete).classes(
                        'bg-red-600 text-white'
                    )

            def open_edit(team):
                edit_id['value'] = team['Id']
                edit_team_ar_input.value = team['TeamAR'] or ''
                edit_team_en_input.value = team['TeamEN'] or ''
                edit_category_select.value = team['Teamcatgoryid']
                edit_sport_select.value = team['Sportid']
                edit_dialog.open()

            def open_delete(team_id):
                delete_target_id['value'] = team_id
                delete_dialog.open()

            def refresh_teams():
                teams_container.clear()
                teams = db.fetch_all(
                    """
                    SELECT 
                        t.Id, t.TeamAR, t.TeamEN, t.Teamcatgoryid, t.Sportid,
                        tc.TeamCategoryNameAR, tc.TeamCategoryNameEN,
                        s.SportNameAR, s.SportNameEN
                    FROM Team t
                    LEFT JOIN TeamCategory tc ON tc.Id = t.Teamcatgoryid
                    LEFT JOIN Sport s ON s.Id = t.Sportid
                    WHERE t.Clubid = ?
                    ORDER BY t.Id DESC
                    """,
                    (club_id,),
                )

                with teams_container:
                    with ui.element('div').classes('teams-list-card'):
                        with ui.row().classes(
                            'teams-list-header w-full items-center justify-between p-5'
                        ):
                            with ui.row().classes('items-center gap-3'):
                                ui.icon('groups').classes('text-2xl')
                                ui.label('قائمة فرق النادي').classes(
                                    'text-lg font-bold'
                                )
                            ui.label(f'{len(teams)} فريق').classes(
                                'bg-white/20 px-3 py-1 rounded-full text-xs font-bold'
                            )

                        if not teams:
                            with ui.column().classes(
                                'p-8 items-center justify-center text-center gap-2'
                            ):
                                ui.icon('sports_soccer').classes(
                                    'text-5xl text-slate-400'
                                )
                                ui.label(
                                    'لا توجد فرق مسجلة حتى الآن'
                                ).classes('text-lg font-bold text-slate-700')
                        else:
                            with ui.element('div').classes('teams-grid'):
                                for team in teams:
                                    t_name = team['TeamAR'] or 'فريق بدون اسم'
                                    t_cat = (
                                        team['TeamCategoryNameAR']
                                        or team['TeamCategoryNameEN']
                                        or 'غير محدد'
                                    )
                                    t_sport = (
                                        team['SportNameAR']
                                        or team['SportNameEN']
                                        or 'غير محدد'
                                    )

                                    with ui.element('div').classes('team-card'):
                                        with ui.element('div').classes(
                                            'team-actions'
                                        ):
                                            ui.button(
                                                icon='edit',
                                                on_click=lambda t=team: open_edit(
                                                    t
                                                ),
                                            ).props('flat round dense').classes(
                                                'text-white'
                                            )
                                            ui.button(
                                                icon='delete',
                                                on_click=lambda tid=team[
                                                    'Id'
                                                ]: open_delete(tid),
                                            ).props('flat round dense').classes(
                                                'text-red-300'
                                            )

                                        ui.label(t_name).classes('team-name')
                                        if team['TeamEN']:
                                            ui.label(team['TeamEN']).classes(
                                                'text-xs text-slate-300'
                                            )

                                        with ui.row().classes(
                                            'gap-2 mt-4 flex-wrap'
                                        ):
                                            with ui.element('div').classes(
                                                'team-meta category'
                                            ):
                                                ui.icon('category').classes(
                                                    'text-xs'
                                                )
                                                ui.label(t_cat)
                                            with ui.element('div').classes(
                                                'team-meta sport'
                                            ):
                                                ui.icon('sports').classes(
                                                    'text-xs'
                                                )
                                                ui.label(t_sport)

            # Initial load
            refresh_teams()