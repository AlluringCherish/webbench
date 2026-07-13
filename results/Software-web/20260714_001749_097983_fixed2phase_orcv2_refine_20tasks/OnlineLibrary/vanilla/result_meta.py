# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the comprehensive design specification for the 'OnlineLibrary' Python web application and produce design_spec.md and gated design_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator creates or revises design_spec.md based on user_task_description and prior design_feedback.md; DesignCritic reviews the design_spec.md, producing design_feedback.md with approval or modification requests. The loop runs for at most two iterations, stopping early if DesignCritic's feedback begins with [APPROVED].",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Produce or revise the detailed adaptive design_spec.md describing all 10 web pages, element IDs, data formats, and storage structure for the 'OnlineLibrary' Python web application based on user_task_description and DesignCritic feedback.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        },
        {
            "agent_name": "DesignCritic",
            "role": "Review design_spec.md thoroughly to ensure alignment with user_task_description, consistency of page elements, data storage design, and usability; write design_feedback.md starting with [APPROVED] if satisfactory or NEED_MODIFY for revisions.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_feedback.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignGenerator",
            "reviewer_agent": "DesignCritic",
            "review_criteria": "Verify completeness of page definitions, element IDs, data formats, and adherence to all user requirements without adding new features.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Produce and iteratively refine the complete Python Flask application including app.py and all HTML templates with exact element IDs, local text file data integration, and verification via gated code_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator develops or revises app.py and templates/*.html based on design_spec.md and previous code_feedback.md; CodeCritic reviews the codebase for correctness, style, functional completeness, and compliance with design_spec.md, producing code_feedback.md beginning with [APPROVED] or NEED_MODIFY. The process runs for up to two iterations or until approval.",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Implement or fully revise the Python Flask backend (app.py) and all HTML templates (templates/*.html), ensuring all 10 pages, navigation, exact element IDs, and local text file storage interaction conform to design_spec.md and prior feedback.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"},
                {"type": "text_file", "name": "code_feedback.md", "source": "CodeCritic"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        },
        {
            "agent_name": "CodeCritic",
            "role": "Review the Python Flask backend and HTML templates for syntax, runtime correctness, functional adherence to design_spec.md, presence of required element IDs, and proper management of local text file data; generate comprehensive code_feedback.md with approval or modification requests.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "code_feedback.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "AppGenerator",
            "reviewer_agent": "CodeCritic",
            "review_criteria": "Ensure all pages, elements, data storage, and functionality strictly comply with design_spec.md and coding best practices without omissions or unauthorized extensions.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the 'OnlineLibrary' Python Flask web application from user requirements with full design specification and implementation including all pages, elements, and local text file data management.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the design specification of the OnlineLibrary application until approval.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Create and refine detailed design spec for pages, elements, and data storage."}
            ]
        },
        {
            "step": 2,
            "description": "Develop and iteratively verify the complete implementation of app.py and HTML templates until approval.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Implement and refine full Flask backend and frontend matching design specification."}
            ]
        }
    ]
): pass
# Orchestrate_End