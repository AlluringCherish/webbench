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

    # Sequential Flow:
    # Step 1: RequirementsAnalyst produces requirements_analysis.md
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce requirements_analysis.md with complete page specs, navigation flows, data formats, user actions.")

    # Read requirements_analysis.md content
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    # Step 2: WebArchitect produces design_spec.md based on user_task_description and requirements_analysis.md
    await execute(WebArchitect,
                  f"Using user_task_description and the following requirements_analysis.md content, create detailed design_spec.md defining Flask routes, templates, page structure, element IDs, backend data files, and navigation actions.\n\n=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    # Declare agents
    ImplementationAgent = build_resilient_agent(
        agent_name="ImplementationAgent",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    IntegrationAgent = build_resilient_agent(
        agent_name="IntegrationAgent",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution
    # Step 1: ImplementationAgent creates app_draft.py and templates_draft/*.html drafts
    await execute(
        ImplementationAgent,
        "Create complete draft of app_draft.py with all Flask routes, data handling, and templates_draft/*.html with exact element IDs, page titles, and navigation, based on design_spec.md and user requirements."
    )

    # Step 2: Read draft files for IntegrationAgent
    app_draft_content = ""
    templates_draft_content = ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    try:
        # As templates_draft/*.html means multiple files, we read all and concatenate with separators for context
        import glob
        files = glob.glob("templates_draft/*.html")
        contents = []
        for f in files:
            try:
                content = open(f).read()
                contents.append(f"=== {f} ===\n{content}\n")
            except:
                contents.append(f"=== {f} ===\n\n")
        templates_draft_content = "\n".join(contents)
    except:
        pass

    # Step 3: IntegrationAgent integrates drafts into final app.py and templates/*.html
    await execute(
        IntegrationAgent,
        f"Integrate and finalize app.py and templates/*.html based on design_spec.md, user requirements, app_draft.py, and templates_draft/*.html drafts. Produce clean, runnable final application with full compliance.\n\n=== app_draft.py ===\n{app_draft_content}\n=== Templates Draft ===\n{templates_draft_content}"
    )
# Phase2_End

# Phase3_Start
async def verification_phase():
    # Declare agents
    ValidatorAgent = build_resilient_agent(
        agent_name="ValidatorAgent",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=60
    )
    FixerAgent = build_resilient_agent(
        agent_name="FixerAgent",
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
    user_task_description = ""
    design_spec = ""
    app_py = ""
    templates_content = ""

    try:
        user_entries = CONTEXT.get("user_task_description", [])
        user_task_description = user_entries[-1]["content"] if user_entries else ""
    except:
        pass

    try:
        design_entries = CONTEXT.get("design_spec.md", [])
        design_spec = design_entries[-1]["content"] if design_entries else ""
    except:
        pass

    try:
        app_py = open("app.py").read()
    except:
        app_py = ""

    import glob
    import os

    templates_files_content = ""
    try:
        templates_files = [f for f in glob.glob("templates/*.html") if os.path.isfile(f)]
        for tf in templates_files:
            try:
                content = open(tf).read()
                templates_files_content += f"=== {tf} ===\n{content}\n\n"
            except:
                pass
    except:
        templates_files_content = ""

    # Execute ValidatorAgent
    await execute(ValidatorAgent,
                  f"Validate backend and frontend files for compliance:\n"
                  f"user_task_description:\n{user_task_description}\n\n"
                  f"design_spec.md:\n{design_spec}\n\n"
                  f"app.py content:\n{app_py}\n\n"
                  f"templates content:\n{templates_files_content}\n\n"
                  "Run validate_python_file on app.py, check runtime routes, verify route existence, element IDs in templates, navigation correctness, data file access,"
                  " and produce detailed validation_report.md with all errors and actionable feedback. Use validate_python_file and execute_python_code tools. "
                  "Do NOT fix issues here.")
    
    # Read validation_report.md for FixerAgent injection
    validation_report = ""
    try:
        validation_report = open("validation_report.md").read()
    except:
        validation_report = ""

    # Execute FixerAgent to fix issues reported
    await execute(FixerAgent,
                  f"Apply all fixes to app.py and templates/*.html based on the validation report below:\n\n"
                  f"user_task_description:\n{user_task_description}\n\n"
                  f"design_spec.md:\n{design_spec}\n\n"
                  f"Current app.py content:\n{app_py}\n\n"
                  f"Current templates:\n{templates_files_content}\n\n"
                  f"Validation Report:\n{validation_report}\n\n"
                  "Fix all syntax/runtime errors, missing routes, element IDs, navigation issues, and data handling defects."
                  " Output corrected app.py and all templates/*.html as final artifacts.")
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