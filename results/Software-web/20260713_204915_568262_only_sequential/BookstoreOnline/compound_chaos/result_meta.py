# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the BookstoreOnline requirements and produce a detailed design_spec.md covering pages, routes, elements, data files, and navigation.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md tracing all user-visible pages, elements with IDs, navigation, and data requirements; "
        "WebArchitect reads requirements_analysis.md and user input to produce design_spec.md covering Flask routes, page titles, element IDs, data file usage, "
        "and navigation paths."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Analyze the user task description and extract every requested page, exact element IDs, page titles, navigation buttons, and user actions into requirements_analysis.md."
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
                "Convert requirements_analysis.md into a detailed design_spec.md that defines Flask app routes, HTTP methods, required page titles, all exact element IDs, "
                "navigation flows (including buttons to pages), and data storage contracts using the specified local text files."
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
                "Verify requirements_analysis.md captures all pages, exact requested element IDs, page titles, navigation buttons, and data storage details before architecture."
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
                "Verify design_spec.md fully covers all Flask routes, page titles, element IDs, data files, and navigation flows required to implement the app."
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
    goal: str = "Implement the BookstoreOnline Flask application as app_draft.py and templates_draft/*.html according to design_spec.md, supporting local text file data management and all specified pages with navigation.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "ImplementationEngineer writes app_draft.py and templates_draft/*.html implementing all Flask routes, page titles, element IDs, navigation, and reading/writing required local text files. "
        "IntegrationEngineer then converts the drafts into final app.py and templates/*.html ready for deployment."
    ),
    team: list = [
        {
            "agent_name": "ImplementationEngineer",
            "role": (
                "Develop app_draft.py implementing all frontend routes and backend logic per design_spec.md, managing local text files for data storage, and write every templates_draft/*.html page with exact element IDs."
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
                "Transform app_draft.py and templates_draft/*.html into the final app.py and templates/*.html, verifying exact routes, page titles, element IDs, data file integration, and navigation flows."
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
                "Check app_draft.py and templates_draft/*.html against design_spec.md for completeness, correctness, and exact compliance before integration."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "source_agent": "IntegrationEngineer",
            "reviewer_agent": "VerificationEngineer",
            "review_criteria": (
                "Ensure final app.py and templates/*.html strictly follow design_spec.md with accurate routes, page titles, element IDs, navigation, and local text file data management."
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
    goal: str = "Validate and test the final app.py and templates/*.html for syntax, runtime, and UI element correctness, producing a validation_report.md and applying necessary fixes to finalize the application.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "VerificationEngineer validates app.py and templates/*.html including syntax, execution, UI element presence, correct navigation, and data file management, producing validation_report.md; "
        "BugFixEngineer applies reported fixes to produce the final app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "VerificationEngineer",
            "role": (
                "Perform syntax validation, runtime execution checks, UI element ID verification per design_spec.md, test navigation flows and local text file access on app.py and templates/*.html, then write validation_report.md."
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
            "agent_name": "BugFixEngineer",
            "role": (
                "Address issues documented in validation_report.md by modifying app.py and templates/*.html accordingly to produce the final corrected application files."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "validation_report.md", "source": "VerificationEngineer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "VerificationEngineer",
            "reviewer_agent": "BugFixEngineer",
            "review_criteria": (
                "Check that validation_report.md contains clear, actionable, and design-aligned issues and recommendations."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "source_agent": "BugFixEngineer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": (
                "Confirm that the final updated app.py and templates/*.html fully address validation issues and conform to original requirements."
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
    goal: str = "Develop the BooksOnline Flask web application with all specified pages, navigation, and local text file data management according to user requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce design specification document.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce detailed Flask app design specification."}
            ]
        },
        {
            "step": 2,
            "description": "Develop and integrate the Flask application and templates as per the design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Implement and integrate Flask app and templates."}
            ]
        },
        {
            "step": 3,
            "description": "Validate, test, and fix the Flask app and templates to ensure correctness and user requirement fulfillment.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and finalize the Flask application."}
            ]
        }
    ]
): pass
# Orchestrate_End