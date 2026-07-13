# Phase1_Start
async def design_specification_phase():
    BackendDesignArchitect = build_resilient_agent(
        agent_name="BackendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
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
        max_retries=2,
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
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Parallel execution of backend and frontend design architecture
    await asyncio.gather(
        execute(BackendDesignArchitect, "Independently create backend_design.md specifying Flask routes, data schemas, and backend logic based on user_task_description."),
        execute(FrontendDesignArchitect, "Independently create frontend_design.md specifying all 8 HTML templates, element IDs, navigation, and UI components based on user_task_description.")
    )

    # Read the outputs from backend and frontend design architects for merger
    backend_design, frontend_design = "", ""
    try:
        backend_design = open("backend_design.md").read()
    except FileNotFoundError:
        pass
    try:
        frontend_design = open("frontend_design.md").read()
    except FileNotFoundError:
        pass

    # Merge backend and frontend design into a unified design_spec.md
    await execute(DesignMerger,
                  f"User task description:\n{CONTEXT.get('user_task_description', '')}\n\n"
                  f"=== Backend Design Specification ===\n{backend_design}\n\n"
                  f"=== Frontend Design Specification ===\n{frontend_design}")
# Phase1_End
# Phase2_Start
async def implementation_and_verification_phase():
    import asyncio

    BackendDeveloper = build_resilient_agent(
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
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
        timeout_threshold=450,
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
        timeout_threshold=500,
        failure_threshold=2,
        recovery_time=60
    )

    # Run BackendDeveloper and FrontendDeveloper in parallel
    await asyncio.gather(
        execute(
            BackendDeveloper,
            "Implement full Flask backend app.py per design_spec.md including all routes, file I/O, and business logic."
        ),
        execute(
            FrontendDeveloper,
            "Implement all HTML templates under templates/ with exact IDs, Jinja2 syntax, and navigation per design_spec.md."
        )
    )

    # Read outputs after backend and frontend completion
    app_py_content = ""
    templates_content = ""
    import glob

    try:
        with open("app.py", "r", encoding="utf-8") as f:
            app_py_content = f.read()
    except Exception:
        pass

    for tpl_path in sorted(glob.glob("templates/*.html")):
        try:
            with open(tpl_path, "r", encoding="utf-8") as f:
                templates_content += f"\n=== {tpl_path} ===\n" + f.read()
        except Exception:
            pass

    # Execute IntegrationMerger to finalize integrated app.py and templates/*.html
    await execute(
        IntegrationMerger,
        f"Integrate and verify backend and frontend implementations.\n\n"
        f"=== app.py ===\n{app_py_content}\n\n"
        f"=== templates/*.html ===\n{templates_content}\n\n"
        f"Confirm full consistency between routes and templates, context variables, element IDs, navigation, and produce final app.py and templates/*.html."
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