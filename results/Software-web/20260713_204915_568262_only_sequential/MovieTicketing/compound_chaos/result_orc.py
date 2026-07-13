# Phase1_Start
async def design_specification_phase():
    # Build agents
    RequirementsAnalyst = build_resilient_agent(
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=260,
        failure_threshold=1,
        recovery_time=40
    )
    WebArchitect = build_resilient_agent(
        agent_name="WebArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce requirements_analysis.md covering all pages, UI elements, data files, navigation flows")

    # Read requirements_analysis.md content to inject for WebArchitect
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except Exception:
        pass

    await execute(WebArchitect,
                  f"Based on requirements_analysis.md and user_task_description, produce design_spec.md specifying Flask routes, pages, element IDs, navigation, and data file contracts.\n\n=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    # Create agents
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
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=50
    )

    # Execute ImplementationEngineer first
    await execute(ImplementationEngineer,
                  "Develop draft Flask app named app_draft.py with all 8 routes, "
                  "and create draft HTML templates under templates_draft/ with exact page titles and element IDs. "
                  "Include navigation buttons for page transitions starting from Dashboard. "
                  "Parse local text-based data files with exact formats.")

    # Read draft app and draft templates for injection
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    try:
        # Note: For templates_draft/*.html, since this is a wildcard, just read as empty or not read here explicitly.
        # Agents should read these internally, but requirement states to inject content for subsequent calls when refinement loop or debate patterns,
        # Here, we won't read all templates files individually, just pass message referencing them
        templates_draft_content = ""  
    except:
        pass

    # Execute IntegrationEngineer with injected draft app and templates content
    await execute(IntegrationEngineer,
                  "Refine draft app_draft.py and templates_draft/*.html into final app.py and templates/*.html "
                  "enforcing exact routes, element IDs, and data parsing from design_spec.md. "
                  "Start routing from Dashboard page with exact route behaviors. "
                  "Ensure robust file parsing and accurate navigation buttons. "                   
                  f"=== app_draft.py ===\n{app_draft_content}\n"
                  f"=== templates_draft/*.html ===\n{templates_draft_content}")
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
        failure_threshold=1,
        recovery_time=50
    )
    SequentialFixer = build_resilient_agent(
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=50
    )

    # Execute WebValidator first for full validation and produce validation_report.md
    await execute(WebValidator, 
                  "Validate app.py using validate_python_file and execute_python_code tools. "
                  "Validate templates/*.html for structure, element IDs, and design_spec.md compliance. "
                  "Check Flask routes, context variables, and data file handling against design_spec.md sections. "
                  "Produce detailed validation_report.md with all findings and actionable comments.")

    # Read validation_report.md content for injection
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except:
        pass

    # SequentialFixer applies fixes based on validation_report.md
    await execute(SequentialFixer,
                  f"Fix all issues identified in validation_report.md to finalize app.py and templates/*.html. "
                  f"Ensure full compliance with design_spec.md and user requirements. "
                  f"Maintain artifact file names and formats.\n\n=== Validation Report ===\n{validation_report_content}")
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