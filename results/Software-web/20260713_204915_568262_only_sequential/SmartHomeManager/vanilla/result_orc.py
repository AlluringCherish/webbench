# Phase1_Start
async def design_specification_phase():
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
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution: RequirementsAnalyst produces requirements_analysis.md, then WebArchitect produces design_spec.md
    await execute(RequirementsAnalyst,
                  "Analyze user task description and produce requirements_analysis.md including all pages, element IDs, navigation buttons, and data storage definitions.")
    
    # Read requirements_analysis.md content for injection
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    await execute(WebArchitect,
                  f"Using the following requirements_analysis.md content, create a detailed design_spec.md with explicit page details, navigation routing, data file formats, and user flows.\n\n=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start
async def implementation_phase():
    ImplementationEngineer = build_resilient_agent(
        agent_name="ImplementationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )

    design_spec_content = ""
    try:
        with open("design_spec.md", "r") as f:
            design_spec_content = f.read()
    except:
        pass

    await execute(
        ImplementationEngineer,
        f"Develop complete Flask app.py and all templates/*.html files based on the design_spec.md below. "
        f"Implement 7 pages with exact route functions, UI element IDs, navigation, and local data file read/write in 'data/' folder.\n\n"
        f"=== design_spec.md ===\n{design_spec_content}"
    )
# Phase2_End

# Phase3_Start
async def verification_phase():
    Validator = build_resilient_agent(
        agent_name="Validator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    Fixer = build_resilient_agent(
        agent_name="Fixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=45
    )

    # Read all relevant files to inject into Validator
    design_spec_md = ""
    app_py = ""
    templates_html = ""
    try:
        design_spec_md = open("design_spec.md").read()
    except:
        pass
    try:
        app_py = open("app.py").read()
    except:
        pass
    import glob
    try:
        template_files = glob.glob("templates/*.html")
        templates_html = ""
        for tf in template_files:
            try:
                templates_html += f"=== {tf} ===\n" + open(tf).read() + "\n\n"
            except:
                pass
    except:
        pass

    # Execute Validator to produce validation_report.md
    await execute(
        Validator,
        f"Validate Flask backend and HTML templates for SmartHomeManager application.\n\n"
        f"=== design_spec.md ===\n{design_spec_md}\n\n"
        f"=== app.py ===\n{app_py}\n\n"
        f"=== Templates ===\n{templates_html}\n\n"
        "Perform syntax and runtime checks on app.py using validate_python_file and execute_python_code tools. "
        "Simulate HTTP requests to all Flask routes, check status codes and presence of all specified element IDs in templates. "
        "Verify correct local file data operations as per design_spec.md. "
        "Output a detailed validation_report.md including syntax errors, runtime errors, UI defects, and data issues."
    )

    # Read validation_report.md content for fixing
    validation_report_md = ""
    try:
        validation_report_md = open("validation_report.md").read()
    except:
        pass

    # Inject validation_report.md plus design_spec.md plus current app.py and templates/* for Fixer agent
    await execute(
        Fixer,
        f"Apply all fixes to app.py and all templates/*.html as per validation_report.md below:\n\n"
        f"=== validation_report.md ===\n{validation_report_md}\n\n"
        f"=== design_spec.md ===\n{design_spec_md}\n\n"
        f"=== Current app.py ===\n{app_py}\n\n"
        f"=== Current Templates ===\n{templates_html}\n\n"
        "Fix all backend defects (syntax, routes, data handling) and frontend defects (element IDs, navigation, structure). "
        "Output corrected app.py and templates/*.html files using write_text_file tool."
    )
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