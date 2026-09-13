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
    # =========================================================
    # النادي المختار
    # =========================================================

    selected_club_id = app.storage.user.get('selected_club_id')

    if not selected_club_id:
        ui.navigate.to('/select_club')
        return

    # =========================================================
    # بيانات النادي من الداتابيز
    # =========================================================

    club = db.fetch_one(
        """
        SELECT Id, ClubNameAR, ClubNameEN, Logo
        FROM Club
        WHERE Id = ?
        """,
        (selected_club_id,)
    )
    
    ui.query('body').style('''
        margin: 0 !important;
        padding: 0 !important;
        overflow-x: hidden;
        background-image: linear-gradient(rgba(15, 23, 42, 0.45), rgba(15, 23, 42, 0.45)), 
                          url('https://imgs.search.brave.com/HltLxaMmkYX97pQ9takCQTwKZVV8C_YLYGMXIp4-kp8/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90NC5m/dGNkbi5uZXQvanBn/LzIwLzQzLzI1LzEz/LzM2MF9GXzIwNDMy/NTEzNTFfRnFFeE9k/SzNUN2s1V0JGY3dr/SHE3V3RtZTc2b1ZD/VmcuanBn');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        min-height: 100vh;
    ''')
    

    if not club:
        app.storage.user.pop('selected_club_id', None)
        ui.notify('النادي غير موجود', color='negative')
        ui.navigate.to('/select_club')
        return

    club_name = club.get('ClubNameAR') or ''
    club_name_en = club.get('ClubNameEN') or ''

    # =========================================================
    # جلب اللوجو الصحيح وفق اسم النادي المختار
    # =========================================================
    raw_logo = club.get('Logo')
    club_logo_src = None

    if raw_logo:
        if isinstance(raw_logo, bytes):
            encoded = base64.b64encode(raw_logo).decode('utf-8')
            club_logo_src = f'data:image/png;base64,{encoded}'
        elif isinstance(raw_logo, str) and raw_logo.strip():
            club_logo_src = raw_logo

    # إذا لم يوجد لوجو في الداتابيز، البحث في القاموس حسب اسم النادي المختار
    if not club_logo_src:
        club_logo_src = get_club_logo_url(club_name)

    # =========================================================
    # CSS: إزالة كافة الحواف، الخانات البيضاء، والبرواز نهائياً
    # =========================================================

    ui.add_head_html('''
        <style>

            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                overflow-x: hidden;
                font-family: system-ui, -apple-system, sans-serif;
            }

            .login-page {
                position: relative;
                min-height: 100vh;
                width: 100%;
                overflow: hidden;
                background-image: linear-gradient(rgba(15, 23, 42, 0.45), rgba(15, 23, 42, 0.45)), 
                                  url('https://imgs.search.brave.com/HltLxaMmkYX97pQ9takCQTwKZVV8C_YLYGMXIp4-kp8/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90NC5m/dGNkbi5uZXQvanBn/LzIwLzQzLzI1LzEz/LzM2MF9GXzIwNDMy/NTEzNTFfRnFFeE9k/SzNUN2s1V0JGY3dr/SHE3V3RtZTc2b1ZD/VmcuanBn');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }

            .login-card {
                position: relative;
                z-index: 2;
                width: 440px;
                max-width: calc(100vw - 28px);
                background: rgba(255, 255, 255, 0.98);
                border: none !important;
                border-radius: 26px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.22);
                overflow: hidden;
            }

            .login-top {
                height: 6px;
                width: 100%;
                background: linear-gradient(
                    90deg,
                    #0f172a 0%,
                    #1e3a8a 48%,
                    #f59e0b 100%
                );
            }

            .login-content {
                width: 100%;
                padding: 30px 34px 28px;
            }

            /* =================================================
               إلغاء المربع الأبيض والحواف نهائياً وعرض اللوجو شفاف
               ================================================= */

            .club-logo-wrapper {
                width: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-top: 5px;
                margin-bottom: 16px;
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
            }

            .club-logo-img {
                height: 110px !important;
                width: auto !important;
                max-width: 160px !important;
                object-fit: contain !important;
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                outline: none !important;
                filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.12));
            }

            .club-logo-icon {
                color: #1e3a8a;
                font-size: 64px;
            }

            .login-title {
                color: #0f172a;
                font-size: 26px;
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
                color: #64748b;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: .7px;
                text-transform: uppercase;
            }

            .login-subtitle {
                color: #64748b;
                font-size: 14px;
                line-height: 1.6;
            }

            .security-badge {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 6px 14px;
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
            }

            .login-input {
                margin-top: 8px;
            }

            .login-input .q-field__control {
                min-height: 54px !important;
                border-radius: 14px !important;
                background: #f8fafc;
            }

            .login-input input {
                font-size: 16px !important;
                font-weight: 650 !important;
                color: #0f172a !important;
            }

            .login-input .q-field__label {
                font-weight: 600;
            }

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

            .login-button {
                height: 52px !important;
                border-radius: 14px !important;
                background: #1e3a8a !important;
                color: white !important;
                font-size: 16px !important;
                font-weight: 850 !important;
                box-shadow: 0 4px 12px rgba(30, 58, 138, 0.25);
            }

            .login-button.q-btn--disabled {
                opacity: .7 !important;
            }

            .back-button {
                height: 44px !important;
                border-radius: 12px !important;
                color: #64748b !important;
                font-size: 13px !important;
                font-weight: 750 !important;
            }

            .info-box {
                width: 100%;
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
                padding: 12px 14px;
            }

            .info-icon-box {
                width: 36px;
                height: 36px;
                flex-shrink: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 10px;
                background: rgba(30, 58, 138, .08);
            }

            .info-title {
                color: #334155;
                font-size: 12px;
                font-weight: 800;
            }

            .info-value {
                color: #64748b;
                font-size: 12px;
                font-weight: 700;
            }

            .login-footer {
                color: #94a3b8;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: .3px;
            }

            @media (max-width: 520px) {
                .login-page {
                    padding: 12px !important;
                }
                .login-card {
                    width: 100%;
                    max-width: 420px;
                    border-radius: 20px;
                }
                .login-content {
                    padding: 24px 18px 20px;
                }
                .club-logo-img {
                    height: 90px !important;
                }
                .login-title {
                    font-size: 22px;
                }
                .club-name {
                    font-size: 17px;
                }
            }
        </style>
    ''')

    # =========================================================
    # الواجهة
    # =========================================================

    with ui.column().classes('login-page w-full items-center justify-center p-4'):
        with ui.card().classes('login-card p-0'):
            ui.element('div').classes('login-top')

            with ui.column().classes('login-content items-center'):

                # عرض اللوجو الخاص بالنادي المختار بدون أطراف بيضاء
                with ui.element('div').classes('club-logo-wrapper'):
                    if club_logo_src:
                        ui.html(f'<img src="{club_logo_src}" class="club-logo-img" alt="{club_name}" />')
                    else:
                        ui.icon('sports_soccer').classes('club-logo-icon')

                # الشارة الأمنية
                with ui.row().classes('items-center justify-center mb-4'):
                    with ui.element('div').classes('security-badge'):
                        ui.element('span').classes('security-dot')
                        ui.label('نظام آمن لإدارة النادي')

                # العناوين
                ui.label('تسجيل الدخول').classes('login-title mb-2')
                ui.label(club_name).classes('club-name text-center')
                ui.label(club_name_en).classes('club-name-en mt-1')
                ui.label('مرحبًا بك في نظام إدارة النادي').classes('login-subtitle text-center mt-3 mb-6')

                # إدخال كلمة المرور
                password = ui.input(
                    'كلمة المرور',
                    password=True,
                    password_toggle_button=True
                ).props('outlined').classes('w-full login-input')

                # التلميح
                with ui.element('div').classes('password-hint'):
                    ui.label('كلمة المرور الافتتاحية').classes('password-hint-label')
                    ui.label('123').classes('password-hint-value')

                is_logging_in = False

                def handle_login():
                    nonlocal is_logging_in
                    if is_logging_in:
                        return

                    entered_password = password.value or ''

                    if not entered_password.strip():
                        ui.notify('من فضلك أدخل كلمة المرور', color='warning', position='top')
                        password.run_method('focus')
                        return

                    is_logging_in = True
                    login_button.disable()

                    try:
                        if entered_password != '123':
                            ui.notify('كلمة المرور غير صحيحة', color='negative', position='top')
                            password.value = ''
                            password.run_method('focus')
                            return

                        app.storage.user.update({
                            'is_logged_in': True,
                            'club_id': selected_club_id,
                            'club_name': club_name
                        })

                        ui.notify(f'تم تسجيل الدخول إلى {club_name} بنجاح', color='positive', position='top')
                        ui.navigate.to('/dashboard')

                    finally:
                        is_logging_in = False
                        login_button.enable()

                login_button = ui.button(
                    'دخول إلى النظام',
                    icon='login',
                    on_click=handle_login
                ).props('unelevated no-caps').classes('login-button w-full mb-2')

                password.on('keydown.enter', lambda e: handle_login())

                def change_club():
                    app.storage.user.pop('selected_club_id', None)
                    ui.navigate.to('/select_club')

                ui.button(
                    'اختيار نادي آخر',
                    icon='swap_horiz',
                    on_click=change_club
                ).props('flat no-caps').classes('back-button w-full')

                with ui.element('div').classes('info-box mt-5'):
                    with ui.row().classes('w-full items-center gap-3'):
                        with ui.element('div').classes('info-icon-box'):
                            ui.icon('account_balance').classes('text-blue-700 text-lg')
                        with ui.column().classes('gap-0'):
                            ui.label('النادي المختار').classes('info-title')
                            ui.label(club_name).classes('info-value mt-1')

                ui.label('Egypt Football Club Management System').classes('login-footer mt-6')