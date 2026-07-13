# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the complete design specification and UI contract for the VirtualMuseum Python web application including all pages, element IDs, navigation flows, and data storage, producing design_spec.md and gated design_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "DesignGenerator produces design_spec.md detailing all required pages (Dashboard, Artifact Catalog, Exhibitions, Exhibition Details, Visitor Tickets, Virtual Events, Audio Guides), UI elements with IDs, navigation button mappings, and data file formats; "
        "DesignCritic reviews design_spec.md for completeness, clarity, and consistency writing design_feedback.md starting with [APPROVED] or NEED_MODIFY for revision; "
        "This refinement loop runs at most two iterations."
    ),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Author comprehensive design_spec.md document detailing page layouts, exact element IDs, navigation scheme, and data file formats for VirtualMuseum web app from user_task_description and design_feedback.md",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"},
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}],
        },
        {
            "agent_name": "DesignCritic",
            "role": "Review design_spec.md for clarity, completeness, alignment to requirements, and consistency; produce design_feedback.md starting with [APPROVED] or NEED_MODIFY",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_feedback.md"}],
        },
    ],
    review_policy: list = [
        {
            "source_agent": "DesignGenerator",
            "reviewer_agent": "DesignCritic",
            "review_criteria": "Check for completeness of all pages, element IDs, navigation accuracy, adherence to data format specifications, and clarity of design_spec.md; ensure no requirements are omitted or inconsistent.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}],
        }
    ],
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Develop and refine the full backend and frontend implementation of VirtualMuseum Python web app including app.py and templates/*.html from design_spec.md and address code_feedback.md to final approved quality",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "AppGenerator writes or revises app.py and templates/*.html implementing all specified pages, elements, navigation, data loading/saving from local text files in 'data' directory as defined in design_spec.md; "
        "CodeCritic reviews code bundle for functional completeness, conformance to design_spec.md, syntax, runtime validation, and UI correctness producing code_feedback.md starting with [APPROVED] or NEED_MODIFY; "
        "The refinement loop runs at most two iterations."
    ),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Implement or revise app.py and templates/*.html combining frontend UI elements and backend Python logic for VirtualMuseum platform ensuring data persistence via local text files, guided by design_spec.md and code_feedback.md",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"},
                {"type": "text_file", "name": "code_feedback.md", "source": "CodeCritic"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
            ],
        },
        {
            "agent_name": "CodeCritic",
            "role": "Review app.py and templates/*.html for technical correctness, adherence to design_spec.md, data file handling logic, UI correctness including exact element IDs and navigation, and validate code syntax and runtime; produce code_feedback.md starting with [APPROVED] or NEED_MODIFY",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"},
            ],
            "output_artifacts": [{"type": "text_file", "name": "code_feedback.md"}],
        },
    ],
    review_policy: list = [
        {
            "source_agent": "AppGenerator",
            "reviewer_agent": "CodeCritic",
            "review_criteria": "Verify code conformance to design_spec.md, correctness of data file interactions, completeness of all pages and UI elements with specified IDs, and successful syntax/runtime validation.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
            ],
        }
    ],
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the complete Python VirtualMuseum web application with dashboard start page, seven defined pages, exact element IDs, local text file data storage, and robust functionality as specified",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the full design specification and UI contract for VirtualMuseum including pages, elements, navigation, and data formats.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Adaptive design refinement and contract specification for VirtualMuseum web app.",
                }
            ],
        },
        {
            "step": 2,
            "description": "Develop and refine implementation including app.py and templates/*.html from design_spec.md until approved.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Adaptive backend and frontend implementation refinement for VirtualMuseum.",
                }
            ],
        },
    ],
): pass
# Orchestrate_End