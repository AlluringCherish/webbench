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

    # Run BackendDesignArchitect and FrontendDesignArchitect in parallel
    await asyncio.gather(
        execute(BackendDesignArchitect, "Create backend_design.md specifying Flask routes, data schemas, and file interaction patterns based on user_task_description."),
        execute(FrontendDesignArchitect, "Create frontend_design.md specifying HTML templates, element IDs, UI components, and navigation based on user_task_description.")
    )

    # Read outputs for merger
    backend_content, frontend_content = "", ""
    try:
        backend_content = open("backend_design.md").read()
    except Exception:
        pass
    try:
        frontend_content = open("frontend_design.md").read()
    except Exception:
        pass

    # Merge backend and frontend designs into design_spec.md
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md to create unified design_spec.md.\n\n"
        f"=== backend_design.md ===\n{backend_content}\n\n"
        f"=== frontend_design.md ===\n{frontend_content}"
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
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Run BackendDeveloper and FrontendDeveloper in parallel
    await asyncio.gather(
        execute(
            BackendDeveloper,
            "Implement app.py with routes, data loading, search, playlist management, and statistics as specified in design_spec.md. "
            "Save output to app.py."
        ),
        execute(
            FrontendDeveloper,
            "Implement all HTML templates (*.html) according to design_spec.md with exact element IDs, navigation, and UI features. "
            "Save output to templates/*.html."
        )
    )

    # Read latest outputs for IntegrationMerger
    app_content = ""
    templates_content = ""
    try:
        app_content = open("app.py").read()
    except FileNotFoundError:
        pass

    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except OSError:
            pass

    # Run IntegrationMerger to merge and verify full integration, output final app.py and templates
    await execute(
        IntegrationMerger,
        "Consolidate and reconcile backend app.py and frontend templates/*.html to ensure interface consistency and correctness "
        "per design_spec.md. Adjust only integration points, no new features. Output final app.py and templates/*.html.\n\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
        f"=== app.py ===\n{app_content}\n\n"
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