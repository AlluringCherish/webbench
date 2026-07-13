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

    # Parallel execution of BackendDesignArchitect and FrontendDesignArchitect
    await asyncio.gather(
        execute(BackendDesignArchitect, "Read user_task_description and create backend_design.md specifying backend data models and Flask routes according to requirements."),
        execute(FrontendDesignArchitect, "Read user_task_description and create frontend_design.md specifying HTML templates structure, element IDs, UI components, and navigation flows as per requirements.")
    )

    # Read outputs of both architects for merger
    backend_design_content, frontend_design_content = "", ""
    try:
        backend_design_content = open("backend_design.md").read()
    except FileNotFoundError:
        pass
    try:
        frontend_design_content = open("frontend_design.md").read()
    except FileNotFoundError:
        pass

    # Merge backend_design.md and frontend_design.md into design_spec.md
    await execute(
        DesignMerger,
        f"Read user_task_description, backend_design.md, and frontend_design.md.\n"
        f"Reconcile and merge into design_spec.md ensuring consistency and completeness.\n\n"
        f"=== backend_design.md ===\n{backend_design_content}\n\n"
        f"=== frontend_design.md ===\n{frontend_design_content}"
    )
# Phase1_End
# Phase2_Start
async def implementation_and_verification_phase():
    import glob

    BackendDeveloper = build_resilient_agent(
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=40
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
        recovery_time=40
    )

    IntegrationMerger = build_resilient_agent(
        agent_name="IntegrationMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=30
    )

    # Parallel implementation of backend and frontend
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete runnable app.py backend from design_spec.md, "
                "handling all Flask routes, data files and business logic for smart home system."),
        execute(FrontendDeveloper,
                "Implement all templates/*.html frontend pages with exact element IDs, layout and Jinja2 syntax "
                "from design_spec.md.")
    )

    # Read outputs from BackendDeveloper and FrontendDeveloper for integration
    design_spec_content = ""
    try:
        design_spec_content = open("design_spec.md").read()
    except FileNotFoundError:
        pass

    app_py_content = ""
    try:
        app_py_content = open("app.py").read()
    except FileNotFoundError:
        pass

    templates_content = ""
    for tpl_path in sorted(glob.glob("templates/*.html")):
        try:
            content = open(tpl_path).read()
            templates_content += f"\n=== {tpl_path} ===\n{content}"
        except OSError:
            pass

    # IntegrationMerger merges and reconciles backend and frontend into final deliverables
    await execute(
        IntegrationMerger,
        "Integrate backend app.py and frontend templates/*.html into final consistent application.\n\n"
        f"=== design_spec.md ===\n{design_spec_content}\n\n"
        f"=== Backend app.py ===\n{app_py_content}\n\n"
        f"=== Frontend templates ===\n{templates_content}"
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