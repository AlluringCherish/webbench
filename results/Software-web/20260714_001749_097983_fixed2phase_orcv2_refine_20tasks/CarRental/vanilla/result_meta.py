# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the design contract for the 'CarRental' Python Flask web application, producing 'design_spec.md' and gated 'design_feedback.md'.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = ("DesignGenerator writes or revises 'design_spec.md' describing the architecture, page designs, element IDs, "
                                        "data storage format, and user flows for the CarRental application based on 'user_task_description' and previous 'design_feedback.md'. "
                                        "DesignCritic reviews 'design_spec.md' and writes 'design_feedback.md' beginning with [APPROVED] or NEED_MODIFY. "
                                        "Loop runs for at most two iterations or until approval."),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Architect the overall system design and detailed UI/UX specifications for CarRental app, including page structure, element IDs, navigation, and data file formats.",
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
            "role": "Critically evaluate the 'design_spec.md' for completeness, correctness, and conformance to the user task without adding requirements; produce gated 'design_feedback.md'.",
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
            "review_criteria": ("Check that the design_spec.md covers all required pages with specified element IDs, data storage "
                                "formats, no authentication, proper navigation flow starting from Dashboard, and consistency with user instructions."),
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Refine the complete Python Flask implementation with app.py and templates/*.html along with gated code_feedback.md for the CarRental web application.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = ("AppGenerator writes or revises 'app.py' and all HTML template files 'templates/*.html' implementing the CarRental design_spec.md and handles all specified features and element IDs. "
                                        "CodeCritic reviews output conformance to design_spec.md, checks functionality, data file integration, and writes 'code_feedback.md' starting with [APPROVED] or NEED_MODIFY. "
                                        "Loop runs at most two iterations or until approval."),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": ("Develop the combined backend and frontend code for CarRental app in Python Flask with text file data storage, implementing all nine pages, "
                     "element ID requirements, navigation from dashboard, and user interactions as specified in design_spec.md and code_feedback.md."),
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
            "role": ("Critically evaluate the code files 'app.py' and 'templates/*.html' for correctness, adherence to design_spec.md, inclusion of required element IDs, "
                     "functionality of all features without authentication, and proper data access from local text files; produce gated 'code_feedback.md'."),
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
            "review_criteria": ("Verify that app.py and HTML templates completely implement all design_spec.md features, element IDs exactly as defined, "
                                "local text data files are read and updated properly, the website starts at dashboard page, and no authentication is implemented."),
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
    goal: str = "Develop the CarRental Python Flask web application with all specified pages, features, element IDs, and local text file data management as defined by the user.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the design specification with architecture, UI/UX details, and data format for at most two iterations.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce the detailed design specification and gate it through feedback."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement and verify the full Python Flask application with web pages, backend logic, and local file integration for at most two iterations.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Generate the backend/frontend code and templates with feedback gating."
                }
            ]
        }
    ]
): pass
# Orchestrate_End