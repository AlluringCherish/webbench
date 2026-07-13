# Phase1_Start
async def design_specification_phase():
    BackendDesignArchitect = build_resilient_agent(
        agent_name="BackendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    FrontendDesignArchitect = build_resilient_agent(
        agent_name="FrontendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    DesignMerger = build_resilient_agent(
        agent_name="DesignMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Parallel execution: Backend and Frontend Design Architects work independently
    await asyncio.gather(
        execute(BackendDesignArchitect,
                "Create backend_design.md specifying Flask routes for NewsPortal, HTTP methods, and data file schemas for all relevant entities. Output backend_design.md."),
        execute(FrontendDesignArchitect,
                "Create frontend_design.md specifying NewsPortal HTML page templates with all element IDs, types, page titles, navigation flows, and interactive elements. Output frontend_design.md.")
    )

    # Read outputs for DesignMerger
    backend_design_content = ""
    try:
        backend_design_content = open("backend_design.md").read()
    except FileNotFoundError:
        pass

    frontend_design_content = ""
    try:
        frontend_design_content = open("frontend_design.md").read()
    except FileNotFoundError:
        pass

    # Merge backend and frontend designs into a unified design_spec.md
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md into design_spec.md for NewsPortal.\n\n"
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
        recovery_time=50
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
        recovery_time=50
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
        recovery_time=50
    )

    # Parallel execution of BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete app.py backend based on design_spec.md from DesignMerger including all Flask routes, data handling, and server-side logic strictly conforming to design_spec.md."),
        execute(FrontendDeveloper,
                "Implement all frontend HTML templates (*.html) based on design_spec.md from DesignMerger including exact element IDs, page layouts, Jinja2 syntax, and navigation.")
    )

    # Read BackendDeveloper output app.py
    backend_app_py = ""
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            backend_app_py = f.read()
    except FileNotFoundError:
        backend_app_py = ""

    # Read FrontendDeveloper output templates/*.html
    frontend_templates_content = ""
    for template_file in sorted(glob.glob("templates/*.html")):
        try:
            with open(template_file, "r", encoding="utf-8") as f:
                frontend_templates_content += f"\n=== {template_file} ===\n" + f.read()
        except OSError:
            pass

    # IntegrationMerger verifies and reconciles final outputs
    await execute(
        IntegrationMerger,
        f"Verify and merge backend app.py and frontend templates from DesignMerger.\n\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
        f"=== Backend app.py ===\n{backend_app_py}\n\n"
        f"=== Frontend Templates ===\n{frontend_templates_content}\n\n"
        "Produce final consistent app.py and templates/*.html artifacts ready for deployment."
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