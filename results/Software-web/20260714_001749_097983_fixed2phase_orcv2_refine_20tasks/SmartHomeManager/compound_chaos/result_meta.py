# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the comprehensive design specification for the SmartHomeManager Flask web application including page structure, navigation, UI elements with exact element IDs, and data file organization, producing design_spec.md and gated design_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator produces design_spec.md detailing pages, element IDs, and data storage contract; DesignCritic reviews this specification and produces design_feedback.md with either [APPROVED] or NEED_MODIFY to guide revision; iteration halts after approval or two cycles.",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Produce or revise the detailed design_spec.md for the SmartHomeManager Flask web app based on user_task_description and design_feedback.md, including all page designs, exact element IDs, navigation flow, data file formats, and storage conventions",
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
            "role": "Critically review the design_spec.md for full coverage of user requirements, correctness of element IDs, Flask routing conventions, and data storage consistency; produce design_feedback.md starting with [APPROVED] or NEED_MODIFY",
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
            "review_criteria": "Verify that the design_spec.md fully captures the user requirements, uses exact element IDs for all components, defines the Flask page routing starting at the dashboard, and correctly specifies all data storage files and formats.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Produce and iteratively refine the complete Flask application code (app.py and templates/*.html) for SmartHomeManager with data handling per design_spec.md, and gated by code_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator creates or revises app.py and all corresponding HTML templates under templates/ directory based on design_spec.md and code_feedback.md; CodeCritic reviews these artifacts for functional correctness, UI compliance, data handling accuracy, and Flask conventions and produces code_feedback.md with [APPROVED] or NEED_MODIFY; up to two iterations per refinement.",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Develop or refine the full SmartHomeManager Flask app implementation including app.py and all templates/*.html files ensuring exact element IDs, navigation, data file interactions per design_spec.md and incorporating feedback from code_feedback.md",
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
            "role": "Perform detailed review of app.py and templates/*.html for compliance with design_spec.md requirements including exact element IDs, Flask routing correctness, data handling with local text files, UI consistency, and report thorough code_feedback.md starting with [APPROVED] or NEED_MODIFY",
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
            "review_criteria": "Check that app.py and templates/*.html fully implement the design_spec.md features, use exact element IDs, Flask routes start at dashboard page, and manage local text data files correctly without missing elements.",
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
    goal: str = "Develop the SmartHomeManager Flask web application with precise UI element IDs and local text data storage complying with given requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Iteratively refine the detailed design specification of the SmartHomeManager Flask web app including all pages, elements, and data storage format.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Refine the detailed design specification document for the Flask web app."
                }
            ]
        },
        {
            "step": 2,
            "description": "Iteratively produce and verify the Flask web app implementation (app.py and templates) strictly following the approved design specification.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Produce and refine Flask app code and templates with validation by CodeCritic."
                }
            ]
        }
    ]
): pass
# Orchestrate_End