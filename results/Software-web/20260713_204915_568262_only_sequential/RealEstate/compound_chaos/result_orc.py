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

    # Sequential execution per Sequential Flow
    # Step 1: RequirementsAnalyst produces requirements_analysis.md
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce requirements_analysis.md detailing all pages, elements, user interactions, navigation flows, and data storage formats exactly as specified.")

    # Step 2: WebArchitect reads requirements_analysis.md and produces design_spec.md
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        requirements_analysis_content = ""
    await execute(WebArchitect,
                  f"Read requirements_analysis.md content and produce design_spec.md with complete Flask routes, page templates, element IDs, navigation routes, and data file contracts matching requirements_analysis.md perfectly.\n\n"
                  f"=== requirements_analysis.md ===\n"
                  f"{requirements_analysis_content}")
# Phase1_End

# Phase2_Start
async def implementation_phase():
    # Create agents
    DraftDeveloper = build_resilient_agent(
        agent_name="DraftDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )
    IntegrationDeveloper = build_resilient_agent(
        agent_name="IntegrationDeveloper",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=2,
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential Flow: DraftDeveloper first, then IntegrationDeveloper

    # Read draft files content for integration step
    app_draft_content = ""
    templates_draft_content = ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    try:
        # For templates_draft/*.html, read content of all files and join for injection
        import glob
        all_templates_draft = ""
        for template_file in glob.glob("templates_draft/*.html"):
            try:
                content = open(template_file).read()
                all_templates_draft += f"\n=== {template_file} ===\n{content}\n"
            except:
                continue
        templates_draft_content = all_templates_draft
    except:
        pass

    await execute(DraftDeveloper,
                  "Implement complete app_draft.py with all Flask routes, handlers, and logic based on design_spec.md. "
                  "Implement all templates_draft/*.html with exact element IDs and page titles. "
                  "Use local text files for data persistence and CRUD operations.")

    await execute(IntegrationDeveloper,
                  f"Refine and unify draft app and templates into final app.py and templates/*.html. "
                  f"Ensure full route consistency starting from Dashboard page, "
                  f"exact element IDs, page titles, and robust data persistence. "
                  f"Remove all draft artifacts and produce runnable final app.\n\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n\n"
                  f"=== Templates Draft ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start
async def verification_phase():
    # Create agents
    AppValidator = build_resilient_agent(
        agent_name="AppValidator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=60
    )
    FinalFixer = build_resilient_agent(
        agent_name="FinalFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Read file artifacts needed for injection
    design_spec_content, app_py_content, templates_content = "", "", ""
    try:
        design_spec_content = open("design_spec.md").read()
    except:
        pass
    try:
        app_py_content = open("app.py").read()
    except:
        pass
    # For templates/*.html, we concatenate all template files' content
    import glob
    import os
    templates_files = glob.glob("templates/*.html")
    templates_content_parts = []
    for tpl_file in templates_files:
        try:
            content = open(tpl_file).read()
            templates_content_parts.append(f"=== {os.path.basename(tpl_file)} ===\n{content}")
        except:
            pass
    templates_content = "\n\n".join(templates_content_parts)

    # Execute AppValidator
    await execute(AppValidator,
                  f"Validate app.py and templates/*.html for syntax, runtime, routes, element IDs, data file operations, and startup behavior. "
                  f"Reference design_spec.md for full specifications.\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n"
                  f"=== templates/*.html ===\n{templates_content}\n\n"
                  "Output detailed validation_report.md with all findings.")

    # Read validation_report.md to inject into FinalFixer
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except:
        pass

    # Execute FinalFixer, injecting the validation report and source files
    await execute(FinalFixer,
                  f"Fix all issues found in validation_report.md and refine app.py and templates/*.html to fully comply with design_spec.md.\n\n"
                  f"=== validation_report.md ===\n{validation_report_content}\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n"
                  f"=== templates/*.html ===\n{templates_content}\n\n"
                  "Output final corrected app.py and templates/*.html.")
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