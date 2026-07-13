# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the OnlineLibrary requirements and produce a complete design_spec.md specifying all page designs, navigation routes, page titles, element IDs, data files format, and user interactions.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst reads the user task description and writes requirements_analysis.md outlining all requested pages, elements, "
        "navigation, data formats, and user flows; only after its completion, "
        "WebArchitect reads requirements_analysis.md and writes design_spec.md with detailed Flask route mappings, exact element IDs, "
        "template and data file structures, and interaction contracts."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": "Analyze the user task description for requirements and write requirements_analysis.md detailing all page titles, element IDs, user interactions, data formats, and navigation flows.",
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
            "role": "Convert requirements_analysis.md into design_spec.md specifying the Flask app architecture, including exact route-to-template mappings, page titles, element IDs, data file parsing contracts, user interaction flows, and technical constraints (starting at dashboard).",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
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
                "Verify requirements_analysis.md fully covers all user-visible pages, with explicit element IDs, page titles, navigation buttons, "
                "data storage formats, and functional descriptions before architecture begins."
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
    goal: str = "Implement the OnlineLibrary web application with a runnable Flask app.py and all required templates/*.html following design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer first writes app_draft.py and templates_draft/*.html implementing all requested pages with specified elements, navigation, "
        "data file access as per design_spec.md; after completion, IntegrationEngineer refines and integrates drafts into final app.py and templates/*.html, "
        "ensuring all route handlers, templates, and local file handling work flawlessly."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "role": "Write the initial draft of app_draft.py and all templates_draft/*.html files as per design_spec.md, ensuring each page uses Flask render_template, correct routes, exact element IDs, and data file reading/writing in data/ directory.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationEngineer",
            "role": "Refine and integrate drafts into final app.py and templates/*.html, removing draft folder dependencies, closing design gaps, and verifying all pages start from dashboard with correct data flows and element IDs.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
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
            "review_criteria": "Check app_draft.py and templates_draft/*.html against design_spec.md to ensure all routes, pages, element IDs, and local file handling conform before final integration.",
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
    goal: str = "Validate the final OnlineLibrary app.py and templates/*.html for syntax, runtime, and functional correctness, producing a validation_report.md and corrected final app.py and templates.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator validates app.py and templates/*.html for syntax and runtime errors and tests all routes/functions as per design_spec.md, writing validation_report.md; "
        "SequentialFixer then fixes all identified issues and produces the final corrected app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "role": "Validate app.py and templates/*.html for syntax and runtime errors; test route accessibility and page content against design_spec.md; write detailed validation_report.md documenting issues and suggestions.",
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
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
            "role": "Apply corrections from validation_report.md to produce the final, fully working app.py and templates/*.html; ensure conformity to all requirements.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"}
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
            "review_criteria": "Ensure validation_report.md is complete, precise, and includes actionable items covering syntax, runtime, and functional tests per design_spec.md.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": "Verify the final app.py and templates/*.html fully address and resolve validation_report.md issues and retain full requirement coverage.",
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
    goal: str = "Develop a comprehensive OnlineLibrary web application in Python with local text file data management, implementing all requested pages, navigation, and features, starting from the dashboard page.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce a detailed design specification.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce the detailed design_spec.md for the OnlineLibrary application."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the web application with drafts and integration of app.py and templates.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Produce the runnable OnlineLibrary Flask app.py and full templates/*.html set."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and finalize the web application through testing and corrections.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and produce the final corrected OnlineLibrary app.py and templates/*.html."}
            ]
        }
    ]
): pass
# Orchestrate_End