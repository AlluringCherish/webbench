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
        max_retries=3,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
    )

    # Parallel execution of backend and frontend design architects
    await asyncio.gather(
        execute(BackendDesignArchitect,
                "Read user_task_description. Independently create backend_design.md specifying Flask routes, data schemas, "
                "local text file usage and business logic for VirtualMuseum backend."),
        execute(FrontendDesignArchitect,
                "Read user_task_description. Independently create frontend_design.md specifying detailed HTML template specifications, "
                "exact element IDs, navigation, and UI components for VirtualMuseum frontend.")
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

    # Merge backend and frontend design specs into design_spec.md
    await execute(DesignMerger,
                  f"User task description:\n{CONTEXT.get('user_task_description', '')}\n\n"
                  f"=== Backend Design ===\n{backend_design_content}\n\n"
                  f"=== Frontend Design ===\n{frontend_design_content}")
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
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )

    # Parallel execution of BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete app.py backend Flask application based on design_spec.md backend specifications, including routes, request handling, file-based data persistence, and business logic."),
        execute(FrontendDeveloper,
                "Implement all 7 HTML templates in templates/*.html with exact element IDs, Jinja2 syntax, page structure, and navigation as per design_spec.md frontend specifications.")
    )

    # Read outputs for IntegrationMerger
    backend_code = ""
    frontend_templates = ""
    try:
        backend_code = open("app.py").read()
    except Exception:
        pass
    for tpl_path in sorted(glob.glob("templates/*.html")):
        try:
            frontend_templates += f"\n=== {tpl_path} ===\n" + open(tpl_path).read()
        except Exception:
            pass

    # IntegrationMerger merges and reconciles backend and frontend artifacts
    await execute(
        IntegrationMerger,
        f"Integrate and reconcile app.py backend and templates/*.html frontend artifacts ensuring full interface consistency and readiness for deployment.\n\n"
        f"=== design_spec.md ===\n{CONTEXT['design_spec.md']}\n\n"
        f"=== app.py ===\n{backend_code}\n\n"
        f"=== Templates ===\n{frontend_templates}"
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