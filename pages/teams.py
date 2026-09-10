from nicegui import ui
import database as db

def content(club_id=1):
    ui.label('⚽ إدارة الفرق الرياضية').classes('text-2xl font-bold mb-4')
    
    # نموذج إضافة فريق جديد
    with ui.card().classes('w-full p-4 mb-6'):
        ui.label('إضافة فريق جديد').classes('text-lg font-bold mb-2')
        with ui.row().classes('w-full items-center gap-4'):
            team_ar = ui.input('اسم الفريق (عربي)').classes('flex-1')
            team_en = ui.input('اسم الفريق (إنجليزي)').classes('flex-1')
            
            def add_team():
                if team_ar.value:
                    db.execute_query(
                        "INSERT INTO Team (TeamAR, TeamEN, Clubid) VALUES (?, ?, ?)",
                        (team_ar.value, team_en.value, club_id)
                    )
                    ui.notify('تمت إضافة الفريق بنجاح!', color='positive')
                    team_ar.value = ''
                    team_en.value = ''
                    refresh_teams_table()

            ui.button('حفظ الفريق', on_click=add_team).classes('bg-blue-600 text-white')

    # جدول عرض الفرق
    teams_container = ui.column().classes('w-full')
    
    def refresh_teams_table():
        teams_container.clear()
        teams = db.fetch_all("SELECT Id, TeamAR, TeamEN FROM Team WHERE Clubid = ?", (club_id,))
        
        columns = [
            {'name': 'id', 'label': 'الكود', 'field': 'Id'},
            {'name': 'team_ar', 'label': 'اسم الفريق (عربي)', 'field': 'TeamAR'},
            {'name': 'team_en', 'label': 'اسم الفريق (إنجليزي)', 'field': 'TeamEN'},
        ]
        
        with teams_container:
            ui.table(columns=columns, rows=teams, row_key='Id').classes('w-full')

    refresh_teams_table()