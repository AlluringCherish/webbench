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
        recovery_time=30
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
        recovery_time=30
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
        recovery_time=30
    )

    # Multi-Agent Debate: exactly 2 total rounds (1=initial, 2=one peer-informed revision)
    for round_num in range(1, 3):
        design_a, design_b = "", ""
        if round_num > 1:
            try:
                design_a = open("design_debate_a.md", "r", encoding="utf-8").read()
            except OSError:
                design_a = ""
            try:
                design_b = open("design_debate_b.md", "r", encoding="utf-8").read()
            except OSError:
                design_b = ""

        if round_num == 1:
            msg_a = "(No peer design yet - initial draft based solely on user_task_description.)"
            msg_b = "(No peer design yet - initial draft based solely on user_task_description.)"
        else:
            msg_a = f"Peer DesignDebaterB's draft:\n{design_b}"
            msg_b = f"Peer DesignDebaterA's draft:\n{design_a}"

        await asyncio.gather(
            execute(DesignDebaterA, msg_a),
            execute(DesignDebaterB, msg_b)
        )

    # After 2 rounds, adjudicate final design_spec.md
    try:
        final_a = open("design_debate_a.md", "r", encoding="utf-8").read()
    except OSError:
        final_a = ""
    try:
        final_b = open("design_debate_b.md", "r", encoding="utf-8").read()
    except OSError:
        final_b = ""

    await execute(
        DesignJudge,
        "Adjudicate and synthesize the final design_spec.md using user_task_description and the two final candidate drafts.\n\n"
        "=== DesignDebaterA Final ===\n" + final_a + "\n\n"
        "=== DesignDebaterB Final ===\n" + final_b
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

    # Multi-Agent Debate: exactly 2 total rounds
    for round_num in range(1, 3):
        # Read all current relevant artifacts for this round
        app_a = ""
        app_b = ""
        templates_a = ""
        templates_b = ""

        try:
            app_a = open("app_debate_a.py", "r", encoding="utf-8").read()
        except OSError:
            pass
        try:
            app_b = open("app_debate_b.py", "r", encoding="utf-8").read()
        except OSError:
            pass

        for path in sorted(glob.glob("templates_debate_a/*.html")):
            try:
                templates_a += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
            except OSError:
                pass
        for path in sorted(glob.glob("templates_debate_b/*.html")):
            try:
                templates_b += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
            except OSError:
                pass

        # Prepare messages for ImplementationDebaterA and ImplementationDebaterB
        if round_num == 1:
            msg_a = "Round 1 of 2: independently draft complete app_debate_a.py and all templates_debate_a/*.html based on design_spec.md without peer input."
            msg_b = "Round 1 of 2: independently draft complete app_debate_b.py and all templates_debate_b/*.html based on design_spec.md without peer input."
        else:
            msg_a = (
                "Round 2 of 2: revise app_debate_a.py and templates_debate_a/*.html incorporating peer revisions.\n\n"
                "=== Peer app_debate_b.py ===\n" + app_b + "\n\n"
                "=== Peer templates_debate_b/*.html ===" + templates_b
            )
            msg_b = (
                "Round 2 of 2: revise app_debate_b.py and templates_debate_b/*.html incorporating peer revisions.\n\n"
                "=== Peer app_debate_a.py ===\n" + app_a + "\n\n"
                "=== Peer templates_debate_a/*.html ===" + templates_a
            )

        # Run both debaters in parallel
        await asyncio.gather(
            execute(ImplementationDebaterA, msg_a),
            execute(ImplementationDebaterB, msg_b)
        )

    # After round 2, read final candidates for judge evaluation
    app_a = ""
    app_b = ""
    templates_a = ""
    templates_b = ""

    try:
        app_a = open("app_debate_a.py", "r", encoding="utf-8").read()
    except OSError:
        pass
    try:
        app_b = open("app_debate_b.py", "r", encoding="utf-8").read()
    except OSError:
        pass

    for path in sorted(glob.glob("templates_debate_a/*.html")):
        try:
            templates_a += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
        except OSError:
            pass
    for path in sorted(glob.glob("templates_debate_b/*.html")):
        try:
            templates_b += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
        except OSError:
            pass

    # Judge evaluates and merges final implementations
    await execute(
        ImplementationJudge,
        "Adjudicate the two final round-2 app and template bundles, and write canonical app.py and templates/*.html.\n\n"
        "=== Candidate A: app_debate_a.py ===\n" + app_a + "\n\n"
        "=== Candidate A: templates_debate_a/*.html ===" + templates_a + "\n\n"
        "=== Candidate B: app_debate_b.py ===\n" + app_b + "\n\n"
        "=== Candidate B: templates_debate_b/*.html ===" + templates_b
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