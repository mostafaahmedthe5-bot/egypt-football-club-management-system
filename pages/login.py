from nicegui import ui, app
import database as db

def content():
    club_id = app.storage.user.get('selected_club_id')
    
    if not club_id:
        ui.navigate.to('/select_club')
        return

    # جلب اسم النادي والمستخدم المرتبط به
    club = db.fetch_one("SELECT * FROM Club WHERE Id = ?", (club_id,))
    user = db.fetch_one("SELECT * FROM Users WHERE ClubId = ?", (club_id,))
    
    club_name = club['ClubNameAR'] if club else 'النادي'

    with ui.card().classes('absolute-center w-96 p-6 shadow-lg rounded-lg items-center'):
        ui.label(f'🔐 تسجيل دخول {club_name}').classes('text-xl font-bold mb-4 text-blue-800 text-center')
        ui.label('كلمة المرور الافتتاحية: 123').classes('text-xs text-gray-400 mb-4')
        
        password = ui.input('كلمة المرور', password=True, password_toggle_button=True).classes('w-full mb-4')

        def handle_login():
            if user and password.value == user['Password']:
                app.storage.user['is_logged_in'] = True
                app.storage.user['username'] = user['Username']
                app.storage.user['role'] = user['Role']
                app.storage.user['club_id'] = user['ClubId']
                
                ui.notify('تم تسجيل الدخول بنجاح!', color='positive')
                ui.navigate.to('/')
            else:
                ui.notify('كلمة المرور غير صحيحة!', color='negative')

        ui.button('دخول', on_click=handle_login).classes('w-full bg-blue-600 text-white mb-2')
        ui.button('اختر نادي آخر', on_click=lambda: ui.navigate.to('/select_club')).classes('w-full text-gray-500').props('flat')