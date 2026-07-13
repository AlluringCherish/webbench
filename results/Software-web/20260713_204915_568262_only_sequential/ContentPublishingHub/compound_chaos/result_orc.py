# Phase1_Start
async def design_specification_phase():
    # Create agents
    RequirementsAnalyst = build_resilient_agent(
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=30
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
        recovery_time=30
    )

    # Sequential execution
    await execute(RequirementsAnalyst,
                  "Read user_task_description and produce requirements_analysis.md capturing all page routes, element IDs, page purposes, and local data storage formats without assumptions.")

    # Read requirements_analysis.md for WebArchitect
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    await execute(WebArchitect,
                  f"Read user_task_description and requirements_analysis.md. Convert the requirements_analysis.md content into design_spec.md specifying Flask routes, HTML templates with exact element IDs, data storage file schema, button behaviors, and application flow. Maintain full consistency and naming exactness.\n\n=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start
async def implementation_phase():
    # Create agents
    DraftEngineer = build_resilient_agent(
        agent_name="DraftEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    IntegrationEngineer = build_resilient_agent(
        agent_name="IntegrationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution: DraftEngineer first, then IntegrationEngineer
    await execute(DraftEngineer,
                  "Create complete app_draft.py implementing all routes and data handling per design_spec.md. "
                  "Create all templates_draft/*.html with exact element IDs, page layouts, and placeholders. Use render_template with templates_draft folder.")

    # Read draft files content to inject for IntegrationEngineer
    app_draft_code = ""
    templates_draft_content = ""
    try:
        app_draft_code = open("app_draft.py").read()
    except:
        pass
    # Attempt to read all templates_draft/*.html files - simplistic approach: read at least one or multiple files if needed
    # For orchestration, we provide only aggregated content string representing templates draft.
    # This can be improved with explicit names if known.
    import glob
    templates_files = []
    try:
        templates_files = glob.glob("templates_draft/*.html")
    except:
        templates_files = []

    templates_content_accum = ""
    for t_file in templates_files:
        try:
            t_content = open(t_file).read()
            templates_content_accum += f"=== {t_file} ===\n{t_content}\n\n"
        except:
            continue
    templates_draft_content = templates_content_accum

    await execute(IntegrationEngineer,
                  f"Integrate draft into final app.py and templates/*.html per design_spec.md. "
                  f"Refactor routes to use templates folder, verify all element IDs and page structures strictly follow design_spec.md. "
                  f"Ensure final app.py is runnable without draft references.\n\n"
                  f"=== app_draft.py content ===\n{app_draft_code}\n\n"
                  f"=== templates_draft content ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start
async def verification_phase():
    WebValidator = build_resilient_agent(
        agent_name="WebValidator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    SequentialFixer = build_resilient_agent(
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=420,
        failure_threshold=1,
        recovery_time=40
    )

    # Run WebValidator to produce validation_report.md
    await execute(WebValidator,
                  "Validate backend app.py using validate_python_file and execute_python_code tools. "
                  "Check all routes from design_spec.md including /dashboard and dynamic routes, HTTP methods, and runtime stability. "
                  "Validate frontend templates/*.html for presence of all required element IDs and UI components as specified in design_spec.md and user task description. "
                  "Produce detailed validation_report.md with pass/fail for routes and UI elements.")

    # Read validation_report.md content for injection
    validation_report = ""
    try:
        validation_report = open("validation_report.md", "r").read()
    except Exception:
        validation_report = ""

    # Run SequentialFixer to fix all issues based on validation_report.md
    await execute(SequentialFixer,
                  "Apply all fixes to app.py and templates/*.html based on the following validation_report.md. "
                  "Ensure full conformance with design_spec.md and user task requirements, resolving all reported functional, route, and UI element issues.\n"
                  f"=== validation_report.md ===\n{validation_report}")
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