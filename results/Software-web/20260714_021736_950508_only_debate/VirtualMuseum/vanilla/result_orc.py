# Phase1_Start
async def design_specification_phase():
    DesignDebaterA = build_resilient_agent(
        agent_name="DesignDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
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
        timeout_threshold=350,
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
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
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
            msg_a = "(No peer draft yet - initial independent draft round 1)"
            msg_b = "(No peer draft yet - initial independent draft round 1)"
        else:
            msg_a = f"Revise your draft after reviewing the peer draft below, incorporating only improvements supported by user requirements.\n\n=== Peer DesignDebaterB draft ===\n{design_b_text}"
            msg_b = f"Revise your draft after reviewing the peer draft below, incorporating only improvements supported by user requirements.\n\n=== Peer DesignDebaterA draft ===\n{design_a_text}"

        await asyncio.gather(
            execute(DesignDebaterA, msg_a),
            execute(DesignDebaterB, msg_b)
        )

    # After round 2, read both final drafts and run the judge to adjudicate canonical design_spec.md
    design_a_final = ""
    design_b_final = ""
    try:
        design_a_final = open("design_debate_a.md", "r", encoding="utf-8").read()
    except OSError:
        design_a_final = ""
    try:
        design_b_final = open("design_debate_b.md", "r", encoding="utf-8").read()
    except OSError:
        design_b_final = ""

    await execute(
        DesignJudge,
        "Adjudicate the two final design drafts and write canonical design_spec.md document.\n\n"
        "=== DesignDebaterA Final Draft ===\n"
        + design_a_final
        + "\n\n=== DesignDebaterB Final Draft ===\n"
        + design_b_final
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
        recovery_time=30,
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
        recovery_time=30,
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
        recovery_time=30,
    )

    # Exactly 2 total debate rounds: round 1 initial, round 2 peer informed revision
    for round_num in range(1, 3):
        app_a_content = ""
        templates_a_content = ""
        app_b_content = ""
        templates_b_content = ""

        # Read latest candidate artifacts if available
        if round_num > 1:
            try:
                with open("app_debate_a.py", "r", encoding="utf-8") as f:
                    app_a_content = f.read()
            except OSError:
                app_a_content = ""
            try:
                template_paths_a = sorted(glob.glob("templates_debate_a/*.html"))
                for path in template_paths_a:
                    try:
                        templates_a_content += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
                    except OSError:
                        pass
            except OSError:
                templates_a_content = ""

            try:
                with open("app_debate_b.py", "r", encoding="utf-8") as f:
                    app_b_content = f.read()
            except OSError:
                app_b_content = ""
            try:
                template_paths_b = sorted(glob.glob("templates_debate_b/*.html"))
                for path in template_paths_b:
                    try:
                        templates_b_content += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
                    except OSError:
                        pass
            except OSError:
                templates_b_content = ""

        if round_num == 1:
            msg_a = "Round 1 of 2: Independently implement the full app_debate_a.py and templates_debate_a/*.html based on design_spec.md, with no peer info."
            msg_b = "Round 1 of 2: Independently implement the full app_debate_b.py and templates_debate_b/*.html based on design_spec.md, with no peer info."
        else:
            msg_a = (
                "Round 2 of 2: Revise your app_debate_a.py and templates_debate_a/*.html using the peer ImplementationDebaterB artifacts below "
                "and the design_spec.md as authoritative source.\n\n=== Peer app_debate_b.py ===\n"
                + app_b_content
                + "\n\n=== Peer templates_debate_b/*.html ===\n"
                + templates_b_content
            )
            msg_b = (
                "Round 2 of 2: Revise your app_debate_b.py and templates_debate_b/*.html using the peer ImplementationDebaterA artifacts below "
                "and the design_spec.md as authoritative source.\n\n=== Peer app_debate_a.py ===\n"
                + app_a_content
                + "\n\n=== Peer templates_debate_a/*.html ===\n"
                + templates_a_content
            )

        await asyncio.gather(
            execute(ImplementationDebaterA, msg_a),
            execute(ImplementationDebaterB, msg_b),
        )

    # After 2 rounds, read the final candidates for adjudication
    final_app_a = ""
    final_templates_a = ""
    final_app_b = ""
    final_templates_b = ""

    try:
        with open("app_debate_a.py", "r", encoding="utf-8") as f:
            final_app_a = f.read()
    except OSError:
        final_app_a = ""

    try:
        template_paths = sorted(glob.glob("templates_debate_a/*.html"))
        for path in template_paths:
            try:
                final_templates_a += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
            except OSError:
                pass
    except OSError:
        final_templates_a = ""

    try:
        with open("app_debate_b.py", "r", encoding="utf-8") as f:
            final_app_b = f.read()
    except OSError:
        final_app_b = ""

    try:
        template_paths = sorted(glob.glob("templates_debate_b/*.html"))
        for path in template_paths:
            try:
                final_templates_b += f"\n=== {path} ===\n" + open(path, "r", encoding="utf-8").read()
            except OSError:
                pass
    except OSError:
        final_templates_b = ""

    # Compose message to ImplementationJudge for final adjudication
    final_msg = (
        "Evaluate and merge the two final full implementation candidates from ImplementationDebaterA and ImplementationDebaterB, producing the final canonical app.py and templates/*.html.\n\n"
        "=== Candidate A: app_debate_a.py ===\n"
        + final_app_a
        + "\n\n=== Candidate A: templates_debate_a/*.html ===\n"
        + final_templates_a
        + "\n\n=== Candidate B: app_debate_b.py ===\n"
        + final_app_b
        + "\n\n=== Candidate B: templates_debate_b/*.html ===\n"
        + final_templates_b
    )

    await execute(ImplementationJudge, final_msg)
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