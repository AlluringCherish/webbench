# Phase1_Start
async def design_specification_phase():
    BackendDesignArchitect = build_resilient_agent(
        agent_name="BackendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDesignArchitect = build_resilient_agent(
        agent_name="FrontendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    DesignMerger = build_resilient_agent(
        agent_name="DesignMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=50
    )

    # Parallel execution of BackendDesignArchitect and FrontendDesignArchitect
    await asyncio.gather(
        execute(BackendDesignArchitect, "Define Flask routes, data file schemas, and local file handling for EventPlanning app. Save output to backend_design.md."),
        execute(FrontendDesignArchitect, "Specify all HTML templates with exact element IDs, page titles, and navigation flow for EventPlanning app. Save output to frontend_design.md.")
    )

    # Read backend and frontend design outputs
    backend_design_content, frontend_design_content = "", ""
    try:
        backend_design_content = open("backend_design.md").read()
    except Exception:
        pass
    try:
        frontend_design_content = open("frontend_design.md").read()
    except Exception:
        pass

    # Merge backend and frontend designs into unified design_spec.md
    await execute(
        DesignMerger,
        "Merge backend_design.md and frontend_design.md into a comprehensive, consistent design_spec.md for EventPlanning app.\n\n"
        f"=== Backend Design ===\n{backend_design_content}\n\n"
        f"=== Frontend Design ===\n{frontend_design_content}"
    )
# Phase1_End
# Phase2_Start
import asyncio
import glob

async def implementation_and_verification_phase():
    BackendDeveloper = build_resilient_agent(
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    FrontendDeveloper = build_resilient_agent(
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    IntegrationMerger = build_resilient_agent(
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Parallel: BackendDeveloper and FrontendDeveloper generate app.py and templates/*.html respectively
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete Flask backend app.py based on design_spec.md backend specifications for EventPlanning, handling all routes, data schemas, and functionality."),
        execute(FrontendDeveloper,
                "Implement all EventPlanning frontend HTML templates (*.html) based on design_spec.md, ensuring correct element IDs, page titles, and navigation using Jinja2 syntax.")
    )

    # Upon both completion, read outputs for integration
    design_spec_content = ""
    app_content = ""
    templates_content = ""
    try:
        design_spec_content = open("design_spec.md").read()
    except FileNotFoundError:
        pass
    try:
        app_content = open("app.py").read()
    except FileNotFoundError:
        pass
    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # IntegrationMerger merges and harmonizes app.py and templates using design_spec.md
    await execute(IntegrationMerger,
                  f"Integrate and harmonize backend app.py and frontend templates/*.html.\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"=== app.py ===\n{app_content}\n\n"
                  f"=== Templates *.html ===\n{templates_content}")
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