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

    # Sequential execution: RequirementsAnalyst then WebArchitect

    # Step 1: RequirementsAnalyst analyzes user_task_description and outputs requirements_analysis.md
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description for MusicStreaming app and write comprehensive requirements_analysis.md including pages, UI elements with exact IDs, navigation flows starting at Dashboard, and data storage formats.")

    # Step 2: Read requirements_analysis.md content to pass to WebArchitect
    requirements_content = ""
    try:
        requirements_content = open("requirements_analysis.md").read()
    except Exception:
        requirements_content = ""

    # Step 3: WebArchitect reads user_task_description and requirements_analysis.md and writes design_spec.md
    await execute(WebArchitect,
                  f"Read user_task_description and requirements_analysis.md to create detailed design_spec.md specifying Flask routes, page titles, element IDs, navigation from Dashboard, and pipe-delimited data file contracts.\n\n"
                  f"=== requirements_analysis.md ===\n{requirements_content}\n")
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

    # Sequential execution for Sequential Flow pattern
    # 1. ImplementationEngineer produces drafts: app_draft.py and templates_draft/*.html
    await execute(ImplementationEngineer,
                  "Develop draft app_draft.py implementing all Flask routes and logic from design_spec.md for MusicStreaming app. "
                  "Create draft HTML templates in templates_draft/ with exact IDs and elements per design_spec.md.")

    # Read draft outputs for IntegrationEngineer
    app_draft_code, templates_draft_content = "", ""
    try:
        app_draft_code = open("app_draft.py").read()
    except Exception:
        pass
    try:
        import glob
        draft_files = glob.glob("templates_draft/*.html")
        templates_draft_content = ""
        for fpath in draft_files:
            try:
                templates_draft_content += f"=== {fpath} ===\n" + open(fpath).read() + "\n\n"
            except Exception:
                pass
    except Exception:
        pass

    # 2. IntegrationEngineer merges drafts and refines into final app.py and templates/*.html
    await execute(IntegrationEngineer,
                  f"Integrate and finalize app_draft.py and templates_draft/*.html into runnable app.py and templates/*.html as per design_spec.md. "
                  f"Ensure stable routes, proper navigation, and correct local data access.\n\n"
                  f"=== app_draft.py ===\n"
                  f"{app_draft_code}\n\n"
                  f"=== templates_draft/*.html ===\n"
                  f"{templates_draft_content}")
# Phase2_End

# Phase3_Start
async def verification_phase():
    # Create agents
    ValidationEngineer = build_resilient_agent(
        agent_name="ValidationEngineer",
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

    # Sequential execution
    await execute(ValidationEngineer,
                  "Validate app.py and all templates/*.html thoroughly using validate_python_file and execute_python_code tools. "
                  "Verify routes, UI elements, data interaction against design_spec.md and user_task_description. "
                  "Output detailed validation_report.md with all issues.")

    # Read validation_report.md content to inject into SequentialFixer
    validation_report_content = ""
    try:
        with open("validation_report.md", "r", encoding="utf-8") as f:
            validation_report_content = f.read()
    except Exception:
        pass

    # Correction by SequentialFixer based on validation_report.md
    await execute(SequentialFixer,
                  f"Apply all fixes listed in validation_report.md to app.py and templates/*.html to fully comply with design_spec.md and user requirements. "
                  "Preserve existing functionality and project structure. Output corrected app.py and templates/*.html.\n"
                  f"=== validation_report.md ===\n{validation_report_content}")
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