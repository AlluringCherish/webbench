# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the RealEstate requirements and produce a complete design_spec.md detailing pages, routes, element IDs, and data contracts.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md detailing all pages, elements, and data storage formats; "
        "WebArchitect then reads requirements_analysis.md and produces design_spec.md with Flask route definitions, page templates, "
        "element IDs, and data file interface contracts."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Extract and document all functional requirements, pages, elements with exact IDs, user interactions, and data storage "
                "formats into requirements_analysis.md from the user task description."
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
                "Convert requirements_analysis.md into design_spec.md covering Flask app architecture with route definitions starting from "
                "Dashboard page, page titles, element IDs per page, user interactions via buttons and inputs, and detailed data file reading/writing "
                "contracts matching specifications."
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
            "review_criteria": "Check that requirements_analysis.md thoroughly covers all pages, elements with precise IDs, user navigation flow, and data storage formats as per user task.",
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
    goal: str = "Implement the RealEstate Flask web application producing app_draft.py and templates_draft/*.html based on design_spec.md",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftDeveloper writes app_draft.py implementing all Flask routes, handlers, and logic, and templates_draft/*.html for every page "
        "based on design_spec.md; IntegrationDeveloper then refines them into final app.py and templates/*.html with all navigation and data integration."
    ),
    team: list = [
        {
            "agent_name": "DraftDeveloper",
            "role": (
                "Write a complete Flask app_draft.py and all corresponding templates_draft/*.html files enforcing routes starting at Dashboard page, "
                "page titles, exact element IDs, user navigation via buttons, form input handling, and CRUD operations on local data text files as specified."
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
            "agent_name": "IntegrationDeveloper",
            "role": (
                "Integrate app_draft.py and templates_draft/*.html into final app.py and templates/*.html, resolving references, ensuring all pages "
                "start or route correctly from the Dashboard page, embedding exact element IDs, and enabling data persistence in local text files."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "DraftDeveloper"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "DraftDeveloper"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DraftDeveloper",
            "reviewer_agent": "IntegrationDeveloper",
            "review_criteria": "Verify app_draft.py and templates_draft/*.html correctly implement all routes, page titles, element IDs, user interactions, and local text file data management as specified in design_spec.md.",
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
    goal: str = "Validate app.py and templates/*.html for full functionality and conformity, producing validation_report.md and final corrected app.py and templates",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "AppValidator runs syntax and runtime validation on app.py and templates/*.html and writes validation_report.md; "
        "FinalFixer applies fixes and refinements to app.py and templates/*.html until all issues are resolved."
    ),
    team: list = [
        {
            "agent_name": "AppValidator",
            "role": (
                "Validate that app.py and templates/*.html are syntactically correct, implement all pages, routes, and element IDs exactly as specified, "
                "properly read/write local text files for data, and that the app starts correctly at the Dashboard page; produce validation_report.md."
            ),
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationDeveloper"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationDeveloper"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "FinalFixer",
            "role": (
                "Apply corrections and improvements from validation_report.md to app.py and templates/*.html, ensuring compliance with all requirements "
                "and flawless operation, producing the final application artifacts."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "AppValidator"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationDeveloper"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationDeveloper"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "AppValidator",
            "reviewer_agent": "FinalFixer",
            "review_criteria": "Ensure validation_report.md identifies all functional gaps, syntax and runtime errors, and verifies exact element IDs and data file operations.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "FinalFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": "Confirm final app.py and templates/*.html fully resolve validation issues and remain consistent with original requirement coverage.",
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
    goal: str = "Develop a complete RealEstate Flask web application with precise page navigation, element IDs, and local text file data management as specified.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce design specification document.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce the complete design specification including pages, elements, routes, and data contracts."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the Flask application and templates from design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Implement the draft application and templates then produce final app.py and templates."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and refine the final application for full functionality and compliance.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and correct the Flask app and templates to final form."}
            ]
        }
    ]
): pass
# Orchestrate_End