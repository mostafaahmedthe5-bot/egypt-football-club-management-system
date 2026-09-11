from nicegui import app, ui
from pages import (
    dashboard,
    teams,
    players,
    login,
    select_club,
    teams_buttons,
    medical,
    tournaments,
    memberships,
)

# =========================================================
# قائمة التوجيه وتفاصيل الهيدر
# =========================================================
NAV_ITEMS = [
    ('الرئيسية', 'dashboard', '/dashboard'),
    ('الفرق', 'groups', '/teams'),
    ('اللاعبين', 'person', '/players'),
    ('الكشف الطبي', 'medical_services', '/medical'),
    ('البطولات', 'emoji_events', '/tournaments'),
    ('العضويات', 'card_membership', '/memberships'),
    ('كل الأندية', 'sports_soccer', '/all_teams'),
]

# =========================================================
# دالة التحقق من الصلاحيات والتحويل
# =========================================================
def check_auth_and_redirect() -> bool:
    """التحقق من حالة تسجيل الدخول واختيار النادي قبل تحميل الصفحة."""
    if not app.storage.user.get('is_logged_in', False):
        if 'selected_club_id' not in app.storage.user:
            ui.navigate.to('/select_club')
        else:
            ui.navigate.to('/login')
        return False
    return True


# =========================================================
# القالب العام للواجهة (Global Layout)
# =========================================================
def apply_layout(title: str, page_content_func):
    if not check_auth_and_redirect():
        return

    username = app.storage.user.get('username', 'المستخدم')
    role = app.storage.user.get('role', '')
    club_id = app.storage.user.get('club_id')

    # تنسيق الاتجاه والخلفية العائمة للصفحة
    ui.query('body').style(
        'margin: 0; min-height: 100vh; background: #f8fafc; direction: rtl;'
    )

    # --- الهيدر العلوي ---
    with ui.header().classes(
    'w-full bg-[#F7F3EC]/10 backdrop-blur-lg '
    'text-slate-900 border-b border-[#B49A5A]/10 '
    'px-4 lg:px-6 py-3'
):
        with ui.row().classes('w-full items-center justify-between gap-4 flex-wrap'):

            # الهوية واللوجو
            with ui.row().classes('items-center gap-3'):
                with ui.element('div').classes(
                    'w-11 h-11 rounded-xl bg-amber-500 flex items-center justify-center shadow-sm'
                ):
                    ui.icon('sports_soccer').classes('text-2xl text-slate-950')

                with ui.column().classes('gap-0'):
                    ui.label('نظام إدارة الأندية الرياضية').classes(
                        'text-base md:text-lg font-black text-slate-900 leading-tight'
                    )

                    ui.label('Sports Club Management System').classes(
                        'text-[9px] md:text-[10px] text-slate-500 tracking-widest'
                    )

            # شريط التنقل الرئيسي (مع تمييز الصفحة الحالية)
            with ui.row().classes('items-center gap-1 flex-wrap justify-center'):
                for label, icon, path in NAV_ITEMS:
                    is_active = title == label
                    active_classes = (
                    'bg-[#B49A5A] text-black font-bold'
                    if is_active
                    else 'text-black hover:bg-[#E8DCC8]'
                )

                    ui.button(
                        label,
                        icon=icon,
                        on_click=lambda p=path: ui.navigate.to(p)
                    ).props('flat no-caps').classes(
                        f'{active_classes} text-xs rounded-lg px-3 py-1.5 transition-colors'
                    )

            # منطقة المستخدم وزر الخروج
            with ui.row().classes('items-center gap-2'):
                with ui.element('div').classes(
                    'flex items-center gap-2 bg-[#B89F7A] border border-slate-700 rounded-xl px-3 py-1.5'
                ):
                    with ui.element('div').classes(
                        'w-7 h-7 rounded-lg bg-slate-700 flex items-center justify-center'
                    ):
                        ui.icon('person').classes('text-base text-slate-200')

                    with ui.column().classes('gap-0'):
                        ui.label(username).classes('text-xs font-bold text-white')
                        if role:
                            ui.label(role).classes('text-[9px] text-slate-400')

                def logout():
                    app.storage.user.clear()
                    ui.navigate.to('/select_club')

                ui.button('خروج', icon='logout', on_click=logout).props(
                    'unelevated no-caps'
                ).classes(
                    'bg-red-600 hover:bg-red-700 text-white text-xs font-bold rounded-xl px-4 transition-colors'
                )

    # --- المحتوى الرئيسي للصفحة ---
    with ui.element('main').classes('w-full min-h-[calc(100vh-80px)] bg-slate-50'):
        with ui.column().classes('w-full px-3 sm:px-4 md:px-6 lg:px-8 py-4 md:py-6'):
            page_content_func(club_id)


# =========================================================
# المسارات والتوجيه (Routes)
# =========================================================

@ui.page('/select_club')
def select_club_page():
    select_club.content()


@ui.page('/login')
def login_page():
    if 'selected_club_id' not in app.storage.user:
        ui.navigate.to('/select_club')
        return
    if app.storage.user.get('is_logged_in', False):
        ui.navigate.to('/dashboard')
        return
    login.content()


@ui.page('/')
def index_page():
    apply_layout('الرئيسية', dashboard.content)


@ui.page('/dashboard')
def dashboard_page():
    apply_layout('الرئيسية', dashboard.content)


@ui.page('/teams')
def teams_page():
    apply_layout('الفرق', teams.content)


@ui.page('/players')
def players_page():
    apply_layout('اللاعبين', players.content)


@ui.page('/medical')
def medical_page():
    apply_layout('الكشف الطبي', medical.content)
    
    
    
    
@ui.page('/memberships')
def memberships_page():
    apply_layout(
        'العضويات',
        memberships.content
    )



@ui.page('/tournaments')
def tournaments_page():
    apply_layout(
        'البطولات',
        tournaments.content
    )


@ui.page('/all_teams')
def all_teams_page():
    apply_layout('كل الأندية', teams_buttons.content)


# =========================================================
# تشغيل التطبيق
# =========================================================
ui.run(
    title='نظام الأندية',
    language='ar',
    port=8080,
    storage_secret='football_secret_key_123',
)