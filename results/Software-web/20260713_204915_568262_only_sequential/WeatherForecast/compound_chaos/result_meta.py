# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze 'WeatherForecast' app requirements and produce a detailed design_spec.md covering all pages, elements, routes, and data fixtures.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md capturing all user-visible features, page titles, UI elements with IDs, "
        "route mappings, and data file usage; then WebArchitect reads it and produces design_spec.md, specifying Flask application architecture, "
        "template filenames and layouts, route methods, context variables, and data file interaction."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Trace every user-visible feature and UI element ID from requirements into requirements_analysis.md. Identify all Flask routes, "
                "page titles, buttons, inputs, and other page elements. List expected data files and formats to be consumed."
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
                "Convert requirements_analysis.md into design_spec.md describing detailed Flask routes and methods, template file names and structure "
                "under templates/, exact element IDs, context variables passed to templates, and data file reading logic per feature."
            ),
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
                "Verify requirements_analysis.md covers all user-visible pages, exact element IDs, page titles, navigation paths, and required data files "
                "before architecture begins."
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
    goal: str = "Implement the 'WeatherForecast' Flask application as app_draft.py and templates/*.html drafts according to design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer develops app_draft.py with all routes and logic plus templates_draft/*.html files for each page based on design_spec.md; "
        "then IntegrationEngineer integrates drafts into final app.py and templates/*.html with correct render_template calls and local data file usage."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "role": (
                "Write app_draft.py implementing all Flask routes and logic described in design_spec.md, using templates_draft/*.html as views. "
                "Create templates_draft/*.html files with exact page element IDs, buttons, inputs, and layouts. Use placeholders for data file access."
            ),
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
            "role": (
                "Convert app_draft.py and templates_draft/*.html into final app.py and templates/*.html, integrating data file reads from the 'data' directory, "
                "adjusting render_template calls, and ensuring all routes, element IDs, and navigation are precisely implemented."
            ),
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
            "review_criteria": (
                "Ensure the draft app_draft.py and templates_draft/*.html correctly implement all routes and UI elements as per design_spec.md before integration."
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
    goal: str = "Validate final app.py and templates/*.html to ensure correct functionality, route coverage, UI elements, and data integration.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator conducts thorough syntax, runtime, and functional validation on app.py and templates/*.html producing validation_report.md; "
        "SequentialFixer applies all fixes identified and writes final corrected app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "role": (
                "Validate app.py and templates/*.html for syntax errors, startup runtime errors, route coverage, template rendering with correct element IDs, "
                "and proper data file usage. Produce validation_report.md with detailed findings."
            ),
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
            "role": (
                "Apply all corrections from validation_report.md to produce the final app.py and templates/*.html, ensuring full compliance with design_spec.md "
                "and fixing issues in routes, functionality, and UI elements."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"}
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
                "Verify validation_report.md contains exhaustive test coverage results, error traces, and actionable fixes for both backend and frontend."
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
                "Confirm that the final app.py and templates/*.html address all validation issues and fully implement all user requirements "
                "from requirements_analysis.md."
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
    goal: str = "Develop a Flask 'WeatherForecast' web application with local text file data storage according to detailed requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce comprehensive design specification for the Flask app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce detailed design_spec.md specifying app architecture and UI."}
            ]
        },
        {
            "step": 2,
            "description": "Implement draft Flask application and templates based on the design specification, then integrate into final app.py and templates.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Develop app_draft.py, templates_draft/*.html and integrate into final app.py and templates/*.html."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and fix the final application to ensure full correctness and requirement coverage.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and correct final app.py and templates/*.html with feedback-driven refinements."}
            ]
        }
    ]
): pass
# Orchestrate_End