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
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDesignArchitect = build_resilient_agent(
        agent_name="FrontendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
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

    # Parallel generation of backend_design.md and frontend_design.md
    await asyncio.gather(
        execute(BackendDesignArchitect, "Analyze user_task_description and create backend_design.md with Flask routes and local text file schemas."),
        execute(FrontendDesignArchitect, "Analyze user_task_description and create frontend_design.md with detailed HTML templates, element IDs, and navigation flows.")
    )

    backend_design = ""
    frontend_design = ""
    try:
        backend_design = open("backend_design.md").read()
    except FileNotFoundError:
        pass
    try:
        frontend_design = open("frontend_design.md").read()
    except FileNotFoundError:
        pass

    # Merge backend and frontend designs into design_spec.md
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md with user_task_description.\n\n"
        f"=== Backend Design ===\n{backend_design}\n\n"
        f"=== Frontend Design ===\n{frontend_design}"
    )
# Phase1_End
# Phase2_Start
import glob
import asyncio

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
        recovery_time=45
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
        recovery_time=45
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

    # Parallel implementation by BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(BackendDeveloper, "Implement backend Flask app.py based on design_spec.md provided by DesignMerger."),
        execute(FrontendDeveloper, "Implement frontend templates/*.html based on design_spec.md provided by DesignMerger.")
    )

    # Read the outputs of BackendDeveloper and FrontendDeveloper
    app_py_content = ""
    templates_content = ""
    try:
        app_py_content = open("app.py").read()
    except FileNotFoundError:
        pass

    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # IntegrationMerger merges and reconciles backend and frontend implementations
    await execute(
        IntegrationMerger,
        "Merge and reconcile backend app.py and frontend templates/*.html for final consistent deployable artifacts.\n\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
        f"=== app.py ===\n{app_py_content}\n\n"
        f"=== templates/*.html ===\n{templates_content}"
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