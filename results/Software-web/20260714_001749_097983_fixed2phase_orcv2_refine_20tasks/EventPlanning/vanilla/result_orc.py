# Phase1_Start
async def design_specification_phase():
    DesignGenerator = build_resilient_agent(
        agent_name="DesignGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=400,
        failure_threshold=1,
        recovery_time=40
    )
    DesignCritic = build_resilient_agent(
        agent_name="DesignCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
        failure_threshold=1,
        recovery_time=40
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        current_design = ""
        feedback_content = ""
        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            pass
        if iteration > 0:
            try:
                feedback_content = open("design_feedback.md").read()
            except FileNotFoundError:
                pass

        await execute(
            DesignGenerator,
            "Create or revise the complete adaptive web design specification for the EventPlanning application including all 8 pages, exact element IDs, navigation flow, and local data file structures.\n\n"
            f"=== Current design_spec.md ===\n{current_design}\n\n"
            f"=== DesignCritic Feedback ===\n{feedback_content}"
        )

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Review the design_spec.md ensuring completeness of pages, element IDs, data storage format, and navigation.\n"
            "Write design_feedback.md beginning exactly with [APPROVED] or NEED_MODIFY.\n\n"
            f"=== Latest design_spec.md ===\n{current_design}"
        )

        try:
            feedback_content = open("design_feedback.md").read()
        except FileNotFoundError:
            feedback_content = ""

        if feedback_content.startswith("[APPROVED]"):
            break
# Phase1_End
# Phase2_Start
import glob
async def implementation_and_verification_phase():
    AppGenerator = build_resilient_agent(
        agent_name="AppGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=450,
        failure_threshold=2,
        recovery_time=60
    )
    CodeCritic = build_resilient_agent(
        agent_name="CodeCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=350,
        failure_threshold=2,
        recovery_time=60
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        app_py_content = ""
        templates_content = ""
        code_feedback_content = ""

        # Read current app.py content
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                app_py_content = f.read()
        except FileNotFoundError:
            pass

        # Read all templates/*.html content combined
        templates_content = ""
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                with open(template_path, "r", encoding="utf-8") as f:
                    templates_content += f"\n=== {template_path} ===\n" + f.read()
            except OSError:
                pass

        # On iteration > 0, read code_feedback.md content
        if iteration > 0:
            try:
                with open("code_feedback.md", "r", encoding="utf-8") as f:
                    code_feedback_content = f.read()
            except FileNotFoundError:
                code_feedback_content = ""

        # Prepare message for AppGenerator
        msg_for_generator = (
            "Create or revise the complete app.py and templates/*.html files for the EventPlanning Python web app.\n\n"
            f"=== design_spec.md from CONTEXT ===\n{CONTEXT.get('design_spec.md', '')}\n\n"
            f"=== Current app.py ===\n{app_py_content}\n\n"
            f"=== Current Templates ===\n{templates_content}\n\n"
            f"=== CodeCritic Feedback ===\n{code_feedback_content}\n\n"
            "If feedback starts with NEED_MODIFY, incorporate all corrections by full rewrite.\n"
            "If first iteration, produce full implementation with exact element IDs, navigation, and file data handling."
        )

        # Execute AppGenerator
        await execute(AppGenerator, msg_for_generator)

        # Re-read outputs after Generator finishes
        try:
            with open("app.py", "r", encoding="utf-8") as f:
                app_py_content = f.read()
        except FileNotFoundError:
            app_py_content = ""

        templates_content = ""
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                with open(template_path, "r", encoding="utf-8") as f:
                    templates_content += f"\n=== {template_path} ===\n" + f.read()
            except OSError:
                pass

        # Prepare message for CodeCritic
        msg_for_critic = (
            "Review the latest app.py and templates for correctness of element IDs, page functionality, local text file operations, "
            "navigation starting from Dashboard, and full compliance with design_spec.md.\n\n"
            f"=== design_spec.md from CONTEXT ===\n{CONTEXT.get('design_spec.md', '')}\n\n"
            f"=== Latest app.py ===\n{app_py_content}\n\n"
            f"=== Latest Templates ===\n{templates_content}"
        )

        # Execute CodeCritic
        await execute(CodeCritic, msg_for_critic)

        # Read latest code_feedback.md content
        try:
            with open("code_feedback.md", "r", encoding="utf-8") as f:
                code_feedback_content = f.read()
        except FileNotFoundError:
            code_feedback_content = ""

        # Stop if approved
        if code_feedback_content.startswith("[APPROVED]"):
            break
# Phase2_End
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
        implementation_and_verification_phase()
    ]

    await asyncio.gather(*step1)
    await asyncio.gather(*step2)

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