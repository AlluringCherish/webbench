# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the comprehensive design specification for the 'OnlineCourse' Python web application capturing all pages, UI element IDs, data formats, and user workflows into design_spec.md with gated feedback in design_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator writes design_spec.md from user_task_description and design_feedback.md; DesignCritic reviews design_spec.md producing design_feedback.md; iteration runs up to two times or stops on [APPROVED].",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Use detailed analysis of user requirements to write or fully revise design_spec.md describing UI pages, element IDs, data storage schemas, and functional workflows for the 'OnlineCourse' Python web app.",
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
            "role": "Review design_spec.md for completeness, correctness of page layouts, element ID accuracy, data format consistency, and adherence to user objectives; produce design_feedback.md with [APPROVED] or NEED_MODIFY.",
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
            "review_criteria": "Ensure the design covers all required pages and UI elements with correct IDs, accurately describes local text data storage formats, and aligns fully with user functional objectives.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Refine complete Python Flask web application source code (app.py and templates/*.html) implementing the 'OnlineCourse' system to specification with gated feedback in code_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator writes or fully revises app.py and all templates/*.html implementing design_spec.md and code_feedback.md feedback; CodeCritic reviews code correctness, UI element IDs, data file handling, and application functionality, producing code_feedback.md; iteration runs up to two times or stops on [APPROVED].",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Develop or completely revise the Python Flask app.py backend and HTML template files implementing all application pages, UI elements with exact IDs, local text file data management, and workflow logic meeting the design specification and incorporating code_feedback.md.",
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
            "role": "Review the app.py and HTML templates for syntax correctness, functional completeness, adherence to UI element ID specifications, proper file-based data handling, and workflow consistency; produce code_feedback.md with [APPROVED] or NEED_MODIFY.",
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
            "review_criteria": "Validate code correctness, full implementation of design_spec.md functional requirements, exact UI element IDs usage, and local text file data integration.",
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
    goal: str = "Build the full 'OnlineCourse' Python web application with specified UI pages, local text data management, and user workflows.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine design specification document describing all UI pages, elements with IDs, data formats, and workflows.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Refine comprehensive design specification for 'OnlineCourse' app."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement and verify the full Python Flask app.py and templates/*.html with feedback loops.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Implement and refine 'OnlineCourse' application code and templates."
                }
            ]
        }
    ]
): pass
# Orchestrate_End