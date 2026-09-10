from nicegui import ui
import database as db

def content(club_id=1):
    ui.label('🏃‍♂️ قائمة وإدارة اللاعبين').classes('text-2xl font-bold mb-4')

    # جلب الفرق المتاحة للنادي
    teams = db.fetch_all("SELECT Id, TeamAR FROM Team WHERE Clubid = ?", (club_id,))
    team_options = {t['Id']: t['TeamAR'] for t in teams}

    # إضافة لاعب جديد
    with ui.card().classes('w-full p-4 mb-6'):
        ui.label('تسجيل لاعب جديد').classes('text-lg font-bold mb-2')
        with ui.row().classes('w-full items-center gap-4'):
            name_ar = ui.input('اسم اللاعب بالعربي').classes('flex-1')
            name_en = ui.input('اسم اللاعب بالإنجليزي').classes('flex-1')
            
            def save_player():
                if name_ar.value:
                    db.execute_query(
                        "INSERT INTO Player (PlayerNameAR, PlayerNameEN, ClubId) VALUES (?, ?, ?)",
                        (name_ar.value, name_en.value, club_id)
                    )
                    ui.notify('تم حفظ اللاعب بنجاح', color='positive')
                    name_ar.value = ''
                    name_en.value = ''
                    refresh_players()

            ui.button('تسجيل', on_click=save_player).classes('bg-green-600 text-white')

    # جدول اللاعبين
    players_container = ui.column().classes('w-full')

    def refresh_players():
        players_container.clear()
        players = db.fetch_all(
            "SELECT Id, PlayerNameAR, PlayerNameEN FROM Player WHERE ClubId = ?", 
            (club_id,)
        )
        
        columns = [
            {'name': 'id', 'label': 'الكود', 'field': 'Id'},
            {'name': 'name_ar', 'label': 'الاسم بالعربي', 'field': 'PlayerNameAR'},
            {'name': 'name_en', 'label': 'الاسم بالإنجليزي', 'field': 'PlayerNameEN'},
        ]
        
        with players_container:
            ui.table(columns=columns, rows=players, row_key='Id').classes('w-full')

    refresh_players()