# Phase1_Start
def design_specification_phase(
    goal: str = "Create detailed backend and frontend design specifications for the OnlineLibrary app and merge them into a unified design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = "BackendDesignArchitect and FrontendDesignArchitect independently create backend and frontend design documents respectively; DesignMerger reconciles both into a consistent design_spec.md.",
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design the backend architecture including data management via local text files, Python business logic, routes, data models for users, books, borrowings, reservations, reviews, and fines with appropriate functionality.",
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
            "role": "Design the frontend architecture specifying HTML templates, element IDs for the 10 pages, navigation flows, UI components, and interactive elements based on user requirements.",
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
            "role": "Reconcile backend_design.md and frontend_design.md ensuring a cohesive and internally consistent design_spec.md that fulfills all user requirements without adding or removing features.",
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
        },
    ],
    review_policy: list = [
        {
            "source_agent": "BackendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify backend design completeness and conforming to user task.",
            "review_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend design completeness including page elements and navigation.",
            "review_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend and frontend from design_spec.md in parallel and merge into complete application files app.py and templates/*.html",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = "BackendDeveloper and FrontendDeveloper independently implement backend Flask app and frontend HTML templates using design_spec.md; IntegrationMerger reconciles and integrates their outputs into final app.py and templates/*.html.",
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Implement the Python Flask backend app.py according to backend design details, managing data via local text files in 'data' directory and providing all required routes and logic.",
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
            "role": "Implement HTML templates for all 10 pages with correct element IDs, navigation buttons, and UI components as per frontend design in design_spec.md.",
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
            "role": "Reconcile backend app.py and frontend templates/*.html ensuring consistency with design_spec.md and resolving interface issues, producing final consistent app.py and templates/*.html.",
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
            "review_criteria": "Check backend implementation correctness and compliance with design_spec.md.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Check frontend templates correctness and compliance with design_spec.md.",
            "review_artifacts": [
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the OnlineLibrary Python Flask web app with specified pages, data management, and user functionality using local text files, delivering complete backend and frontend implementations.",
    workflow: list = [
        {
            "step": 1,
            "description": "Create and merge detailed backend and frontend design specifications.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Merged comprehensive design specification document."}
            ]
        },
        {
            "step": 2,
            "description": "Implement backend and frontend independently and integrate into the final app files.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Merged backend and frontend implementation and integration."}
            ]
        }
    ]
): pass
# Orchestrate_End