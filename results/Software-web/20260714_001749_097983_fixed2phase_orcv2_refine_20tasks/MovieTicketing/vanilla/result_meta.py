# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the MovieTicketing web app design contract with page structure, element IDs, navigation, and data management; deliver design_spec.md and design_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator creates or revises design_spec.md based on user_task_description and previous design_feedback.md; DesignCritic reviews and writes design_feedback.md indicating approval or needed modifications.",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Design the architecture and detailed page specifications for MovieTicketing, including pages, UI elements with exact IDs, navigation flow, and data storage format, producing design_spec.md.",
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
            "role": "Critically review design_spec.md for completeness, consistency with user requirements, clarity of element IDs and navigation, and data storage format correctness; produce design_feedback.md starting with [APPROVED] or NEED_MODIFY.",
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
            "review_criteria": "Verify that the design_spec.md fully and accurately captures all user requirements, specifies all page elements with correct IDs, navigation paths, and data file formats without omissions or contradictions.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Refine the complete Python MovieTicketing web app implementation including app.py, HTML templates for all 8 pages, and associated local text file data handling; deliver app.py, templates/*.html, and code_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator produces or revises app.py and all HTML templates (*.html) implementing the web app per design_spec.md and code_feedback.md; CodeCritic reviews these files for correctness, completeness, data integration, and UI compliance and produces code_feedback.md starting with [APPROVED] or NEED_MODIFY.",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Develop the Python backend app.py and frontend HTML templates covering all 8 pages with exact element IDs, functional navigation, user interaction, and local text file data management as per design_spec.md.",
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
            "role": "Review the app.py and HTML templates for functional correctness, completeness per design_spec.md, adherence to element ID specifications, routing, local data file interaction, and user navigation flow; produce code_feedback.md starting with [APPROVED] or NEED_MODIFY.",
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
            "review_criteria": "Ensure app.py and templates/*.html fully implement all functional pages, UI elements with correct IDs, proper routing, and local text data integration exactly as defined in design_spec.md without errors.",
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
    goal: str = "Develop a Python Flask MovieTicketing web application with 8 specified pages, exact element IDs, local text file data management, and no authentication, starting from the Dashboard page.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the design specifications for the MovieTicketing app including all page designs, navigation, element IDs, and data storage formats.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Refine the movie ticketing web app design contract with detailed UI and data specifications."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement and verify the complete backend and frontend of the MovieTicketing app including app.py and HTML templates.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Develop and validate the Python Flask app.py and all templates with local text data integration as per design specifications."
                }
            ]
        }
    ]
): pass
# Orchestrate_End