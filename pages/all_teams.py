from nicegui import ui, app
import database as db


def content():
    # =========================================================
    # جلب الأندية
    # =========================================================

    clubs = db.fetch_all(
        """
        SELECT
            c.Id,
            c.ClubNameAR,
            c.ClubNameEN,
            COUNT(DISTINCT t.Id) AS TeamCount,
            COUNT(DISTINCT p.Id) AS PlayerCount
        FROM Club c
        LEFT JOIN Team t
            ON t.Clubid = c.Id
        LEFT JOIN Player p
            ON p.ClubId = c.Id
        GROUP BY
            c.Id,
            c.ClubNameAR,
            c.ClubNameEN
        ORDER BY c.Id
        """
    )

    # =========================================================
    # CSS
    # =========================================================

    ui.add_head_html(
        '''
        <style>

            .clubs-page {
                min-height: 100vh;
                background:
                    radial-gradient(
                        circle at top right,
                        rgba(30,58,138,.08),
                        transparent 28%
                    ),
                    radial-gradient(
                        circle at bottom left,
                        rgba(245,158,11,.08),
                        transparent 28%
                    ),
                    linear-gradient(
                        135deg,
                        #f8fafc 0%,
                        #eef2f7 100%
                    );
            }

            .hero {
                background:
                    linear-gradient(
                        135deg,
                        #0f172a 0%,
                        #1e293b 55%,
                        #1e3a8a 100%
                    );
                border-radius: 28px;
                box-shadow:
                    0 20px 45px rgba(15,23,42,.15);
                position: relative;
                overflow: hidden;
            }

            .hero::before {
                content: "";
                position: absolute;
                width: 260px;
                height: 260px;
                border-radius: 50%;
                right: -90px;
                top: -120px;
                background: rgba(255,255,255,.06);
            }

            .hero::after {
                content: "";
                position: absolute;
                width: 190px;
                height: 190px;
                border-radius: 50%;
                left: 25%;
                bottom: -120px;
                background: rgba(245,158,11,.08);
            }

            .club-card {
                width: 285px;
                min-height: 245px;
                background: rgba(255,255,255,.97);
                border: 1px solid #e2e8f0;
                border-radius: 24px;
                box-shadow:
                    0 8px 25px rgba(15,23,42,.06);
                transition:
                    transform .22s ease,
                    box-shadow .22s ease,
                    border-color .22s ease;
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }

            .club-card::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 5px;
                background:
                    linear-gradient(
                        90deg,
                        #0f172a,
                        #1e3a8a,
                        #f59e0b
                    );
            }

            .club-card:hover {
                transform: translateY(-8px);
                box-shadow:
                    0 20px 45px rgba(15,23,42,.13);
                border-color: #f59e0b;
            }

            .club-logo {
                width: 82px;
                height: 82px;
                border-radius: 24px;
                background:
                    linear-gradient(
                        135deg,
                        #0f172a,
                        #1e293b
                    );
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow:
                    0 10px 25px rgba(15,23,42,.16);
            }

            .club-name {
                color: #0f172a;
                font-size: 19px;
                font-weight: 900;
                text-align: center;
                line-height: 1.5;
            }

            .club-name-en {
                color: #94a3b8;
                font-size: 12px;
                text-align: center;
            }

            .stat-box {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
                padding: 9px 14px;
                min-width: 95px;
            }

            .section-title {
                color: #0f172a;
                font-size: 21px;
                font-weight: 900;
            }

            .empty-card {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 24px;
                box-shadow:
                    0 8px 25px rgba(15,23,42,.05);
            }

        </style>
        '''
    )

    # =========================================================
    # الصفحة
    # =========================================================

    with ui.column().classes(
        'clubs-page w-full p-4 md:p-6 lg:p-8 gap-6'
    ):

        # =====================================================
        # Header
        # =====================================================

        with ui.element('div').classes(
            'hero w-full p-6 md:p-8'
        ):

            with ui.row().classes(
                'w-full items-center justify-between relative z-10'
            ):

                with ui.column().classes('gap-1'):

                    ui.label(
                        '⚽ أندية الدوري المصري الممتاز'
                    ).classes(
                        'text-3xl md:text-4xl font-black text-white'
                    )

                    ui.label(
                        'اختر النادي للوصول إلى صفحة تسجيل الدخول'
                    ).classes(
                        'text-white/75 text-base md:text-lg mt-1'
                    )

                    ui.label(
                        '2026/27'
                    ).classes(
                        'text-amber-400 font-black text-lg mt-2'
                    )

                with ui.element('div').classes(
                    'w-20 h-20 md:w-24 md:h-24 '
                    'rounded-3xl bg-white/10 '
                    'border border-white/20 '
                    'flex items-center justify-center'
                ):
                    ui.label('⚽').classes(
                        'text-5xl'
                    )

        # =====================================================
        # Summary
        # =====================================================

        with ui.row().classes(
            'w-full items-center justify-between'
        ):

            with ui.row().classes(
                'items-center gap-3'
            ):

                ui.icon(
                    'groups'
                ).classes(
                    'text-2xl text-blue-700'
                )

                ui.label(
                    'الأندية'
                ).classes(
                    'section-title'
                )

            with ui.element('div').classes(
                'bg-white border border-slate-200 '
                'px-4 py-2 rounded-full shadow-sm'
            ):

                ui.label(
                    f'{len(clubs)} نادي'
                ).classes(
                    'text-slate-700 font-bold'
                )

        # =====================================================
        # Clubs
        # =====================================================

        if not clubs:

            with ui.column().classes(
                'empty-card w-full items-center '
                'justify-center p-14'
            ):

                ui.icon(
                    'sports_soccer'
                ).classes(
                    'text-7xl text-slate-300'
                )

                ui.label(
                    'لا توجد أندية'
                ).classes(
                    'text-2xl font-black text-slate-600 mt-5'
                )

                ui.label(
                    'لم يتم تسجيل أي نادي في قاعدة البيانات حتى الآن'
                ).classes(
                    'text-slate-400 text-sm mt-2'
                )

        else:

            with ui.row().classes(
                'w-full justify-center flex-wrap gap-6'
            ):

                for club in clubs:

                    club_id = club['Id']
                    club_name_ar = (
                        club['ClubNameAR']
                        or 'بدون اسم'
                    )
                    club_name_en = (
                        club['ClubNameEN']
                        or ''
                    )

                    team_count = (
                        club['TeamCount']
                        or 0
                    )

                    player_count = (
                        club['PlayerCount']
                        or 0
                    )

                    def select_club(
                        selected_club_id=club_id
                    ):
                        app.storage.user.update({
                            'selected_club_id': selected_club_id
                        })

                        ui.navigate.to('/login')

                    with ui.element(
                        'div'
                    ).classes(
                        'club-card'
                    ).on(
                        'click',
                        select_club
                    ):

                        with ui.column().classes(
                            'w-full h-full items-center '
                            'justify-center p-6'
                        ):

                            # =================================
                            # Logo
                            # =================================

                            with ui.element(
                                'div'
                            ).classes(
                                'club-logo mb-4'
                            ):
                                ui.label(
                                    '⚽'
                                ).classes(
                                    'text-4xl'
                                )

                            # =================================
                            # Name
                            # =================================

                            ui.label(
                                club_name_ar
                            ).classes(
                                'club-name'
                            )

                            if club_name_en:

                                ui.label(
                                    club_name_en
                                ).classes(
                                    'club-name-en mt-1'
                                )

                            # =================================
                            # Statistics
                            # =================================

                            with ui.row().classes(
                                'items-center justify-center '
                                'gap-2 mt-5'
                            ):

                                with ui.element(
                                    'div'
                                ).classes(
                                    'stat-box'
                                ):

                                    with ui.row().classes(
                                        'items-center '
                                        'justify-center gap-2'
                                    ):
                                        ui.icon(
                                            'groups'
                                        ).classes(
                                            'text-blue-600 text-lg'
                                        )

                                        with ui.column().classes(
                                            'items-start gap-0'
                                        ):
                                            ui.label(
                                                str(team_count)
                                            ).classes(
                                                'text-slate-900 '
                                                'font-black text-lg'
                                            )

                                            ui.label(
                                                'Team'
                                            ).classes(
                                                'text-slate-400 '
                                                'text-xs'
                                            )

                                with ui.element(
                                    'div'
                                ).classes(
                                    'stat-box'
                                ):

                                    with ui.row().classes(
                                        'items-center '
                                        'justify-center gap-2'
                                    ):
                                        ui.icon(
                                            'person'
                                        ).classes(
                                            'text-emerald-600 text-lg'
                                        )

                                        with ui.column().classes(
                                            'items-start gap-0'
                                        ):
                                            ui.label(
                                                str(player_count)
                                            ).classes(
                                                'text-slate-900 '
                                                'font-black text-lg'
                                            )

                                            ui.label(
                                                'Player'
                                            ).classes(
                                                'text-slate-400 '
                                                'text-xs'
                                            )

                            # =================================
                            # Login
                            # =================================

                            with ui.row().classes(
                                'items-center gap-2 mt-5'
                            ):

                                ui.icon(
                                    'login'
                                ).classes(
                                    'text-amber-500 text-sm'
                                )

                                ui.label(
                                    'اضغط للدخول'
                                ).classes(
                                    'text-slate-500 '
                                    'text-sm font-bold'
                                )

        # =====================================================
        # Footer
        # =====================================================

        with ui.column().classes(
            'w-full items-center mt-4'
        ):

            ui.label(
                'Egypt Football Club Management System'
            ).classes(
                'text-slate-400 text-sm font-medium'
            )

            ui.label(
                'نظام إدارة أندية كرة القدم'
            ).classes(
                'text-slate-400 text-xs mt-1'
            )