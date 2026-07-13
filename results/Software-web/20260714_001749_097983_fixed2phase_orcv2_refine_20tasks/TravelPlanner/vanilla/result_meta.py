# Phase1_Start
def design_specification_phase(
    goal: str = "Create and refine the detailed design specification for the TravelPlanner web application, producing 'design_spec.md' and gated 'design_feedback.md'.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "DesignGenerator drafts and revises the comprehensive design_spec.md including all pages, UI element IDs, data storage format, and user navigation flows. "
        "DesignCritic reviews design_spec.md for completeness, consistency, and adherence to requirements, producing design_feedback.md starting with [APPROVED] or NEED_MODIFY."
    ),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Develop and iteratively refine the detailed design specification 'design_spec.md' for the TravelPlanner web app according to user requirements and feedback.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "agent_name": "DesignCritic",
            "role": "Evaluate the design_spec.md for completeness, correctness, and adherence to specifications, and write design_feedback.md starting with [APPROVED] or NEED_MODIFY.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_feedback.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignGenerator",
            "reviewer_agent": "DesignCritic",
            "review_criteria": "Verify completeness of page designs, all element IDs, data formats, and ensure no missing features per user requirements.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Iteratively develop and refine the TravelPlanner Python Flask web application including app.py and templates/*.html, producing code feedback for gating.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "AppGenerator writes and revises the Flask app.py and HTML templates based on design_spec.md and code_feedback.md. "
        "CodeCritic reviews the implementation for functional correctness, alignment with design, route conformance, element IDs, and performance, producing code_feedback.md starting with [APPROVED] or NEED_MODIFY."
    ),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Implement and iteratively refine the complete TravelPlanner Flask app including app.py and templates/*.html following design_spec.md and feedback.",
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
            "role": "Review app.py and templates/*.html for compliance with design_spec.md, code quality, presence of specified element IDs, page routing, and functional correctness. Write code_feedback.md with gating status.",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "code_feedback.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "AppGenerator",
            "reviewer_agent": "CodeCritic",
            "review_criteria": "Ensure all required pages, routes, element IDs, local text file data handling, and design conformance are correctly implemented and error-free.",
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
    goal: str = "Develop the TravelPlanner Python Flask web application with complete page implementations and data handling as per requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Iterative creation and refinement of the detailed design specification for the TravelPlanner app.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce a comprehensive design contract capturing all pages, UI elements, and data formats."
                }
            ]
        },
        {
            "step": 2,
            "description": "Iterative implementation and verification of the TravelPlanner Flask app code including templates, following the approved design spec.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Develop and refine the complete app.py and HTML templates with correctness and adherence to design."
                }
            ]
        }
    ]
): pass
# Orchestrate_End