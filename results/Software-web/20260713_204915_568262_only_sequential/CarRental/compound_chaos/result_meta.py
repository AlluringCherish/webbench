# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the CarRental web application requirements and produce a complete design_spec.md detailing all pages, elements, data files, and interactions.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first produces requirements_analysis.md capturing detailed user requirements; then WebArchitect reads it and writes design_spec.md "
        "covering page structure, element IDs, navigation, data files, file formats, and programmatic constraints."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Extract and document all features, page structures, UI elements, data storage formats, and navigation flows from the user task into requirements_analysis.md."
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
                "Transform requirements_analysis.md into design_spec.md describing the complete Flask application architecture including all 9 pages with exact element IDs, "
                "local data file structures under 'data/', their formats, and navigational flows between pages starting from the Dashboard."
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
                "Verify requirements_analysis.md correctly and comprehensively captures all pages, elements, data formats, and navigation before architecture design."
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
    goal: str = "Implement the CarRental Flask web application with app.py and complete templates/*.html per design_spec.md, managing data via local text files.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "ImplementationEngineer first writes app_draft.py and draft templates_draft/*.html from design_spec.md, then IntegrationEngineer integrates drafts into the final "
        "app.py and templates/*.html ensuring Flask compatibility and all functional requirements."
    ),
    team: list = [
        {
            "agent_name": "ImplementationEngineer",
            "role": (
                "Write a full draft of app_draft.py implementing Flask routes, handlers, and business logic following design_spec.md. Also create templates_draft/*.html for all 9 pages with exact element IDs and UI components."
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
                "Integrate app_draft.py and templates_draft/*.html into final app.py and templates/*.html. Ensure Flask app starts at Dashboard page, routes are correct, and data storage and retrieval from local text files under data/ "
                "matches specified formats with no dependency on drafts."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
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
                "Check app_draft.py and templates_draft/*.html to ensure full coverage of design_spec.md including precise element IDs, routing, and local data file handling before final integration."
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
    goal: str = "Validate and refine the final CarRental Flask app.py and templates/*.html to ensure correctness, complete functionality, and adherence to design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "QualityAssurer validates app.py and templates/*.html against design_spec.md producing validation_report.md; then SequentialFixer applies corrections producing the final validated application."
    ),
    team: list = [
        {
            "agent_name": "QualityAssurer",
            "role": (
                "Perform syntax and runtime checks on app.py. Validate templates/*.html for correct element IDs and page titles. Verify correct handling of all pages, routes, data reading/writing from local text files, and functionality coverage. Write validation_report.md with findings."
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
                "Apply all corrections from validation_report.md to app.py and templates/*.html producing the final release version. Ensure fixes retain complete alignment with the design_spec.md and resolve all validation issues."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "validation_report.md", "source": "QualityAssurer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "QualityAssurer",
            "reviewer_agent": "SequentialFixer",
            "review_criteria": (
                "Confirm validation_report.md accurately identifies all issues and that corrections for final app.py and templates/*.html address these while retaining full feature coverage."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": (
                "Verify that final app.py and templates/*.html fully implement all requirements from validation_report.md and ultimately the original user task."
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
    goal: str = "Build the CarRental Flask web application with specified pages, local text file data management, and complete functional coverage.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements and produce the design_spec.md.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce the comprehensive design specification for the web application."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the application code and templates according to design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Implement the draft and integrate final application artifacts."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and finalize the CarRental web application ensuring full correctness and requirement fulfillment.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and repair the application producing the final deliverables."}
            ]
        }
    ]
): pass
# Orchestrate_End