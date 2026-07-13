# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend design specifications for the FoodDelivery web application and merge them into one consistent design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect specifies Flask routes, data schema, and local text file data management; "
        "FrontendDesignArchitect specifies HTML templates, element IDs, context variables, and navigation. "
        "DesignMerger reconciles backend_design.md and frontend_design.md into a single design_spec.md delivering a consistent design aligned to the user task."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design the Flask backend routes, API endpoints, data handling logic, and define data models using local text files for FoodDelivery application.",
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
            "role": "Design the frontend HTML templates with exact element IDs, page structure, navigation flow, and user interface details for FoodDelivery application.",
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
            "role": "Integrate backend_design.md and frontend_design.md into a unified and internally consistent design_spec.md aligned precisely to FoodDelivery user requirements.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "backend_design.md", "source": "BackendDesignArchitect"},
                {"type": "text_file", "name": "frontend_design.md", "source": "FrontendDesignArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
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
            "review_criteria": "Verify backend design completeness, consistency with user requirements, and accuracy of route and data model definitions.",
            "review_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend design alignment with user requirements, correct element IDs, page navigation, and template structure.",
            "review_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend and frontend artifacts in parallel from design_spec.md and merge them to produce final app.py and templates with verified interface consistency",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements app.py based on the design_spec.md backend contract; "
        "FrontendDeveloper implements all HTML templates with exact element IDs and navigation from design_spec.md frontend contract; "
        "IntegrationMerger reconciles app.py and templates/*.html with design_spec.md, ensuring full interface consistency and correctness."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Implement the Flask backend app.py with all required routes, local text data handling, and business logic as per design_spec.md.",
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
            "role": "Implement HTML templates with exact element IDs, navigation, and UI components for FoodDelivery as per design_spec.md.",
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
            "role": "Merge and reconcile app.py backend and templates frontend implementations ensuring full conformance to design_spec.md, correcting interface mismatches without adding features.",
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
            "review_criteria": "Check that app.py fully implements the backend routes, data handling, and logic per design_spec.md.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify that all frontend templates meet the design_spec.md element ID, navigation flow, and UI specifications.",
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
    goal: str = "Build the FoodDelivery Python Flask web application with specified pages and local text file data storage as detailed in the user requirements",
    workflow: list = [
        {
            "step": 1,
            "description": "Design backend and frontend specifications in parallel and merge into a unified design_spec.md",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce unified design specification for backend and frontend"}
            ]
        },
        {
            "step": 2,
            "description": "Implement backend and frontend in parallel from design_spec.md and merge into final app.py and templates",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Produce final backend app.py and frontend templates with guaranteed interface consistency"}
            ]
        }
    ]
): pass
# Orchestrate_End