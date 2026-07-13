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
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution
    # Step 1: RequirementsAnalyst creates requirements_analysis.md
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce comprehensive requirements_analysis.md capturing all pages, exact element IDs, page titles, navigation buttons, and data requirements.")

    # Step 2: WebArchitect creates design_spec.md based on user input and requirements_analysis.md
    req_analysis_content = ""
    try:
        req_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    user_task_desc = ""
    entries = CONTEXT.get("user_task_description", [])
    if entries:
        user_task_desc = entries[-1]["content"]

    await execute(WebArchitect,
                  f"Read user_task_description and requirements_analysis.md. Produce design_spec.md with complete Flask routes (paths, HTTP methods, function names), page titles, exact element IDs (including dynamic patterns), navigation mappings (buttons→route functions), and data storage contracts (data files with filenames, pipe-delimited formats, fields, and usage). Ensure no ambiguity and full coverage.\n\n"
                  f"=== User Task Description ===\n{user_task_desc}\n\n"
                  f"=== Requirements Analysis ===\n{req_analysis_content}")
# Phase1_End

# Phase2_Start
async def implementation_phase():
    # Declare agents
    ImplementationEngineer = build_resilient_agent(
        agent_name="ImplementationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=50
    )
    IntegrationEngineer = build_resilient_agent(
        agent_name="IntegrationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=50
    )

    # Sequential execution: First ImplementationEngineer, then IntegrationEngineer
    # Execute ImplementationEngineer to produce app_draft.py and templates_draft/*.html
    await execute(ImplementationEngineer,
                  "Develop full draft implementation with app_draft.py and templates_draft/*.html "
                  "including all Flask routes, local text file data management, pages, navigation, and element IDs "
                  "per design_spec.md and user_task_description.")

    # Read draft files for integration
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    # For templates_draft/*.html, assume reading all template files content
    # Since file names are unknown, read all matching pattern files in directory would be necessary in real environment
    # Here we read as empty string placeholder as per instructions
    try:
        import glob
        template_files = glob.glob("templates_draft/*.html")
        templates_draft_content = ""
        for tf in template_files:
            try:
                templates_draft_content += f"\n=== {tf} ===\n" + open(tf).read() + "\n"
            except:
                continue
    except:
        templates_draft_content = ""

    # Execute IntegrationEngineer to convert drafts into final production code app.py and templates/*.html
    await execute(IntegrationEngineer,
                  f"Refine and verify draft code into final production-ready app.py and templates/*.html. "
                  f"Use user_task_description, design_spec.md, app_draft.py, and all draft templates.\n\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n"
                  f"=== templates_draft/*.html ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start
async def verification_phase():
    VerificationEngineer = build_resilient_agent(
        agent_name="VerificationEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )
    BugFixEngineer = build_resilient_agent(
        agent_name="BugFixEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Sequential Flow Execution
    # 1. VerificationEngineer runs validation and produces validation_report.md
    await execute(
        VerificationEngineer,
        "Validate syntax and runtime of app.py using validate_python_file and execute_python_code. "
        "Verify all UI element IDs and navigation in templates/*.html against design_spec.md. "
        "Check data file access and parsing in app.py as per design_spec.md. "
        "Output a comprehensive validation_report.md with errors, warnings, and fix suggestions."
    )

    # 2. BugFixEngineer applies fixes based on validation_report.md and outputs corrected files
    # Reading validation_report.md content to inject for bug fixing
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except Exception:
        pass

    # Reading current artifacts for bug fixing injection
    design_spec_content = ""
    app_py_content = ""
    templates_content = ""
    try:
        design_spec_content = open("design_spec.md").read()
    except Exception:
        pass
    try:
        app_py_content = open("app.py").read()
    except Exception:
        pass
    # For templates/*.html, read as a single string; if multiple files, concatenate with separators for clarity
    try:
        import glob
        templates_files = glob.glob("templates/*.html")
        templates_contents_list = []
        for tf in templates_files:
            try:
                tf_content = open(tf).read()
                templates_contents_list.append(f"=== {tf} ===\n{tf_content}\n")
            except Exception:
                continue
        templates_content = "\n".join(templates_contents_list)
    except Exception:
        templates_content = ""

    await execute(
        BugFixEngineer,
        f"Analyze validation_report.md and fix all issues in app.py and templates/*.html accordingly. "
        f"Preserve design_spec.md requirements. Output final app.py and templates/*.html files.\n\n"
        f"=== validation_report.md ===\n{validation_report_content}\n\n"
        f"=== design_spec.md ===\n{design_spec_content}\n\n"
        f"=== app.py ===\n{app_py_content}\n\n"
        f"=== templates/*.html ===\n{templates_content}"
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