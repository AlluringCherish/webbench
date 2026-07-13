# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze user requirements and produce a comprehensive design_spec.md detailing Flask routes, page elements, data formats, and application features.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first creates requirements_analysis.md outlining all page routes, elements, and data storage needs; "
        "then WebArchitect reads this and produces design_spec.md with detailed Flask route and page element specifications, data format contracts, and feature descriptions."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Parse the user task to extract all routes, page names, element IDs, page purposes, and data storage format specifications into requirements_analysis.md. "
                "Ensure coverage of all pages, UI components, and local data storage formats without adding assumptions."
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
                "Transform requirements_analysis.md into design_spec.md that specifies Flask routes, expected HTML template filenames per page, "
                "exact element IDs per page for frontend use and testing, data storage file formats and schemas, button behaviors, and application flow. "
                "Include page route details, expected templates/*.html names, and specific element IDs."
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
            "reviewer_agent": "WebArchitect",
            "review_criteria": (
                "Verify that requirements_analysis.md exhaustively enumerates all pages, routes, element IDs, data formats, and system features "
                "matching user input without omissions or alterations."
            ),
            "review_artifacts": [
                {"type": "user", "name": "user_task_description"},
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        },
        {
            "source_agent": "WebArchitect",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": (
                "Validate design_spec.md for thorough Flask route coverage, exact external template filenames, correct and complete element IDs, "
                "precise data storage formats, and conformity to user task requirements."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_phase(
    goal: str = "Develop a Flask web application codebase including app.py and all required templates/*.html files strictly according to design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer writes app_draft.py and all templates_draft/*.html files enforcing all routes, element IDs, page structures, and data handling as per design_spec.md; "
        "then IntegrationEngineer refines and integrates the draft into final app.py and final templates/*.html files fully operational and matching design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "role": (
                "Create a draft Flask app_draft.py implementing every route and data interaction defined in design_spec.md. "
                "Develop corresponding templates_draft/*.html files with exact element IDs and layout per design_spec. "
                "Use render_template with templates_draft folder and ensure all UI elements and behaviors per specification."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationEngineer",
            "role": (
                "Integrate app_draft.py and templates_draft/*.html into final app.py and templates/*.html with all draft features fully realized. "
                "Remove dependence on draft paths, ensure Flask runs correctly, and enforce page route, element ID, and data file access as per design_spec.md."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "DraftEngineer"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "DraftEngineer"}
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
            "review_criteria": "Check app_draft.py and templates_draft/*.html fully implement all design_spec.md requirements and page elements.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "source_agent": "IntegrationEngineer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": "Verify that final app.py and templates/*.html fully realize design_spec.md, are runnable, and expose all specified routes and elements.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase2_End

# Phase3_Start
def verification_phase(
    goal: str = "Comprehensively validate the final Flask app.py and templates/*.html for functional correctness, exact route availability, element presence, and runtime stability; fix issues and produce a validated final version.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator tests app.py and templates/*.html producing validation_report.md with findings; "
        "SequentialFixer then applies these findings to finalize app.py and templates/*.html resolving all reported issues."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "role": (
                "Run syntax, import, and startup validation of app.py. Test Flask routes including /dashboard and all specified pages. "
                "Check presence and correctness of all required element IDs, buttons, and UI components in templates/*.html. Write validation_report.md documenting defects and passes."
            ),
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "SequentialFixer",
            "role": (
                "Apply all actionable corrections from validation_report.md to app.py and templates/*.html until all issues are resolved. "
                "Ensure final deliverables strictly conform to design_spec.md and pass all validation checks."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"}
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
            "review_criteria": (
                "Check validation_report.md correctly identifies missing elements, route issues, and runtime errors with clear, reproducible instructions."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": (
                "Verify the final app.py and templates/*.html incorporate all fixes and fully conform to the original user task and design_spec.md."
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
    goal: str = "Build a fully functional ContentPublishingHub Flask web application with complete page set, data handling, and validation as per user specification.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements and create design specification detailing Flask routes, pages, UI elements, and data storage formats.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce comprehensive design_spec.md from user requirements."}
            ]
        },
        {
            "step": 2,
            "description": "Develop Flask application source code and HTML templates implementing all specified routes and UI elements from design_spec.md.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Implement Flask app.py and templates/*.html based on design_spec.md."}
            ]
        },
        {
            "step": 3,
            "description": "Validate final Flask app.py and templates/*.html for completeness and correctness; fix defects to finalize deliverables.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and fix final Flask application source and templates."}
            ]
        }
    ]
): pass
# Orchestrate_End