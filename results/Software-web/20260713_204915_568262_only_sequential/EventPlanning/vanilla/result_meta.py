# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the user's EventPlanning web app requirements and produce a detailed design_spec.md covering all pages, navigation flow, and data representation.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first produces requirements_analysis.md with detailed page breakdown and data format mapping; "
        "then WebArchitect reads requirements_analysis.md and user task to produce design_spec.md specifying Flask routes, templates, page structure, element IDs, "
        "data files access, navigation actions, and initial format contracts."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Extract detailed UI page specifications, element IDs, data storage formats, and explicit user workflows from the user task description "
                "and write requirements_analysis.md with all page, element, and data details."
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
                "Convert requirements_analysis.md into a Flask-based design_spec.md detailing exact route names, HTTP methods, template filenames, page titles, "
                "element IDs, navigation button targets, data file format access plans, and initial backend logic outline for local file data handling."
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
                "Verify requirements_analysis.md accurately and comprehensively covers all user-visible pages, UI element IDs, navigation links, "
                "and exact data file schema details before design_spec.md creation."
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
    goal: str = "Implement the EventPlanning Flask web app with a runnable app.py and all required templates/*.html files, fully respecting the design_spec.md and user requirements.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "ImplementationAgent first creates app_draft.py and templates_draft/*.html based on design_spec.md; after drafting, IntegrationAgent refines and integrates drafts "
        "into final app.py and templates/*.html ready for execution, enforcing exact routes, element IDs, data file interactions, and navigation."
    ),
    team: list = [
        {
            "agent_name": "ImplementationAgent",
            "role": (
                "Write a complete Flask app_draft.py plus all templates_draft/*.html files with the web app structure, routes, HTTP methods, "
                "page rendering via render_template, requested element IDs, and backend code for local text file data handling as per design_spec.md."
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
            "agent_name": "IntegrationAgent",
            "role": (
                "Integrate app_draft.py and templates_draft/*.html into final app.py and templates/*.html, removing draft placeholders, fixing all broken links, "
                "ensuring Flask renders templates correctly with exact requested routes, element IDs, and data handling from text files."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "ImplementationAgent"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "ImplementationAgent"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "ImplementationAgent",
            "reviewer_agent": "IntegrationAgent",
            "review_criteria": (
                "Ensure app_draft.py and templates_draft/*.html conform fully to design_spec.md and contain all required pages and UI elements "
                "before integration into final app.py and templates."
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
    goal: str = "Validate the final app.py and templates/*.html for syntax, runtime execution, and adherence to the design_spec.md; produce validation_report.md and corrected final files.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "ValidatorAgent first runs static and dynamic validation checks on app.py and templates/*.html and writes validation_report.md; "
        "FixerAgent applies corrections based on report to finalize the app.py and templates."
    ),
    team: list = [
        {
            "agent_name": "ValidatorAgent",
            "role": (
                "Validate syntax and runtime behavior of app.py and correctness of templates/*.html; check for exact route availability, template rendering, "
                "existence of all requested element IDs, navigation buttons functioning, and data file accesses as per design_spec.md."
            ),
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationAgent"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationAgent"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "FixerAgent",
            "role": (
                "Apply necessary fixes from validation_report.md to app.py and templates/*.html; ensure the corrected final artifacts fully comply "
                "with design_spec.md and pass all validation criteria."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationAgent"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationAgent"},
                {"type": "text_file", "name": "validation_report.md", "source": "ValidatorAgent"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "ValidatorAgent",
            "reviewer_agent": "FixerAgent",
            "review_criteria": (
                "Verify validation_report.md thoroughly identifies all missing or incorrect route handlers, elements, navigation, and data handling "
                "issues before fixes are applied."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "source_agent": "FixerAgent",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": (
                "Confirm that final app.py and templates/*.html fully address the validation report and retain full feature coverage of user requirements."
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
    goal: str = "Develop a complete Python Flask web application 'EventPlanning' with local text-file data management and all required features.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements and produce a detailed design specification.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce design_spec.md capturing all pages, navigation, and data format details."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the web application draft and integrate into final runnable code.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Produce final app.py and templates/*.html from design_spec.md."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and correct the final application ensuring full compliance and functionality.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Produce validated final app.py and templates/*.html with validation_report.md."}
            ]
        }
    ]
): pass
# Orchestrate_End