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
            .clubs-page {
                min-height: 100vh;
                background:
    radial-gradient(circle at 10% 10%, rgba(214,194,163,.18), transparent 30%),
    radial-gradient(circle at 90% 20%, rgba(184,159,122,.14), transparent 30%),
    linear-gradient(135deg, #F7F3EC 0%, #EDE3D3 100%);

            .clubs-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                width: 100%;
                max-width: 1280px;
            }

            @media (max-width: 1024px) {
                .clubs-grid {
                    grid-template-columns: repeat(3, 1fr);
                }
            }

            @media (max-width: 768px) {
                .clubs-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
            }

            @media (max-width: 480px) {
                .clubs-grid {
                    grid-template-columns: repeat(1, 1fr);
                }
            }
.club-btn {
    width: 100% !important;
    height: 235px !important;
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 30px rgba(15,23,42,.07) !important;
}

            .club-btn:hover {
                transform: translateY(-8px) !important;
                box-shadow: 0 18px 45px rgba(15,23,42,.15) !important;
                border-color: #f59e0b !important;
            }

            .club-btn .q-btn__content {
                width: 100%;
                height: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 12px;
            }

            .club-icon {
                width: 72px;
                height: 72px;
                border-radius: 20px;
                background: linear-gradient(135deg, #0f172a, #1e293b);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 32px;
                box-shadow: 0 8px 20px rgba(15,23,42,.18);
            }

            .club-name {
                color: #0f172a;
                font-size: 19px;
                font-weight: 800;
            }

            .login-text {
                color: #64748b;
                font-size: 13px;
                font-weight: 600;
            }

            .hero-title {
                background: linear-gradient(90deg, #0f172a, #1e3a8a);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
        </style>
    ''')

    with ui.column().classes('clubs-page w-full items-center p-6 md:p-10'):
        # Header
        with ui.column().classes('items-center text-center mb-10'):
            with ui.element('div').classes(
                'w-20 h-20 rounded-3xl bg-slate-900 flex items-center justify-center shadow-xl mb-5'
            ):
                 ui.image(
                'https://image.pngaaa.com/856/449856-middle.png'
            ).classes('w-20 h-20 object-contain')

            with ui.row().classes(
                'items-center gap-2 mt-4 bg-white px-5 py-2 rounded-full shadow-sm border border-slate-200'
            ):
                ui.icon('groups').classes('text-amber-500')
                ui.label(f'{len(clubs)}    نادي ').classes(
                    'text-slate-700 font-bold'
                )

        # Clubs
        if not clubs:
            with ui.column().classes(
                'items-center justify-center bg-white rounded-3xl p-12 shadow-sm border border-slate-200'
            ):
                ui.icon('sports_soccer').classes('text-6xl text-slate-300')
                ui.label('لا توجد أندية حاليًا').classes(
                    'text-xl font-bold text-slate-600 mt-4'
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

                        with ui.element('div').classes('club-icon'):
                            if logo_url:
                                ui.image(logo_url).classes(
                                    'w-16 h-16 object-contain'
                                )
                            else:
                                ui.icon('sports_soccer').classes(
                                    'text-4xl text-white'
                                )

                        ui.label(c_name).classes('club-name')

                        with ui.row().classes('items-center gap-1'):
                            ui.icon('login').classes('text-amber-500 text-sm')
                            ui.label('تسجيل الدخول').classes('login-text')

        with ui.column().classes('items-center mt-12'):
            ui.label('Egypt Football Club Management System').classes(
                'text-slate-400 text-sm font-medium'
            )
            ui.label('نظام إدارة الأندية الرياضية').classes(
                'text-slate-400 text-xs mt-1'
            )