# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the RestaurantReservation requirements and produce design_spec.md detailing Flask routes, page structure, element IDs, and data management using local text files.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md capturing all page elements, navigation, and user stories; "
        "then WebArchitect reads requirements_analysis.md and produces design_spec.md covering Flask app routing, template filenames and locations, "
        "exact page titles, element IDs, form inputs, data file access, and user flow ensuring dashboard as the root page."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Extract detailed requirements for all pages, UI elements, user actions, and data interactions from the user task and "
                "compile a structured requirements_analysis.md file capturing these details clearly and exhaustively."
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
                "Design a detailed Flask web application architecture based on requirements_analysis.md that includes page route mappings, "
                "template filenames under templates/, page titles, element IDs, button interactions, form fields, and data file usage "
                "(with pipe-delimited local text files in data/). Ensure the root route points to the Dashboard page."
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
            "review_criteria": (
                "Verify requirements_analysis.md fully captures every user-visible page, exact element IDs, data file formats, navigation paths, "
                "and user functionality needed before architecture design."
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
    goal: str = "Implement the RestaurantReservation Flask application including app.py and templates/*.html files according to design_spec.md and requirements.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer writes initial app_draft.py and all templates_draft/*.html with correct routing, page content, element IDs, forms, and data "
        "handling per design_spec.md. IntegrationEngineer then finalizes app.py and templates/*.html for deployment by replacing draft paths and closing gaps."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "role": (
                "Develop app_draft.py implementing all Flask routes, starting with '/' as Dashboard page. Create templates_draft/*.html with "
                "all specified pages, elements, IDs, and proper Flask render_template usage along with correct data file read/write logic using pipe-delimited text files."
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
                "Refine app_draft.py and templates_draft/*.html into final app.py and templates/*.html. Eliminate draft paths, ensure all routes and template references are finalized, "
                "enforce root route as Dashboard, and confirm data file paths and formats exactly match requirements."
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
            "review_criteria": (
                "Ensure app_draft.py and templates_draft/*.html implement all routes, elements, and data management from design_spec.md with accurate page titles and element IDs."
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
    goal: str = "Validate the final app.py and templates/*.html for correctness, compliance with requirements, and seamless functionality.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator performs syntax and runtime checks on app.py, ensures templates/*.html render correctly, tests route accessibility, and verifies UI elements, IDs, "
        "startup behavior, and data handling per design_spec.md. SequentialFixer applies corrections from validation_report.md and produces the final corrected application files."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "role": (
                "Thoroughly validate app.py and all templates/*.html by checking Python syntax, runtime Flask app behavior, route correctness, template rendering with expected element IDs, "
                "data read/write operations for local text files, and produce validation_report.md summarizing issues and suggestions."
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
                "Implement all corrections and improvements from validation_report.md to produce final, fully compliant app.py and templates/*.html ensuring stable routes, "
                "correct data handling, and exact adherence to requirements."
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
            "review_criteria": "Ensure validation_report.md clearly identifies all functional, UI, and data handling defects with actionable recommendations.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "WebArchitect",
            "review_criteria": (
                "Verify the final app.py and templates/*.html fully resolve all issues reported in validation_report.md and strictly match design_spec.md and requirements."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase3_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop a full-featured, requirements-compliant Flask RestaurantReservation web application with local file data storage.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce detailed web app design specifications.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce comprehensive design spec for Flask web app."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the Flask application and HTML templates based on the design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Create initial and final Flask app.py and templates with required UI and data handling."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and fix the Flask application and templates ensuring full compliance and correctness.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate, report issues, and apply fixes to finalize application code and templates."}
            ]
        }
    ]
): pass
# Orchestrate_End