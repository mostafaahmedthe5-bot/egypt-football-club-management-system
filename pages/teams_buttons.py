from nicegui import ui

def content(club_id=1):
    ui.label('⚽ أندية الدوري المصري الممتاز (2026/27)').classes('text-2xl font-bold mb-4')
    ui.label('اضغط على أي نادي لعرضه:').classes('text-gray-500 mb-4')

    # قائمة الأندية
    teams_list = [
        "الأهلي", "الزمالك", "بيراميدز", "المصري", "الإسماعيلي",
        "الاتحاد السكندري", "سموحة", "إنبي", "البنك الأهلي",
        "سيراميكا كليوباترا", "الجونة", "طلائع الجيش", "مودرن سبورت",
        "زد", "المقاولون العرب", "وادي دجلة", "غزل المحلة", "فاركو",
        "حرس الحدود", "بتروجيت", "كهرباء الإسماعيلية"
    ]

    # عرض الأندية في شكل أزرار متجاورة في سطور
    with ui.row().classes('w-full flex-wrap gap-2'):
        for team in teams_list:
            ui.button(
                team, 
                on_click=lambda t=team: ui.notify(f'تم اختيار نادي: {t}')
            ).classes('bg-white text-blue-900 border border-blue-300 hover:bg-blue-600 hover:text-white shadow-sm')