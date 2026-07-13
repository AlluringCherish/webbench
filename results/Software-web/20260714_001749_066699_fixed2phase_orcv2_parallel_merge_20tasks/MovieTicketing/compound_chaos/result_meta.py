# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend design specifications and merge them into a consistent design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = "BackendDesignArchitect defines Flask routes, data schemas and business logic contracts; FrontendDesignArchitect specifies HTML templates, element IDs, context variables and navigation details independently; DesignMerger consolidates both designs into design_spec.md ensuring consistency and compliance with user requirements.",
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design the Flask backend routes, data schemas, and operations to support all user functionalities according to the requirements, ensuring correct interaction with local text data files.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "agent_name": "FrontendDesignArchitect",
            "role": "Design the HTML page templates with exact element IDs, context variables, and navigation per the page specifications in the user task, ensuring usability and completeness.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        },
        {
            "agent_name": "DesignMerger",
            "role": "Merge backend_design.md and frontend_design.md into a single consistent design_spec.md, verifying alignment with user requirements and resolving any discrepancies without adding features.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "backend_design.md", "source": "BackendDesignArchitect"},
                {"type": "text_file", "name": "frontend_design.md", "source": "FrontendDesignArchitect"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "BackendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify backend design completeness, correctness, and compliance with requirements; ensure no conflicts with frontend design.",
            "review_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend design completeness, correctness, element IDs, and navigation flows; ensure no conflicts with backend design.",
            "review_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend and frontend code independently from design_spec.md and merge them into complete functional app.py and templates/*.html",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = "BackendDeveloper implements Flask app.py features according to backend design; FrontendDeveloper implements templates/*.html per frontend design; IntegrationMerger merges and reconciles both implementations for functional correctness and interface consistency.",
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Implement the Flask backend in app.py including all routes, data reads/writes to local text files, and business logic as specified in design_spec.md.",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"}
            ]
        },
        {
            "agent_name": "FrontendDeveloper",
            "role": "Implement the HTML templates located in templates/*.html with exact element IDs, layout, and dynamic placeholders as specified in design_spec.md.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "templates/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationMerger",
            "role": "Merge and reconcile app.py and templates/*.html with design_spec.md, identify and correct interface inconsistencies without adding features, producing final usable application code.",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"},
                {"type": "text_file", "name": "app.py", "source": "BackendDeveloper"},
                {"type": "text_file", "name": "templates/*.html", "source": "FrontendDeveloper"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "BackendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Check backend implementation against design_spec.md, verify routes, logic, and text file data handling correctness.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Check frontend templates against design_spec.md, verifying element IDs, dynamic data placeholders, layout, and navigation.",
            "review_artifacts": [
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the full MovieTicketing Python Flask web application with local text data storage according to detailed user requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Design backend and frontend specifications in parallel and merge into design_spec.md.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Build merged backend and frontend design specification document."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement backend and frontend in parallel and merge into final app.py and templates/*.html.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Build merged implementation of backend and frontend code."
                }
            ]
        }
    ]
): pass
# Orchestrate_End