# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the VirtualMuseum requirements and produce a detailed design_spec.md specifying pages, routes, and data structures",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first produces requirements_analysis.md capturing user needs and data specifications; "
        "then SystemArchitect consumes it and writes design_spec.md covering Flask routes, page titles, element IDs, data file structures, "
        "and navigation flows."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Extract all user requirements, page designs, UI elements, navigation buttons, and data storage details from the user task to create requirements_analysis.md."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        },
        {
            "agent_name": "SystemArchitect",
            "role": (
                "Create design_spec.md defining Flask app architecture with all endpoints, templates, exact page titles, element IDs, button actions, page navigation flow starting from Dashboard, "
                "and data model specifications reflecting all described local text files under 'data' directory."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "requirements_analysis.md", "source": "RequirementsAnalyst"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "RequirementsAnalyst",
            "reviewer_agent": "SystemArchitect",
            "review_criteria": (
                "Verify requirements_analysis.md fully and accurately captures all page specifications, UI element IDs, navigation, and data file details."
            ),
            "review_artifacts": [
                {"type": "user", "name": "user_task_description"},
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_phase(
    goal: str = "Implement a Flask-based VirtualMuseum web application with all specified pages, navigation, and data file integration as app_draft.py and templates drafts",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "Developer writes app_draft.py implementing all Flask routes and logic based on design_spec.md; TemplateDesigner creates draft HTML templates under templates_draft/ directory with exact element IDs, titles, buttons, and navigation; only after both complete, IntegrationEngineer combines drafts into final app.py and template files."
    ),
    team: list = [
        {
            "agent_name": "Developer",
            "role": (
                "Implement all Flask backend routes, data file read/write logic under 'data' directory, starting from Dashboard page, "
                "enabling features for exhibitions, artifacts, audio guides, tickets, virtual events, and collections as per design_spec.md."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "SystemArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_draft.py"}
            ]
        },
        {
            "agent_name": "TemplateDesigner",
            "role": (
                "Create every required HTML template under templates_draft/ replicating all UI page structures, exact element IDs, buttons, and page titles from design_spec.md."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "SystemArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationEngineer",
            "role": (
                "Integrate app_draft.py and templates_draft/*.html into final app.py and templates/*.html ensuring exact adherence to design_spec.md, "
                "enforce all Flask render_template calls to final templates directory and close any inconsistencies."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "app_draft.py", "source": "Developer"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "TemplateDesigner"},
                {"type": "text_file", "name": "design_spec.md", "source": "SystemArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "Developer",
            "reviewer_agent": "IntegrationEngineer",
            "review_criteria": (
                "Verify app_draft.py correctness against design_spec.md before integration."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "TemplateDesigner",
            "reviewer_agent": "IntegrationEngineer",
            "review_criteria": (
                "Check templates_draft/*.html for exact UI element IDs, titles, navigation buttons, and consistent styling as per design_spec.md."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "templates_draft/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase2_End

# Phase3_Start
def verification_phase(
    goal: str = "Validate the final app.py and templates/*.html for Flask runtime correctness and full compliance with design_spec.md, and produce the final corrected application",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator tests app.py and templates/*.html for syntax, runtime behavior, Flask test client routing, and UI compliance writing validation_report.md; "
        "FinalFixer corrects issues from validation_report.md and rewrites app.py and templates/*.html accordingly."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "role": (
                "Perform syntax and runtime validation of app.py and templates/*.html, including Flask test client routing starting from Dashboard, "
                "page title accuracy, UI element ID verification, navigation correctness, and produce validation_report.md."
            ),
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "design_spec.md", "source": "SystemArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "FinalFixer",
            "role": (
                "Apply all issues and corrections from validation_report.md to produce the final corrected app.py and templates/*.html fully conforming to the design spec."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "design_spec.md", "source": "SystemArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "WebValidator",
            "reviewer_agent": "FinalFixer",
            "review_criteria": (
                "Ensure validation_report.md covers all runtime, syntax and UI compliance issues."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "FinalFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": (
                "Verify final app.py and templates/*.html fully implement all requirements and resolve validation report issues."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase3_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop a fully functional VirtualMuseum Flask web application from user requirements to validated final implementation",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements and produce a detailed design specification for the Flask web application.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce an accurate Flask design spec covering all pages, UI elements, navigation, and local text file data models"}
            ]
        },
        {
            "step": 2,
            "description": "Implement the Flask application and HTML templates drafts based on design spec, then integrate into final code and templates.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Implement Flask routes, data handling, and draft HTML templates; integrate into final app.py and templates"}
            ]
        },
        {
            "step": 3,
            "description": "Validate the final implementation for syntax, runtime, navigation correctness and UI compliance, then fix issues to produce final deliverables.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and correct the Flask app and templates to fully conform to design and requirements"}
            ]
        }
    ]
): pass
# Orchestrate_End