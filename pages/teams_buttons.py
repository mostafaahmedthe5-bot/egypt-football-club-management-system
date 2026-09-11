from nicegui import ui
import database as db

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



def content(club_id=None):
    # =========================================================
    # جلب كل الأندية
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
                background: rgba(255,255,255,.98);
                border: 1px solid #e2e8f0;
                border-radius: 24px;
                box-shadow:
                    0 8px 25px rgba(15,23,42,.06);
                transition:
                    transform .22s ease,
                    box-shadow .22s ease,
                    border-color .22s ease;
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
                transform: translateY(-6px);
                box-shadow:
                    0 20px 45px rgba(15,23,42,.12);
                border-color: #cbd5e1;
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
                        ' جميع الأندية'
                    ).classes(
                        'text-3xl md:text-4xl '
                        'font-black text-white'
                    )

                    ui.label(
                        'نظرة عامة على الأندية الموجودة في النظام'
                    ).classes(
                        'text-white/75 '
                        'text-base md:text-lg mt-1'
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
                    'الأندية الموجودة'
                ).classes(
                    'section-title'
                )

            ui.label(
                f'{len(clubs)} نادي'
            ).classes(
                'bg-white border border-slate-200 '
                'text-slate-700 px-4 py-2 '
                'rounded-full shadow-sm font-bold'
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
                    'text-2xl font-black '
                    'text-slate-600 mt-5'
                )

                ui.label(
                    'لا توجد بيانات في جدول Club'
                ).classes(
                    'text-slate-400 text-sm mt-2'
                )

        else:

            with ui.row().classes(
                'w-full justify-center '
                'flex-wrap gap-6'
            ):


                for club in clubs:

                    club_name_ar = (
                        club['ClubNameAR']
                        or 'بدون اسم'
                    )

                    logo_url = get_club_logo_url(club_name_ar)

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



                    # =================================================
                    # Card - View Only
                    # =================================================

                    with ui.element(
                        'div'
                    ).classes(
                        'club-card'
                    ):

                        with ui.column().classes(
                            'w-full h-full items-center '
                            'justify-center p-6'
                        ):

                            # =========================================
                            # Logo
                            # =========================================

                           
                            with ui.element(
                                'div'
                            ).classes(
                                'club-logo mb-4'
                            ):

                                if logo_url:

                                    ui.image(
                                        logo_url
                                    ).classes(
                                        'w-[72px] h-[72px] object-contain'
                                    )

                                else:

                                    ui.icon(
                                        'sports_soccer'
                                    ).classes(
                                        'text-4xl text-slate-400'
                                    )



                            # =========================================
                            # Name
                            # =========================================

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

                            # =========================================
                            # Statistics
                            # =========================================

                            with ui.row().classes(
                                'items-center '
                                'justify-center '
                                'gap-2 mt-5'
                            ):

                                # Teams
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
                                                'text-slate-400 text-xs'
                                            )

                                # Players
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
                                                'text-slate-400 text-xs'
                                            )

                            # =========================================
                            # View Only
                            # =========================================

                            with ui.row().classes(
                                'items-center gap-2 mt-5'
                            ):

                                ui.icon(
                                    'visibility'
                                ).classes(
                                    'text-slate-400 text-sm'
                                )

                                ui.label(
                                    'عرض فقط'
                                ).classes(
                                    'text-slate-400 '
                                    'text-xs font-bold'
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