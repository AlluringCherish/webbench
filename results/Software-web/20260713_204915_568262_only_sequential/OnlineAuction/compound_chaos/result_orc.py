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
        timeout_threshold=300,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution: RequirementsAnalyst then WebArchitect
    await execute(RequirementsAnalyst, "Analyze user_task_description and produce detailed requirements_analysis.md capturing all UI elements, pages, templates, element IDs, buttons, filters, data files, and navigation flows including Dashboard as start page.")
    
    # Read requirements_analysis.md content for WebArchitect input injection
    requirements_analysis_md = ""
    try:
        requirements_analysis_md = open("requirements_analysis.md").read()
    except Exception:
        pass

    await execute(WebArchitect, f"Based on user_task_description and the following requirements_analysis.md content, produce a detailed design_spec.md specifying Flask routes, HTTP methods, route function names, template filenames, page titles, element IDs, navigation mappings, context variables, and data file handling contracts including start page redirect to Dashboard.\n\n=== requirements_analysis.md ===\n{requirements_analysis_md}")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    DraftEngineer = build_resilient_agent(
        agent_name="DraftEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=45
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
        recovery_time=50
    )

    # Sequential execution: DraftEngineer first, then IntegrationEngineer
    await execute(DraftEngineer,
                  "Draft app_draft.py implementing all Flask routes with correct HTTP methods and data loading from text files. "
                  "Draft all templates_draft/*.html with exact element IDs, page titles, navigation buttons, forms and content per design_spec.md.")
    
    # Reading the outputs of drafts for injection
    app_draft_code = ""
    templates_draft_code = ""
    try:
        app_draft_code = open("app_draft.py").read()
    except Exception:
        pass
    try:
        # As templates_draft/*.html is a glob pattern, injection here will be generic.
        # In practice, multiple files would be read; here just try to read one or leave empty.
        # We inject all drafts content read from templates_draft/*.html files, but here simplified.
        templates_draft_code = open("templates_draft/index.html").read()
    except Exception:
        pass

    await execute(IntegrationEngineer,
                  f"Integrate draft implementations by reading app_draft.py and templates_draft/*.html. "
                  f"Produce final app.py and templates/*.html files, ensuring adherence to design_spec.md and runnable Flask app.\n\n"
                  f"=== app_draft.py ===\n{app_draft_code}\n\n=== templates_draft examples ===\n{templates_draft_code}")
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
        timeout_threshold=480,
        failure_threshold=1,
        recovery_time=45
    )
    SequentialFixer = build_resilient_agent(
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=1,
        recovery_time=45
    )

    # Sequential execution of validation and fixing
    await execute(WebValidator,
                  "Validate app.py and all templates/*.html with syntax, runtime, routing, UI element presence, navigation, and data integration. "
                  "Write detailed validation_report.md.")

    # Read validation report content to inject into fixer
    validation_report_content = ""
    try:
        with open("validation_report.md", "r") as f:
            validation_report_content = f.read()
    except FileNotFoundError:
        validation_report_content = ""

    await execute(SequentialFixer,
                  "Apply all corrections in validation_report.md to app.py and templates/*.html. "
                  "Produce corrected final app.py and templates/*.html."

                  f"\n=== Validation Report ===\n{validation_report_content}")
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