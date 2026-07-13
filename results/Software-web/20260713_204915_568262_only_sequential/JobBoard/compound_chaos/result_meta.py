# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the 'JobBoard' web application requirements and produce a complete design_spec.md covering pages, routes, UI element IDs, and data models.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst reads the user task and writes requirements_analysis.md detailing each page, required routes, page titles, UI element IDs, and the data model. "
        "WebArchitect then reads requirements_analysis.md and converts it into design_spec.md with finalized page architecture, route specifications, template mapping, element IDs, and data file contracts."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Analyze the user-provided task description to identify all pages, their titles, UI element IDs, navigation structure, and data storage requirements for the 'JobBoard' application, "
                "and write these details in requirements_analysis.md for architectural planning."
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
            "agent_name": "WebArchitect",
            "role": (
                "Create design_spec.md from requirements_analysis.md specifying Flask route endpoints, HTTP methods, exact page titles, template filenames, UI element IDs, navigation flow, "
                "and detailed data file schemas and formats. Ensure architecture supports user navigation starting at the Dashboard page without authentication."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md", "source": "RequirementsAnalyst"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "RequirementsAnalyst",
            "reviewer_agent": "WebArchitect",
            "review_criteria": "Verify requirements_analysis.md covers all pages, UI element IDs, and data storage requirements as specified in the user task with no omissions.",
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
    goal: str = "Implement the 'JobBoard' web application as a Flask app.py and corresponding templates/*.html files based on design_spec.md and user requirements.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer develops app_draft.py and draft templates/*.html files implementing all pages, routes, UIs, and data file handling as specified. "
        "IntegrationEngineer then refines and integrates drafts into a final app.py and templates/*.html set that fully comply with the design_spec.md and run as a cohesive Flask web app with dashboard as the start page."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "role": (
                "From design_spec.md and user requirements, write app_draft.py implementing Flask routes and handlers, and draft the templates/*.html files for all pages with correct UI element IDs, "
                "navigation buttons, and data interaction with local text files. Use render_template referencing templates draft directory."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationEngineer",
            "role": (
                "Integrate and refine app_draft.py and templates_draft/*.html into final app.py and templates/*.html files, ensuring all routes, page titles, element IDs, and local file data handling comply with design_spec.md. "
                "Remove any draft dependencies and ensure Flask app starts at Dashboard page."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "DraftEngineer"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "DraftEngineer"},
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
            "source_agent": "DraftEngineer",
            "reviewer_agent": "IntegrationEngineer",
            "review_criteria": "Check that app_draft.py and templates_draft/*.html conform to design_spec.md and user requirements before producing the final integration.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase2_End

# Phase3_Start
def verification_phase(
    goal: str = "Validate and finalize the 'JobBoard' Flask application by testing app.py and templates/*.html, then apply fixes to produce the final application.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator inspects and tests the integrated app.py and templates/*.html for syntax correctness, compliance with design_spec.md, route availability, UI element presence (element IDs), data handling, and navigation. "
        "SequentialFixer applies all corrections based on validation_report.md to produce the final runnable Flask application with complete requirement coverage."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "role": (
                "Validate the app.py and templates/*.html files for syntax errors, adherence to design_spec.md, proper Flask routing for all pages, presence of all UI elements with correct IDs, local file data handling, "
                "and start page set as the Dashboard. Write detailed validation_report.md with findings."
            ),
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "SequentialFixer",
            "role": (
                "Apply all issues found in validation_report.md to app.py and templates/*.html to fix errors, ensure design compliance and full feature support. Produce the final production-ready Flask application files."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
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
            "reviewer_agent": "SequentialFixer",
            "review_criteria": "Verify validation_report.md covers all critical syntax, route, UI element ID errors, and data handling issues thoroughly.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": "Confirm the final app.py and templates/*.html completely address all validation issues while preserving full user requirement coverage.",
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
    goal: str = "Build a comprehensive 'JobBoard' Python Flask web application per user requirements with local text file data storage.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements and create complete design specification for the JobBoard app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce the Web design specification including pages, routes, UI elements, and data models."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the Flask application and templates according to the design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Write draft and final Flask app.py and templates with all specified features and data file handling."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and fix the implementation to produce a fully compliant and functional final web application.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Test, validate, and apply fixes to finalize the Flask web application."}
            ]
        }
    ]
): pass
# Orchestrate_End