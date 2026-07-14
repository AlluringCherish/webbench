# Phase1_Start
async def design_specification_phase():
    DesignDebaterA = build_resilient_agent(
        agent_name="DesignDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    DesignDebaterB = build_resilient_agent(
        agent_name="DesignDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    DesignJudge = build_resilient_agent(
        agent_name="DesignJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
    )

    # Multi-Agent Debate: exactly 2 total rounds (1=initial drafts, 2=peer-informed revisions)
    for round_num in range(1, 3):
        design_a_content = ""
        design_b_content = ""

        if round_num > 1:
            try:
                design_a_content = open("design_debate_a.md", "r", encoding="utf-8").read()
            except OSError:
                design_a_content = ""
            try:
                design_b_content = open("design_debate_b.md", "r", encoding="utf-8").read()
            except OSError:
                design_b_content = ""

        if round_num == 1:
            msg_a = "(No peer artifact yet; first round initial independent draft.)"
            msg_b = "(No peer artifact yet; first round initial independent draft.)"
        else:
            msg_a = f"Round 2 peer revision: read your own design_debate_a.md and peer design_debate_b.md artifacts to revise and fully overwrite design_debate_a.md.\n\nPeer DesignDebaterB content:\n{design_b_content}"
            msg_b = f"Round 2 peer revision: read your own design_debate_b.md and peer design_debate_a.md artifacts to revise and fully overwrite design_debate_b.md.\n\nPeer DesignDebaterA content:\n{design_a_content}"

        # Run both debaters in parallel each round
        await asyncio.gather(
            execute(DesignDebaterA, msg_a),
            execute(DesignDebaterB, msg_b)
        )

    # After 2 rounds, read final debater artifacts for adjudication
    final_design_a = ""
    final_design_b = ""
    try:
        final_design_a = open("design_debate_a.md", "r", encoding="utf-8").read()
    except OSError:
        final_design_a = ""
    try:
        final_design_b = open("design_debate_b.md", "r", encoding="utf-8").read()
    except OSError:
        final_design_b = ""

    # Run the DesignJudge to adjudicate and produce canonical design_spec.md
    await execute(
        DesignJudge,
        "Adjudicate the complete final round 2 design_debate_a.md and design_debate_b.md, "
        "compare and unify Flask routes, HTTP methods, templates, element IDs, navigation flows, "
        "data file schemas, and local text persistence. Produce one consistent, implementation-ready design_spec.md.\n\n"
        "=== Final DesignDebaterA ===\n" + final_design_a + "\n\n=== Final DesignDebaterB ===\n" + final_design_b
    )
# Phase1_End
# Phase2_Start
async def implementation_and_verification_phase():
    import glob

    ImplementationDebaterA = build_resilient_agent(
        agent_name="ImplementationDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )
    ImplementationDebaterB = build_resilient_agent(
        agent_name="ImplementationDebaterB",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )
    ImplementationJudge = build_resilient_agent(
        agent_name="ImplementationJudge",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=40
    )

    # Multi-Agent Debate: exactly 2 total rounds (1=initial, 2=one peer-informed revision)
    for round_num in range(1, 3):
        app_a_content = ""
        templates_a_content = ""
        app_b_content = ""
        templates_b_content = ""

        if round_num > 1:
            try:
                app_a_content = open("app_debate_a.py", "r", encoding="utf-8").read()
            except OSError:
                app_a_content = ""
            for template_path in sorted(glob.glob("templates_debate_a/*.html")):
                try:
                    templates_a_content += f"\n=== {template_path} ===\n" + open(template_path, "r", encoding="utf-8").read()
                except OSError:
                    pass

            try:
                app_b_content = open("app_debate_b.py", "r", encoding="utf-8").read()
            except OSError:
                app_b_content = ""
            for template_path in sorted(glob.glob("templates_debate_b/*.html")):
                try:
                    templates_b_content += f"\n=== {template_path} ===\n" + open(template_path, "r", encoding="utf-8").read()
                except OSError:
                    pass

        if round_num == 1:
            msg_a = "Round 1 of 2: independently implement full app_debate_a.py and templates_debate_a/*.html based on design_spec.md."
            msg_b = "Round 1 of 2: independently implement full app_debate_b.py and templates_debate_b/*.html based on design_spec.md."
        else:
            msg_a = (
                "Round 2 of 2: revise app_debate_a.py and templates_debate_a/*.html "
                "incorporating peer artifacts below.\n\n"
                "=== Peer app_debate_b.py ===\n" + app_b_content + "\n\n"
                "=== Peer templates_debate_b/*.html ===\n" + templates_b_content
            )
            msg_b = (
                "Round 2 of 2: revise app_debate_b.py and templates_debate_b/*.html "
                "incorporating peer artifacts below.\n\n"
                "=== Peer app_debate_a.py ===\n" + app_a_content + "\n\n"
                "=== Peer templates_debate_a/*.html ===\n" + templates_a_content
            )

        await asyncio.gather(
            execute(ImplementationDebaterA, msg_a),
            execute(ImplementationDebaterB, msg_b),
        )

    # After debate rounds, ImplementationJudge adjudicates final canonical app.py and templates/*.html
    app_a_content = ""
    templates_a_content = ""
    app_b_content = ""
    templates_b_content = ""

    try:
        app_a_content = open("app_debate_a.py", "r", encoding="utf-8").read()
    except OSError:
        app_a_content = ""
    for template_path in sorted(glob.glob("templates_debate_a/*.html")):
        try:
            templates_a_content += f"\n=== {template_path} ===\n" + open(template_path, "r", encoding="utf-8").read()
        except OSError:
            pass

    try:
        app_b_content = open("app_debate_b.py", "r", encoding="utf-8").read()
    except OSError:
        app_b_content = ""
    for template_path in sorted(glob.glob("templates_debate_b/*.html")):
        try:
            templates_b_content += f"\n=== {template_path} ===\n" + open(template_path, "r", encoding="utf-8").read()
        except OSError:
            pass

    await execute(
        ImplementationJudge,
        "Adjudicate the two final round-2 candidate implementations and write canonical app.py and templates/*.html files.\n\n"
        "=== Candidate A ===\n" + app_a_content + "\n\n" + templates_a_content + "\n\n"
        "=== Candidate B ===\n" + app_b_content + "\n\n" + templates_b_content,
    )
# Phase2_End
# Orchestrate_Start
async def orchestrate():
    """Execute the complete multi-agent workflow in steps."""
    import time
    import json
    from pathlib import Path
    from essential_modules import aggregate_task_metrics
    orchestrate_start_time = time.time()

    step1 = [
        design_specification_phase()
    ]
    step2 = [
        implementation_and_verification_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)

    # Record task duration
    orchestrate_end_time = time.time()
    CONTEXT["_task_duration"] = orchestrate_end_time - orchestrate_start_time

    # Print chaos engineering report (if enabled)
    cc = None
    if 'chaos_controller' in globals():
        print("\n" + "="*80)
        print("Chaos Engineering Report")
        print("="*80)
        chaos_controller.print_report(context=CONTEXT)
        cc = chaos_controller

    # Save metrics to JSON (with resilience_metrics if chaos enabled)
    task_metrics = aggregate_task_metrics(CONTEXT, chaos_controller=cc)
    metrics_path = Path("metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(task_metrics, f, indent=2)
    print(f" Metrics saved to: {{metrics_path.resolve()}}")
# Orchestrate_End