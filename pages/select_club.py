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


def content():
    clubs = db.fetch_all('SELECT * FROM Club')

    ui.add_head_html('''
        <style>
            /* إزالة هوامش الصفحة وحواف NiceGUI كلياً */
            html, body, #app, .q-layout, .q-page-container, .q-page {
                margin: 0 !important;
                padding: 0 !important;
                width: 100% !important;
                min-height: 100vh !important;
                overflow-x: hidden;
            }

            /* استخدام رابط الصورة الخاص بك مع تدرج لوني خفيف لإبراز النصوص */
            body {
                background-color: #0b1329 !important;
                background-image: 
                    linear-gradient(to bottom, rgba(15, 23, 42, 0.65), rgba(15, 23, 42, 0.85)),
                    url('https://imgs.search.brave.com/BzO8Rt9REFyhlH67zRUECw0iPCXflK9eQ2upLcJaIcQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMudmVjdGVlenku/Y29tL3N5c3RlbS9y/ZXNvdXJjZXMvdGh1/bWJuYWlscy8wMDMv/Mzg2LzM1My9zbWFs/bC9mb290YmFsbC1z/dGFkaXVtLWxpZ2h0/aW5nLWZyZWUtcGhv/dG8uanBn') !important;
                background-size: cover !important;
                background-position: center center !important;
                background-attachment: fixed !important;
                background-repeat: no-repeat !important;
            }

            .clubs-container {
                min-height: 100vh;
                width: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 40px 20px;
            }

            .clubs-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 24px;
                width: 100%;
                max-width: 1200px;
            }

            @media (max-width: 1024px) {
                .clubs-grid { grid-template-columns: repeat(3, 1fr); }
            }

            @media (max-width: 768px) {
                .clubs-grid { grid-template-columns: repeat(2, 1fr); }
            }

            @media (max-width: 480px) {
                .clubs-grid { grid-template-columns: repeat(1, 1fr); }
            }

            /* كروت أنيقة وشبه شفافة تظهر جمال الخلفية */
            .club-btn {
                width: 100% !important;
                height: 220px !important;
                background: rgba(15, 23, 42, 0.75) !important;
                border: 1px solid rgba(255, 255, 255, 0.15) !important;
                border-radius: 18px !important;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            }

            .club-btn:hover {
                transform: translateY(-6px) scale(1.02) !important;
                border-color: #f59e0b !important;
                background: rgba(30, 41, 59, 0.9) !important;
                box-shadow: 0 15px 35px rgba(245, 158, 11, 0.4) !important;
            }

            .club-btn .q-btn__content {
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }

            .club-name {
                color: #ffffff;
                font-size: 20px;
                font-weight: 800;
                text-shadow: 0 2px 4px rgba(0,0,0,0.8);
            }

            .login-text {
                color: #cbd5e1;
                font-size: 13px;
                font-weight: 600;
            }
        </style>
    ''')

    with ui.element('div').classes('clubs-container'):
        # الهيدر والشعار الرئيسي
        with ui.column().classes('items-center text-center mb-8'):
            with ui.element('div').classes(
                'w-32 h-32 rounded-3xl bg-white border border-slate-700 flex items-center justify-center shadow-2xl mb-3'
            ):
                ui.image(
                    'https://imgs.search.brave.com/kjpGtjdXYb6_IVbYia_lNxN0-a0MguZhhvw4Znb8fdo/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YXlrLmdlbWluaS5t/ZWRpYS9pbWcveWFs/bGFrb3JhL3RvdXJs/b2dvL0VQTExvZ28x/OS05LTIwMjMtMTYt/MzEtMjEucG5n'
                ).classes('w-28 h-28 object-contain')

            with ui.row().classes(
                'items-center gap-2 bg-slate-900/90 border border-slate-700 px-5 py-2 rounded-full shadow-lg'
            ):
                ui.icon('groups').classes('text-amber-400 text-lg')
                ui.label(f'{len(clubs)} نادي').classes(
                    'text-white font-bold tracking-wide'
                )

        # شبكة الأندية
        if not clubs:
            with ui.column().classes(
                'items-center justify-center bg-slate-900/90 rounded-3xl p-10 border border-slate-700'
            ):
                ui.icon('sports_soccer').classes('text-6xl text-slate-500')
                ui.label('لا توجد أندية حاليًا').classes(
                    'text-xl font-bold text-slate-300 mt-4'
                )
        else:
            with ui.element('div').classes('clubs-grid'):
                for club in clubs:
                    c_id = club['Id']
                    c_name = club['ClubNameAR']
                    logo_url = get_club_logo_url(c_name)

                    with ui.button(
                        on_click=lambda id_=c_id: (
                            app.storage.user.__setitem__(
                                'selected_club_id', id_
                            ),
                            ui.navigate.to('/login'),
                        )
                    ).props('flat no-caps').classes('club-btn'):

                        with ui.element('div').classes(
                            'w-20 h-20 flex items-center justify-center'
                        ):
                            if logo_url:
                                ui.image(logo_url).classes(
                                    'w-20 h-20 object-contain'
                                )
                            else:
                                ui.icon('sports_soccer').classes(
                                    'text-5xl text-slate-400'
                                )

                        ui.label(c_name).classes('club-name')

                        with ui.row().classes('items-center gap-1.5'):
                            ui.icon('login').classes('text-amber-400 text-sm')
                            ui.label('تسجيل الدخول').classes('login-text')

        # الفوتر
        with ui.column().classes('items-center mt-10 text-center'):
            ui.label('Egyptian Premier League Management').classes(
                'text-slate-300 text-sm font-semibold tracking-wider'
            )