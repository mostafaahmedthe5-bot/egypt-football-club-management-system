from nicegui import ui
import database as db

def content(club_id=1): # افترضنا النادي رقم 1 حالياً للتجربة
    ui.label('📊 لوحة التحكم والإحصائيات').classes('text-2xl font-bold mb-4')
    
    # جلب إحصائيات
    players_count = len(db.fetch_all("SELECT Id FROM Player WHERE ClubId = ?", (club_id,)))
    teams_count = len(db.fetch_all("SELECT Id FROM Team WHERE Clubid = ?", (club_id,)))
    
    # كروت الإحصائيات
    with ui.row().classes('w-full gap-4 mb-6'):
        with ui.card().classes('w-60 p-4 bg-blue-50 text-center border-l-4 border-blue-500'):
            ui.label('إجمالي اللاعبين').classes('text-gray-600')
            ui.label(str(players_count)).classes('text-3xl font-bold text-blue-600')
            
        with ui.card().classes('w-60 p-4 bg-green-50 text-center border-l-4 border-green-500'):
            ui.label('إجمالي الفرق').classes('text-gray-600')
            ui.label(str(teams_count)).classes('text-3xl font-bold text-green-600')