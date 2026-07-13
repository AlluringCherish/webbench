# Phase1_Start
def design_specification_phase(
    goal: str = "Create a detailed adaptive web design contract defining all 10 web pages with exact element IDs, navigation flows, user roles, and local data file formats in design_spec.md and gate it with design_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator produces the design_spec.md text file from the user task description and any previous feedback; DesignCritic reviews the design_spec.md for completeness, correctness, and adherence to user specifications, producing design_feedback.md with approval or revision requests.",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Use the detailed user task description to draft or revise a comprehensive web app design specification covering all pages, exact element IDs, navigation, data file formats, and user workflows in design_spec.md.",
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
            "role": "Review design_spec.md for full compliance with all requirements, including page structures, element IDs, navigation, data management, and user roles; produce design_feedback.md starting with [APPROVED] or NEED_MODIFY.",
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
            "review_criteria": "Verify the design specification correctly covers all pages, elements, data files, navigation flows, user roles, and the start point dashboard with required element IDs exactly."
            ,
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Fully implement the PetAdoptionCenter Python web app with all pages, exact element IDs, local text file data storage, and navigation as per design_spec.md; produce app.py and templates/*.html, and gate implementation with code_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator creates or revises the Python Flask app.py source code and the complete set of HTML templates in templates/*.html based on design_spec.md and code_feedback.md; CodeCritic reviews the app.py and templates for conformity, correctness, and functionality producing code_feedback.md with approval or revision requests.",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Develop or revise the entire Python Flask application backend and frontend templates to fulfill the design_spec.md including all 10 pages, exact element IDs, navigation routes starting from dashboard, and local text file data storage.",
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
            "role": "Examine the combined app.py backend and templates/*.html frontend code for correctness, syntax, runtime, adherence to design_spec.md, exact element ID usage, data handling with local text files, and expected navigation; produce code_feedback.md starting with [APPROVED] or NEED_MODIFY.",
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
            "review_criteria": "Validate adherence to design_spec.md with correct element IDs, page navigation from dashboard, data management in local text files, and Python Flask app correctness.",
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
    goal: str = "Build the complete PetAdoptionCenter Python Flask web application with exact element IDs, local text file data management, and navigation starting from the dashboard page.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the detailed design specification document for PetAdoptionCenter including all pages, element IDs, navigation, and data files.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce detailed adaptive web design specification document."
                }
            ]
        },
        {
            "step": 2,
            "description": "Develop and verify the full Python Flask backend and frontend templates implementation based on the finalized design specification.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Implement and verify the full PetAdoptionCenter application codebase."
                }
            ]
        }
    ]
): pass
# Orchestrate_End