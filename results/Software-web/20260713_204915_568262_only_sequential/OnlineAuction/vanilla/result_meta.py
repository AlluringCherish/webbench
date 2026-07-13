# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the OnlineAuction requirements and produce a complete design_spec.md covering Flask routes, templates, page titles, element IDs, and data file usage.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md with detailed tracing of all UI elements, data files, and user flows; then WebArchitect reads requirements_analysis.md "
        "and writes design_spec.md defining Flask routes, template filenames, page titles, element IDs, data handling contracts for text files, and navigation flow including the Dashboard as start page."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Trace every requested page, exact external template filenames and page-to-template mapping, exact page titles and element IDs, action buttons, search/filter options, and data file usage into requirements_analysis.md."
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
                "Convert requirements_analysis.md into design_spec.md specifying Flask routes and HTTP methods, exact page titles and element IDs, navigation actions, context variables, "
                "and data file handling conventions for auctions.txt, bids.txt, categories.txt, winners.txt, bid_history.txt, items.txt, and trending.txt. Enforce Dashboard as the start page."
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
                "Verify requirements_analysis.md includes all pages, exact element IDs, navigation paths, data file references, and UI elements as specified in user requirements."
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
    goal: str = "Implement the OnlineAuction web application with Flask app.py and templates/*.html files adhering to design_spec.md and using local text file data.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer writes app_draft.py and all templates_draft/*.html according to design_spec.md, configuring routes, page titles, element IDs, UI interactions, and data parsing from text files; then IntegrationEngineer integrates drafts into final app.py and templates/*.html optimized for Flask rendering and stable functionality."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "role": (
                "Write app_draft.py implementing all Flask routes with required methods, data loading/parsing logic from local text files, and all templates_draft/*.html with exact element IDs, page titles, navigation buttons, forms, and data display as per design_spec.md."
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
                "Integrate app_draft.py and templates_draft/*.html into final app.py and templates/*.html ensuring Flask app is runnable, paths are correct, templates load properly, navigation flows are correct, data from text files is accurately handled, and all element IDs and page titles match requirements."
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
                "Check that app_draft.py and templates_draft/*.html adhere to design_spec.md exactly with correct routes, element IDs, page titles, data handling, and UI elements before integration."
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
    goal: str = "Validate app.py and templates/*.html through syntax, runtime, and functionality checks; produce validation_report.md and final corrected application.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator validates app.py and templates/*.html for syntax, execution, route correctness, page rendering, UI element presence, navigation, and data file integration writing validation_report.md; then SequentialFixer updates app.py and templates/*.html resolving issues to deliver a fully compliant final application."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "role": (
                "Validate app.py and templates/*.html for syntax, successful import and startup, Flask test client route functionality, presence of required element IDs, correct page titles, navigation functionality, and accurate data integration from text files, then write detailed validation_report.md."
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
                "Apply every problem and improvement suggested in validation_report.md to produce corrected app.py and templates/*.html ensuring full compliance with original user requirements, design_spec.md, and functional correctness."
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
                "Ensure validation_report.md includes complete and actionable information about syntax, runtime, routing, template correctness, UI elements, and data integration issues."
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
                "Verify final app.py and templates/*.html fully satisfy user requirements and resolve all issues reported in validation_report.md."
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
    goal: str = "Complete the 'OnlineAuction' Python web application per requirements with validated, fully functional Flask app.py and templates.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and create design specification for the OnlineAuction application.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce the detailed design specification including Flask routes, templates, and data handling."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the OnlineAuction application with Flask and Jinja2 templates using local text file data, as per design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Develop app.py and templates implementing the full required functionality and UI."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and fix the final OnlineAuction application ensuring correctness, usability, and compliance.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and refine the final Flask application producing a fully compliant final product."}
            ]
        }
    ]
): pass
# Orchestrate_End