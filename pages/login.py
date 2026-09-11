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
    # بيانات النادي
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
    club_name_en = club['ClubNameEN'] or 'Sports Club'

    # =========================================================
    # CSS
    # =========================================================

    ui.add_head_html('''
        <style>

            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                overflow-x: hidden;
            }

            /* =================================================
               Main Page
               ================================================= */

            .login-page {
                position: relative;
                min-height: 100vh;
                width: 100%;
                overflow: hidden;

                
                    background:
    radial-gradient(circle at 10% 10%, rgba(214,194,163,.18), transparent 30%),
    radial-gradient(circle at 90% 20%, rgba(184,159,122,.14), transparent 30%),
    linear-gradient(135deg, #F7F3EC 0%, #EDE3D3 100%);
            }

            /* =================================================
               Decorative Background
               ================================================= */

            .login-page::before {
                content: "";
                position: absolute;

                width: 420px;
                height: 420px;

                border-radius: 50%;

                top: -220px;
                left: -180px;

                background:
                    radial-gradient(
                        circle,
                        rgba(30, 58, 138, .08),
                        transparent 70%
                    );

                pointer-events: none;
            }

            .login-page::after {
                content: "";
                position: absolute;

                width: 500px;
                height: 500px;

                border-radius: 50%;

                bottom: -280px;
                right: -220px;

                background:
                    radial-gradient(
                        circle,
                        rgba(245, 158, 11, .08),
                        transparent 70%
                    );

                pointer-events: none;
            }

            /* =================================================
               Login Card
               ================================================= */

            .login-card {
                position: relative;
                z-index: 2;

                width: 440px;
                max-width: calc(100vw - 28px);

                background: rgba(255, 255, 255, .97);

                border: 1px solid rgba(226, 232, 240, .9);

                border-radius: 30px;

                box-shadow:
                    0 35px 90px rgba(15, 23, 42, .13),
                    0 10px 30px rgba(15, 23, 42, .06);

                overflow: hidden;

                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);

                animation: login-card-enter .55s ease-out;
            }

            @keyframes login-card-enter {
                from {
                    opacity: 0;
                    transform: translateY(18px) scale(.985);
                }

                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }

            /* =================================================
               Top Gradient
               ================================================= */

            .login-top {
                height: 7px;
                width: 100%;

                background:
                    linear-gradient(
                        90deg,
                        #0f172a 0%,
                        #1e3a8a 48%,
                        #f59e0b 100%
                    );
            }

            /* =================================================
               Inner Content
               ================================================= */

            .login-content {
                width: 100%;
                padding: 38px 38px 30px;
            }

            /* =================================================
               Club Logo
               ================================================= */

            .club-logo-wrapper {
                position: relative;

                width: 102px;
                height: 102px;

                margin-bottom: 22px;
            }

            .club-logo-glow {
                position: absolute;

                inset: -8px;

                border-radius: 31px;

                background:
                    linear-gradient(
                        135deg,
                        rgba(30, 58, 138, .12),
                        rgba(245, 158, 11, .10)
                    );

                filter: blur(5px);

                opacity: .9;
            }

            .club-logo {
                position: relative;

                width: 102px;
                height: 102px;

                border-radius: 30px;

                display: flex;
                align-items: center;
                justify-content: center;

                background:
                    linear-gradient(
                        145deg,
                        #0f172a 0%,
                        #172554 55%,
                        #1e3a8a 100%
                    );

                border: 1px solid rgba(255, 255, 255, .15);

                box-shadow:
                    0 18px 35px rgba(15, 23, 42, .22),
                    inset 0 1px 0 rgba(255, 255, 255, .12);

                overflow: hidden;
            }

            .club-logo::before {
                content: "";

                position: absolute;

                width: 70px;
                height: 70px;

                border-radius: 50%;

                border: 1px solid rgba(255, 255, 255, .10);

                top: -25px;
                right: -25px;
            }

            .club-logo::after {
                content: "";

                position: absolute;

                width: 55px;
                height: 55px;

                border-radius: 50%;

                border: 1px solid rgba(245, 158, 11, .16);

                bottom: -20px;
                left: -20px;
            }

            .club-logo-icon {
                position: relative;
                z-index: 2;

                color: white;

                font-size: 48px;

                filter:
                    drop-shadow(
                        0 5px 8px rgba(0, 0, 0, .25)
                    );
            }

            /* =================================================
               Heading
               ================================================= */

            .login-title {
                color: #0f172a;

                font-size: 27px;
                line-height: 1.2;

                font-weight: 900;

                letter-spacing: -.4px;
            }

            .club-name {
                color: #1e3a8a;

                font-size: 20px;
                line-height: 1.4;

                font-weight: 850;
            }

            .club-name-en {
                color: #94a3b8;

                font-size: 11px;

                font-weight: 700;

                letter-spacing: .7px;

                text-transform: uppercase;
            }

            .login-subtitle {
                color: #64748b;

                font-size: 14px;

                line-height: 1.7;
            }

            /* =================================================
               Security Badge
               ================================================= */

            .security-badge {
                display: flex;
                align-items: center;
                gap: 8px;

                padding: 7px 11px;

                border-radius: 999px;

                background: #f8fafc;

                border: 1px solid #e2e8f0;

                color: #64748b;

                font-size: 11px;

                font-weight: 700;
            }

            .security-dot {
                width: 7px;
                height: 7px;

                border-radius: 50%;

                background: #10b981;

                box-shadow:
                    0 0 0 4px rgba(16, 185, 129, .10);
            }

            /* =================================================
               Input
               ================================================= */

            .login-input {
                margin-top: 8px;
            }

            .login-input .q-field__control {
                min-height: 56px !important;

                border-radius: 15px !important;

                background: #f8fafc;

                transition:
                    border-color .2s ease,
                    box-shadow .2s ease,
                    background .2s ease;
            }

            .login-input .q-field__control:hover {
                background: #ffffff;
            }

            .login-input .q-field__control:focus-within {
                background: #ffffff;

                box-shadow:
                    0 0 0 4px rgba(30, 58, 138, .08);
            }

            .login-input input {
                font-size: 16px !important;

                font-weight: 650 !important;

                color: #0f172a !important;
            }

            .login-input .q-field__label {
                font-weight: 600;
            }

            /* =================================================
               Demo Password
               ================================================= */

            .password-hint {
                width: 100%;

                display: flex;
                align-items: center;
                justify-content: space-between;

                margin-top: 8px;
                margin-bottom: 18px;

                padding: 10px 12px;

                border-radius: 12px;

                background: #fffbeb;

                border: 1px solid #fef3c7;
            }

            .password-hint-label {
                color: #92400e;

                font-size: 11px;

                font-weight: 700;
            }

            .password-hint-value {
                color: #b45309;

                font-size: 13px;

                font-weight: 900;

                direction: ltr;

                letter-spacing: 1px;
            }

            /* =================================================
               Login Button
               ================================================= */

            .login-button {
                height: 55px !important;

                border-radius: 15px !important;

                background:
                    linear-gradient(
                        135deg,
                        #0f172a 0%,
                        #172554 52%,
                        #1e3a8a 100%
                    ) !important;

                color: white !important;

                font-size: 16px !important;

                font-weight: 850 !important;

                box-shadow:
                    0 12px 25px rgba(15, 23, 42, .18);

                transition:
                    transform .2s ease,
                    box-shadow .2s ease,
                    opacity .2s ease;
            }

            .login-button:hover {
                transform: translateY(-2px);

                box-shadow:
                    0 17px 32px rgba(15, 23, 42, .23);
            }

            .login-button:active {
                transform: translateY(0);
            }

            .login-button.q-btn--disabled {
                opacity: .7 !important;
            }

            /* =================================================
               Change Club
               ================================================= */

            .back-button {
                height: 46px !important;

                border-radius: 13px !important;

                color: #64748b !important;

                font-size: 13px !important;

                font-weight: 750 !important;

                transition:
                    background .2s ease,
                    color .2s ease;
            }

            .back-button:hover {
                background: #f8fafc !important;

                color: #0f172a !important;
            }

            /* =================================================
               Club Info
               ================================================= */

            .info-box {
                width: 100%;

                background:
                    linear-gradient(
                        135deg,
                        #f8fafc,
                        #f1f5f9
                    );

                border: 1px solid #e2e8f0;

                border-radius: 16px;

                padding: 14px 15px;

                transition:
                    border-color .2s ease,
                    transform .2s ease;
            }

            .info-box:hover {
                border-color: #cbd5e1;

                transform: translateY(-1px);
            }

            .info-icon-box {
                width: 38px;
                height: 38px;

                flex-shrink: 0;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 11px;

                background: rgba(30, 58, 138, .08);
            }

            .info-title {
                color: #334155;

                font-size: 12px;

                font-weight: 800;
            }

            .info-value {
                color: #94a3b8;

                font-size: 11px;

                font-weight: 600;
            }

            /* =================================================
               Footer
               ================================================= */

            .login-footer {
                color: #94a3b8;

                font-size: 10px;

                font-weight: 600;

                letter-spacing: .3px;
            }

            /* =================================================
               Mobile
               ================================================= */

            @media (max-width: 520px) {

                .login-page {
                    padding: 14px !important;
                }

                .login-card {
                    width: 100%;
                    max-width: 420px;

                    border-radius: 24px;
                }

                .login-content {
                    padding: 30px 22px 24px;
                }

                .club-logo-wrapper,
                .club-logo {
                    width: 88px;
                    height: 88px;
                }

                .club-logo {
                    border-radius: 26px;
                }

                .club-logo-icon {
                    font-size: 41px;
                }

                .login-title {
                    font-size: 24px;
                }

                .club-name {
                    font-size: 18px;
                }
            }

        </style>
    ''')

    # =========================================================
    # Main Page
    # =========================================================

    with ui.column().classes(
        'login-page w-full items-center justify-center p-4'
    ):

        # =====================================================
        # Login Card
        # =====================================================

        with ui.card().classes(
            'login-card p-0'
        ):

            # =================================================
            # Top Gradient
            # =================================================

            ui.element(
                'div'
            ).classes(
                'login-top'
            )

            # =================================================
            # Content
            # =================================================

            with ui.column().classes(
                'login-content items-center'
            ):

                # =============================================
                # Logo
                # =============================================

                with ui.element(
                    'div'
                ).classes(
                    'club-logo-wrapper'
                ):

                    ui.element(
                        'div'
                    ).classes(
                        'club-logo-glow'
                    )

                    with ui.element(
                        'div'
                    ).classes(
                        'club-logo'
                    ):

                        ui.icon(
                            'sports_soccer'
                        ).classes(
                            'club-logo-icon'
                        )

                # =============================================
                # Security Status
                # =============================================

                with ui.row().classes(
                    'items-center justify-center mb-4'
                ):

                    with ui.element(
                        'div'
                    ).classes(
                        'security-badge'
                    ):

                        ui.element(
                            'span'
                        ).classes(
                            'security-dot'
                        )

                        ui.label(
                            'نظام آمن لإدارة النادي'
                        )

                # =============================================
                # Title
                # =============================================

                ui.label(
                    'تسجيل الدخول'
                ).classes(
                    'login-title mb-2'
                )

                ui.label(
                    club_name
                ).classes(
                    'club-name text-center'
                )

                ui.label(
                    club_name_en
                ).classes(
                    'club-name-en mt-1'
                )

                ui.label(
                    'مرحبًا بك في نظام إدارة النادي'
                ).classes(
                    'login-subtitle text-center mt-3 mb-6'
                )

                # =============================================
                # Password
                # =============================================

                password = ui.input(
                    'كلمة المرور',
                    password=True,
                    password_toggle_button=True
                ).props(
                    'outlined'
                ).classes(
                    'w-full login-input'
                )

                # =============================================
                # Password Hint
                # =============================================

                with ui.element(
                    'div'
                ).classes(
                    'password-hint'
                ):

                    ui.label(
                        'كلمة المرور الافتتاحية'
                    ).classes(
                        'password-hint-label'
                    )

                    ui.label(
                        '123'
                    ).classes(
                        'password-hint-value'
                    )

                # =============================================
                # Login Logic
                # =============================================

                is_logging_in = False

                def handle_login():

                    nonlocal is_logging_in

                    if is_logging_in:
                        return

                    entered_password = password.value or ''

                    # =========================================
                    # Validation
                    # =========================================

                    if not entered_password.strip():

                        ui.notify(
                            'من فضلك أدخل كلمة المرور',
                            color='warning',
                            position='top'
                        )

                        password.run_method(
                            'focus'
                        )

                        return

                    # =========================================
                    # Start Login
                    # =========================================

                    is_logging_in = True

                    login_button.disable()

                    try:

                        # =====================================
                        # Current Demo Password
                        # =====================================

                        if entered_password != '123':

                            ui.notify(
                                'كلمة المرور غير صحيحة',
                                color='negative',
                                position='top'
                            )

                            password.value = ''

                            password.run_method(
                                'focus'
                            )

                            return

                        # =====================================
                        # Login Successful
                        # =====================================

                        app.storage.user.update({
                            'is_logged_in': True,
                            'club_id': selected_club_id,
                            'club_name': club_name
                        })

                        ui.notify(
                            f'تم تسجيل الدخول إلى {club_name} بنجاح',
                            color='positive',
                            position='top'
                        )

                        ui.navigate.to(
                            '/dashboard'
                        )

                    finally:

                        is_logging_in = False

                        login_button.enable()

                # =============================================
                # Login Button
                # =============================================

                login_button = ui.button(
                    'دخول إلى النظام',
                    icon='login',
                    on_click=handle_login
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'login-button w-full mb-2'
                )

                # =============================================
                # Enter Key
                # =============================================

                password.on(
                    'keydown.enter',
                    lambda e: handle_login()
                )

                # =============================================
                # Change Club
                # =============================================

                def change_club():

                    app.storage.user.pop(
                        'selected_club_id',
                        None
                    )

                    ui.navigate.to(
                        '/select_club'
                    )

                ui.button(
                    'اختيار نادي آخر',
                    icon='swap_horiz',
                    on_click=change_club
                ).props(
                    'flat no-caps'
                ).classes(
                    'back-button w-full'
                )

                # =============================================
                # Selected Club Info
                # =============================================

                with ui.element(
                    'div'
                ).classes(
                    'info-box mt-5'
                ):

                    with ui.row().classes(
                        'w-full items-center gap-3'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'info-icon-box'
                        ):

                            ui.icon(
                                'account_balance'
                            ).classes(
                                'text-blue-700 text-lg'
                            )

                        with ui.column().classes(
                            'gap-0'
                        ):

                            ui.label(
                                'النادي المختار'
                            ).classes(
                                'info-title'
                            )

                            ui.label(
                                club_name
                            ).classes(
                                'info-value mt-1'
                            )

                # =============================================
                # Footer
                # =============================================

                ui.label(
                    'Egypt Football Club Management System'
                ).classes(
                    'login-footer mt-6'
                )