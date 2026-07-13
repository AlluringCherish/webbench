# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze user requirements and produce a comprehensive design_spec.md detailing pages, routes, elements, and data files.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst produces requirements_analysis.md based on the user task description; "
        "WebArchitect then reads requirements_analysis.md to generate design_spec.md specifying Flask routes, page titles, element IDs, "
        "data storage formats, and flexible parsing contracts."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Analyze the user's requirements to identify all requested pages, UI elements, data entities, and storage details, "
                "and produce requirements_analysis.md tracing all these requirements exactly."
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
                "Convert requirements_analysis.md into a detailed design_spec.md that specifies all Flask routes, HTTP methods, "
                "page titles, exact element IDs, navigation flows, and contracts for data parsing from the specified text files."
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
                "Verify requirements_analysis.md contains complete and accurate tracing of all user-visible pages, elements, "
                "and data storage requirements before architecture proceeds."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_phase(
    goal: str = "Implement the MovieTicketing Flask web application with exact requested routes, templates, and data handling.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "ImplementationEngineer writes app_draft.py and all templates_draft/*.html from design_spec.md; "
        "IntegrationEngineer then refines these drafts into final app.py and templates/*.html enforcing exact routes, element IDs, and data parsing."
    ),
    team: list = [
        {
            "agent_name": "ImplementationEngineer",
            "role": (
                "Develop a draft Flask application (app_draft.py) and all required HTML templates under templates_draft/ "
                "implementing the design_spec.md, including all 8 pages with routes, page titles, element IDs, "
                "navigation buttons, and local text-based data file parsing."
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
                "Refine app_draft.py and templates_draft/*.html into finalized app.py and templates/*.html, "
                "ensuring all routes start from the Dashboard page, exact element IDs, and stable data parsing from text files."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "ImplementationEngineer"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "ImplementationEngineer"},
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
            "source_agent": "ImplementationEngineer",
            "reviewer_agent": "IntegrationEngineer",
            "review_criteria": (
                "Review app_draft.py and templates_draft/*.html to ensure full compliance with design_spec.md, including correct routes, "
                "element IDs, and local file data handling."
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
    goal: str = "Validate the completed app.py and templates/*.html for correctness, completeness, and runnability.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator runs syntax and runtime validation on app.py and templates/*.html, producing validation_report.md; "
        "SequentialFixer then applies fixes and writes final artifacts."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "role": (
                "Validate app.py and templates/*.html for Flask syntax correctness, proper route handling, page content matching the design_spec.md, "
                "and stable data file interactions, producing validation_report.md."
            ),
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "SequentialFixer",
            "role": (
                "Apply corrections from validation_report.md to app.py and templates/*.html, ensuring final delivery of a fully functional "
                "MovieTicketing application that meets all specified requirements."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
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
                "Ensure that validation_report.md accurately identifies syntax, runtime, and design compliance issues."
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
                "Verify that final app.py and templates/*.html fully resolve all issues from validation_report.md while maintaining full "
                "traceability to user requirements."
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
    goal: str = "Develop and deliver a Python Flask-based MovieTicketing web application handling local text file data storage as per requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce the design specification for the application.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce the detailed design specification document."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the Flask app and HTML templates according to design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Develop the application code and templates from the design specification."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and fix the application to ensure correctness and completeness.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Perform validation and final fixes to produce a runnable MovieTicketing app."}
            ]
        }
    ]
): pass
# Orchestrate_End