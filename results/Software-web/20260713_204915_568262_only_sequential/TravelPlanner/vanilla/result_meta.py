# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the TravelPlanner requirements and produce a complete design_spec.md detailing all pages, elements, interactions, and data storage specifications.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst writes requirements_analysis.md from user task description; "
        "then WebArchitect reads requirements_analysis.md and writes design_spec.md covering Flask routes, page titles, element IDs, "
        "navigation methods, data contracts for local text files, and interactions."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Extract all user-visible pages, elements, navigation flows, and data specifications into requirements_analysis.md "
                "preserving exact IDs, page titles, and data file formats without adding authentication or hidden features."
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
                "Translate requirements_analysis.md into design_spec.md specifying Flask routes and methods, page titles, element IDs, "
                "template filenames, navigation button actions, and data storage details for local text files in data/*.txt."
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
            "review_criteria": "Ensure requirements_analysis.md covers every user-visible page, exact element IDs, navigation buttons, and data file format as specified.",
            "review_artifacts": [
                {"type": "user", "name": "user_task_description"},
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        },
        {
            "source_agent": "WebArchitect",
            "reviewer_agent": "BackendDeveloper",
            "review_criteria": "Verify design_spec.md is coherent, complete, and ready for implementation including precise Flask routing and data file usage.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_phase(
    goal: str = "Implement the TravelPlanner Flask web application consisting of app_draft.py and templates_draft/*.html from design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "BackendDeveloper writes app_draft.py using design_spec.md with routes, local file data handling, and button navigation; "
        "FrontendDeveloper writes all templates_draft/*.html files implementing page layout, element IDs, forms, and buttons."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": (
                "Develop app_draft.py implementing the Flask backend with exact routes, route methods, reading and writing local text files for data, "
                "and routing button-triggered navigation as described in design_spec.md."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_draft.py"}
            ]
        },
        {
            "agent_name": "FrontendDeveloper",
            "role": (
                "Create templates_draft/*.html files for every page, containing all container divs, buttons, inputs, dropdowns, and other UI elements with correct IDs "
                "and visuals as specified by design_spec.md."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "BackendDeveloper",
            "reviewer_agent": "FrontendDeveloper",
            "review_criteria": "Ensure app_draft.py routes correctly map to templates with proper reading/writing of local text data files.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app_draft.py"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "Tester",
            "review_criteria": "Validate templates_draft/*.html files contain all specified page elements, IDs, and navigation buttons consistent with backend routes.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        }
    ]
): pass
# Phase2_End

# Phase3_Start
def verification_phase(
    goal: str = "Validate and finalize app.py and templates/*.html to ensure a fully functional TravelPlanner application meeting all specifications.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "Tester validates app_draft.py and templates_draft/*.html and produces validation_report.md; "
        "FinalIntegrator implements fixes from the report producing the final app.py and templates/*.html files."
    ),
    team: list = [
        {
            "agent_name": "Tester",
            "role": (
                "Perform syntax, runtime, and functional validation on app_draft.py and templates_draft/*.html, covering routes, navigation, data file interaction, "
                "and UI element presence; produce validation_report.md with actionable findings."
            ),
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "app_draft.py", "source": "BackendDeveloper"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "FrontendDeveloper"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "FinalIntegrator",
            "role": (
                "Apply all fixes from validation_report.md, ensuring final app.py and templates/*.html conform fully to requirements, "
                "routing, and file data handling with no remaining errors."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "Tester"},
                {"type": "text_file", "name": "app_draft.py", "source": "BackendDeveloper"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "FrontendDeveloper"},
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
            "source_agent": "Tester",
            "reviewer_agent": "FinalIntegrator",
            "review_criteria": "Verify that validation_report.md covers all needed fixes and that all issues are actionable and traceable to design_spec.md.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "source_agent": "FinalIntegrator",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": "Confirm final app.py and templates/*.html fully implement design_spec.md and pass all key functional and UI requirements.",
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
    goal: str = "Build the TravelPlanner Flask web application fully implementing the specified pages, data handling, and UI elements per requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce design specification for TravelPlanner app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce complete design_spec.md covering pages, UI, navigation, and data."}
            ]
        },
        {
            "step": 2,
            "description": "Implement Flask backend and frontend templates based on design specifications.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Produce app_draft.py and templates_draft/*.html as draft implementation."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and finalize the TravelPlanner application ensuring correctness and compliance.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Produce final app.py and templates/*.html validated against requirements."}
            ]
        }
    ]
): pass
# Orchestrate_End