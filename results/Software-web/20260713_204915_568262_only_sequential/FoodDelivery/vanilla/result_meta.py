# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the FoodDelivery requirements and produce a detailed design_spec.md covering all pages, routes, elements, data files, and interactions.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md with detailed page routes, titles, element IDs, and core user flows; "
        "only after that WebArchitect reads this and produces design_spec.md documenting Flask route methods, template names, data file usage, and UI contracts."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Extract and trace every requested route, page title, exact element IDs, interaction flows, and data dependencies from the user "
                "requirements into requirements_analysis.md."
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
                "Transform requirements_analysis.md into design_spec.md defining exact Flask routes to expose, HTTP methods, templates filenames under templates/, "
                "page titles, element IDs, buttons, inputs, data file access and format contracts, and navigation flows."
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
                "Verify that requirements_analysis.md precisely lists all page routes, titles, UI element IDs per page, "
                "and captures all interactive UI elements and data file references to ensure clarity before architecture drafting."
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
    goal: str = "Implement a complete Flask application with app.py and templates/*.html following design_spec.md, supporting all pages, UI elements, and local text file data access.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer writes app_draft.py and all templates_draft/*.html files from design_spec.md; only after both complete, "
        "IntegrationEngineer produces final app.py and templates/*.html closing all gaps and enforcing web-compatible routes, element IDs, and data interactions."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "role": (
                "Write a complete app_draft.py implementing Flask routes, rendering templates in templates_draft/, and accessing local text file data for all features. "
                "Draft templates_draft/*.html for every page with correct element IDs and UI components."
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
                "Integrate app_draft.py and templates_draft/*.html into a final runnable Flask app.py and templates/*.html. "
                "Ensure precise requested routes, UI element IDs, correct render_template usage, and robust data file handling."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "app_draft.py", "source": "DraftEngineer"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "DraftEngineer"},
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
            "source_agent": "DraftEngineer",
            "reviewer_agent": "IntegrationEngineer",
            "review_criteria": (
                "Verify that app_draft.py and templates_draft/*.html fully implement design_spec.md routes and UI, "
                "with correct Flask route decorators, template rendering, and local file data interactions before final integration."
            ),
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
    goal: str = "Validate and test app.py with templates/*.html for Flask compliance, syntax, route coverage, element correctness, and produce the final corrected app.py and templates.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator performs comprehensive validation of app.py and templates/*.html generating validation_report.md; "
        "SequentialFixer reads this report and applies corrections producing final app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "role": (
                "Validate app.py for Python syntax, Flask app instantiation, route accessibility, response correctness, and verify all templates/*.html files "
                "for presence of requested element IDs, structure, and data bindings; produce validation_report.md."
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
                "Apply all actionable corrections from validation_report.md to app.py and templates/*.html for final delivery, ensuring full compliance with requirements."
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
            "review_criteria": (
                "Ensure validation_report.md contains precise, reproducible findings covering Flask route coverage, template element ID correctness, "
                "and runtime errors to guide correction effectively."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": (
                "Verify the final app.py and templates/*.html fully realize the user requirements as documented in requirements_analysis.md and design_spec.md."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        }
    ]
): pass
# Phase3_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Build the FoodDelivery Python web application with local text file data store, supporting all required pages, functions, and UI elements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements and produce the design specification document.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce complete design specification document from requirements."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the Flask application and page templates following design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Develop and integrate Flask app and HTML templates based on design_spec.md."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and correct the application code and templates to meet requirements.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and finalize the Flask app and templates for the FoodDelivery application."}
            ]
        }
    ]
): pass
# Orchestrate_End