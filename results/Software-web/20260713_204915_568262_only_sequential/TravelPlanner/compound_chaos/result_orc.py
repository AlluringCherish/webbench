# Phase1_Start
async def design_specification_phase():
    # Declare agents
    RequirementsAnalyst = build_resilient_agent(
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    WebArchitect = build_resilient_agent(
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution flow:
    # 1. RequirementsAnalyst produces requirements_analysis.md from user_task_description
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce detailed requirements_analysis.md covering all pages, UI elements, navigation flows, and data specifications")

    # 2. WebArchitect reads requirements_analysis.md and user_task_description, then produces design_spec.md
    # Read requirements_analysis.md content to inject
    req_analysis_content = ""
    try:
        with open("requirements_analysis.md", "r") as f:
            req_analysis_content = f.read()
    except:
        pass

    await execute(WebArchitect,
                  f"Read the following requirements_analysis.md content and user_task_description. "
                  f"Produce a comprehensive design_spec.md detailing Flask routes, templates, element IDs, navigation mappings, and data file contracts.\n\n"
                  f"=== requirements_analysis.md ===\n{req_analysis_content}")
# Phase1_End

# Phase2_Start
async def implementation_phase():
    BackendDeveloper = build_resilient_agent(
        agent_name="BackendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )
    FrontendDeveloper = build_resilient_agent(
        agent_name="FrontendDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    await execute(BackendDeveloper,
                  "Implement app_draft.py with all Flask routes, local file data handling, routing, "
                  "button-triggered navigation based on design_spec.md and user_task_description.")

    await execute(FrontendDeveloper,
                  "Implement all HTML templates in templates_draft/ with exact element IDs, page titles, forms, "
                  "buttons, and navigation consistent with backend routes from design_spec.md and user_task_description.")
# Phase2_End

# Phase3_Start
async def verification_phase():
    # Create agents
    Tester = build_resilient_agent(
        agent_name="Tester",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    FinalIntegrator = build_resilient_agent(
        agent_name="FinalIntegrator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=420,
        failure_threshold=2,
        recovery_time=60
    )

    # Sequential execution for verification phase
    await execute(Tester,
                  "Validate app_draft.py and templates_draft/*.html using validate_python_file and execute_python_code tools. "
                  "Check conformity to design_spec.md and user_task_description including backend routes, data handling, and UI elements. "
                  "Produce detailed validation_report.md with syntax/runtime errors, UI issues, navigation mismatches, and data handling problems.")

    # Read validation report content for FinalIntegrator
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except:
        pass

    # FinalIntegrator applies fixes based on validation report
    app_draft_content, templates_draft_content, design_spec_content, user_task_desc = "", "", "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    # Read all templates_draft/*.html files content as one string injection (concatenated)
    import glob
    import os
    templates_draft_files = glob.glob("templates_draft/*.html")
    templates_draft_content = ""
    for filepath in templates_draft_files:
        try:
            templates_draft_content += f"=== {os.path.basename(filepath)} ===\n"
            templates_draft_content += open(filepath).read() + "\n"
        except:
            continue
    try:
        design_spec_content = open("design_spec.md").read()
    except:
        pass
    entries = CONTEXT.get("user_task_description", [])
    user_task_desc = entries[-1]["content"] if entries else ""

    await execute(FinalIntegrator,
                  f"Apply all fixes from the following validation_report.md to produce final app.py and templates/*.html. "
                  f"Fixes must address syntax, runtime, routing, navigation, UI elements, and data handling. Do not add unrequested features.\n\n"
                  f"=== Validation Report ===\n{validation_report_content}\n\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n\n"
                  f"=== Templates Draft ===\n{templates_draft_content}\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"=== user_task_description ===\n{user_task_desc}")
# Phase3_End

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
        implementation_phase()
    ]
    step3 = [
        verification_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)
    await asyncio.gather(*step3)

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