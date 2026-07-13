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
        timeout_threshold=280,
        failure_threshold=1,
        recovery_time=40
    )

    # Sequential Flow
    # Step 1: RequirementsAnalyst produces requirements_analysis.md
    await execute(RequirementsAnalyst,
                  "Extract and document all user requirements from user_task_description. Save detailed requirements_analysis.md.")
    # Read requirements_analysis.md content for WebArchitect
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    # Step 2: WebArchitect reads requirements_analysis.md and produces design_spec.md
    await execute(WebArchitect,
                  f"Read the following requirements_analysis.md content carefully and produce design_spec.md with detailed page definitions, element IDs, navigation mappings, data file schemas, and programmatic constraints.\n\n=== requirements_analysis.md ===\n{requirements_analysis_content}")
# Phase1_End

# Phase2_Start
async def implementation_phase():
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
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=45
    )

    # Execute ImplementationEngineer to create app_draft.py and templates_draft/*.html from design_spec.md
    await execute(ImplementationEngineer,
                  "Create app_draft.py implementing Flask backend routes and request handling per design_spec.md. "
                  "Also create complete templates_draft/*.html for all 9 pages with exact element IDs and UI components. "
                  "Save outputs to app_draft.py and templates_draft/*.html.")

    # Read draft files to inject content for IntegrationEngineer
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    try:
        import os
        templates_draft_files = [f for f in os.listdir("templates_draft") if f.endswith(".html")]
        templates_draft_content = ""
        for fname in templates_draft_files:
            try:
                templates_draft_content += f"=== {fname} ===\n" + open(f"templates_draft/{fname}").read() + "\n\n"
            except:
                pass
    except:
        pass

    # Execute IntegrationEngineer to produce final app.py and templates/*.html from drafts and design_spec.md
    await execute(IntegrationEngineer,
                  f"Use app_draft.py and templates_draft/*.html below along with full design_spec.md to produce finalized app.py "
                  f"and templates/*.html with exact routing, functional requirements, and data file handling.\n\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n\n"
                  f"=== templates_draft ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start
async def verification_phase():
    # Declare agents
    QualityAssurer = build_resilient_agent(
        agent_name="QualityAssurer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase3"],
        max_retries=3,
        timeout_threshold=400,
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
        timeout_threshold=450,
        failure_threshold=1,
        recovery_time=45
    )

    # Read input artifacts content for QualityAssurer
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
    # Note: For templates/*.html, aggregate contents of all template files into a single string
    import glob
    try:
        template_files = glob.glob("templates/*.html")
        templates_agg = []
        for tf in template_files:
            try:
                content = open(tf).read()
                templates_agg.append(f"=== {tf} ===\n{content}\n")
            except Exception:
                continue
        templates_content = "\n".join(templates_agg)
    except Exception:
        templates_content = ""

    # Execute QualityAssurer with core instructions
    await execute(QualityAssurer,
                  "Validate CarRental Flask backend app.py and frontend templates/*.html against design_spec.md. "
                  "Use validate_python_file tool on app.py for syntax/runtime checking and execute_python_code tool for runtime tests. "
                  "Check all Flask routes, element IDs, page titles, data bindings, navigation correctness, and coverage. "
                  "Write detailed validation_report.md describing all issues and verification results. "
                  "Input contents:\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n"
                  f"=== app.py ===\n{app_py_content}\n"
                  f"=== templates/*.html ===\n{templates_content}")

    # After QualityAssurer completes, SequentialFixer runs to fix issues
    # Read validation_report.md content for SequentialFixer injection
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except Exception:
        pass

    await execute(SequentialFixer,
                  "Apply all necessary fixes to finalize app.py and templates/*.html ensuring compliance with design_spec.md and all validation criteria. "
                  "Read validation_report.md below and design_spec.md, app.py, templates/*.html to identify and address all reported issues. "
                  "Output final corrected app.py and templates/*.html files.\n"
                  f"=== validation_report.md ===\n{validation_report_content}\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n"
                  f"=== app.py ===\n{app_py_content}\n"
                  f"=== templates/*.html ===\n{templates_content}")
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