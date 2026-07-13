# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the complete ContentPublishingHub Flask web application design, including all pages, routes, element IDs, and user interaction flows; deliver design_spec.md with detailed UI and data contract specifications.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator drafts design_spec.md describing pages, routes, UI element IDs, data storage formats, and navigation based on user requirements; DesignCritic reviews design_spec.md against user task requirements and writes design_feedback.md with required modifications or approval.",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Generate or revise a complete design_spec.md detailing the Flask app's page structure, exact route definitions, UI element IDs, data file formats, and interaction specifications from user_task_description and design_feedback.md.",
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
            "role": "Critically review the design_spec.md to ensure completeness, correctness, and alignment with the user task focusing on UI element IDs, routing, data format conformance, and testing start from Dashboard; write design_feedback.md beginning with '[APPROVED]' if acceptable or 'NEED_MODIFY' if revision is needed.",
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
            "review_criteria": "Check that design_spec.md meets all page design requirements including routes, exact element IDs, data storage formats, version control workflows, analytics presentation, and testing start point; require precise and unambiguous specifications; feedback must prompt either approval or detailed modification requests.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "design_feedback.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Develop the canonical Flask application files app.py and templates/*.html implementing the ContentPublishingHub specification with all routes, UI elements, data handling, version control, and analytics; iterate based on code feedback until at most two iterations.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator writes or revises app.py and all template HTML files based on the finalized design_spec.md and code_feedback.md; CodeCritic evaluates code correctness, adherence to design_spec.md, routing accuracy, element ID correctness, and basic runtime validation, then writes code_feedback.md with '[APPROVED]' or 'NEED_MODIFY'.",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Implement or revise the Flask app's app.py and templates/*.html files strictly according to design_spec.md and prior code_feedback.md; ensure compliance with all route definitions and exact UI element ID requirements, local text file data storage, version control, content scheduling, and analytics display.",
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
            "role": "Review app.py and templates/*.html against design_spec.md ensuring exact routing, UI elements with correct IDs, data storage interactions, and start testing from Dashboard page; check runtime validation and code quality, then generate code_feedback.md with '[APPROVED]' or 'NEED_MODIFY' at most two iterations.",
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
            "review_criteria": "Validate that app.py and templates/*.html strictly conform to design_spec.md requirements including route correctness, HTML element IDs, data file access, version control implementation, content scheduling, and analytics display; also verify code passes syntax and runtime validation.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "code_feedback.md"}
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Build a Flask ContentPublishingHub web application with precise routing, UI elements, version control, scheduling, and analytics per specification, starting testing from the Dashboard page.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the complete design specification including all pages, routes, UI elements, and data formats.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce and refine comprehensive Flask app design specification."}
            ]
        },
        {
            "step": 2,
            "description": "Implement and verify app.py and templates/*.html according to finalized design specification.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Develop and validate Flask application implementation."}
            ]
        }
    ]
): pass
# Orchestrate_End