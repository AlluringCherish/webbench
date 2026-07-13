# Phase1_Start
async def design_specification_phase():
    DesignGenerator = build_resilient_agent(
        agent_name="DesignGenerator",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase1"],
        max_retries=2,
        timeout_threshold=350,
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
        timeout_threshold=300,
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

        # Compose prompt message for DesignGenerator
        if iteration == 0:
            msg = (
                "Create a comprehensive and complete design_spec.md describing the CarRental application architecture, "
                "page designs including element IDs, navigation flows starting from the Dashboard page, and data storage formats. "
                "Use user_task_description from CONTEXT. This is the initial iteration."
            )
        else:
            if feedback_content.startswith("NEED_MODIFY"):
                msg = (
                    "Revise the entire design_spec.md fully based on the following previous design and critic feedback.\n\n"
                    f"=== Previous design_spec.md ===\n{current_design}\n\n"
                    f"=== DesignCritic Feedback ===\n{feedback_content}"
                )
            elif feedback_content.startswith("[APPROVED]"):
                # If approved, no need to change design; preserve content
                msg = (
                    "The design_spec.md was approved with no changes needed. Preserve its content fully."
                )
            else:
                # Unknown or missing feedback, treat as need to revise
                msg = (
                    "Revise design_spec.md based on previous design and any feedback available.\n\n"
                    f"=== Previous design_spec.md ===\n{current_design}\n\n"
                    f"=== DesignCritic Feedback ===\n{feedback_content}"
                )

        await execute(DesignGenerator, msg)

        try:
            current_design = open("design_spec.md").read()
        except FileNotFoundError:
            current_design = ""

        await execute(
            DesignCritic,
            "Critically review the latest design_spec.md for completeness, correctness, and conformance with user_task_description. "
            "Write design_feedback.md starting exactly with [APPROVED] if no issues, or NEED_MODIFY followed by detailed corrections otherwise.\n\n"
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
        recovery_time=45
    )
    CodeCritic = build_resilient_agent(
        agent_name="CodeCritic",
        agent_profiles=AGENT_PROFILES,
        review_profiles=REVIEW_PROFILES,
        context=CONTEXT,
        phase_context=Phase_info["phase2"],
        max_retries=3,
        timeout_threshold=400,
        failure_threshold=2,
        recovery_time=45
    )

    MAX_ITERATIONS = 2
    for iteration in range(MAX_ITERATIONS):
        app_content = ""
        templates_content = ""
        feedback_content = ""

        try:
            app_content = open("app.py").read()
        except FileNotFoundError:
            pass

        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
            except OSError:
                pass

        if iteration > 0:
            try:
                feedback_content = open("code_feedback.md").read()
            except FileNotFoundError:
                pass

        await execute(
            AppGenerator,
            "Create or revise the complete app.py and templates/*.html implementing all nine CarRental pages with required element IDs.\n\n"
            "Design specification and current code are provided.\n"
            "Apply any corrections from the following feedback:\n"
            f"{feedback_content}\n\n"
            f"=== Current app.py ===\n{app_content}\n\n"
            f"=== Current templates/*.html ===\n{templates_content}"
        )

        try:
            app_content = open("app.py").read()
        except FileNotFoundError:
            app_content = ""

        templates_content = ""
        for template_path in sorted(glob.glob("templates/*.html")):
            try:
                templates_content += f"\n=== {template_path} ===\n" + open(template_path).read()
            except OSError:
                pass

        await execute(
            CodeCritic,
            "Review the latest app.py and templates/*.html against design_spec.md for completeness, correctness, and exact element IDs.\n"
            "Confirm all features function as specified, data files are updated properly, and the site starts at the dashboard page without authentication.\n"
            "Provide feedback beginning exactly with [APPROVED] if all requirements are met, else NEED_MODIFY with detailed corrections.\n\n"
            f"=== design_spec.md ===\n{CONTEXT.get('design_spec.md','')}\n\n"
            f"=== Latest app.py ===\n{app_content}\n\n"
            f"=== Latest templates/*.html ===\n{templates_content}"
        )

        try:
            feedback_content = open("code_feedback.md").read()
        except FileNotFoundError:
            feedback_content = ""

        if feedback_content.startswith("[APPROVED]"):
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