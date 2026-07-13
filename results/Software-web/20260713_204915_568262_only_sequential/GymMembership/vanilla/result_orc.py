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
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential Flow
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce requirements_analysis.md detailing GymMembership pages, UI elements with exact IDs, navigation flows, and data file specifications.")

    # Read requirements_analysis.md content for WebArchitect input
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    await execute(WebArchitect,
                  f"Using requirements_analysis.md content and user_task_description, produce design_spec.md with Flask routes, templates, element IDs, navigation mappings, data file formats, and context variable contracts.\n\n"
                  f"=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start
async def implementation_phase():
    DraftEngineer = build_resilient_agent(
        agent_name="DraftEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=300,
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
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=50
    )

    # Sequential execution: DraftEngineer then IntegrationEngineer

    # DraftEngineer creates app_draft.py and templates_draft/*.html based on design_spec.md
    await execute(DraftEngineer,
                  "Implement app_draft.py and all templates in templates_draft/ strictly following design_spec.md. "
                  "Include exact routes, element IDs, page titles, and local data file handling. "
                  "Ensure root route '/' redirects or serves Dashboard page.")

    # Read outputs for IntegrationEngineer injection
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    # Note: For multiple draft templates, read all and concatenate with separators
    import glob
    try:
        template_files = glob.glob("templates_draft/*.html")
        templates_draft_content = ""
        for filepath in template_files:
            with open(filepath, "r") as f:
                templates_draft_content += f"=== {filepath} ===\n{f.read()}\n\n"
    except:
        pass

    # IntegrationEngineer refines draft into final app.py and templates/*.html
    await execute(IntegrationEngineer,
                  f"Refine and polish app_draft.py and templates_draft/*.html into final app.py and templates/*.html fully compliant with design_spec.md. "
                  f"Remove draft artifacts and placeholders. Maintain exact route names and UI elements.\n\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n\n"
                  f"{templates_draft_content}")
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
        failure_threshold=2,
        recovery_time=45
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
        recovery_time=45
    )

    # Sequential execution
    # Step 1: WebValidator validates code and templates producing validation_report.md
    await execute(WebValidator,
                  "Validate app.py using validate_python_file and execute_python_code tools for syntax and runtime errors. "
                  "Verify all Flask routes from design_spec.md exist and respond correctly, including root route redirect. "
                  "Parse all templates/*.html to check presence of all required element IDs, page titles and navigation elements. "
                  "Write detailed validation_report.md describing all found issues and suggestions.")

    # Step 2: SequentialFixer fixes all issues from validation_report.md, updating app.py and templates/*.html
    # Read validation_report.md content for injection
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except:
        pass

    await execute(SequentialFixer,
                  f"Analyze validation_report.md and fix all reported issues in app.py and templates/*.html. "
                  f"Ensure full compliance with design_spec.md and user requirements, including routing, UI elements, and data file access.\n\n"
                  f"=== Validation Report ===\n{validation_report_content}")
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