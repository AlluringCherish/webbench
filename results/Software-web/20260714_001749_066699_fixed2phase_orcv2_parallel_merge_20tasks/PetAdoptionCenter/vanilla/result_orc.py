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
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Parallel execution of backend and frontend design architects
    await asyncio.gather(
        execute(
            BackendDesignArchitect,
            "Design backend architecture and produce backend_design.md based on user_task_description. "
            "Define Flask routes, data schemas, and backend logic for all pages."
        ),
        execute(
            FrontendDesignArchitect,
            "Design frontend templates and produce frontend_design.md based on user_task_description. "
            "Specify exact element IDs, page titles, navigation flows, and data placeholders for all pages."
        ),
    )

    # Read backend_design.md and frontend_design.md outputs for merger
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

    # Run DesignMerger to produce final design_spec.md
    await execute(
        DesignMerger,
        f"Merge backend_design.md and frontend_design.md into a consistent design_spec.md with coverage of all user requirements.\n\n"
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

    # Parallel execution of BackendDeveloper and FrontendDeveloper
    await asyncio.gather(
        execute(BackendDeveloper,
                "Implement complete backend Flask app.py strictly from design_spec.md including all routes, data handling, forms."),
        execute(FrontendDeveloper,
                "Create all HTML templates in templates/*.html strictly from design_spec.md including correct element IDs and navigation.")
    )

    # Read the backend output app.py
    backend_code = ""
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            backend_code = f.read()
    except FileNotFoundError:
        backend_code = ""

    # Read all frontend templates together content
    templates_content = ""
    for path in sorted(glob.glob("templates/*.html")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                templates_content += f"\n=== {path} ===\n" + f.read()
        except OSError:
            continue

    # IntegrationMerger merges and reconciles
    await execute(
        IntegrationMerger,
        f"Integrate and reconcile backend app.py and frontend templates with design_spec.md.\n"
        f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md', '')}\n\n"
        f"=== app.py ===\n{backend_code}\n\n"
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