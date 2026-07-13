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

    # Parallel execution of BackendDesignArchitect and FrontendDesignArchitect
    await asyncio.gather(
        execute(BackendDesignArchitect, "Design complete backend architecture and output backend_design.md"),
        execute(FrontendDesignArchitect, "Design complete frontend specification and output frontend_design.md")
    )

    # Read backend_design.md and frontend_design.md for merger
    backend_design_content = ""
    frontend_design_content = ""
    try:
        backend_design_content = open("backend_design.md").read()
    except FileNotFoundError:
        pass
    try:
        frontend_design_content = open("frontend_design.md").read()
    except FileNotFoundError:
        pass

    # Merge backend and frontend designs into design_spec.md
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md into a consistent design_spec.md.\n\n"
        f"=== Backend Design ===\n{backend_design_content}\n\n"
        f"=== Frontend Design ===\n{frontend_design_content}"
    )
# Phase1_End
# Phase2_Start
import glob
async def implementation_and_verification_phase():
    BackendDeveloper = build_resilient_agent(
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
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
        timeout_threshold=450,
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
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=40
    )

    # Parallel execution of BackendDeveloper and FrontendDeveloper implementations
    await asyncio.gather(
        execute(
            BackendDeveloper,
            "Implement the complete backend app.py with all Flask routes, data management, version control, approvals, content scheduling, and analytics as specified in design_spec.md."
        ),
        execute(
            FrontendDeveloper,
            "Implement all frontend templates in templates/*.html with exact page structure, element IDs, navigation, and dynamic placeholders as specified in design_spec.md."
        )
    )

    # Read latest backend and frontend outputs for integration
    backend_code = ""
    frontend_templates_content = ""
    try:
        backend_code = open("app.py").read()
    except FileNotFoundError:
        pass
    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            frontend_templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # Run IntegrationMerger to reconcile backend and frontend outputs with design_spec.md
    await execute(
        IntegrationMerger,
        "Combine and reconcile backend app.py and frontend templates/*.html ensuring consistency with design_spec.md.\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
        f"=== backend app.py ===\n{backend_code}\n\n"
        f"=== frontend templates ==={frontend_templates_content}"
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