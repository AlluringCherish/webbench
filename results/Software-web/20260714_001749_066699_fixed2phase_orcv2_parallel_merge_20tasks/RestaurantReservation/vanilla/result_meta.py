# Phase1_Start
def design_specification_phase(
    goal: str = "Create backend and frontend design specifications for the RestaurantReservation web application and merge them into a consistent design_spec.md document",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect designs Flask backend routes, data models, and file interactions based on the user task; "
        "FrontendDesignArchitect designs HTML templates with exact element IDs and navigations; "
        "DesignMerger reconciles backend and frontend designs into a unified design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design Flask backend routes, data schemas, and text file data parsing/writing specifications for RestaurantReservation app",
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
            "role": "Design HTML templates with exact element IDs, page layouts, navigation flows, and context variables for RestaurantReservation app",
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
            "role": "Merge backend_design.md and frontend_design.md into a single internally consistent design_spec.md without adding new requirements",
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
            "review_criteria": "Verify backend design completeness and alignment with user requirements",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend design completeness and alignment with user requirements",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement the backend app.py and frontend templates for RestaurantReservation app based on design_spec.md and integrate them into final deployable artifacts",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements app.py with routes, data handling, business logic from design_spec.md independently; "
        "FrontendDeveloper implements templates/*.html with all exact element IDs and navigation requirements independently; "
        "IntegrationMerger reconciles backend and frontend for interface consistency and produces the final app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Implement Flask app.py backend including routes, data storage to text files, and business logic as specified in design_spec.md",
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
            "role": "Implement all HTML templates with specified element IDs, layout, and navigation based on design_spec.md",
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
            "role": "Merge and reconcile app.py backend and templates/*.html frontend into final deployable artifacts correcting only interface inconsistencies",
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
            "review_criteria": "Check backend implementation matches design_spec.md and handles all specified data files and routes",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Check frontend templates conform to design_spec.md element IDs and navigation requirements",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the complete RestaurantReservation Python Flask web application with specified pages, data storage, and navigation.",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel backend and frontend design, merging complementary architectural specifications.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce unified backend and frontend design specification document."}
            ]
        },
        {
            "step": 2,
            "description": "Parallel backend and frontend implementation based on design_spec.md and integration into final app.py and templates.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Final implementation and integration of backend and frontend components."}
            ]
        }
    ]
): pass
# Orchestrate_End