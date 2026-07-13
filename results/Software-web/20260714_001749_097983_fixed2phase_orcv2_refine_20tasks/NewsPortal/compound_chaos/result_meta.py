# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the comprehensive design specification for the NewsPortal Flask web application including all 9 page designs, element IDs, navigation flow, and local text data storage formats; deliver design_spec.md and gated design_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator produces design_spec.md describing UI pages with element IDs, navigation, and data storage contract; DesignCritic reviews design_spec.md and produces design_feedback.md starting with [APPROVED] or NEED_MODIFY.",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Generate or revise the detailed design_spec.md outlining the Flask app structure, page templates with exact element IDs, navigation routes starting from the dashboard, and local text file data management for articles, categories, bookmarks, comments, and trending data.",
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
            "role": "Critically review design_spec.md for completeness, fidelity to user requirements, correct element IDs, navigation flow, and data storage design; write design_feedback.md beginning with [APPROVED] if criteria met or NEED_MODIFY if revisions needed.",
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
            "review_criteria": "Ensure design_spec.md accurately represents all 9 required pages with exact element IDs, provides clear navigation starting from dashboard page, and specifies local text file data format per user requirements.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Iteratively develop and refine the NewsPortal Flask application code base with all 9 page templates, exact element IDs, local text file data handling, and navigation; deliver final app.py and templates/*.html and gated code_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator writes or revises app.py and each templates/*.html file implementing the design_spec.md and incorporating code_feedback.md; CodeCritic reviews all code files for functional correctness, element ID compliance, data access reliability, and navigation, returning code_feedback.md starting with [APPROVED] or NEED_MODIFY.",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Implement or revise the Flask application code app.py and HTML templates with all 9 pages, exact element IDs as per design_spec.md, local text file data management for articles, categories, bookmarks, comments, trending data, and navigation starting from dashboard page.",
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
            "role": "Conduct detailed code review and validation of app.py and HTML templates ensuring compliance with design_spec.md and correct implementation of local text file data handling, page elements, and navigation flow; produce code_feedback.md starting with [APPROVED] if quality standards met or NEED_MODIFY if fixes required.",
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
            "review_criteria": "Validate that all 9 pages and their exact element IDs exist, local text file data reading/writing is correctly integrated, and navigation begins from the dashboard page; ensure adherence to design_spec.md without adding functionalities.",
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
    goal: str = "Develop the NewsPortal Python Flask web application with all specified pages, exact element IDs, local text data handling, and navigation starting from dashboard page as per user requirements",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine design specification documents for the NewsPortal application for up to two iterations",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce and gate the comprehensive design specification including all UI pages, element IDs, navigation flow, and data storage formats"
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement and verify the NewsPortal Flask application code and templates for up to two iterations",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Develop and refine the Flask app.py and templates/*.html implementing the design with correct element IDs and local text data management"
                }
            ]
        }
    ]
): pass
# Orchestrate_End