# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the PetAdoptionCenter requirements and produce a complete design_spec.md describing all pages, routes, data files, and UI element mappings",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md with detailed page elements and data descriptions; only after it "
        "completes, WebArchitect converts it into design_spec.md with precise Flask architecture, route definitions, data access strategies, "
        "and UI contract specifications."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Extract and document all user requirements, UI elements with exact IDs, intended page titles, data file formats, and user flows "
                "into requirements_analysis.md directly from the user task description."
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
                "Transform requirements_analysis.md into a finalized design_spec.md file containing the Flask route architecture, page-to-template mapping, "
                "exact UI element IDs and types per page, navigation logic (starting at Dashboard), local data storage schemas and filenames in data/, "
                "and interaction contracts for all user flows and buttons."
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
                "Verify requirements_analysis.md completely and accurately captures every required page, UI elements by ID, data files, their formats, and "
                "the user interaction flows as described by the user."
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
    goal: str = "Implement the PetAdoptionCenter Flask Web application as app.py and templates/*.html accurately reflecting design_spec.md",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer writes app_draft.py and templates_draft/*.html from design_spec.md covering all 10 pages, exact routes, UI IDs, "
        "buttons, and local file I/O; IntegrationEngineer then refines drafts into final app.py and templates/*.html fixing paths and final integration."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "role": (
                "Create a full app_draft.py Flask application implementing all routes, views, and logic per design_spec.md, using local text file "
                "read/write under data/. Also write all templates_draft/*.html with exact UI element IDs and proper Flask render_template usage, referencing "
                "required CSS/JS if any."
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
                "Integrate app_draft.py and templates_draft/*.html into final app.py and templates/*.html addressing all runtime path corrections, "
                "ensuring app.py runs with Flask and templates render with correct template_folder. Maintain exact requested routes, UI IDs, and data file "
                "access conforming to design_spec.md."
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
            "review_criteria": (
                "Review app_draft.py and templates_draft/*.html against design_spec.md for correctness, completeness, and adherence to UI IDs and data storage before producing final files."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        }
    ]
): pass
# Phase2_End

# Phase3_Start
def verification_phase(
    goal: str = "Validate the Flask app.py and templates/*.html for syntax, runtime behavior and correct implementation of all user requirements before final release",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator runs syntax and runtime validation on app.py and templates/*.html verifying coverage of all design specification features "
        "and writes validation_report.md; SequentialFixer reviews validation_report.md and applies all corrections to deliver the final application."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "role": (
                "Run validate_python_file and execute_python_code on app.py to check for syntax and runtime errors; additionally verify template correctness, "
                "route coverage, UI element presence, button actions, and data file I/O. Produce validation_report.md listing any issues found."
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
                "Apply every correction from validation_report.md to app.py and templates/*.html ensuring all required pages, UI elements by ID, "
                "data storage in local text files, and interactions conform fully to the design_spec.md and user requirements."
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
                "Confirm validation_report.md precisely identifies all syntax, runtime, functional, and UI-related issues for targeted correction."
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
                "Verify that the final app.py and templates/*.html fully implement all specified user requirements and resolve all validation issues."
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
    goal: str = "Develop the PetAdoptionCenter Python web application with correct routes, user-facing pages, local text file data management, and UI per user specifications",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user specifications and produce complete design specification for the Flask web application.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce a detailed web app design_spec.md specifying pages, UI, routes, and data files."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the application and templates according to design_spec.md.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Develop complete Flask app.py and all page templates *.html."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and correct the application for completeness, correctness, and runtime operation.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Perform syntax, runtime validation and fix all issues to finalize the app."}
            ]
        }
    ]
): pass
# Orchestrate_End