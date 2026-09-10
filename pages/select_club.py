from nicegui import ui, app
import database as db


def content():
    clubs = db.fetch_all("SELECT * FROM Club")

    ui.add_head_html('''
        <style>
            .clubs-page {
                min-height: 100vh;
                background:
                    radial-gradient(circle at 10% 10%, rgba(59,130,246,.08), transparent 30%),
                    radial-gradient(circle at 90% 20%, rgba(245,158,11,.08), transparent 30%),
                    linear-gradient(135deg, #f8fafc 0%, #eef2f7 100%);
            }

            .club-btn {
                width: 250px !important;
                height: 200px !important;
                background: white !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 24px !important;
                box-shadow: 0 8px 30px rgba(15,23,42,.07) !important;
                transition: all .25s ease !important;
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
                'w-20 h-20 rounded-3xl bg-slate-900 '
                'flex items-center justify-center shadow-xl mb-5'
            ):
                ui.label('⚽').classes('text-4xl')

            ui.label('اختر ناديك').classes(
                'hero-title text-4xl md:text-5xl font-black mb-2'
            )

            ui.label(
                'اختر النادي للدخول إلى نظام إدارة النادي'
            ).classes(
                'text-slate-500 text-lg md:text-xl font-medium'
            )

            with ui.row().classes(
                'items-center gap-2 mt-4 bg-white px-5 py-2 '
                'rounded-full shadow-sm border border-slate-200'
            ):
                ui.icon('groups').classes('text-amber-500')
                ui.label(f'{len(clubs)} نادي متاح').classes(
                    'text-slate-700 font-bold'
                )

        # Clubs
        if not clubs:

            with ui.column().classes(
                'items-center justify-center bg-white '
                'rounded-3xl p-12 shadow-sm border border-slate-200'
            ):
                ui.icon('sports_soccer').classes(
                    'text-6xl text-slate-300'
                )

                ui.label('لا توجد أندية حاليًا').classes(
                    'text-xl font-bold text-slate-600 mt-4'
                )

        else:

            with ui.row().classes(
                'w-full max-w-7xl justify-center flex-wrap gap-6'
            ):

                for club in clubs:

                    c_id = club['Id']
                    c_name = club['ClubNameAR']

                    def select_club(club_id=c_id):
                        app.storage.user['selected_club_id'] = club_id
                        ui.navigate.to('/login')

                    with ui.button(
                        on_click=select_club
                    ).props(
                        'flat no-caps'
                    ).classes('club-btn'):

                        ui.element('div').classes('club-icon').props(
                            'innerHTML="⚽"'
                        )

                        ui.label(c_name).classes('club-name')

                        with ui.row().classes(
                            'items-center gap-1'
                        ):
                            ui.icon('login').classes(
                                'text-amber-500 text-sm'
                            )

                            ui.label('تسجيل الدخول').classes(
                                'login-text'
                            )

        with ui.column().classes('items-center mt-12'):
            ui.label(
                'Egypt Football Club Management System'
            ).classes(
                'text-slate-400 text-sm font-medium'
            )

            ui.label(
                'نظام إدارة الأندية الرياضية'
            ).classes(
                'text-slate-400 text-xs mt-1'
            )