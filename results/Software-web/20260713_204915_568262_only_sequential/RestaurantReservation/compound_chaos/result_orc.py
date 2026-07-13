# Phase1_Start
async def design_specification_phase():
    # Create RequirementsAnalyst agent
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
    # Create WebArchitect agent
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

    # Execute RequirementsAnalyst first
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description. Extract all user-visible pages, element IDs, user actions, navigation flows, and data file schemas. Write detailed requirements_analysis.md in markdown.")

    # Read requirements_analysis.md content for WebArchitect
    req_analysis_content = ""
    try:
        req_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    # Execute WebArchitect after RequirementsAnalyst
    await execute(WebArchitect,
                  f"Read the following requirements_analysis.md content and user_task_description.\n"
                  f"=== requirements_analysis.md ===\n"
                  f"{req_analysis_content}\n"
                  f"Analyze and produce design_spec.md covering Flask routes, template files, page titles, element IDs, forms, data files, and user navigation. Ensure root '/' leads to dashboard.")
# Phase1_End

# Phase2_Start
async def implementation_phase():
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
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution: DraftEngineer first, then IntegrationEngineer
    await execute(DraftEngineer,
                  "Develop initial app_draft.py with all Flask routes starting at '/', implementing data handling and forms according to design_spec.md and user requirements. "
                  "Also draft all templates_draft/*.html with correct element IDs, navigation, and page content per specs.")

    # Read draft outputs for integration
    app_draft_code, templates_draft_files = "", ""
    try:
        app_draft_code = open("app_draft.py").read()
    except:
        pass
    # read all templates_draft/*.html files content concatenated (if needed)
    # but since templates_draft/*.html are multiple files, we do not read content here; inject message refers to them collectively

    await execute(IntegrationEngineer,
                  "Refine app_draft.py and templates_draft/*.html by replacing draft paths with production paths, correct template references, verify '/' route as Dashboard, "
                  "and ensure all filenames, element IDs, and page titles strictly match design_spec.md and user requirements. Output final app.py and templates/*.html files.")
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
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )
    SequentialFixer = build_resilient_agent(
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )

    # Read file artifacts for injection
    app_py_content = ""
    templates_content = ""
    try:
        app_py_content = open("app.py").read()
    except Exception:
        pass
    from glob import glob
    templates_files = glob("templates/*.html")
    aggregated_templates = []
    for tpl_file in templates_files:
        try:
            content = open(tpl_file).read()
            aggregated_templates.append(f"=== {tpl_file} ===\n{content}")
        except Exception:
            pass
    templates_content = "\n\n".join(aggregated_templates)

    # Execute WebValidator sequentially then SequentialFixer
    await execute(WebValidator,
                  f"Validate app.py, templates/*.html, and project correctness. "
                  f"Use validate_python_file and execute_python_code tools. "
                  f"Follow design_spec.md and user_task_description. "
                  f"Output detailed validation_report.md with issues and improvement suggestions.\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n=== templates ===\n{templates_content}")

    # After validation, read validation_report.md content for injection
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except Exception:
        pass

    await execute(SequentialFixer,
                  f"Apply fixes from validation_report.md to app.py and templates/*.html. "
                  f"Ensure final app.py and templates fully comply with design_spec.md and user_task_description. "
                  f"Do not introduce new features, only corrections. Produce final corrected files.\n\n"
                  f"=== validation_report.md ===\n{validation_report_content}\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n=== templates ===\n{templates_content}")
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