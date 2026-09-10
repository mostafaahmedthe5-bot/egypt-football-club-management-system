from nicegui import ui, app
from pages import dashboard, teams, players, login, select_club, teams_buttons, medical


def apply_layout(title, page_content_func):
    if not app.storage.user.get('is_logged_in', False):
        ui.navigate.to('/login')
        return

    username = app.storage.user.get('username')
    role = app.storage.user.get('role')
    club_id = app.storage.user.get('club_id')

    with ui.header().classes(
        'bg-blue-800 text-white justify-between items-center p-4'
    ):
        ui.label(
            'نظام إدارة أندية كرة القدم ⚽'
        ).classes(
            'text-xl font-bold'
        )

        with ui.row().classes(
            'items-center gap-4'
        ):
            ui.label(
                f'المستخدم: {username} ({role})'
            ).classes(
                'text-sm bg-blue-900 px-3 py-1 rounded'
            )

            ui.button(
                'خروج',
                on_click=lambda: (
                    app.storage.user.clear(),
                    ui.navigate.to('/select_club')
                )
            ).classes(
                'bg-red-600 text-sm'
            )

    with ui.left_drawer().classes(
        'bg-gray-100 p-4'
    ):
        ui.label(
            'القائمة الرئيسية'
        ).classes(
            'font-bold text-gray-500 mb-4'
        )

        ui.button(
            '📊 لوحة التحكم',
            on_click=lambda: ui.navigate.to('/')
        ).classes(
            'w-full text-right mb-2'
        ).props(
            'flat icon=dashboard'
        )

        ui.button(
            '⚽ إدارة الفرق',
            on_click=lambda: ui.navigate.to('/teams')
        ).classes(
            'w-full text-right mb-2'
        ).props(
            'flat icon=groups'
        )

        ui.button(
            '🏃‍♂️ اللاعبين',
            on_click=lambda: ui.navigate.to('/players')
        ).classes(
            'w-full text-right mb-2'
        ).props(
            'flat icon=person'
        )

        ui.button(
            '🩺 الكشف الطبي',
            on_click=lambda: ui.navigate.to('/medical')
        ).classes(
            'w-full text-right mb-2'
        ).props(
            'flat icon=medical_services'
        )

        ui.button(
            '🏆 كل الأندية',
            on_click=lambda: ui.navigate.to('/all_teams')
        ).classes(
            'w-full text-right mb-2'
        ).props(
            'flat icon=sports_soccer'
        )

    with ui.column().classes(
        'w-full p-6'
    ):
        page_content_func(club_id)


# =========================================================
# Routes
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
        ui.navigate.to('/')
        return

    login.content()


@ui.page('/')
def index_page():
    if not app.storage.user.get('is_logged_in', False):

        if 'selected_club_id' not in app.storage.user:
            ui.navigate.to('/select_club')
        else:
            ui.navigate.to('/login')

        return

    apply_layout(
        'لوحة التحكم',
        dashboard.content
    )


@ui.page('/dashboard')
def dashboard_page():
    if not app.storage.user.get('is_logged_in', False):

        if 'selected_club_id' not in app.storage.user:
            ui.navigate.to('/select_club')
        else:
            ui.navigate.to('/login')

        return

    apply_layout(
        'لوحة التحكم',
        dashboard.content
    )


@ui.page('/teams')
def teams_page():
    apply_layout(
        'الفرق',
        teams.content
    )


@ui.page('/players')
def players_page():
    apply_layout(
        'اللاعبين',
        players.content
    )


@ui.page('/medical')
def medical_page():
    apply_layout(
        'الكشف الطبي',
        medical.content
    )


@ui.page('/all_teams')
def all_teams_page():
    apply_layout(
        'جميع الأندية',
        teams_buttons.content
    )


ui.run(
    title='نظام الأندية',
    language='ar',
    port=8080,
    storage_secret='football_secret_key_123'
)