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

    # Sequential execution flow
    # Step 1: RequirementsAnalyst analyzes user_task_description and creates requirements_analysis.md
    await execute(RequirementsAnalyst,
                  "Analyze the full user_task_description and produce detailed requirements_analysis.md including pages, UI elements with exact IDs, navigation flows, functionality behaviors, and data schemas.")

    # Step 2: WebArchitect reads requirements_analysis.md and creates design_spec.md specifying Flask routes, templates, UI elements, navigation and data contracts
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    await execute(WebArchitect,
                  f"Read requirements_analysis.md content below and produce design_spec.md specifying precise Flask routes, HTTP methods, template file structure, UI element IDs, context variables, navigation mappings, and data storage schemas.\n\n=== requirements_analysis.md ===\n{requirements_analysis_content}")
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

    # Sequential execution
    await execute(DraftEngineer, "Read design_spec.md and create initial draft implementations: app_draft.py and templates_draft/*.html with core backend routes, logic, and frontend UI layouts matching all element IDs and page titles exactly. Save drafts with placeholders for incomplete features.")
    
    # Read drafts for integration
    app_draft_code, templates_draft_content = "", ""
    try:
        app_draft_code = open("app_draft.py").read()
    except:
        pass
    try:
        # Assuming multiple draft templates - reading all files content concatenated for context injection
        import glob
        content_list = []
        for filename in glob.glob("templates_draft/*.html"):
            with open(filename, 'r') as f:
                content_list.append(f.read())
        templates_draft_content = "\n\n".join(content_list)
    except:
        pass

    # Inject drafts content for integration
    await execute(IntegrationEngineer,
                  f"Using design_spec.md, app_draft.py, and templates_draft/*.html drafts, create final app.py and templates/*.html with complete route implementations, full functionality, and removal of draft placeholders and paths. Ensure all element IDs and page titles match design_spec.md precisely."
                  f"\n\n=== app_draft.py ===\n{app_draft_code}\n\n=== templates_draft/*.html ===\n{templates_draft_content}")
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

    # Sequential Flow Execution: Validate then fix
    await execute(WebValidator,
                  "Validate app.py using validate_python_file and execute_python_code tools, inspect templates/*.html for required elements, page titles and UI structure, "
                  "perform functional tests including enrollment, assignment submission, course progress update, certificate generation, "
                  "and produce detailed validation_report.md with all findings and suggestions.")

    # Read validation_report.md content for injection
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except Exception:
        pass

    await execute(SequentialFixer,
                  f"Read validation_report.md for issues to fix. Update app.py and all templates/*.html to correct all reported errors, "
                  f"ensure full compliance with design_spec.md, maintain application integrity, and prepare final validated files.\n\n"
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