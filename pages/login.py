from nicegui import ui, app
import database as db


def content():
    # =========================================================
    # النادي المختار
    # =========================================================

    selected_club_id = app.storage.user.get('selected_club_id')

    if not selected_club_id:
        ui.navigate.to('/select_club')
        return

    # =========================================================
    # بيانات النادي من جدول Club
    # =========================================================

    club = db.fetch_one(
        """
        SELECT Id, ClubNameAR, ClubNameEN
        FROM Club
        WHERE Id = ?
        """,
        (selected_club_id,)
    )

    if not club:
        app.storage.user.pop('selected_club_id', None)

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

    ui.add_head_html('''
        <style>

            .login-page {
                min-height: 100vh;
                background:
                    radial-gradient(
                        circle at 15% 15%,
                        rgba(59,130,246,.10),
                        transparent 30%
                    ),
                    radial-gradient(
                        circle at 85% 20%,
                        rgba(245,158,11,.10),
                        transparent 30%
                    ),
                    linear-gradient(
                        135deg,
                        #f8fafc 0%,
                        #eef2f7 100%
                    );
            }

            .login-card {
                width: 430px;
                max-width: 94vw;
                background: rgba(255,255,255,.98);
                border: 1px solid #e2e8f0;
                border-radius: 28px;
                box-shadow:
                    0 25px 70px rgba(15,23,42,.12);
                overflow: hidden;
            }

            .login-top {
                height: 7px;
                background:
                    linear-gradient(
                        90deg,
                        #0f172a,
                        #1e3a8a,
                        #f59e0b
                    );
            }

            .club-logo {
                width: 88px;
                height: 88px;
                border-radius: 26px;
                background:
                    linear-gradient(
                        135deg,
                        #0f172a,
                        #1e293b
                    );
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow:
                    0 12px 30px rgba(15,23,42,.20);
            }

            .login-title {
                color: #0f172a;
                font-size: 25px;
                font-weight: 900;
            }

            .club-name {
                color: #1e3a8a;
                font-size: 19px;
                font-weight: 800;
            }

            .login-input input {
                font-size: 16px !important;
                font-weight: 600;
            }

            .login-button {
                height: 52px !important;
                border-radius: 14px !important;
                background:
                    linear-gradient(
                        135deg,
                        #0f172a,
                        #1e3a8a
                    ) !important;
                color: white !important;
                font-size: 16px !important;
                font-weight: 800 !important;
                box-shadow:
                    0 8px 20px rgba(15,23,42,.18);
                transition: all .2s ease;
            }

            .login-button:hover {
                transform: translateY(-2px);
                box-shadow:
                    0 12px 28px rgba(15,23,42,.24);
            }

            .back-button {
                height: 45px !important;
                border-radius: 12px !important;
                color: #64748b !important;
                font-weight: 700 !important;
            }

            .info-box {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
            }

        </style>
    ''')

    # =========================================================
    # Login
    # =========================================================

    with ui.column().classes(
        'login-page w-full items-center justify-center p-4'
    ):

        with ui.card().classes(
            'login-card p-0'
        ):

            # =================================================
            # Top
            # =================================================

            ui.element(
                'div'
            ).classes(
                'login-top w-full'
            )

            with ui.column().classes(
                'w-full items-center p-7 md:p-9'
            ):

                # =================================================
                # Club Logo
                # =================================================

                with ui.element('div').classes(
                    'club-logo mb-5'
                ):
                    ui.label('⚽').classes(
                        'text-5xl'
                    )

                # =================================================
                # Title
                # =================================================

                ui.label(
                    'تسجيل الدخول'
                ).classes(
                    'login-title mb-1'
                )

                ui.label(
                    club_name
                ).classes(
                    'club-name mb-2'
                )

                ui.label(
                    'مرحبًا بك في نظام إدارة النادي'
                ).classes(
                    'text-slate-500 text-sm mb-7'
                )

                # =================================================
                # Password
                # =================================================

                password = ui.input(
                    'كلمة المرور',
                    password=True,
                    password_toggle_button=True
                ).props(
                    'outlined rounded'
                ).classes(
                    'w-full login-input mb-2'
                )

                ui.label(
                    'كلمة المرور الافتتاحية: 123'
                ).classes(
                    'text-xs text-slate-400 self-start mb-5'
                )

                # =================================================
                # Login
                # =================================================

                def handle_login():

                    entered_password = password.value or ''

                    # كلمة المرور الحالية للتجربة
                    if entered_password != '123':

                        ui.notify(
                            'كلمة المرور غير صحيحة!',
                            color='negative'
                        )

                        password.value = ''
                        password.run_method('focus')
                        return

                    # =================================================
                    # Login Successful
                    # =================================================

                    app.storage.user.update({
                        'is_logged_in': True,
                        'club_id': selected_club_id,
                        'club_name': club_name
                    })

                    ui.notify(
                        'تم تسجيل الدخول بنجاح!',
                        color='positive'
                    )

                    ui.navigate.to('/dashboard')

                login_button = ui.button(
                    'دخول',
                    icon='login',
                    on_click=handle_login
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'login-button w-full mb-3'
                )

                # Enter
                password.on(
                    'keydown.enter',
                    lambda e: handle_login()
                )

                # =================================================
                # Change Club
                # =================================================

                ui.button(
                    'اختيار نادي آخر',
                    icon='swap_horiz',
                    on_click=lambda: (
                        app.storage.user.pop(
                            'selected_club_id',
                            None
                        ),
                        ui.navigate.to('/select_club')
                    )
                ).props(
                    'flat no-caps'
                ).classes(
                    'back-button w-full'
                )

                # =================================================
                # Info
                # =================================================

                with ui.element('div').classes(
                    'info-box w-full p-4 mt-6'
                ):

                    with ui.row().classes(
                        'w-full items-center gap-3'
                    ):

                        ui.icon(
                            'info'
                        ).classes(
                            'text-blue-500 text-xl'
                        )

                        with ui.column().classes(
                            'gap-0'
                        ):

                            ui.label(
                                'النادي المختار'
                            ).classes(
                                'text-slate-700 text-sm font-bold'
                            )

                            ui.label(
                                club_name
                            ).classes(
                                'text-slate-400 text-xs mt-1'
                            )

                # =================================================
                # Footer
                # =================================================

                ui.label(
                    'Egypt Football Club Management System'
                ).classes(
                    'text-slate-400 text-xs mt-7'
                )