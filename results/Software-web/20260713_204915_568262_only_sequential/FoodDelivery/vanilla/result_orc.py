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

    # Sequential execution according to Sequential Flow pattern
    await execute(RequirementsAnalyst,
                  "Extract all pages, routes, page titles, element IDs, interaction flows, and data file references "
                  "from user_task_description. Save detailed requirements_analysis.md.")
    # Read requirements_analysis.md content to inject in next agent
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except Exception:
        requirements_analysis_content = ""

    # Pass requirements_analysis.md and user_task_description to WebArchitect
    user_task_description = ""
    entries = CONTEXT.get("user_task_description", [])
    if entries:
        user_task_description = entries[-1]["content"]

    await execute(WebArchitect,
                  f"Read requirements_analysis.md and user_task_description.\n"
                  f"Produce detailed design_spec.md defining Flask routes, HTTP methods, templates, element IDs, buttons, inputs, "
                  f"data file formats, and navigation flows.\n\n"
                  f"=== requirements_analysis.md ===\n{requirements_analysis_content}\n\n"
                  f"=== user_task_description ===\n{user_task_description}")
# Phase1_End

# Phase2_Start
async def implementation_phase():
    DraftEngineer = build_resilient_agent(
        agent_name="DraftEngineer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
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
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=45
    )

    # Sequential execution
    # Step 1: DraftEngineer writes app_draft.py and templates_draft/*.html
    await execute(DraftEngineer,
                  "Read design_spec.md and user_task_description. "
                  "Write a complete draft Flask app (app_draft.py) covering all pages and UI elements, "
                  "reading local text files as specified. "
                  "Create draft HTML templates in templates_draft/ with all required element IDs and UI components.")
    
    # Read drafts for injection
    app_draft_code, templates_draft = "", ""
    try:
        app_draft_code = open("app_draft.py").read()
    except:
        pass
    try:
        # Since templates_draft/*.html can be multiple files, read all files in templates_draft/ folder content if available
        import glob
        paths = glob.glob("templates_draft/*.html")
        contents = []
        for p in paths:
            try:
                contents.append(f"=== {p} ===\n" + open(p).read())
            except:
                pass
        templates_draft = "\n\n".join(contents)
    except:
        pass

    # Step 2: IntegrationEngineer creates final app.py and templates/*.html using drafts
    await execute(IntegrationEngineer,
                  f"Refine and integrate drafts into final app.py and templates/*.html. "
                  f"Use app_draft.py and all templates_draft/*.html content below, along with design_spec.md and user_task_description. "
                  f"Fix all gaps, enforce correct routes, element IDs, data handling, and final polish.\n\n"
                  f"=== app_draft.py ===\n{app_draft_code}\n\n"
                  f"=== templates_draft ===\n{templates_draft}")
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

    # Sequential Flow: WebValidator then SequentialFixer
    await execute(
        WebValidator,
        (
            "Comprehensively validate app.py and templates/*.html for Flask syntax, runtime, route coverage, "
            "template element IDs and data bindings using design_spec.md and user_task_description. "
            "Generate detailed validation_report.md."
        )
    )

    # Read validation_report.md to pass content for context if needed (optional here, just execute directly)
    report_content = ""
    try:
        report_content = open("validation_report.md").read()
    except Exception:
        pass

    await execute(
        SequentialFixer,
        (
            "Apply all corrections described in validation_report.md to app.py and templates/*.html "
            "to produce final compliant files fully meeting design_spec.md and user requirements. "
            "Use the following validation report for detailed fixes:\n"
            f"=== validation_report.md ===\n{report_content}"
        )
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