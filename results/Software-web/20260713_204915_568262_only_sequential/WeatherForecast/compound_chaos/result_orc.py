# Phase1_Start
async def design_specification_phase():
    RequirementsAnalyst = build_resilient_agent(
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=220,
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
        timeout_threshold=250,
        failure_threshold=1,
        recovery_time=30
    )

    # Sequential execution: RequirementsAnalyst then WebArchitect
    await execute(RequirementsAnalyst, "Analyze user_task_description and produce requirements_analysis.md covering all pages, element IDs, routes, and data files.")
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    await execute(WebArchitect,
                  f"Read requirements_analysis.md and produce design_spec.md specifying Flask routes, HTTP methods, template files, element IDs, context variables, and data file interactions.\n\n"
                  f"=== requirements_analysis.md ===\n{requirements_analysis_content}")
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
        max_retries=2,
        timeout_threshold=260,
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
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=50
    )

    # Sequential Flow
    # Step 1: DraftEngineer creates app_draft.py and templates_draft/*.html based on design_spec.md
    await execute(DraftEngineer, "Implement draft Flask backend as app_draft.py with route placeholders and templates_draft/*.html with exact element IDs and layouts from design_spec.md using placeholders for data and logic")

    # Read draft artifacts for IntegrationEngineer
    app_draft_content = ""
    templates_draft_content = ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    try:
        # As templates_draft/*.html is a pattern, read all draft templates content concatenated
        import glob
        draft_files = glob.glob("templates_draft/*.html")
        contents = []
        for file in draft_files:
            try:
                contents.append(f"=== {file} ===\n" + open(file).read())
            except:
                pass
        templates_draft_content = "\n\n".join(contents)
    except:
        pass

    # Step 2: IntegrationEngineer integrates drafts into final app.py and templates/*.html with full data integration
    await execute(IntegrationEngineer,
        f"Integrate draft backend and frontend to fully functional app.py and templates/*.html. "
        f"Use design_spec.md, app_draft.py, and all templates_draft/*.html. "
        f"Implement file I/O from 'data' directory, parse exact field orders, convert templates with Jinja2 dynamic placeholders, preserve all element IDs and navigation as per design_spec.md.\n\n"
        f"=== app_draft.py ===\n{app_draft_content}\n\n=== Templates Draft ===\n{templates_draft_content}"
    )
# Phase2_End

# Phase3_Start
import asyncio

async def verification_phase():
    WebValidator = build_resilient_agent(
        agent_name="WebValidator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=400,
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
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )

    # Execute WebValidator to produce validation_report.md
    await execute(WebValidator,
                  "Perform thorough validation of app.py syntax and runtime using validate_python_file and execute_python_code tools. "
                  "Check that all routes from design_spec.md are implemented and render correct templates. "
                  "Verify all required UI element IDs are present in templates/*.html, ensure data files usage matches design_spec.md schemas. "
                  "Produce comprehensive validation_report.md with detailed findings, error traces, warnings, and passes.")

    # Read validation report content
    validation_report_content = ""
    try:
        with open("validation_report.md", "r") as f:
            validation_report_content = f.read()
    except FileNotFoundError:
        validation_report_content = ""

    # Execute SequentialFixer to fix all issues based on validation_report.md
    # Inject validation_report.md content directly for fixing
    await execute(SequentialFixer,
                  f"Apply all corrections identified in validation_report.md to produce final versions of app.py and templates/*.html. "
                  f"Fix syntax/runtime errors, complete route coverage, correct template UI element IDs, and align data loading with design_spec.md. "
                  f"Produce production-ready, error-free backend and frontend code.\n\n"
                  f"=== Validation Report ===\n"
                  f"{validation_report_content}")
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