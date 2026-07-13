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
        recovery_time=45
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
        recovery_time=45
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

    # Parallel execution of backend and frontend design creation
    await asyncio.gather(
        execute(BackendDesignArchitect, "Read user_task_description and create detailed backend_design.md with backend routes, data models, and business logic."),
        execute(FrontendDesignArchitect, "Read user_task_description and create detailed frontend_design.md with HTML template specifications, element IDs, navigation, and UI interactions.")
    )

    # Read backend_design.md and frontend_design.md for merging
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

    # Merge backend and frontend designs into unified design_spec.md
    await execute(
        DesignMerger,
        f"Read user_task_description, backend_design.md, and frontend_design.md and merge into coherent design_spec.md.\n\n"
        f"=== Backend Design ===\n{backend_design}\n\n"
        f"=== Frontend Design ===\n{frontend_design}"
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
        timeout_threshold=480,
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
        timeout_threshold=480,
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
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )

    # Run BackendDeveloper and FrontendDeveloper in parallel
    await asyncio.gather(
        execute(
            BackendDeveloper,
            "Implement complete backend app.py from design_spec.md backend sections. "
            "Use exact data file formats and routes as specified. Output app.py."
        ),
        execute(
            FrontendDeveloper,
            "Implement all 10 frontend HTML templates using design_spec.md frontend sections. "
            "Include correct IDs, navigation, Jinja2 syntax as specified. Output templates/*.html."
        )
    )

    # Read outputs for integration merge
    backend_code = ""
    frontend_templates_content = ""
    try:
        backend_code = open("app.py").read()
    except Exception:
        pass
    for filepath in sorted(glob.glob("templates/*.html")):
        try:
            frontend_templates_content += f"\n=== {filepath} ===\n" + open(filepath).read()
        except Exception:
            pass

    # Run IntegrationMerger to reconcile and finalize outputs
    await execute(
        IntegrationMerger,
        f"Read design_spec.md, backend app.py and frontend templates/*.html.\n\n"
        f"=== app.py ===\n{backend_code}\n\n"
        f"=== templates/*.html ===\n{frontend_templates_content}"
        "\n\nReconcile all differences ensuring consistency in route names, variable names, template usage, "
        "and navigation buttons. Output final consistent app.py and templates/*.html."
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