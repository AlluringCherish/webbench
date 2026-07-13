# Phase1_Start
async def design_specification_phase():
    RequirementsAnalyst = build_resilient_agent(
        agent_name="RequirementsAnalyst",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=200,
        failure_threshold=1,
        recovery_time=30
    )
    SystemArchitect = build_resilient_agent(
        agent_name="SystemArchitect",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=240,
        failure_threshold=1,
        recovery_time=30
    )

    # Sequential flow execution
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and create requirements_analysis.md containing all page designs, element IDs, navigation flows, and data file specifications.")

    # Read requirements_analysis.md content for SystemArchitect input
    requirements_analysis_md = ""
    try:
        requirements_analysis_md = open("requirements_analysis.md").read()
    except:
        pass

    await execute(SystemArchitect,
                  f"Using user_task_description and the following requirements_analysis.md content, create design_spec.md specifying Flask routes with function names, HTTP methods, templates, context variables; HTML templates with exact page titles and element IDs; navigation flows; and data file schemas.\n\n=== requirements_analysis.md ===\n{requirements_analysis_md}")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    Developer = build_resilient_agent(
        agent_name="Developer",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    TemplateDesigner = build_resilient_agent(
        agent_name="TemplateDesigner",
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
        max_retries=2,
        timeout_threshold=480,
        failure_threshold=1,
        recovery_time=50
    )

    # Sequential Flow execution:
    # 1. Developer implements backend app_draft.py
    await execute(Developer, "Implement all backend Flask routes and logic for VirtualMuseum in app_draft.py based on design_spec.md and user_task_description. Focus on backend logic only, no templates.")
    
    # 2. TemplateDesigner creates draft HTML templates in templates_draft/
    await execute(TemplateDesigner, "Create draft HTML templates for VirtualMuseum in templates_draft/ directory with exact element IDs, page titles, buttons, and navigation based on design_spec.md and user_task_description. No backend logic.")
    
    # 3. IntegrationEngineer integrates app_draft.py and templates_draft/*.html into final app.py and templates/*.html fully consistent with design_spec.md and user_task_description
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except:
        pass
    # Since templates_draft/*.html is multiple files, read all files matching pattern 'templates_draft/*.html'
    import glob
    import os

    templates_draft_all_content = {}
    for filepath in glob.glob("templates_draft/*.html"):
        try:
            with open(filepath, "r") as f:
                templates_draft_all_content[os.path.basename(filepath)] = f.read()
        except:
            templates_draft_all_content[os.path.basename(filepath)] = ""

    # Compose message for IntegrationEngineer including app_draft.py and all templates draft content
    templates_draft_combined = "\n\n".join([f"=== {filename} ===\n{content}" for filename, content in templates_draft_all_content.items()])

    msg_integration = (
        "Integrate backend app_draft.py and HTML templates drafts into final app.py and templates/*.html ensuring exact element IDs, page titles, buttons, navigation, and matching design_spec.md.\n\n"
        "=== app_draft.py ===\n" + app_draft_content + "\n\n"
        + templates_draft_combined
    )
    await execute(IntegrationEngineer, msg_integration)
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

    # Read file artifacts for injection
    app_py_content, templates_content, design_spec_content, user_task_desc = "", "", "", ""
    try:
        app_py_content = open("app.py").read()
    except:
        pass
    try:
        # Concatenate all templates/*.html files content for injection
        import glob
        templates_files = glob.glob("templates/*.html")
        templates_content = ""
        for tf in templates_files:
            try:
                content = open(tf).read()
                templates_content += f"=== {tf} ===\n{content}\n\n"
            except:
                continue
    except:
        pass
    try:
        design_spec_content = open("design_spec.md").read()
    except:
        pass
    try:
        user_task_desc = CONTEXT.get("user_task_description", [])
        user_task_desc = user_task_desc[-1]["content"] if user_task_desc else ""
    except:
        pass

    # Step 1: WebValidator validates runtime correctness and UI compliance
    msg_validator = (
        "Validate app.py and templates/*.html for syntax, runtime correctness, Flask routing behavior, and "
        "UI compliance strictly against design_spec.md and user_task_description. Output a comprehensive "
        "validation_report.md detailing all backend and frontend issues found."
        f"\n\n=== app.py ===\n{app_py_content}\n"
        f"=== templates/*.html ===\n{templates_content}"
        f"=== design_spec.md ===\n{design_spec_content}\n"
        f"=== user_task_description ===\n{user_task_desc}"
    )
    await execute(WebValidator, msg_validator)

    # Step 2: FinalFixer reads validation_report.md and original sources, applies fixes accordingly
    validation_report_content = ""
    try:
        validation_report_content = open("validation_report.md").read()
    except:
        pass

    msg_finalfixer = (
        "Read validation_report.md below and apply all corrections to produce a fully compliant, corrected app.py "
        "and templates/*.html files according to design_spec.md and user_task_description. Do not add any "
        "features beyond the reported issues.\n\n"
        "=== validation_report.md ===\n"
        f"{validation_report_content}\n\n"
        "=== original app.py ===\n"
        f"{app_py_content}\n\n"
        "=== original templates/*.html ===\n"
        f"{templates_content}\n\n"
        "=== design_spec.md ===\n"
        f"{design_spec_content}\n\n"
        "=== user_task_description ===\n"
        f"{user_task_desc}"
    )
    await execute(FinalFixer, msg_finalfixer)
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