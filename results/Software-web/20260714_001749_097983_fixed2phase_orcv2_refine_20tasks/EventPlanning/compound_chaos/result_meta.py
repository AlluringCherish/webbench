# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the complete adaptive web design specification for the EventPlanning application including all 8 pages, exact element IDs, navigation flow, and local data file structures; deliver design_spec.md and gated design_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "DesignGenerator creates or revises design_spec.md based on user_task_description and previous design_feedback.md. "
        "DesignCritic reviews design_spec.md ensuring completeness of pages, element IDs, data storage format, and navigation; "
        "writes design_feedback.md starting with [APPROVED] or NEED_MODIFY. "
        "At most two refinement iterations."
    ),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Write or comprehensively revise the full adaptive web design specification for EventPlanning including page layout, element IDs, navigation between pages, and data file structures according to the user task and design_feedback.md.",
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
            "role": "Perform detailed review of design_spec.md ensuring all 8 pages are fully covered with required element IDs, inter-page navigation is logical, local text file data storage formats match requirements, and design meets the user task; produce design_feedback.md with [APPROVED] or NEED_MODIFY prefix.",
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
            "review_criteria": "Conduct a comprehensive check for completeness, correctness of element IDs, page titles, local data formats compliance, and logical navigation flow.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Refine the complete adaptive implementation of the EventPlanning Python web app with all required pages, exact element IDs, local text file data handling, and produce app.py with templates/*.html files along with gated code_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "AppGenerator writes or revises the full backend and frontend implementation producing app.py and HTML templates for all pages, implementing navigation and local text file data management based on design_spec.md and previous code_feedback.md. "
        "CodeCritic reviews the app.py and templates for correctness of element IDs, page functionality, data file access, and adherence to design_spec.md producing code_feedback.md starting with [APPROVED] or NEED_MODIFY. "
        "At most two refinement iterations."
    ),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Implement or thoroughly revise the complete Python web application backend and frontend, producing app.py and templates/*.html that realize the design_spec.md including all page elements with exact IDs, local text file operations, and navigation; incorporate suggestions from code_feedback.md.",
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
            "role": "Perform detailed review of app.py and HTML templates checking correctness of element IDs, routes (starting with Dashboard), data file handling consistency, and full functional alignment with design_spec.md; produce code_feedback.md with [APPROVED] or NEED_MODIFY prefix.",
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
            "review_criteria": "Ensure all pages are implemented with exact element IDs, correct navigation routes, local text data storage conformity, and that the app runs without error.",
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
    goal: str = "Develop the EventPlanning Python web application with all specified pages, exact element IDs, and local text file data management, starting from the Dashboard page, using a two-phase refinement workflow.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the complete design specification document for EventPlanning application.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Create and refine the adaptive design specification covering all pages, element IDs, navigation, and local data file formats."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement and verify the complete EventPlanning application with exact element IDs, local data file handling, and navigation according to design spec.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Build and refine the full Python web app including app.py and HTML templates conforming to design spec."
                }
            ]
        }
    ]
): pass
# Orchestrate_End