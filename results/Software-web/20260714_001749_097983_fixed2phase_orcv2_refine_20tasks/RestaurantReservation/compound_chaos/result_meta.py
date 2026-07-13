# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the adaptive Web design contract specifying all page layouts, element IDs, navigation flow and data file schema; deliver design_spec.md and design_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator drafts design_spec.md from user_task_description and prior design_feedback.md; DesignCritic reviews and produces design_feedback.md with gating status.",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Create or revise the detailed design_spec.md covering page titles, element IDs, navigation, and data storage formats from user requirements and design_feedback.md.",
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
            "role": "Evaluate design_spec.md for completeness against user_task_description including page requirements, element IDs accuracy, navigation coherence, and data file consistency; produce design_feedback.md starting with [APPROVED] or NEED_MODIFY.",
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
            "review_criteria": "Verify design_spec.md aligns precisely with all user-stated page structure, element ID requirements, navigation logic, and data file formats.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Develop and refine the full RestaurantReservation Python Flask web app implementation with all specified pages, element IDs, navigation, and data management per design_spec.md; deliver app.py, templates/*.html and gated code_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator writes or revises canonical app.py and templates/*.html from design_spec.md and code_feedback.md; CodeCritic assesses code correctness, page completeness, route correctness, element ID exactness, and data file access, producing code_feedback.md with approval status.",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Implement or revise the complete RestaurantReservation Python Flask app including app.py and all HTML templates matching design_spec.md with exact page elements, IDs, navigation routes, and local text file data integration; incorporate feedback from code_feedback.md.",
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
            "role": "Conduct comprehensive code review for app.py and templates/*.html ensuring full coverage of all nine pages with exact element IDs, correct navigation and button routing, proper integration with local data text files per design_spec.md, and write code_feedback.md beginning with [APPROVED] or NEED_MODIFY.",
            "tools": ["write_text_file"],
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
            "review_criteria": "Ensure accuracy and completeness of app.py and templates/*.html against design_spec.md, including correctness of routes, element IDs, and data file handling.",
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
    goal: str = "Build the complete RestaurantReservation Python Flask web application with specified pages, navigation, element IDs, and local text file data handling.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine and finalize the design specification for the RestaurantReservation application.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Create detailed design specifications including page layout, IDs, data storage format."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement the comprehensive Python Flask app and HTML templates, and refine through review cycles.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Develop and refine the implementation of the web application according to design."
                }
            ]
        }
    ]
): pass
# Orchestrate_End