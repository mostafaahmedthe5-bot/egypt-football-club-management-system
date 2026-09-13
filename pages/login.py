from nicegui import ui, app
import database as db
import base64

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
    return logos.get((club_name or '').strip())

def content():
    selected_club_id = app.storage.user.get('selected_club_id')
    if not selected_club_id:
        ui.navigate.to('/select_club')
        return

    club = db.fetch_one(
        """
        SELECT Id, ClubNameAR, ClubNameEN, Logo
        FROM Club
        WHERE Id = ?
        """,
        (selected_club_id,)
    )

    if not club:
        app.storage.user.pop('selected_club_id', None)
        ui.notify('النادي غير موجود', color='negative', position='top')
        ui.navigate.to('/select_club')
        return

    club_name = club.get('ClubNameAR') or ''
    club_name_en = club.get('ClubNameEN') or club_name

    # =========================================================
    # Logo
    # =========================================================

    raw_logo = club.get('Logo')
    club_logo_src = None

    if raw_logo:
        if isinstance(raw_logo, bytes):
            encoded = base64.b64encode(raw_logo).decode('utf-8')
            club_logo_src = f'data:image/png;base64,{encoded}'

        elif isinstance(raw_logo, str) and raw_logo.strip():
            club_logo_src = raw_logo.strip()

    if not club_logo_src:
        club_logo_src = get_club_logo_url(club_name)

    # =========================================================
    # Body
    # =========================================================

    ui.query('body').style("""
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        background: #ffffff !important;
        font-family: Inter, Arial, sans-serif;
    """)

    # =========================================================
    # CSS
    # =========================================================

    ui.add_head_html("""
        <style>
            * {
                box-sizing: border-box;
            }

            html,
            body {
                width: 100%;
                height: 100%;
            }

            /* =====================================================
               MAIN
               ===================================================== */

            .login-page {
                width: 100vw;
                height: 100vh;
                min-height: 600px;
                display: flex;
                flex-direction: row;
                direction: ltr;
                overflow: hidden;
                background: #ffffff;
            }

            /* =====================================================
               LEFT SIDE
               ===================================================== */

            .login-form-side {
                width: 43%;
                min-width: 500px;
                height: 100%;
                padding: 38px 58px 32px;
                background: #ffffff;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                position: relative;
                z-index: 5;
            }

            .brand {
                display: flex;
                align-items: center;
                gap: 9px;
                width: fit-content;
            }

            .brand-mark {
                width: 9px;
                height: 9px;
                background: #f59e0b;
                display: block;
            }

            .brand-name {
                margin: 0;
                font-size: 23px;
                line-height: 1;
                font-weight: 900;
                letter-spacing: -1px;
                color: #18181b;
            }

            .login-center {
                width: 100%;
                max-width: 410px;
                margin: auto;
            }

            .welcome-label {
                display: inline-flex;
                align-items: center;
                height: 27px;
                padding: 0 11px;
                margin-bottom: 18px;
                background: #fafafa;
                border-left: 3px solid #f59e0b;
                color: #71717a;
                font-size: 10px;
                font-weight: 800;
                letter-spacing: 1.2px;
                text-transform: uppercase;
            }

            .title-text {
                margin: 0 0 9px 0;
                color: #18181b;
                font-size: 31px;
                line-height: 1.15;
                font-weight: 800;
                letter-spacing: -1.1px;
            }

            .club-name {
                color: #f59e0b;
            }

            .subtitle-text {
                margin: 0 0 31px 0;
                color: #71717a;
                font-size: 13px;
                line-height: 1.6;
                font-weight: 400;
            }

            /* =====================================================
               INPUT
               ===================================================== */

            .password-input {
                width: 100%;
            }

            .password-input .q-field__control {
                height: 54px !important;
                min-height: 54px !important;
                border-radius: 0 !important;
                background: #ffffff !important;
            }

            .password-input .q-field__native {
                color: #18181b !important;
                font-size: 14px !important;
                font-weight: 500 !important;
            }

            .password-input .q-field__label {
                color: #a1a1aa !important;
                font-size: 13px !important;
            }

            .password-input .q-field__control:before {
                border: 1px solid #e4e4e7 !important;
                border-left: 3px solid #f59e0b !important;
            }

            .password-input .q-field__control:hover:before {
                border-color: #d4d4d8 !important;
                border-left-color: #f59e0b !important;
            }

            .password-input .q-field__control:after {
                border-color: #f59e0b !important;
                border-left-width: 3px !important;
            }

            .password-input .q-icon {
                color: #a1a1aa !important;
            }

            /* =====================================================
               INFO ROW
               ===================================================== */

            .info-row {
                width: 100%;
                min-height: 32px;
                margin-top: 9px;
                margin-bottom: 25px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
            }

            .password-hint {
                padding: 5px 9px;
                background: #fff7ed;
                color: #c2410c;
                border-left: 2px solid #f59e0b;
                font-size: 10px;
                font-weight: 800;
                letter-spacing: .2px;
            }

            .forgot-password {
                color: #71717a;
                font-size: 11px;
                font-weight: 600;
                cursor: pointer;
                transition: color .2s ease;
            }

            .forgot-password:hover {
                color: #18181b;
            }

            /* =====================================================
               BUTTONS
               ===================================================== */

            .buttons-row {
                width: 100%;
                display: flex;
                gap: 10px;
            }

            .login-button,
            .change-button {
                height: 52px !important;
                min-height: 52px !important;
                border-radius: 0 !important;
                box-shadow: none !important;
                transition:
                    transform .18s ease,
                    background .18s ease,
                    border-color .18s ease;
            }

            .login-button {
                flex: 1.15;
                background: #18181b !important;
                color: #ffffff !important;
            }

            .login-button:hover {
                background: #27272a !important;
                transform: translateY(-1px);
            }

            .change-button {
                flex: 1;
                background: #ffffff !important;
                color: #27272a !important;
                border: 1px solid #d4d4d8 !important;
            }

            .change-button:hover {
                background: #fafafa !important;
                border-color: #a1a1aa !important;
                transform: translateY(-1px);
            }

            .login-button .q-btn__content,
            .change-button .q-btn__content {
                font-size: 10px !important;
                font-weight: 800 !important;
                letter-spacing: 1px;
            }

            /* =====================================================
               FOOTER
               ===================================================== */

            .login-footer {
                width: 100%;
                display: flex;
                flex-direction: column;
                gap: 8px;
            }

            .footer-links {
                display: flex;
                align-items: center;
                gap: 20px;
            }

            .footer-link {
                color: #52525b;
                font-size: 10px;
                font-weight: 700;
                cursor: pointer;
                transition: color .2s ease;
            }

            .footer-link:hover {
                color: #18181b;
            }

            .footer-divider {
                width: 3px;
                height: 3px;
                background: #d4d4d8;
            }

            .copyright {
                color: #a1a1aa;
                font-size: 9px;
                font-weight: 500;
            }

            /* =====================================================
               RIGHT IMAGE
               ===================================================== */

            .login-image-side {
                width: 57%;
                height: 100%;
                position: relative;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                background-image:
                    linear-gradient(
                        135deg,
                        rgba(15, 23, 42, .58),
                        rgba(15, 23, 42, .18)
                    ),
                    url('https://images.unsplash.com/photo-1508098682722-e99c43a406b2?q=85&w=2000&auto=format&fit=crop');
                background-size: cover;
                background-position: center;
            }

            .login-image-side::before {
                content: '';
                position: absolute;
                inset: 0;
                background:
                    linear-gradient(
                        to bottom,
                        rgba(0, 0, 0, .05),
                        rgba(0, 0, 0, .28)
                    );
                pointer-events: none;
            }

            .image-label {
                position: absolute;
                top: 34px;
                right: 38px;
                z-index: 2;
                padding: 7px 11px;
                background: rgba(255, 255, 255, .9);
                color: #27272a;
                font-size: 9px;
                font-weight: 900;
                letter-spacing: 1.2px;
                text-transform: uppercase;
            }

            /* =====================================================
               LOGO CARD
               ===================================================== */

            .logo-wrapper {
                position: relative;
                z-index: 2;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 17px;
            }

            .logo-card {
                width: 285px;
                height: 285px;
                padding: 34px;
                background: rgba(255, 255, 255, .97);
                border-radius: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow:
                    0 30px 80px rgba(0, 0, 0, .38),
                    0 8px 25px rgba(0, 0, 0, .16);
                position: relative;
                overflow: hidden;
            }

            .logo-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 5px;
                background: #f59e0b;
            }

            .logo-card img {
                width: 100%;
                height: 100%;
                max-width: 100%;
                max-height: 100%;
                object-fit: contain;
                position: relative;
                z-index: 1;
            }

            .logo-fallback {
                color: #27272a !important;
            }

            .club-caption {
                padding: 8px 15px;
                background: rgba(0, 0, 0, .38);
                backdrop-filter: blur(8px);
                color: #ffffff;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: .4px;
            }

            /* =====================================================
               TABLET
               ===================================================== */

            @media (max-width: 1100px) {
                .login-form-side {
                    width: 48%;
                    min-width: 430px;
                    padding-left: 42px;
                    padding-right: 42px;
                }

                .login-image-side {
                    width: 52%;
                }

                .logo-card {
                    width: 245px;
                    height: 245px;
                }
            }

            /* =====================================================
               MOBILE
               ===================================================== */

            @media (max-width: 800px) {
                html,
                body {
                    overflow: auto !important;
                }

                .login-page {
                    min-height: 100vh;
                    height: auto;
                    flex-direction: column-reverse;
                    overflow: visible;
                }

                .login-image-side {
                    width: 100%;
                    height: 330px;
                    min-height: 330px;
                }

                .login-form-side {
                    width: 100%;
                    min-width: 0;
                    min-height: 560px;
                    height: auto;
                    padding: 28px 24px 25px;
                }

                .login-center {
                    max-width: 460px;
                    margin: 55px auto;
                }

                .logo-card {
                    width: 180px;
                    height: 180px;
                    padding: 25px;
                    border-radius: 25px;
                }

                .image-label {
                    top: 20px;
                    right: 20px;
                }

                .club-caption {
                    font-size: 10px;
                }

                .title-text {
                    font-size: 27px;
                }
            }

            @media (max-width: 450px) {
                .login-form-side {
                    padding-left: 18px;
                    padding-right: 18px;
                }

                .buttons-row {
                    flex-direction: column;
                }

                .login-button,
                .change-button {
                    width: 100%;
                }

                .info-row {
                    align-items: flex-start;
                }

                .forgot-password {
                    text-align: right;
                }

                .login-image-side {
                    height: 285px;
                    min-height: 285px;
                }

                .logo-card {
                    width: 155px;
                    height: 155px;
                    padding: 20px;
                }
            }
        </style>
    """)

    # =========================================================
    # PAGE
    # =========================================================

    with ui.element('div').classes('login-page'):

        # =====================================================
        # LEFT SIDE
        # =====================================================

        with ui.element('div').classes('login-form-side'):

            # Brand
            with ui.element('div').classes('brand'):
                ui.element('span').classes('brand-mark')
                ui.label('Football').classes('brand-name')

            # Login Form
            with ui.column().classes('login-center'):

                ui.label('CLUB MANAGEMENT SYSTEM').classes('welcome-label')

                ui.html(
                    f'<div class="title-text">Sign in to '
                    f'<span class="club-name">{club_name_en}</span></div>'
                )

                ui.label(
                    'Enter your password to access your club management dashboard.'
                ).classes('subtitle-text')

                password = ui.input(
                    'Password',
                    password=True,
                    password_toggle_button=True
                ).props(
                    'outlined'
                ).classes('password-input')

                with ui.row().classes('info-row'):
                    ui.label(
                        'Default Password: 123'
                    ).classes('password-hint')

                    ui.label(
                        'Forgot password?'
                    ).classes('forgot-password')

                # =================================================
                # Login Logic
                # =================================================

                is_logging_in = False

                def handle_login():
                    nonlocal is_logging_in

                    if is_logging_in:
                        return

                    entered_password = password.value or ''

                    if not entered_password.strip():
                        ui.notify(
                            'الرجاء إدخال كلمة المرور',
                            color='warning',
                            position='top'
                        )
                        password.run_method('focus')
                        return

                    is_logging_in = True
                    btn_login.disable()

                    try:
                        if entered_password != '123':
                            ui.notify(
                                'كلمة المرور غير صحيحة',
                                color='negative',
                                position='top'
                            )
                            password.value = ''
                            password.run_method('focus')
                            return

                        app.storage.user.update({
                            'is_logged_in': True,
                            'club_id': selected_club_id,
                            'club_name': club_name
                        })

                        ui.notify(
                            f'تم الدخول بنجاح إلى {club_name}',
                            color='positive',
                            position='top'
                        )

                        ui.navigate.to('/dashboard')

                    finally:
                        is_logging_in = False
                        btn_login.enable()

                def change_club():
                    app.storage.user.pop('selected_club_id', None)
                    ui.navigate.to('/select_club')

                password.on(
                    'keydown.enter',
                    lambda e: handle_login()
                )

                # Buttons
                with ui.row().classes('buttons-row'):

                    btn_login = ui.button(
                        'SIGN IN',
                        on_click=handle_login
                    ).props(
                        'unelevated no-caps'
                    ).classes('login-button')

                    ui.button(
                        'CHANGE CLUB',
                        on_click=change_club
                    ).props(
                        'unelevated no-caps'
                    ).classes('change-button')

            # =====================================================
            # Footer
            # =====================================================

            with ui.column().classes('login-footer'):

                with ui.row().classes('footer-links'):
                    ui.label(
                        'Important Information'
                    ).classes('footer-link')

                    ui.element('span').classes('footer-divider')

                    ui.label(
                        'Privacy Policy'
                    ).classes('footer-link')

                ui.label(
                    '© 2026 Football Management System'
                ).classes('copyright')

        # =====================================================
        # RIGHT SIDE
        # =====================================================

        with ui.element('div').classes('login-image-side'):

            ui.label(
                'SPORTS MANAGEMENT'
            ).classes('image-label')

            with ui.element('div').classes('logo-wrapper'):

                with ui.element('div').classes('logo-card'):

                    if club_logo_src:
                        ui.html(
                            f'<img src="{club_logo_src}" '
                            f'alt="{club_name}" '
                            f'onerror="this.style.display=\'none\'">'
                        )
                    else:
                        ui.icon(
                            'sports_soccer',
                            size='82px'
                        ).classes('logo-fallback')

                ui.label(club_name).classes('club-caption')