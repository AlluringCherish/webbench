# Phase1_Start
async def design_specification_phase():
    BackendDesignArchitect = build_resilient_agent(
        agent_name="BackendDesignArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=450,
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
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )
    DesignMerger = build_resilient_agent(
        agent_name="DesignMerger",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )

    # Parallel execution of BackendDesignArchitect and FrontendDesignArchitect
    await asyncio.gather(
        execute(BackendDesignArchitect, "Create backend_design.md specifying all backend Flask routes, data schemas, and file access logic fully independently."),
        execute(FrontendDesignArchitect, "Create frontend_design.md specifying all HTML templates, element IDs, navigation flows, and UI elements fully independently.")
    )

    # Read backend_design.md and frontend_design.md outputs
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

    # Merge designs into unified design_spec.md
    await execute(
        DesignMerger,
        "Merge backend_design.md and frontend_design.md with user_task_description into a consistent design_spec.md with coherent routes, templates, context variables, data schemas, and navigation.\n\n"
        f"=== backend_design.md ===\n{backend_design_content}\n\n"
        f"=== frontend_design.md ===\n{frontend_design_content}"
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
        failure_threshold=1,
        recovery_time=40
    )

    # Parallel execution of BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(
            BackendDeveloper,
            "Implement complete Flask backend app.py for GymMembership using design_spec.md, "
            "handling all routes, data files, and business logic exactly as specified."
        ),
        execute(
            FrontendDeveloper,
            "Implement all HTML templates (*.html) for GymMembership frontend with specified element IDs, "
            "navigation, and layouts per design_spec.md."
        )
    )

    # Read outputs for IntegrationMerger
    app_py_content = ""
    templates_content = ""
    try:
        app_py_content = open("app.py").read()
    except Exception:
        pass
    for template_path in sorted(glob.glob("templates/*.html")):
        try:
            templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
        except Exception:
            pass

    # IntegrationMerger harmonizes backend and frontend
    await execute(
        IntegrationMerger,
        f"Combine and reconcile GymMembership backend app.py and frontend templates for consistency.\n\n"
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