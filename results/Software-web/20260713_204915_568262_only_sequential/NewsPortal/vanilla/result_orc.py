# Phase1_Start
async def design_specification_phase():
    # Create agents RequirementsAnalyst and WebArchitect
    RequirementsAnalyst = build_resilient_agent(
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=3,
        timeout_threshold=400,
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
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential execution flow
    # Step 1: RequirementsAnalyst creates requirements_analysis.md from user_task_description
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and produce requirements_analysis.md tracing all pages, routes, element IDs, data file formats with example data, navigation flows, bookmarks, comments, trending features.")

    # Step 2: WebArchitect creates design_spec.md using user_task_description and requirements_analysis.md
    # Read requirements_analysis.md content for injection
    req_analysis_content = ""
    try:
        req_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    user_task_desc = ""
    entries = CONTEXT.get("user_task_description", [])
    if entries:
        user_task_desc = entries[-1]["content"]

    await execute(WebArchitect,
                  f"Read user_task_description and requirements_analysis.md to produce design_spec.md with complete Flask routes (paths, methods, function names), exact page titles, element IDs per page, data file parsing contracts with field orders and examples, and UI navigation mappings.\n\n=== requirements_analysis.md ===\n{req_analysis_content}\n\n=== user_task_description ===\n{user_task_desc}")
# Phase1_End

# Phase2_Start
async def implementation_phase():
    # Create agents with parameters for Phase 2
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
    TemplateDesigner = build_resilient_agent(
        agent_name="TemplateDesigner",
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

    # Read input artifact content for injection
    design_spec_content = ""
    app_py_content = ""
    templates_content = ""
    try:
        design_spec_content = open("design_spec.md").read()
    except Exception:
        pass
    try:
        app_py_content = open("app.py").read()
    except Exception:
        pass
    try:
        # For templates/*.html, assume merged or empty string for injection
        import glob
        templates_files = glob.glob("templates/*.html")
        all_templates_content = []
        for file_path in templates_files:
            try:
                content = open(file_path).read()
                all_templates_content.append(f"=== {file_path} ===\n{content}\n")
            except Exception:
                pass
        templates_content = "\n".join(all_templates_content)
    except Exception:
        pass

    # Sequential execution based on Sequential Flow
    # 1. ImplementationEngineer creates app.py
    # 2. TemplateDesigner creates templates/*.html
    # 3. IntegrationEngineer integrates and finalizes app.py and templates/*.html

    await execute(ImplementationEngineer,
                  "Implement complete app.py with all Flask routes and logic strictly following design_spec.md. "
                  "Use design_spec.md content for reference.\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}")

    await execute(TemplateDesigner,
                  "Implement all HTML templates (*.html) with exact element IDs and content structure per design_spec.md.\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}")

    await execute(IntegrationEngineer,
                  "Integrate app.py and templates/*.html files, removing any draft or placeholder references. "
                  "Ensure render_template calls and navigation buttons/links use correct routes and file names. "
                  "Validate data loading and context variable consistency with design_spec.md.\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n"
                  f"=== templates/*.html ===\n{templates_content}")
# Phase2_End

# Phase3_Start
async def verification_phase():
    # Build WebValidator agent
    WebValidator = build_resilient_agent(
        agent_name="WebValidator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=45
    )

    # Build SequentialFixer agent
    SequentialFixer = build_resilient_agent(
        agent_name="SequentialFixer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=480,
        failure_threshold=2,
        recovery_time=45
    )

    # Read files for injection
    design_spec_md = ""
    app_py = ""
    templates_html = ""
    validation_report_md = ""

    try:
        design_spec_md = open("design_spec.md").read()
    except:
        pass

    try:
        app_py = open("app.py").read()
    except:
        pass

    import glob
    try:
        template_files = glob.glob("templates/*.html")
        templates_list = []
        for tpl_file in template_files:
            try:
                content = open(tpl_file).read()
                templates_list.append(f"=== {tpl_file} ===\n{content}\n")
            except:
                templates_list.append(f"=== {tpl_file} ===\n[Unable to read]\n")
        templates_html = "\n".join(templates_list)
    except:
        pass

    # Step 1: WebValidator runs full Flask app validation
    await execute(WebValidator,
                  f"Validate the Flask app as per specifications.\n"
                  f"=== design_spec.md ===\n{design_spec_md}\n\n"
                  f"=== app.py ===\n{app_py}\n\n"
                  f"=== templates/*.html ===\n{templates_html}\n\n"
                  "Use validate_python_file on app.py, execute key Flask routes with execute_python_code, check routes, templates, element IDs, navigation, and data loading.\n"
                  "Output validation_report.md.")

    # Read validation_report.md to inject into SequentialFixer
    try:
        validation_report_md = open("validation_report.md").read()
    except:
        pass

    # Step 2: SequentialFixer applies all fixes based on validation_report.md
    await execute(SequentialFixer,
                  f"Apply all fixes as detailed in validation_report.md to app.py and templates/*.html.\n"
                  f"=== design_spec.md ===\n{design_spec_md}\n\n"
                  f"=== app.py ===\n{app_py}\n\n"
                  f"=== templates/*.html ===\n{templates_html}\n\n"
                  f"=== validation_report.md ===\n{validation_report_md}\n\n"
                  "Produce corrected app.py and templates/*.html.")
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