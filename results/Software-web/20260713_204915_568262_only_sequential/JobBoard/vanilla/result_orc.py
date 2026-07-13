# Phase1_Start
async def design_specification_phase():
    # Declare agents
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
        timeout_threshold=320,
        failure_threshold=1,
        recovery_time=40
    )

    # Execute RequirementsAnalyst first
    await execute(RequirementsAnalyst,
                  "Analyze user_task_description and create requirements_analysis.md detailing pages, titles, UI element IDs, navigation, and data storage requirements")

    # Read requirements_analysis.md content for WebArchitect
    requirements_analysis_content = ""
    try:
        requirements_analysis_content = open("requirements_analysis.md").read()
    except:
        pass

    # Execute WebArchitect after RequirementsAnalyst output is ready
    await execute(WebArchitect,
                  f"Convert requirements_analysis.md to design_spec.md with finalized pages, Flask routes, templates, UI element IDs, navigation flow, and data file schemas.\n\n"
                  f"=== requirements_analysis.md ===\n{requirements_analysis_content}\n\n"
                  f"Also use user_task_description for reference.")
# Phase1_End

# Phase2_Start
import asyncio

async def implementation_phase():
    # Create agents
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
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=50
    )

    # Read draft files for injection before integration
    app_draft_content, templates_draft_content = "", ""
    try:
        app_draft_content = open("app_draft.py").read()
    except Exception:
        app_draft_content = ""
    try:
        # Since templates_draft/*.html could be multiple files,
        # read all and concatenate for injection
        import glob
        paths = glob.glob("templates_draft/*.html")
        templates_contents = []
        for path in paths:
            try:
                templates_contents.append(f"=== {path} ===\n" + open(path).read())
            except Exception:
                continue
        templates_draft_content = "\n\n".join(templates_contents)
    except Exception:
        templates_draft_content = ""

    # Execute DraftEngineer to produce app_draft.py & templates_draft/*.html
    await execute(DraftEngineer,
                  "Create app_draft.py and all HTML templates in templates_draft/ implementing all routes, UI IDs, navigation, and data handling as draft.")

    # After drafts produced, execute IntegrationEngineer injecting draft files content for refinement
    await execute(IntegrationEngineer,
                  f"Integrate and refine app_draft.py and templates_draft/*.html into final app.py and templates/*.html. "
                  f"Ensure full compliance with design_spec.md and user requirements.\n\n"
                  f"=== app_draft.py ===\n{app_draft_content}\n\n=== templates_draft_files ===\n{templates_draft_content}")
# Phase2_End

# Phase3_Start
async def verification_phase():
    # Declare agents
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

    # Read templates content for injection
    templates_content = ""
    import glob
    import os

    # Gather all templates/*.html content
    try:
        template_files = glob.glob("templates/*.html")
    except:
        template_files = []

    for tf in template_files:
        try:
            content = open(tf).read()
            templates_content += f"=== {os.path.basename(tf)} ===\n{content}\n\n"
        except:
            pass

    # Execute WebValidator
    await execute(WebValidator,
                  f"Validate the integrated Flask app.py, templates, design_spec.md, and user task. "
                  f"Validate Python syntax in app.py using validate_python_file tool. "
                  f"Check routes, UI element IDs including dynamic ones, data handling, and navigation correctness. "
                  f"Focus on inputs: app.py, templates/*.html, design_spec.md, user_task_description.\n\n"
                  f"=== app.py content ===\n"
                  f"{CONTEXT.get('app.py', [{'content': ''}])[-1]['content'] if CONTEXT.get('app.py') else ''}\n\n"
                  f"=== Templates content ===\n{templates_content}\n"
                  f"=== design_spec.md content ===\n"
                  f"{CONTEXT.get('design_spec.md', [{'content': ''}])[-1]['content'] if CONTEXT.get('design_spec.md') else ''}\n"
                  f"User task description:\n"
                  f"{CONTEXT.get('user_task_description', [{'content': ''}])[-1]['content'] if CONTEXT.get('user_task_description') else ''}"
                  )

    # Read validation_report.md from file for injection
    validation_report = ""
    try:
        validation_report = open("validation_report.md").read()
    except:
        pass

    # Read app.py content from file for injection
    app_py_content = ""
    try:
        app_py_content = open("app.py").read()
    except:
        pass

    # Re-gather templates content for SequentialFixer (may be updated or unchanged)
    templates_content_for_fixer = ""
    for tf in template_files:
        try:
            content = open(tf).read()
            templates_content_for_fixer += f"=== {os.path.basename(tf)} ===\n{content}\n\n"
        except:
            pass

    # Read design_spec.md content
    design_spec_content = CONTEXT.get("design_spec.md", [{'content': ''}])[-1]['content'] if CONTEXT.get("design_spec.md") else ""

    # Read user_task_description
    user_task_desc = CONTEXT.get("user_task_description", [{'content': ''}])[-1]['content'] if CONTEXT.get("user_task_description") else ""

    # Execute SequentialFixer with injected inputs and validation report
    await execute(SequentialFixer,
                  f"Fix all issues reported in validation_report.md to produce final production-ready app.py and templates.\n\n"
                  f"=== Validation Report ===\n{validation_report}\n\n"
                  f"=== app.py ===\n{app_py_content}\n\n"
                  f"=== Templates ===\n{templates_content_for_fixer}\n\n"
                  f"=== design_spec.md ===\n{design_spec_content}\n\n"
                  f"User task description:\n{user_task_desc}")
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