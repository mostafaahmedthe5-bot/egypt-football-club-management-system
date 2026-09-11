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
    # عدد الرياضات
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
    # بيانات اللاعبين
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
    # الحالات الطبية
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
    # حالات العضوية
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
    # أحدث اللاعبين
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
    # CSS STATIC
    # =========================================================

    ui.add_head_html(
        '''
        <style>

            html,
            body {
                margin: 0;
                padding: 0;
                min-height: 100%;
            }

            body {
                overflow-x: hidden;
                background: #f1f5f9;
            }

            /* =================================================
               MAIN
               ================================================= */

            .rtl-container {
                direction: rtl;
                width: 100%;
                max-width: 100% !important;
                min-height: 100vh;
                margin: 0;
                padding: 4px 4px 30px 4px;
            }

            .dashboard-content {
                width: 100%;
            }

            /* =================================================
               HERO
               ================================================= */

            .hero-card {
                width: 100%;
                min-height: 240px;
                border-radius: 24px;
                padding: 36px 40px;

                position: relative;
                overflow: hidden;

                background:
                    linear-gradient(
                        135deg,
                        #0f172a 0%,
                        #172554 50%,
                        #1e3a8a 100%
                    );

                border: 1px solid rgba(255,255,255,.08);

                box-shadow:
                    0 14px 35px rgba(15,23,42,.16);
            }

            .hero-card::before {
                content: "";

                position: absolute;

                width: 300px;
                height: 300px;

                border-radius: 50%;

                top: -150px;
                right: -90px;

                background:
                    radial-gradient(
                        circle,
                        rgba(56,189,248,.14),
                        transparent 70%
                    );
            }

            .hero-card::after {
                content: "";

                position: absolute;

                width: 240px;
                height: 240px;

                border-radius: 50%;

                bottom: -130px;
                left: 8%;

                background:
                    radial-gradient(
                        circle,
                        rgba(245,158,11,.08),
                        transparent 70%
                    );
            }

            .hero-content {
                position: relative;
                z-index: 2;
            }

            .hero-icon-box {
                width: 68px;
                height: 68px;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 18px;

                background:
                    rgba(255,255,255,.08);

                border:
                    1px solid
                    rgba(255,255,255,.12);
            }

            .hero-title {
                color: white;
                font-size: 32px;
                font-weight: 900;
                line-height: 1.25;
            }

            .hero-club-name {
                color: #38bdf8;
                font-size: 25px;
                font-weight: 850;
            }

            .hero-club-en {
                color: #94a3b8;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 3px;
            }

            .hero-description {
                color: #cbd5e1;
                font-size: 14px;
                line-height: 1.8;
                max-width: 700px;
            }

            .hero-status {
                display: inline-flex;
                align-items: center;
                gap: 8px;

                margin-top: 14px;
                padding: 7px 12px;

                border-radius: 999px;

                color: #d1fae5;
                background: rgba(16,185,129,.10);

                border:
                    1px solid
                    rgba(16,185,129,.18);

                font-size: 11px;
                font-weight: 800;
            }

            .hero-status-dot {
                width: 7px;
                height: 7px;

                border-radius: 50%;

                background: #10b981;
            }

            .hero-graphic {
                position: relative;
                z-index: 2;

                width: 140px;
                height: 140px;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 34px;

                background:
                    rgba(255,255,255,.06);

                border:
                    1px solid
                    rgba(255,255,255,.10);
            }

            /* =================================================
               STAT CARDS
               ================================================= */

            .stat-card {
                min-height: 170px;

                background: white;

                border:
                    1px solid #e2e8f0;

                border-radius: 20px;

                padding: 22px;

                box-shadow:
                    0 7px 20px
                    rgba(15,23,42,.045);

                overflow: hidden;
            }

            .stat-card::before {
                content: "";

                position: absolute;

                width: 100%;
                height: 3px;

                top: 0;
                right: 0;

                background:
                    #e2e8f0;
            }

            .stat-icon-wrapper {
                width: 58px;
                height: 58px;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 16px;
            }

            .stat-label {
                color: #64748b;
                font-size: 12px;
                font-weight: 750;
            }

            .stat-value {
                color: #0f172a;
                font-size: 40px;
                line-height: 1;
                font-weight: 950;
            }

            .stat-bottom-line {
                width: 100%;
                height: 3px;

                border-radius: 999px;

                background:
                    #f1f5f9;
            }

            /* =================================================
               SECTION CARDS
               ================================================= */

            .section-card {
                background: white;

                border:
                    1px solid #e2e8f0;

                border-radius: 20px;

                box-shadow:
                    0 6px 20px
                    rgba(15,23,42,.04);
            }

            .section-title {
                color: #1e293b;
                font-size: 16px;
                font-weight: 850;
            }

            .section-subtitle {
                color: #94a3b8;
                font-size: 11px;
                font-weight: 600;
            }

            .section-icon {
                width: 42px;
                height: 42px;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 12px;
            }

            /* =================================================
               LIST
               ================================================= */

            .list-item {
                width: 100%;

                border-bottom:
                    1px solid #f1f5f9;

                padding: 12px 10px;
            }

            .list-item:last-child {
                border-bottom: none;
            }

            .item-avatar {
                width: 48px;
                height: 48px;

                flex-shrink: 0;

                border-radius: 14px;

                display: flex;
                align-items: center;
                justify-content: center;

                border:
                    1px solid #e2e8f0;
            }

            .number-badge {
                min-width: 42px;
                height: 29px;

                display: inline-flex;
                align-items: center;
                justify-content: center;

                padding: 0 10px;

                border-radius: 999px;

                background: #f8fafc;

                color: #334155;

                border:
                    1px solid #e2e8f0;

                font-size: 12px;
                font-weight: 900;
            }

            /* =================================================
               QUICK ACTIONS
               ================================================= */

            .quick-action {
                min-height: 78px;

                width: 100%;

                border-radius: 15px;

                font-weight: 800 !important;

                box-shadow: none !important;
            }

            /* =================================================
               SCROLLBAR
               ================================================= */

            ::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }

            ::-webkit-scrollbar-track {
                background: transparent;
            }

            ::-webkit-scrollbar-thumb {
                background: #cbd5e1;
                border-radius: 999px;
            }

            /* =================================================
               RESPONSIVE
               ================================================= */

            @media (max-width: 900px) {

                .hero-card {
                    padding: 30px;
                }

                .hero-title {
                    font-size: 27px;
                }

                .hero-club-name {
                    font-size: 21px;
                }

                .hero-graphic {
                    width: 110px;
                    height: 110px;
                }
            }

            @media (max-width: 600px) {

                .rtl-container {
                    padding: 2px 0 20px;
                }

                .hero-card {
                    min-height: auto;
                    border-radius: 18px;
                    padding: 24px 20px;
                }

                .hero-title {
                    font-size: 23px;
                }

                .hero-club-name {
                    font-size: 18px;
                }

                .hero-description {
                    font-size: 12px;
                }

                .hero-graphic {
                    display: none;
                }

                .stat-card {
                    min-height: 145px;
                    border-radius: 17px;
                }

                .section-card {
                    border-radius: 17px;
                }
            }

        </style>
        '''
    )

    # =========================================================
    # Main Container
    # =========================================================

    with ui.element('div').classes(
        'rtl-container flex flex-col gap-6'
    ):

        # =====================================================
        # HERO
        # =====================================================

        with ui.element('div').classes(
            'hero-card'
        ):

            with ui.row().classes(
                'hero-content w-full items-center justify-between flex-wrap gap-8'
            ):

                with ui.column().classes(
                    'gap-2 flex-1'
                ):

                    with ui.row().classes(
                        'items-center gap-4'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'hero-icon-box'
                        ):

                            ui.icon(
                                'dashboard'
                            ).classes(
                                'text-4xl text-white'
                            )

                        ui.label(
                            'لوحة التحكم والإحصائيات'
                        ).classes(
                            'hero-title'
                        )

                    ui.label(
                        club_name_ar
                    ).classes(
                        'hero-club-name mt-1'
                    )

                    if club_name_en:

                        ui.label(
                            club_name_en
                        ).classes(
                            'hero-club-en'
                        )

                    ui.label(
                        'مرحباً بك في نظام الإدارة المتقدم. '
                        'تابع بيانات النادي واللاعبين والفرق والبطولات من مكان واحد.'
                    ).classes(
                        'hero-description mt-2'
                    )

                    with ui.element(
                        'div'
                    ).classes(
                        'hero-status'
                    ):

                        ui.element(
                            'span'
                        ).classes(
                            'hero-status-dot'
                        )

                        ui.label(
                            'النظام يعمل بشكل طبيعي'
                        )

                with ui.element(
                    'div'
                ).classes(
                    'hero-graphic'
                ):

                    ui.icon(
                        'corporate_fare'
                    ).classes(
                        'text-7xl text-white opacity-90'
                    )

        # =====================================================
        # STATISTICS
        # =====================================================

        with ui.row().classes(
            'w-full grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5'
        ):

            # Players
            with ui.card().classes(
                'stat-card'
            ):

                with ui.row().classes(
                    'w-full items-start justify-between'
                ):

                    with ui.column().classes(
                        'gap-2'
                    ):

                        ui.label(
                            'إجمالي اللاعبين'
                        ).classes(
                            'stat-label'
                        )

                        ui.label(
                            str(players_count)
                        ).classes(
                            'stat-value'
                        )

                    with ui.element(
                        'div'
                    ).classes(
                        'stat-icon-wrapper bg-sky-100 text-sky-600'
                    ):

                        ui.icon(
                            'groups'
                        ).classes(
                            'text-3xl'
                        )

                ui.label(
                    'المسجلين بالنادي'
                ).classes(
                    'text-xs text-slate-400 mt-5'
                )

                ui.element(
                    'div'
                ).classes(
                    'stat-bottom-line mt-4'
                )

            # Teams
            with ui.card().classes(
                'stat-card'
            ):

                with ui.row().classes(
                    'w-full items-start justify-between'
                ):

                    with ui.column().classes(
                        'gap-2'
                    ):

                        ui.label(
                            'إجمالي الفرق'
                        ).classes(
                            'stat-label'
                        )

                        ui.label(
                            str(teams_count)
                        ).classes(
                            'stat-value'
                        )

                    with ui.element(
                        'div'
                    ).classes(
                        'stat-icon-wrapper bg-emerald-100 text-emerald-600'
                    ):

                        ui.icon(
                            'diversity_3'
                        ).classes(
                            'text-3xl'
                        )

                ui.label(
                    'الفرق المسجلة'
                ).classes(
                    'text-xs text-slate-400 mt-5'
                )

                ui.element(
                    'div'
                ).classes(
                    'stat-bottom-line mt-4'
                )

            # Subscriptions
            with ui.card().classes(
                'stat-card'
            ):

                with ui.row().classes(
                    'w-full items-start justify-between'
                ):

                    with ui.column().classes(
                        'gap-2'
                    ):

                        ui.label(
                            'اشتراكات اللاعبين'
                        ).classes(
                            'stat-label'
                        )

                        ui.label(
                            str(subscriptions_count)
                        ).classes(
                            'stat-value'
                        )

                    with ui.element(
                        'div'
                    ).classes(
                        'stat-icon-wrapper bg-amber-100 text-amber-600'
                    ):

                        ui.icon(
                            'how_to_reg'
                        ).classes(
                            'text-3xl'
                        )

                ui.label(
                    'الارتباطات الحالية'
                ).classes(
                    'text-xs text-slate-400 mt-5'
                )

                ui.element(
                    'div'
                ).classes(
                    'stat-bottom-line mt-4'
                )

            # Tournaments
            with ui.card().classes(
                'stat-card'
            ):

                with ui.row().classes(
                    'w-full items-start justify-between'
                ):

                    with ui.column().classes(
                        'gap-2'
                    ):

                        ui.label(
                            'البطولات'
                        ).classes(
                            'stat-label'
                        )

                        ui.label(
                            str(tournaments_count)
                        ).classes(
                            'stat-value'
                        )

                    with ui.element(
                        'div'
                    ).classes(
                        'stat-icon-wrapper bg-purple-100 text-purple-600'
                    ):

                        ui.icon(
                            'emoji_events'
                        ).classes(
                            'text-3xl'
                        )

                ui.label(
                    'المشاركات الرسمية'
                ).classes(
                    'text-xs text-slate-400 mt-5'
                )

                ui.element(
                    'div'
                ).classes(
                    'stat-bottom-line mt-4'
                )

        # =====================================================
        # SECONDARY STATS
        # =====================================================

        with ui.row().classes(
            'w-full grid grid-cols-1 md:grid-cols-3 gap-5'
        ):

            # Sports
            with ui.card().classes(
                'section-card p-7 flex flex-col justify-center items-center text-center'
            ):

                with ui.element(
                    'div'
                ).classes(
                    'section-icon bg-blue-50 text-blue-600 mb-4'
                ):

                    ui.icon(
                        'sports'
                    ).classes(
                        'text-2xl'
                    )

                ui.label(
                    'الرياضات المدرجة'
                ).classes(
                    'section-title'
                )

                ui.label(
                    str(sports_count)
                ).classes(
                    'text-5xl font-black text-slate-800 mt-2'
                )

                ui.label(
                    'أنواع الرياضات المرتبطة بفرق النادي'
                ).classes(
                    'section-subtitle mt-2'
                )

            # Medical
            with ui.card().classes(
                'section-card p-6'
            ):

                with ui.row().classes(
                    'items-center gap-3 mb-6'
                ):

                    with ui.element(
                        'div'
                    ).classes(
                        'section-icon bg-emerald-50 text-emerald-600'
                    ):

                        ui.icon(
                            'medical_information'
                        ).classes(
                            'text-xl'
                        )

                    with ui.column().classes(
                        'gap-0'
                    ):

                        ui.label(
                            'الكشوفات الطبية'
                        ).classes(
                            'section-title'
                        )

                        ui.label(
                            'الحالة الصحية للاعبين'
                        ).classes(
                            'section-subtitle'
                        )

                if medical_states:

                    with ui.column().classes(
                        'w-full gap-1'
                    ):

                        for state in medical_states:

                            state_name = (
                                state['MedicalReportStateNameAR']
                                or 'غير محدد'
                            )

                            state_count = (
                                state['Count']
                                or 0
                            )

                            with ui.row().classes(
                                'w-full justify-between items-center px-2 py-2'
                            ):

                                ui.label(
                                    state_name
                                ).classes(
                                    'text-slate-600 font-medium text-sm'
                                )

                                ui.label(
                                    str(state_count)
                                ).classes(
                                    'number-badge'
                                )

                else:

                    with ui.column().classes(
                        'w-full items-center justify-center py-6'
                    ):

                        ui.icon(
                            'medical_information'
                        ).classes(
                            'text-4xl text-slate-300'
                        )

                        ui.label(
                            'لا توجد بيانات طبية'
                        ).classes(
                            'text-slate-400 text-sm mt-2'
                        )

            # Membership
            with ui.card().classes(
                'section-card p-6'
            ):

                with ui.row().classes(
                    'items-center gap-3 mb-6'
                ):

                    with ui.element(
                        'div'
                    ).classes(
                        'section-icon bg-amber-50 text-amber-600'
                    ):

                        ui.icon(
                            'card_membership'
                        ).classes(
                            'text-xl'
                        )

                    with ui.column().classes(
                        'gap-0'
                    ):

                        ui.label(
                            'حالة العضويات'
                        ).classes(
                            'section-title'
                        )

                        ui.label(
                            'موقف العضويات الحالية'
                        ).classes(
                            'section-subtitle'
                        )

                if membership_states:

                    with ui.column().classes(
                        'w-full gap-1'
                    ):

                        for state in membership_states:

                            state_name = (
                                state['MembershipStatusNameAR']
                                or 'غير محدد'
                            )

                            state_count = (
                                state['Count']
                                or 0
                            )

                            with ui.row().classes(
                                'w-full justify-between items-center px-2 py-2'
                            ):

                                ui.label(
                                    state_name
                                ).classes(
                                    'text-slate-600 font-medium text-sm'
                                )

                                ui.label(
                                    str(state_count)
                                ).classes(
                                    'number-badge'
                                )

                else:

                    with ui.column().classes(
                        'w-full items-center justify-center py-6'
                    ):

                        ui.icon(
                            'person_off'
                        ).classes(
                            'text-4xl text-slate-300'
                        )

                        ui.label(
                            'لا توجد بيانات عضويات'
                        ).classes(
                            'text-slate-400 text-sm mt-2'
                        )

        # =====================================================
        # TEAMS + LATEST PLAYERS
        # =====================================================

        with ui.row().classes(
            'w-full grid grid-cols-1 lg:grid-cols-2 gap-5'
        ):

            # Teams
            with ui.card().classes(
                'section-card p-0 overflow-hidden'
            ):

                with ui.row().classes(
                    'w-full items-center justify-between p-5 bg-slate-50 border-b border-slate-100'
                ):

                    with ui.row().classes(
                        'items-center gap-3'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'section-icon bg-indigo-50 text-indigo-600'
                        ):

                            ui.icon(
                                'groups'
                            ).classes(
                                'text-xl'
                            )

                        with ui.column().classes(
                            'gap-0'
                        ):

                            ui.label(
                                'قائمة الفرق'
                            ).classes(
                                'section-title'
                            )

                            ui.label(
                                'الفرق التابعة للنادي'
                            ).classes(
                                'section-subtitle'
                            )

                    ui.label(
                        f'{teams_count} فريق'
                    ).classes(
                        'bg-white text-slate-600 border border-slate-200 px-4 py-1 rounded-full text-xs font-bold'
                    )

                with ui.column().classes(
                    'w-full p-4 gap-1 h-96 overflow-y-auto'
                ):

                    if teams:

                        for team in teams:

                            team_name = (
                                team['TeamAR']
                                or team['TeamEN']
                                or 'فريق غير مسمى'
                            )

                            team_category = (
                                team['TeamCategoryNameAR']
                                or 'فئة غير محددة'
                            )

                            sport_name = (
                                team['SportNameAR']
                                or 'رياضة غير محددة'
                            )

                            player_count = (
                                team['PlayerCount']
                                or 0
                            )

                            with ui.row().classes(
                                'list-item items-center justify-between'
                            ):

                                with ui.row().classes(
                                    'items-center gap-4'
                                ):

                                    with ui.element(
                                        'div'
                                    ).classes(
                                        'item-avatar bg-indigo-50 text-indigo-500'
                                    ):

                                        ui.icon(
                                            'sports_soccer'
                                        ).classes(
                                            'text-xl'
                                        )

                                    with ui.column().classes(
                                        'gap-0'
                                    ):

                                        ui.label(
                                            team_name
                                        ).classes(
                                            'font-bold text-slate-800 text-sm'
                                        )

                                        ui.label(
                                            f'{sport_name} • {team_category}'
                                        ).classes(
                                            'text-xs text-slate-500 mt-1'
                                        )

                                with ui.column().classes(
                                    'items-end gap-1'
                                ):

                                    ui.label(
                                        str(player_count)
                                    ).classes(
                                        'font-black text-slate-700 text-lg'
                                    )

                                    ui.label(
                                        'لاعب'
                                    ).classes(
                                        'text-[10px] text-slate-400'
                                    )

                    else:

                        with ui.column().classes(
                            'w-full h-full items-center justify-center'
                        ):

                            ui.icon(
                                'inbox'
                            ).classes(
                                'text-6xl text-slate-300'
                            )

                            ui.label(
                                'لا توجد فرق مسجلة بعد'
                            ).classes(
                                'text-slate-400 font-medium mt-3'
                            )

            # Latest Players
            with ui.card().classes(
                'section-card p-0 overflow-hidden'
            ):

                with ui.row().classes(
                    'w-full items-center justify-between p-5 bg-slate-50 border-b border-slate-100'
                ):

                    with ui.row().classes(
                        'items-center gap-3'
                    ):

                        with ui.element(
                            'div'
                        ).classes(
                            'section-icon bg-sky-50 text-sky-600'
                        ):

                            ui.icon(
                                'recent_actors'
                            ).classes(
                                'text-xl'
                            )

                        with ui.column().classes(
                            'gap-0'
                        ):

                            ui.label(
                                'أحدث اللاعبين'
                            ).classes(
                                'section-title'
                            )

                            ui.label(
                                'آخر اللاعبين المنضمين'
                            ).classes(
                                'section-subtitle'
                            )

                    ui.label(
                        'آخر 8 لاعبين'
                    ).classes(
                        'bg-white text-slate-600 border border-slate-200 px-4 py-1 rounded-full text-xs font-bold'
                    )

                with ui.column().classes(
                    'w-full p-4 gap-1 h-96 overflow-y-auto'
                ):

                    if latest_players:

                        for player in latest_players:

                            player_name = (
                                player['PlayerNameAR']
                                or 'غير متوفر'
                            )

                            membership_name = (
                                player['MembershipStatusNameAR']
                                or 'حالة غير محددة'
                            )

                            medical_name = (
                                player['MedicalReportStateNameAR']
                                or 'لم يتم الفحص'
                            )

                            with ui.row().classes(
                                'list-item items-center justify-between'
                            ):

                                with ui.row().classes(
                                    'items-center gap-4'
                                ):

                                    with ui.element(
                                        'div'
                                    ).classes(
                                        'item-avatar bg-slate-100 text-slate-500'
                                    ):

                                        ui.icon(
                                            'person'
                                        ).classes(
                                            'text-xl'
                                        )

                                    with ui.column().classes(
                                        'gap-0'
                                    ):

                                        ui.label(
                                            player_name
                                        ).classes(
                                            'font-bold text-slate-800 text-sm'
                                        )

                                        ui.label(
                                            membership_name
                                        ).classes(
                                            'text-xs text-slate-500 mt-1'
                                        )

                                ui.badge(
                                    medical_name
                                ).props(
                                    'outline color=primary rounded'
                                ).classes(
                                    'text-xs px-2 py-1'
                                )

                    else:

                        with ui.column().classes(
                            'w-full h-full items-center justify-center'
                        ):

                            ui.icon(
                                'person_off'
                            ).classes(
                                'text-6xl text-slate-300'
                            )

                            ui.label(
                                'لا يوجد لاعبون مسجلون بعد'
                            ).classes(
                                'text-slate-400 font-medium mt-3'
                            )

        # =====================================================
        # QUICK ACTIONS
        # =====================================================

        with ui.card().classes(
            'section-card w-full p-6'
        ):

            with ui.row().classes(
                'items-center gap-3 mb-5'
            ):

                with ui.element(
                    'div'
                ).classes(
                    'section-icon bg-amber-50 text-amber-600'
                ):

                    ui.icon(
                        'bolt'
                    ).classes(
                        'text-xl'
                    )

                with ui.column().classes(
                    'gap-0'
                ):

                    ui.label(
                        'إجراءات سريعة'
                    ).classes(
                        'section-title'
                    )

                    ui.label(
                        'الوصول السريع إلى أهم أقسام النظام'
                    ).classes(
                        'section-subtitle'
                    )

            with ui.row().classes(
                'w-full grid grid-cols-2 md:grid-cols-4 gap-4'
            ):

                ui.button(
                    'إدارة اللاعبين',
                    icon='manage_accounts',
                    on_click=lambda: ui.navigate.to('/players')
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'quick-action bg-slate-800 text-white'
                )

                ui.button(
                    'إدارة الفرق',
                    icon='account_tree',
                    on_click=lambda: ui.navigate.to('/teams')
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'quick-action bg-sky-600 text-white'
                )

                ui.button(
                    'التسجيلات',
                    icon='app_registration',
                    on_click=lambda: ui.navigate.to('/registrations')
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'quick-action bg-emerald-600 text-white'
                )

                ui.button(
                    'المعدات والعهد',
                    icon='inventory_2',
                    on_click=lambda: ui.navigate.to('/equipment')
                ).props(
                    'unelevated no-caps'
                ).classes(
                    'quick-action bg-amber-500 text-white'
                )