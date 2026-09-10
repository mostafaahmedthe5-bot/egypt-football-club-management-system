from nicegui import ui, app
import database as db


def content(club_id=None):
    # =========================================================
    # النادي الحالي
    # =========================================================
    if club_id is None:
        club_id = app.storage.user.get('club_id')

    if not club_id:
        ui.navigate.to('/select_club')
        return

    # =========================================================
    # بيانات النادي
    # =========================================================
    club = db.fetch_one(
        "SELECT Id, ClubNameAR, ClubNameEN FROM Club WHERE Id = ?",
        (club_id,)
    )

    if not club:
        ui.notify('النادي غير موجود', color='negative')
        ui.navigate.to('/select_club')
        return

    club_name_ar = club['ClubNameAR'] or 'النادي'
    club_name_en = club['ClubNameEN'] or ''

    # =========================================================
    # الإحصائيات الأساسية
    # =========================================================

    players_count = len(
        db.fetch_all(
            "SELECT Id FROM Player WHERE ClubId = ?",
            (club_id,)
        )
    )

    teams_count = len(
        db.fetch_all(
            "SELECT Id FROM Team WHERE Clubid = ?",
            (club_id,)
        )
    )

    subscriptions_count = len(
        db.fetch_all(
            """
            SELECT pts.Id
            FROM PlayerTeamSubscribtion pts
            INNER JOIN Player p
                ON p.Id = pts.Playerid
            INNER JOIN Team t
                ON t.Id = pts.Teamid
            WHERE p.ClubId = ?
            AND t.Clubid = ?
            """,
            (club_id, club_id)
        )
    )

    tournaments_count = len(
        db.fetch_all(
            """
            SELECT DISTINCT tt.TournamentId
            FROM TournamentTable tt
            INNER JOIN Team t
                ON t.Id = tt.Teamid
            WHERE t.Clubid = ?
            """,
            (club_id,)
        )
    )

    # =========================================================
    # عدد الرياضات الموجودة في فرق النادي
    # =========================================================

    sports_count = len(
        db.fetch_all(
            """
            SELECT DISTINCT Sportid
            FROM Team
            WHERE Clubid = ?
            AND Sportid IS NOT NULL
            """,
            (club_id,)
        )
    )

    # =========================================================
    # بيانات Player مع الجداول المرتبطة
    # =========================================================

    player_details = db.fetch_all(
        """
        SELECT
            p.Id,
            p.PlayerNameAR,
            p.PlayerNameEN,
            p.ClubId,
            n.NationalityNameAR,
            bt.BloodTypeNameAR,
            e.EducationLevelNameAR,
            mrs.MedicalReportStateNameAR,
            ms.MembershipStatusNameAR,
            mt.MembershipTypeNameAR,
            r.ReligionNameAR,
            ws.WearingSizeName
        FROM Player p
        LEFT JOIN Nationality n
            ON n.Id = p.NationalityId
        LEFT JOIN BloodType bt
            ON bt.Id = p.BloodTypeId
        LEFT JOIN EducationLevel e
            ON e.Id = p.EducationLevelId
        LEFT JOIN MedicalReportState mrs
            ON mrs.Id = p.MedicalReportStatueId
        LEFT JOIN MembershipStatus ms
            ON ms.Id = p.MembershipStatueId
        LEFT JOIN MembershipType mt
            ON mt.Id = p.MembershipTypeId
        LEFT JOIN Religion r
            ON r.Id = p.ReligionId
        LEFT JOIN WearingSize ws
            ON ws.Id = p.WearingSizeId
        WHERE p.ClubId = ?
        ORDER BY p.Id DESC
        """,
        (club_id,)
    )

    # =========================================================
    # حالات MedicalReportState
    # =========================================================

    medical_states = db.fetch_all(
        """
        SELECT
            mrs.MedicalReportStateNameAR,
            COUNT(p.Id) AS Count
        FROM Player p
        LEFT JOIN MedicalReportState mrs
            ON mrs.Id = p.MedicalReportStatueId
        WHERE p.ClubId = ?
        GROUP BY p.MedicalReportStatueId
        """,
        (club_id,)
    )

    # =========================================================
    # حالات MembershipStatus
    # =========================================================

    membership_states = db.fetch_all(
        """
        SELECT
            ms.MembershipStatusNameAR,
            COUNT(p.Id) AS Count
        FROM Player p
        LEFT JOIN MembershipStatus ms
            ON ms.Id = p.MembershipStatueId
        WHERE p.ClubId = ?
        GROUP BY p.MembershipStatueId
        """,
        (club_id,)
    )

    # =========================================================
    # الفرق
    # =========================================================

    teams = db.fetch_all(
        """
        SELECT
            t.Id,
            t.TeamAR,
            t.TeamEN,
            tc.TeamCategoryNameAR,
            tc.TeamCategoryNameEN,
            s.SportNameAR,
            s.SportNameEN,
            COUNT(DISTINCT pts.Playerid) AS PlayerCount
        FROM Team t
        LEFT JOIN TeamCategory tc
            ON tc.Id = t.Teamcatgoryid
        LEFT JOIN Sport s
            ON s.Id = t.Sportid
        LEFT JOIN PlayerTeamSubscribtion pts
            ON pts.Teamid = t.Id
        WHERE t.Clubid = ?
        GROUP BY
            t.Id,
            t.TeamAR,
            t.TeamEN,
            tc.TeamCategoryNameAR,
            tc.TeamCategoryNameEN,
            s.SportNameAR,
            s.SportNameEN
        ORDER BY t.Id DESC
        """,
        (club_id,)
    )

    # =========================================================
    # آخر اللاعبين
    # =========================================================

    latest_players = db.fetch_all(
        """
        SELECT
            p.Id,
            p.PlayerNameAR,
            ms.MembershipStatusNameAR,
            mrs.MedicalReportStateNameAR
        FROM Player p
        LEFT JOIN MembershipStatus ms
            ON ms.Id = p.MembershipStatueId
        LEFT JOIN MedicalReportState mrs
            ON mrs.Id = p.MedicalReportStatueId
        WHERE p.ClubId = ?
        ORDER BY p.Id DESC
        LIMIT 8
        """,
        (club_id,)
    )

    # =========================================================
    # CSS
    # =========================================================

    ui.add_head_html(
        '''
        <style>

            .dashboard-page {
                min-height: 100vh;
                background:
                    radial-gradient(
                        circle at top right,
                        rgba(245,158,11,.08),
                        transparent 25%
                    ),
                    radial-gradient(
                        circle at bottom left,
                        rgba(30,58,138,.06),
                        transparent 30%
                    ),
                    #f8fafc;
            }

            .hero-card {
                width: 100%;
                border-radius: 26px;
                padding: 28px;
                background:
                    linear-gradient(
                        135deg,
                        #0f172a 0%,
                        #1e293b 55%,
                        #1e3a8a 100%
                    );
                box-shadow:
                    0 20px 45px rgba(15,23,42,.16);
                position: relative;
                overflow: hidden;
            }

            .hero-card::before {
                content: "";
                position: absolute;
                width: 220px;
                height: 220px;
                border-radius: 50%;
                background: rgba(255,255,255,.05);
                top: -100px;
                right: -60px;
            }

            .hero-card::after {
                content: "";
                position: absolute;
                width: 180px;
                height: 180px;
                border-radius: 50%;
                background: rgba(245,158,11,.08);
                bottom: -100px;
                left: 30%;
            }

            .stat-card {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
                padding: 20px;
                min-height: 155px;
                box-shadow:
                    0 8px 25px rgba(15,23,42,.05);
                transition: .2s ease;
            }

            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow:
                    0 18px 35px rgba(15,23,42,.10);
            }

            .stat-icon {
                width: 52px;
                height: 52px;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .section-card {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 22px;
                box-shadow:
                    0 8px 25px rgba(15,23,42,.05);
            }

            .section-title {
                color: #0f172a;
                font-size: 19px;
                font-weight: 900;
            }

            .team-item {
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                background: white;
                transition: .2s ease;
            }

            .team-item:hover {
                background: #f8fafc;
                transform: translateX(-2px);
            }

            .player-item {
                border-bottom: 1px solid #f1f5f9;
                padding: 13px 4px;
            }

            .player-item:last-child {
                border-bottom: none;
            }

        </style>
        '''
    )

    # =========================================================
    # الصفحة
    # =========================================================

    with ui.column().classes(
        'dashboard-page w-full p-4 md:p-6 lg:p-8 gap-6'
    ):

        # =====================================================
        # Header
        # =====================================================

        with ui.element('div').classes('hero-card'):

            with ui.row().classes(
                'w-full items-center justify-between relative z-10'
            ):

                with ui.column().classes('gap-1'):

                    ui.label(
                        '📊 لوحة التحكم والإحصائيات'
                    ).classes(
                        'text-3xl md:text-4xl font-black text-white'
                    )

                    ui.label(
                        club_name_ar
                    ).classes(
                        'text-xl md:text-2xl font-bold text-amber-400'
                    )

                    if club_name_en:
                        ui.label(
                            club_name_en
                        ).classes(
                            'text-sm text-white/60'
                        )

                    ui.label(
                        'مرحباً بك في نظام إدارة النادي'
                    ).classes(
                        'text-sm md:text-base text-white/70 mt-2'
                    )

                with ui.element('div').classes(
                    'w-20 h-20 md:w-24 md:h-24 '
                    'rounded-3xl bg-white/10 '
                    'border border-white/20 '
                    'flex items-center justify-center'
                ):
                    ui.label('⚽').classes(
                        'text-5xl md:text-6xl'
                    )

        # =====================================================
        # Main Statistics
        # =====================================================

        ui.label(
            'الإحصائيات الرئيسية'
        ).classes(
            'section-title'
        )

        with ui.row().classes(
            'w-full grid grid-cols-1 sm:grid-cols-2 '
            'lg:grid-cols-4 gap-4'
        ):

            # Players
            with ui.card().classes('stat-card w-full'):

                with ui.row().classes(
                    'w-full items-center justify-between'
                ):

                    with ui.element('div').classes(
                        'stat-icon bg-blue-50'
                    ):
                        ui.icon('groups').classes(
                            'text-2xl text-blue-600'
                        )

                    ui.label(
                        str(players_count)
                    ).classes(
                        'text-4xl font-black text-slate-900'
                    )

                ui.label(
                    'إجمالي اللاعبين'
                ).classes(
                    'text-slate-600 font-bold mt-4'
                )

                ui.label(
                    'Players'
                ).classes(
                    'text-xs text-slate-400 mt-1'
                )

            # Teams
            with ui.card().classes('stat-card w-full'):

                with ui.row().classes(
                    'w-full items-center justify-between'
                ):

                    with ui.element('div').classes(
                        'stat-icon bg-emerald-50'
                    ):
                        ui.icon('sports_soccer').classes(
                            'text-2xl text-emerald-600'
                        )

                    ui.label(
                        str(teams_count)
                    ).classes(
                        'text-4xl font-black text-slate-900'
                    )

                ui.label(
                    'إجمالي الفرق'
                ).classes(
                    'text-slate-600 font-bold mt-4'
                )

                ui.label(
                    'Team'
                ).classes(
                    'text-xs text-slate-400 mt-1'
                )

            # Subscriptions
            with ui.card().classes('stat-card w-full'):

                with ui.row().classes(
                    'w-full items-center justify-between'
                ):

                    with ui.element('div').classes(
                        'stat-icon bg-amber-50'
                    ):
                        ui.icon('assignment_ind').classes(
                            'text-2xl text-amber-600'
                        )

                    ui.label(
                        str(subscriptions_count)
                    ).classes(
                        'text-4xl font-black text-slate-900'
                    )

                ui.label(
                    'اشتراكات اللاعبين'
                ).classes(
                    'text-slate-600 font-bold mt-4'
                )

                ui.label(
                    'PlayerTeamSubscribtion'
                ).classes(
                    'text-xs text-slate-400 mt-1'
                )

            # Tournaments
            with ui.card().classes('stat-card w-full'):

                with ui.row().classes(
                    'w-full items-center justify-between'
                ):

                    with ui.element('div').classes(
                        'stat-icon bg-purple-50'
                    ):
                        ui.icon('emoji_events').classes(
                            'text-2xl text-purple-600'
                        )

                    ui.label(
                        str(tournaments_count)
                    ).classes(
                        'text-4xl font-black text-slate-900'
                    )

                ui.label(
                    'البطولات'
                ).classes(
                    'text-slate-600 font-bold mt-4'
                )

                ui.label(
                    'Tournament'
                ).classes(
                    'text-xs text-slate-400 mt-1'
                )

        # =====================================================
        # Secondary Statistics
        # =====================================================

        with ui.row().classes(
            'w-full grid grid-cols-1 md:grid-cols-3 gap-4'
        ):

            with ui.card().classes(
                'section-card w-full p-5'
            ):

                with ui.row().classes(
                    'items-center gap-3 mb-4'
                ):
                    with ui.element('div').classes(
                        'w-11 h-11 rounded-xl bg-blue-50 '
                        'flex items-center justify-center'
                    ):
                        ui.icon('sports').classes(
                            'text-xl text-blue-600'
                        )

                    ui.label(
                        'الرياضات'
                    ).classes(
                        'section-title'
                    )

                ui.label(
                    str(sports_count)
                ).classes(
                    'text-3xl font-black text-slate-900'
                )

                ui.label(
                    'رياضة مرتبطة بفرق النادي'
                ).classes(
                    'text-sm text-slate-500 mt-1'
                )

            with ui.card().classes(
                'section-card w-full p-5'
            ):

                with ui.row().classes(
                    'items-center gap-3 mb-4'
                ):
                    with ui.element('div').classes(
                        'w-11 h-11 rounded-xl bg-emerald-50 '
                        'flex items-center justify-center'
                    ):
                        ui.icon('health_and_safety').classes(
                            'text-xl text-emerald-600'
                        )

                    ui.label(
                        'MedicalReportState'
                    ).classes(
                        'section-title'
                    )

                if medical_states:

                    with ui.column().classes(
                        'w-full gap-2'
                    ):
                        for state in medical_states:

                            state_name = (
                                state['MedicalReportStateNameAR']
                                or 'غير محدد'
                            )

                            state_count = state['Count'] or 0

                            with ui.row().classes(
                                'w-full justify-between items-center'
                            ):
                                ui.label(
                                    state_name
                                ).classes(
                                    'text-slate-600 font-semibold'
                                )

                                ui.label(
                                    str(state_count)
                                ).classes(
                                    'font-black text-slate-900'
                                )

                else:

                    ui.label(
                        'لا توجد بيانات'
                    ).classes(
                        'text-slate-400'
                    )

            with ui.card().classes(
                'section-card w-full p-5'
            ):

                with ui.row().classes(
                    'items-center gap-3 mb-4'
                ):
                    with ui.element('div').classes(
                        'w-11 h-11 rounded-xl bg-amber-50 '
                        'flex items-center justify-center'
                    ):
                        ui.icon('card_membership').classes(
                            'text-xl text-amber-600'
                        )

                    ui.label(
                        'MembershipStatus'
                    ).classes(
                        'section-title'
                    )

                if membership_states:

                    with ui.column().classes(
                        'w-full gap-2'
                    ):
                        for state in membership_states:

                            state_name = (
                                state['MembershipStatusNameAR']
                                or 'غير محدد'
                            )

                            state_count = state['Count'] or 0

                            with ui.row().classes(
                                'w-full justify-between items-center'
                            ):
                                ui.label(
                                    state_name
                                ).classes(
                                    'text-slate-600 font-semibold'
                                )

                                ui.label(
                                    str(state_count)
                                ).classes(
                                    'font-black text-slate-900'
                                )

                else:

                    ui.label(
                        'لا توجد بيانات'
                    ).classes(
                        'text-slate-400'
                    )

        # =====================================================
        # Teams + Latest Players
        # =====================================================

        with ui.row().classes(
            'w-full grid grid-cols-1 lg:grid-cols-2 gap-6'
        ):

            # =================================================
            # Teams
            # =================================================

            with ui.card().classes(
                'section-card w-full p-5 md:p-6'
            ):

                with ui.row().classes(
                    'w-full items-center justify-between mb-5'
                ):

                    with ui.row().classes(
                        'items-center gap-3'
                    ):

                        with ui.element('div').classes(
                            'w-11 h-11 rounded-xl bg-slate-100 '
                            'flex items-center justify-center'
                        ):
                            ui.icon('groups').classes(
                                'text-xl text-slate-700'
                            )

                        ui.label(
                            'الفرق'
                        ).classes(
                            'section-title'
                        )

                    ui.label(
                        f'{teams_count} فريق'
                    ).classes(
                        'bg-slate-100 text-slate-600 '
                        'px-3 py-1 rounded-full text-xs font-bold'
                    )

                if teams:

                    with ui.column().classes(
                        'w-full gap-3'
                    ):

                        for team in teams:

                            team_name = (
                                team['TeamAR']
                                or team['TeamEN']
                                or 'فريق'
                            )

                            team_category = (
                                team['TeamCategoryNameAR']
                                or 'غير محدد'
                            )

                            sport_name = (
                                team['SportNameAR']
                                or 'غير محدد'
                            )

                            player_count = (
                                team['PlayerCount']
                                or 0
                            )

                            with ui.element('div').classes(
                                'team-item w-full p-4'
                            ):

                                with ui.row().classes(
                                    'w-full items-center justify-between'
                                ):

                                    with ui.row().classes(
                                        'items-center gap-3'
                                    ):

                                        with ui.element('div').classes(
                                            'w-10 h-10 rounded-xl '
                                            'bg-blue-50 '
                                            'flex items-center justify-center'
                                        ):
                                            ui.icon(
                                                'sports_soccer'
                                            ).classes(
                                                'text-lg text-blue-600'
                                            )

                                        with ui.column().classes(
                                            'gap-0'
                                        ):

                                            ui.label(
                                                team_name
                                            ).classes(
                                                'font-extrabold '
                                                'text-slate-800'
                                            )

                                            ui.label(
                                                f'{team_category} • {sport_name}'
                                            ).classes(
                                                'text-xs text-slate-400 mt-1'
                                            )

                                    with ui.column().classes(
                                        'items-end gap-0'
                                    ):

                                        ui.label(
                                            str(player_count)
                                        ).classes(
                                            'text-xl font-black '
                                            'text-slate-900'
                                        )

                                        ui.label(
                                            'لاعب'
                                        ).classes(
                                            'text-xs text-slate-400'
                                        )

                else:

                    with ui.column().classes(
                        'w-full items-center py-10'
                    ):

                        ui.icon('groups').classes(
                            'text-5xl text-slate-300'
                        )

                        ui.label(
                            'لا توجد فرق'
                        ).classes(
                            'text-slate-500 font-bold mt-3'
                        )

            # =================================================
            # Latest Players
            # =================================================

            with ui.card().classes(
                'section-card w-full p-5 md:p-6'
            ):

                with ui.row().classes(
                    'w-full items-center justify-between mb-5'
                ):

                    with ui.row().classes(
                        'items-center gap-3'
                    ):

                        with ui.element('div').classes(
                            'w-11 h-11 rounded-xl bg-blue-50 '
                            'flex items-center justify-center'
                        ):
                            ui.icon('person').classes(
                                'text-xl text-blue-600'
                            )

                        ui.label(
                            'آخر اللاعبين'
                        ).classes(
                            'section-title'
                        )

                    ui.label(
                        f'{players_count} لاعب'
                    ).classes(
                        'bg-blue-50 text-blue-600 '
                        'px-3 py-1 rounded-full text-xs font-bold'
                    )

                if latest_players:

                    with ui.column().classes(
                        'w-full'
                    ):

                        for player in latest_players:

                            player_name = (
                                player['PlayerNameAR']
                                or 'لاعب'
                            )

                            membership_name = (
                                player['MembershipStatusNameAR']
                                or 'غير محدد'
                            )

                            medical_name = (
                                player['MedicalReportStateNameAR']
                                or 'غير محدد'
                            )

                            with ui.element('div').classes(
                                'player-item w-full'
                            ):

                                with ui.row().classes(
                                    'w-full items-center '
                                    'justify-between'
                                ):

                                    with ui.row().classes(
                                        'items-center gap-3'
                                    ):

                                        with ui.element('div').classes(
                                            'w-9 h-9 rounded-full '
                                            'bg-slate-100 '
                                            'flex items-center justify-center'
                                        ):
                                            ui.icon('person').classes(
                                                'text-lg text-slate-600'
                                            )

                                        with ui.column().classes(
                                            'gap-0'
                                        ):
                                            ui.label(
                                                player_name
                                            ).classes(
                                                'font-bold text-slate-800'
                                            )

                                            ui.label(
                                                f'Membership: {membership_name}'
                                            ).classes(
                                                'text-xs text-slate-400 mt-1'
                                            )

                                    ui.badge(
                                        medical_name
                                    ).props(
                                        'outline'
                                    )

                else:

                    with ui.column().classes(
                        'w-full items-center py-10'
                    ):

                        ui.icon('person_off').classes(
                            'text-5xl text-slate-300'
                        )

                        ui.label(
                            'لا يوجد لاعبون'
                        ).classes(
                            'text-slate-500 font-bold mt-3'
                        )

        # =====================================================
        # Quick Actions
        # =====================================================

        with ui.card().classes(
            'section-card w-full p-5 md:p-6'
        ):

            with ui.row().classes(
                'items-center gap-3 mb-5'
            ):

                with ui.element('div').classes(
                    'w-11 h-11 rounded-xl bg-amber-50 '
                    'flex items-center justify-center'
                ):
                    ui.icon('bolt').classes(
                        'text-xl text-amber-600'
                    )

                ui.label(
                    'الوصول السريع'
                ).classes(
                    'section-title'
                )

            with ui.row().classes(
                'w-full flex-wrap gap-3'
            ):

                ui.button(
                    'اللاعبين',
                    icon='groups',
                    on_click=lambda: ui.navigate.to('/players')
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'bg-slate-900 text-white rounded-xl px-5 py-3'
                )

                ui.button(
                    'الفرق',
                    icon='sports_soccer',
                    on_click=lambda: ui.navigate.to('/teams')
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'bg-blue-700 text-white rounded-xl px-5 py-3'
                )

                ui.button(
                    'التسجيلات',
                    icon='assignment_ind',
                    on_click=lambda: ui.navigate.to('/registrations')
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'bg-emerald-600 text-white rounded-xl px-5 py-3'
                )

                ui.button(
                    'المعدات',
                    icon='inventory_2',
                    on_click=lambda: ui.navigate.to('/equipment')
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'bg-amber-500 text-white rounded-xl px-5 py-3'
                )