from nicegui import ui, app
import database as db

def content():
    with ui.column().classes('w-full items-center p-6'):
        ui.label('⚽ اختر ناديك المفضلة').classes('text-3xl font-bold mb-2 text-blue-900')
        ui.label('اضغط على اسم النادي لتسجيل الدخول مباشرة:').classes('text-gray-600 mb-6 text-lg')
        
        clubs = db.fetch_all("SELECT * FROM Club")
        
        # عرض الأندية في شكل أزرار كبيرة وواضحة ومتجاورة
        with ui.row().classes('w-full max-w-6xl flex-wrap justify-center gap-4'):
            for club in clubs:
                c_id = club['Id']
                c_name = club['ClubNameAR']
                
                # استخدام المتغير المحلي داخل الـ lambda بشكل صحيح
                def make_click_handler(club_id):
                    return lambda: (
                        app.storage.user.update({'selected_club_id': club_id}),
                        ui.navigate.to('/login')
                    )

                ui.button(c_name, on_click=make_click_handler(c_id)).classes(
                    'bg-blue-700 text-white px-6 py-4 text-lg font-bold shadow-lg rounded-xl hover:bg-blue-800 transition-transform transform hover:scale-105'
                )