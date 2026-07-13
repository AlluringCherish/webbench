# Phase1_Start
def design_specification_phase(
    goal: str = "Define backend data structures and API endpoints, frontend HTML templates and UI element IDs for all 8 pages, and merge into a comprehensive design specification document 'design_spec.md'.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect designs Python backend data reading/writing logic and Flask routes based on data files and user features; "
        "FrontendDesignArchitect designs the HTML template structure, element IDs, navigation, and visual layout for all 8 pages; "
        "DesignMerger merges backend_design.md and frontend_design.md with user task constraints into a consistent design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Specify Flask routes, data loading, data schema handling for all user stories based on the local text files in 'data' directory.",
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
            "role": "Specify the HTML templates with exact element IDs, page structure, navigation flow, and UI components for all 8 pages.",
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
            "role": "Integrate backend and frontend design documents into a single coherent design_spec.md ensuring full coverage and consistency without adding new requirements.",
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
            "review_criteria": "Verify that backend_design.md comprehensively specifies all Flask routes, data access, and processing according to requirements.",
            "review_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify that frontend_design.md covers all 8 pages with correct element IDs and navigation per user requirements.",
            "review_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement the Python Flask backend and all HTML frontend templates per design_spec.md, then verify consistency and integration correctness in final app.py and templates/*.html.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper builds app.py implementing all Flask routes, data file access, and logic per design_spec.md; "
        "FrontendDeveloper implements HTML templates with specified IDs and navigation per design_spec.md; "
        "IntegrationMerger integrates and verifies backend and frontend implementations, resolves interface inconsistencies, and produces final deliverables app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Implement the Flask app.py file with all required routes, data handling from local text files, and business logic as specified in design_spec.md.",
            "tools": ["write_text_file"],
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
            "role": "Implement HTML templates named templates/*.html with all required pages, exact element IDs, and UI components per design_spec.md.",
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
            "role": "Integrate backend app.py and HTML templates ensuring interface consistency, route-template alignment, and correctness; produce final app.py and templates/*.html deliverables.",
            "tools": ["write_text_file"],
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
            "review_criteria": "Check backend app.py implementation matches design_spec.md routes, data logic, and structure.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Check frontend templates/*.html fully conform to design_spec.md required IDs, markup, and navigation.",
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
    goal: str = "Develop a Python Flask RealEstate web application implementing all features, pages, and local text data management as per user requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Create backend and frontend design specifications in parallel and merge into a unified design.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce comprehensive backend and frontend design documents merged into design_spec.md."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement backend and frontend code in parallel from design_spec.md and merge into final deliverables.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Produce final app.py and templates/*.html implementing requirements."
                }
            ]
        }
    ]
): pass
# Orchestrate_End