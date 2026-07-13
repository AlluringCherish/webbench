# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the 'MusicStreaming' requirements and produce a complete detailed design_spec.md covering all pages, routes, elements, and data handling.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst writes requirements_analysis.md extracting all detailed elements, pages, and user flows; then "
        "WebArchitect reads requirements_analysis.md and writes design_spec.md specifying Flask routes, page titles, element IDs, "
        "data contracts, and local file storage formats."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Analyze the user task to produce requirements_analysis.md documenting all 10 pages, UI elements with IDs, data storage "
                "formats, and user interactions including navigation buttons and page start point as Dashboard."
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
                "Transform requirements_analysis.md into a detailed design_spec.md that covers the Flask application architecture: "
                "defining exact Flask routes for each page, page titles, exact element IDs, navigation flow starting at Dashboard, "
                "and specifying data handling for all local text file data sources as described."
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
                "Verify that requirements_analysis.md fully captures all page designs, element IDs, buttons, data formats, and the dashboard "
                "start requirement with no omissions or extraneous features."
            ),
            "review_artifacts": [
                {"type": "user", "name": "user_task_description"},
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        },
        {
            "source_agent": "WebArchitect",
            "reviewer_agent": "ImplementationEngineer",
            "review_criteria": (
                "Verify design_spec.md provides complete, unambiguous Flask routes, page titles, element IDs, and data file format contracts "
                "necessary for implementation without gaps."
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
    goal: str = "Implement the MusicStreaming web application as evaluator-compatible app.py and templates/*.html files per design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "ImplementationEngineer writes app_draft.py and templates_draft/*.html implementing all routes, pages, elements, and data handling as per design_spec.md; "
        "IntegrationEngineer then integrates drafts into final app.py and templates/*.html ensuring runnable Flask app with all features, navigation, and data storage."
    ),
    team: list = [
        {
            "agent_name": "ImplementationEngineer",
            "role": (
                "Develop app_draft.py with all Flask routes starting at Dashboard, implement page logics for song catalog, playlists, albums, artists, genres, "
                "and song/artist stats; render templates_draft/*.html with exact IDs and buttons, handle data via local text files per specification."
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
                "Merge app_draft.py and templates_draft/*.html to produce final app.py and templates/*.html, resolving draft paths, ensuring clean navigation, "
                "stable routes, functional UI elements with correct IDs, and correct local data storage accesses."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "ImplementationEngineer"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "ImplementationEngineer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "ImplementationEngineer",
            "reviewer_agent": "IntegrationEngineer",
            "review_criteria": (
                "Review app_draft.py and templates_draft/*.html against design_spec.md to confirm all required pages, routes, UI elements, button IDs, and data "
                "file handling are correctly implemented."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "source_agent": "IntegrationEngineer",
            "reviewer_agent": "ValidationEngineer",
            "review_criteria": (
                "Verify that the final app.py and templates/*.html form a runnable Flask application with all required routes and UI element IDs functioning "
                "and adhering to the design_spec.md."
            ),
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
    goal: str = "Validate and correct the final app.py and templates/*.html to ensure a fully functional and requirement-compliant MusicStreaming web app.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "ValidationEngineer tests and validates app.py with templates/*.html, writing validation_report.md identifying issues; "
        "SequentialFixer applies corrections per validation_report.md and rewrites final app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "ValidationEngineer",
            "role": (
                "Perform validation testing on app.py and templates/*.html for syntax, runtime errors, correct Flask route behaviors, UI element presence and IDs, "
                "data file interactions, and navigation starting point; produce validation_report.md."
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
                "Apply all fixes listed in validation_report.md to app.py and templates/*.html for full compliance with design_spec.md and user requirements, "
                "producing corrected and final versions of app.py and templates/*.html."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "validation_report.md", "source": "ValidationEngineer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "ValidationEngineer",
            "reviewer_agent": "SequentialFixer",
            "review_criteria": (
                "Ensure validation_report.md contains actionable, detailed findings aligned to design_spec.md covering all pages, routes, UI element IDs, and data file usage."
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
                "Verify the final app.py and templates/*.html fully resolve all validation issues and strictly implement the user requirements from validation_report.md."
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
    goal: str = "Develop a fully functional MusicStreaming Python web application using local text files with all required pages, features, and UI elements as per requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements to produce detailed design_spec.md documenting pages, routes, UI elements, and data handling.",
            "phases": [{"phase_name": "design_specification_phase", "role": "Produce the MusicStreaming web app design specification."}]
        },
        {
            "step": 2,
            "description": "Implement the Flask web application and templates according to design_spec.md.",
            "phases": [{"phase_name": "implementation_phase", "role": "Implement the MusicStreaming web app as app.py and templates."}]
        },
        {
            "step": 3,
            "description": "Validate and fix the implementation to produce the final compliant web application.",
            "phases": [{"phase_name": "verification_phase", "role": "Validate and correct the MusicStreaming web application."}]
        }
    ]
): pass
# Orchestrate_End