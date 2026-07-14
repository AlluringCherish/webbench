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
        design_a_text = ""
        design_b_text = ""
        if round_num > 1:
            try:
                design_a_text = open("design_debate_a.md", "r", encoding="utf-8").read()
            except OSError:
                design_a_text = ""
            try:
                design_b_text = open("design_debate_b.md", "r", encoding="utf-8").read()
            except OSError:
                design_b_text = ""
        if round_num == 1:
            msg_a = "(No peer draft yet - this is the initial round)"
            msg_b = "(No peer draft yet - this is the initial round)"
        else:
            msg_a = f"Peer DesignDebaterB draft:\n{design_b_text}"
            msg_b = f"Peer DesignDebaterA draft:\n{design_a_text}"

        await asyncio.gather(
            execute(DesignDebaterA, msg_a),
            execute(DesignDebaterB, msg_b)
        )

    # After two rounds, DesignJudge adjudicates and synthesizes the final canonical design_spec.md
    try:
        design_a_text = open("design_debate_a.md", "r", encoding="utf-8").read()
    except OSError:
        design_a_text = ""
    try:
        design_b_text = open("design_debate_b.md", "r", encoding="utf-8").read()
    except OSError:
        design_b_text = ""

    await execute(
        DesignJudge,
        "Adjudicate and merge the final design drafts from DesignDebaterA and DesignDebaterB into a single cohesive design_spec.md.\n\n"
        "=== DesignDebateA ===\n" + design_a_text + "\n\n=== DesignDebateB ===\n" + design_b_text
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

    # Multi-Agent Debate: exactly 2 total rounds (1=initial drafts, 2=peer-informed revisions)
    for round_num in range(1, 3):
        peer_a_app = peer_a_templates = peer_b_app = peer_b_templates = ""

        if round_num > 1:
            try:
                peer_b_app = open("app_debate_b.py", "r", encoding="utf-8").read()
            except OSError:
                peer_b_app = ""
            peer_b_templates = ""
            for tpl_path in sorted(glob.glob("templates_debate_b/*.html")):
                try:
                    peer_b_templates += f"\n=== {tpl_path} ===\n" + open(tpl_path, "r", encoding="utf-8").read()
                except OSError:
                    pass

            try:
                peer_a_app = open("app_debate_a.py", "r", encoding="utf-8").read()
            except OSError:
                peer_a_app = ""
            peer_a_templates = ""
            for tpl_path in sorted(glob.glob("templates_debate_a/*.html")):
                try:
                    peer_a_templates += f"\n=== {tpl_path} ===\n" + open(tpl_path, "r", encoding="utf-8").read()
                except OSError:
                    pass

        if round_num == 1:
            msg_a = "Round 1 of 2: independently create full app_debate_a.py and templates_debate_a/*.html from design_spec.md."
            msg_b = "Round 1 of 2: independently create full app_debate_b.py and templates_debate_b/*.html from design_spec.md."
        else:
            msg_a = (
                "Round 2 of 2: revise app_debate_a.py and templates_debate_a/*.html using peer artifacts below.\n\n"
                "=== Peer app_debate_b.py ===\n" + peer_b_app + "\n\n"
                "=== Peer templates_debate_b/*.html ===\n" + peer_b_templates
            )
            msg_b = (
                "Round 2 of 2: revise app_debate_b.py and templates_debate_b/*.html using peer artifacts below.\n\n"
                "=== Peer app_debate_a.py ===\n" + peer_a_app + "\n\n"
                "=== Peer templates_debate_a/*.html ===\n" + peer_a_templates
            )

        await asyncio.gather(
            execute(ImplementationDebaterA, msg_a),
            execute(ImplementationDebaterB, msg_b)
        )

    # After 2 rounds, read both final candidates fully
    try:
        final_a_app = open("app_debate_a.py", "r", encoding="utf-8").read()
    except OSError:
        final_a_app = ""
    final_a_templates = ""
    for tpl_path in sorted(glob.glob("templates_debate_a/*.html")):
        try:
            final_a_templates += f"\n=== {tpl_path} ===\n" + open(tpl_path, "r", encoding="utf-8").read()
        except OSError:
            pass

    try:
        final_b_app = open("app_debate_b.py", "r", encoding="utf-8").read()
    except OSError:
        final_b_app = ""
    final_b_templates = ""
    for tpl_path in sorted(glob.glob("templates_debate_b/*.html")):
        try:
            final_b_templates += f"\n=== {tpl_path} ===\n" + open(tpl_path, "r", encoding="utf-8").read()
        except OSError:
            pass

    # ImplementationJudge compares and adjudicates final app and templates
    await execute(
        ImplementationJudge,
        "Adjudicate the two final round-2 candidates and write final canonical app.py and templates/*.html.\n\n"
        "=== Candidate A app_debate_a.py ===\n" + final_a_app + "\n\n"
        "=== Candidate A templates_debate_a/*.html ===\n" + final_a_templates + "\n\n"
        "=== Candidate B app_debate_b.py ===\n" + final_b_app + "\n\n"
        "=== Candidate B templates_debate_b/*.html ===\n" + final_b_templates
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