# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the 'OnlineCourse' web application requirements and produce a comprehensive design_spec.md detailing pages, routes, elements, navigation, and data storage.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md covering all pages, elements, functionality, and data file specs; "
        "only after completion, WebArchitect reads requirements_analysis.md and produces design_spec.md detailing Flask app routes, "
        "template structure, data storage contracts, and UI element IDs."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Extract detailed requirements from user task for each page including exact page titles, element IDs, UI components, navigation "
                "flows, and data file formats; write requirements_analysis.md."
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
                "Convert requirements_analysis.md into design_spec.md by specifying Flask routes, HTTP methods, templates filenames and layout, "
                "page rendering contracts, element IDs with exact naming, and data interface details for text files in the data/ directory."
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
                "Validate that requirements_analysis.md fully captures all user requirements including page titles, element IDs, navigation, "
                "functionality details, and data file schemas before architecture creation."
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
    goal: str = "Implement the 'OnlineCourse' web application as a Flask app.py and templates/*.html based on design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer writes app_draft.py and all templates_draft/*.html files using design_spec.md specifications; "
        "upon completion, IntegrationEngineer converts drafts to final app.py and templates/*.html ensuring all routes, elements, "
        "and data persistence with local text files per design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "role": (
                "Create app_draft.py implementing all specified Flask routes and logic for user authentication, course browsing, enrollment, "
                "assignment submission, progress tracking, and certificate generation. Also create templates_draft/*.html files with exact "
                "page titles, element IDs, and UI structure as designed."
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
                "Integrate app_draft.py and templates_draft/*.html into final app.py and templates/*.html, ensuring all code and templates align "
                "with design_spec.md requirements, support local text file data storage, handle navigation and user actions properly, and "
                "remove all draft references."
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
                "Check that app_draft.py and templates_draft/*.html correctly implement all design_spec.md requested routes, templates, UI elements, "
                "and data persistence before producing final app.py and templates/*.html."
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
    goal: str = "Validate and verify the final app.py and templates/*.html for syntax, runtime correctness, and requirement conformance.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator runs syntax and runtime validation on app.py, checks templates/*.html for all required elements and page titles, "
        "and produces validation_report.md; after validation, SequentialFixer applies fixes and creates the final validated app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "role": (
                "Perform syntax and runtime validation of app.py with all routes; verify templates/*.html contain all required element IDs, page titles, "
                "and UI structure; execute sample navigation and data persistence tests; write validation_report.md detailing issues found."
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
                "Address all issues logged in validation_report.md and revise app.py and templates/*.html accordingly. Ensure the final "
                "application meets full functional and UI requirements and passes validation criteria."
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
                "Verify validation_report.md accurately documents all issues with app.py and templates/*.html, and that fixes applied resolve them."
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
                "Confirm that the final app.py and templates/*.html fully implement all user requirements as captured in requirements_analysis.md "
                "and design_spec.md with no regressions."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "requirements_analysis.md"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase3_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the 'OnlineCourse' Flask web application with local text file data storage fulfilling all specified user requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements and produce comprehensive design specification.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce detailed page, route, template, and data design."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the Flask app and HTML templates based on design specification.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Develop app.py and templates/*.html implementing all features and UI."}
            ]
        },
        {
            "step": 3,
            "description": "Validate, test, and apply fixes to produce final validated web application.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Validate and fix app.py and templates/*.html for production readiness."}
            ]
        }
    ]
): pass
# Orchestrate_End