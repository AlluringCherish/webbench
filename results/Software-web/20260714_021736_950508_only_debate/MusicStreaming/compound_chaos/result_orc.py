# Phase1_Start
async def design_specification_phase():
    DesignDebaterA = build_resilient_agent(
        agent_name="DesignDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=320,
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
        timeout_threshold=320,
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
            msg_a = "(No peer design yet - this is the initial round)"
            msg_b = "(No peer design yet - this is the initial round)"
        else:
            msg_a = f"Peer design_debate_b.md content to consider:\n\n{design_b}"
            msg_b = f"Peer design_debate_a.md content to consider:\n\n{design_a}"

        await asyncio.gather(
            execute(DesignDebaterA, msg_a),
            execute(DesignDebaterB, msg_b)
        )

    # Final: DesignJudge consolidates both final designs
    final_design_a, final_design_b = "", ""
    try:
        final_design_a = open("design_debate_a.md", "r", encoding="utf-8").read()
    except OSError:
        final_design_a = ""
    try:
        final_design_b = open("design_debate_b.md", "r", encoding="utf-8").read()
    except OSError:
        final_design_b = ""

    await execute(
        DesignJudge,
        f"Adjudicate and consolidate the final design documents into design_spec.md.\n\n"
        f"=== design_debate_a.md ===\n{final_design_a}\n\n"
        f"=== design_debate_b.md ===\n{final_design_b}"
    )
# Phase1_End
# Phase2_Start
import asyncio
import glob

async def implementation_and_verification_phase():
    ImplementationDebaterA = build_resilient_agent(
        agent_name="ImplementationDebaterA",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=500,
        failure_threshold=1,
        recovery_time=30
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
        recovery_time=30
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
        recovery_time=30
    )

    # Multi-Agent Debate: exactly 2 total rounds (round 1 = initial independent drafts, round 2 = peer-informed revision)
    for round_num in range(1, 3):
        app_a, app_b = "", ""
        templates_a, templates_b = "", ""

        if round_num > 1:
            try:
                app_a = open("app_debate_a.py", "r", encoding="utf-8").read()
            except OSError:
                app_a = ""
            try:
                app_b = open("app_debate_b.py", "r", encoding="utf-8").read()
            except OSError:
                app_b = ""

            templates_a_parts = []
            for path in sorted(glob.glob("templates_debate_a/*.html")):
                try:
                    templates_a_parts.append("=== " + path + " ===\n" + open(path, "r", encoding="utf-8").read())
                except OSError:
                    pass
            templates_a = "\n\n".join(templates_a_parts)

            templates_b_parts = []
            for path in sorted(glob.glob("templates_debate_b/*.html")):
                try:
                    templates_b_parts.append("=== " + path + " ===\n" + open(path, "r", encoding="utf-8").read())
                except OSError:
                    pass
            templates_b = "\n\n".join(templates_b_parts)

        if round_num == 1:
            msg_a = "(No peer artifacts yet; this is round 1 initial implementation.)"
            msg_b = "(No peer artifacts yet; this is round 1 initial implementation.)"
        else:
            msg_a = (
                "Round 2: revise your implementation informed by the peer's artifacts below.\n\n"
                "=== Peer app_debate_b.py ===\n" + app_b + "\n\n"
                "=== Peer templates_debate_b/*.html ===\n" + templates_b
            )
            msg_b = (
                "Round 2: revise your implementation informed by the peer's artifacts below.\n\n"
                "=== Peer app_debate_a.py ===\n" + app_a + "\n\n"
                "=== Peer templates_debate_a/*.html ===\n" + templates_a
            )

        await asyncio.gather(
            execute(ImplementationDebaterA, msg_a),
            execute(ImplementationDebaterB, msg_b)
        )

    # After two rounds, read all final artifacts for adjudication
    try:
        app_a = open("app_debate_a.py", "r", encoding="utf-8").read()
    except OSError:
        app_a = ""
    try:
        app_b = open("app_debate_b.py", "r", encoding="utf-8").read()
    except OSError:
        app_b = ""

    templates_a_parts = []
    for path in sorted(glob.glob("templates_debate_a/*.html")):
        try:
            templates_a_parts.append("=== " + path + " ===\n" + open(path, "r", encoding="utf-8").read())
        except OSError:
            pass
    templates_a = "\n\n".join(templates_a_parts)

    templates_b_parts = []
    for path in sorted(glob.glob("templates_debate_b/*.html")):
        try:
            templates_b_parts.append("=== " + path + " ===\n" + open(path, "r", encoding="utf-8").read())
        except OSError:
            pass
    templates_b = "\n\n".join(templates_b_parts)

    # Execute ImplementationJudge to adjudicate and produce canonical app.py and templates/*.html
    await execute(
        ImplementationJudge,
        "Compare and adjudicate the two final candidate implementations. Produce final canonical app.py and templates/*.html.\n\n"
        "=== Candidate ImplementationDebaterA app_debate_a.py ===\n" + app_a + "\n\n"
        "=== Candidate ImplementationDebaterA templates_debate_a/*.html ===\n" + templates_a + "\n\n"
        "=== Candidate ImplementationDebaterB app_debate_b.py ===\n" + app_b + "\n\n"
        "=== Candidate ImplementationDebaterB templates_debate_b/*.html ===\n" + templates_b
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