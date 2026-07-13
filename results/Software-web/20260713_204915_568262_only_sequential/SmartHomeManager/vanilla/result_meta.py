# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the SmartHomeManager requirements and produce a detailed design_spec.md with complete page designs, elements, and data storage definitions",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst reads the user task description and writes requirements_analysis.md; then "
        "WebArchitect converts requirements_analysis.md into design_spec.md with explicit page element details, navigation flows, and data formats."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Extract all web application requirements, including pages, elements IDs, navigation, and data storage format from the user task description, "
                "and write a comprehensive requirements_analysis.md."
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
                "Design the overall application architecture and produce design_spec.md from requirements_analysis.md, detailing the exact pages, page titles, "
                "elements with IDs and types, navigation buttons and routes, data file formats, local text file storage paths, and user flows from dashboard as main entry."
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
                "Verify requirements_analysis.md covers all seven pages, element IDs, data file definitions, user flows and matches user task description fully."
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
    goal: str = "Develop the SmartHomeManager Flask web application with page templates and app.py implementing exact routes, navigation, local data storage, "
                "and all page-specific controls as described in design_spec.md",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "ImplementationEngineer writes the Flask app.py and templates/*.html files from design_spec.md, creating all pages, UI elements with correct IDs, and implementing data read/write to local text files. "
        "No front-end or inline templates are allowed; all templates must be separate HTML files."
    ),
    team: list = [
        {
            "agent_name": "ImplementationEngineer",
            "role": (
                "Produce the external Flask application code: app.py defining routes and logic for all seven pages starting at dashboard, and templates/*.html files with all required elements, IDs, buttons, and data controls, "
                "using render_template and file I/O to local text files as per design_spec.md."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
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
            "source_agent": "ImplementationEngineer",
            "reviewer_agent": "DesignChecker",
            "review_criteria": (
                "Verify app.py and templates/*.html implement all pages, routes, element IDs, and local text file storage precisely according to design_spec.md."
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
    goal: str = "Validate the SmartHomeManager app.py and templates/*.html for runtime correctness, Flask compatibility, proper navigation, and data persistence; apply corrections as needed",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "Validator agent tests app.py and templates/*.html by running Flask test client and checking navigation, element presence, and local file data operations; "
        "Fixer agent applies defect fixes and writes final runnable app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "Validator",
            "role": (
                "Run syntax and runtime checks on app.py, test Flask routes and renderings for all pages and elements per design_spec.md, check local text file persistence, and write validation_report.md with issues found."
            ),
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "ImplementationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "ImplementationEngineer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "Fixer",
            "role": (
                "Apply fixes from validation_report.md to app.py and templates/*.html, ensure full adherence to design_spec.md and write final corrected app.py and templates/*.html."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "Validator"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "ImplementationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "ImplementationEngineer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "Validator",
            "reviewer_agent": "Fixer",
            "review_criteria": (
                "Verify validation_report.md contains all actionable findings with runnable repro steps and detailed design trace."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "source_agent": "Fixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": (
                "Verify that final app.py and templates/*.html fully resolve validation issues and adhere strictly to design_spec.md specifications."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "validation_report.md"}
            ]
        }
    ]
): pass
# Phase3_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the SmartHomeManager Flask web application with comprehensive page designs, implementation, and validation ensuring full feature and data compliance.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements and produce detailed design specification.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce detailed design_spec.md with all page, element, navigation, and data storage details."}
            ]
        },
        {
            "step": 2,
            "description": "Implement Flask app and templates according to design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Produce complete app.py and templates/*.html implementing all features and local text file data handling."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and correct app and templates for runtime correctness and design adherence.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Produce fully validated and corrected final app.py and templates/*.html."}
            ]
        }
    ]
): pass
# Orchestrate_End