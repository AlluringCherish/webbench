# Phase1_Start
async def design_specification_phase():
    RequirementsAnalyst = build_resilient_agent(
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=300,
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
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution: RequirementsAnalyst first, then WebArchitect
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce requirements_analysis.md "
                  "capturing all pages, UI elements (IDs and types), data file formats, and user flows.")

    # Read generated requirements_analysis.md content for WebArchitect input injection
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    await execute(WebArchitect,
                  f"Read user_task_description and the following requirements_analysis.md:\n{requirements_analysis_content}\n"
                  "Create design_spec.md with detailed Flask routes, page-template mappings, UI elements, navigation, and data schemas.")
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
        recovery_time=45
    )

    # Sequential execution: DraftEngineer then IntegrationEngineer

    # Step 1: DraftEngineer creates app_draft.py and templates_draft/*.html from design_spec.md
    await execute(DraftEngineer,
                  "Implement complete app_draft.py with all Flask routes and local file I/O, and all templates_draft/*.html "
                  "with exact UI element IDs and Jinja2 templating based on design_spec.md and user_task_description")

    # Reading draft outputs for IntegrationEngineer input injection
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except Exception:
        pass
    try:
        # For templates_draft/*.html, concatenate all files contents or leave empty if none
        import glob
        drafts = glob.glob("templates_draft/*.html")
        templates_draft_content = ""
        for file_path in drafts:
            try:
                with open(file_path, "r") as f:
                    templates_draft_content += f"=== {file_path} ===\n" + f.read() + "\n\n"
            except Exception:
                continue
    except Exception:
        pass

    # Step 2: IntegrationEngineer refines draft app and templates into final app.py and templates/*.html
    await execute(
        IntegrationEngineer,
        f"Read user_task_description, design_spec.md, app_draft.py, and templates_draft/*.html fully. "
        f"Fix all runtime path issues, set correct template folders, refine app_draft.py and templates_draft into final app.py and templates/*.html. "
        f"Maintain exact UI element IDs, routes, and data file access.\n\n"
        f"=== app_draft.py ===\n{app_draft_content}\n\n"
        f"=== templates_draft ===\n{templates_draft_content}"
    )
# Phase2_End

# Phase3_Start
async def verification_phase():
    # Create agents
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
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Sequential Flow: WebValidator then SequentialFixer
    await execute(
        WebValidator,
        "Validate app.py and all templates/*.html for syntax correctness, runtime behavior, full coverage of design specifications and user requirements. "
        "Write detailed validation_report.md listing all issues with precise fix instructions."
    )

    # Read the validation report content for injection
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except Exception:
        validation_report_content = ""

    await execute(
        SequentialFixer,
        f"Apply all corrections needed based on the following validation_report.md content. "
        f"Fix app.py and templates/*.html exactly accordingly while preserving existing correct functionality.\n\n"
        f"=== validation_report.md ===\n{validation_report_content}"
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