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
        timeout_threshold=220,
        failure_threshold=1,
        recovery_time=30
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
    # Step 1: RequirementsAnalyst produces requirements_analysis.md
    await execute(RequirementsAnalyst, "Analyze user task description and produce comprehensive requirements_analysis.md covering all pages, element IDs, navigation buttons, user flows, and data storage formats.")

    # Read requirements_analysis.md file content for WebArchitect
    requirements_analysis = ""
    try:
        requirements_analysis = open("requirements_analysis.md").read()
    except:
        pass

    # Step 2: WebArchitect produces design_spec.md based on requirements_analysis.md
    await execute(WebArchitect, f"Based on requirements_analysis.md content below, create design_spec.md specifying Flask routes, templates, element IDs, data file schemas, and user interactions.\n\n=== requirements_analysis.md ===\n{requirements_analysis}")
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
        recovery_time=40
    )

    # DraftEngineer executes first to produce drafts (app_draft.py and templates_draft/*.html)
    await execute(DraftEngineer,
                  "Read design_spec.md and implement app_draft.py and all templates_draft/*.html for OnlineLibrary Flask app. "
                  "Include all routes, data loading from data/*.txt, element IDs exactly as specified.")

    # Read drafts for IntegrationEngineer
    app_draft_content = ""
    templates_draft_content = ""
    try:
        app_draft_content = open("app_draft.py").read()
    except Exception:
        pass
    try:
        import glob
        import os
        drafts = glob.glob("templates_draft/*.html")
        templates_files_content = []
        for file_path in drafts:
            try:
                content = open(file_path).read()
                templates_files_content.append(f"=== {os.path.basename(file_path)} ===\n{content}\n")
            except Exception:
                continue
        templates_draft_content = "\n".join(templates_files_content)
    except Exception:
        pass

    # IntegrationEngineer refines drafts into final app.py and templates/*.html
    await execute(IntegrationEngineer,
                  f"Read design_spec.md for final specifications.\n"
                  f"Integrate drafts from DraftEngineer into final app.py and templates/*.html.\n"
                  f"Remove all draft folder dependencies.\n"
                  f"Ensure routes start with dashboard page and all element IDs, navigation, and data file access conform to design_spec.md.\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n"
                  f"=== templates_draft ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start
import asyncio

async def verification_phase():
    # Create agents
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
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )

    # Read file contents for injection
    design_spec_md = ""
    app_py = ""
    templates_html = ""
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
        templates_content_list = []
        for tf in template_files:
            try:
                content = open(tf).read()
                templates_content_list.append(f"=== {tf} ===\n{content}")
            except:
                pass
        templates_html = "\n\n".join(templates_content_list)
    except:
        templates_html = ""

    # Execute WebValidator
    await execute(WebValidator,
                  f"Read design_spec.md, app.py, templates/*.html for syntax, runtime, and functional validation. "
                  f"Use validate_python_file on app.py. "
                  f"Use execute_python_code for testing routes per design_spec.md. "
                  f"Check templates for HTML/Jinja2 errors. "
                  f"Write detailed validation_report.md summarizing all findings.\n\n"
                  f"=== design_spec.md ===\n{design_spec_md}\n\n=== app.py ===\n{app_py}\n\n=== templates/*.html ===\n{templates_html}")

    # Read validation_report.md content for SequentialFixer injection
    validation_report_md = ""
    try:
        validation_report_md = open("validation_report.md").read()
    except:
        pass

    # Execute SequentialFixer to fix all reported issues
    await execute(SequentialFixer,
                  f"Read validation_report.md, app.py, templates/*.html from CONTEXT. "
                  f"Fix all syntax, runtime and functional issues per report, fully conforming to design_spec.md. "
                  f"Output corrected app.py and templates/*.html files.\n\n"
                  f"=== validation_report.md ===\n{validation_report_md}\n\n"
                  f"=== app.py ===\n{app_py}\n\n=== templates/*.html ===\n{templates_html}")
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