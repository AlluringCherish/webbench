# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend design specifications for the VirtualMuseum app and merge them into a consistent design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect designs Flask routes, data schemas, and local text file usage based on the user task description; "
        "FrontendDesignArchitect designs the HTML templates with exact element IDs, navigation, and page structures based on the user task; "
        "DesignMerger consolidates backend_design.md and frontend_design.md into one consistent design_spec.md without adding requirements."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design the Flask backend architecture including routes, data models for local text files, and business logic contracts.",
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
            "role": "Design detailed HTML template specifications including page layout, exact element IDs, navigation, and interactive elements.",
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
            "role": "Merge backend and frontend design specifications into a single coherent design_spec.md verifying consistency with user requirements.",
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
            "review_criteria": "Verify completeness and correctness of backend design according to user task and integration consistency.",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend design aligns with user task, includes exact element IDs and navigation consistent with backend.",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend Flask app.py and frontend HTML templates concurrently based on design_spec.md and integrate them into a final deployable application",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements app.py according to backend specifications in design_spec.md; "
        "FrontendDeveloper implements all HTML templates with exact IDs and navigation per frontend design_spec.md; "
        "IntegrationMerger integrates and reconciles app.py and templates/*.html ensuring interface consistency and readiness for deployment."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Implement the Flask backend application app.py using the routes, data model, and logic contract defined in design_spec.md with local text file management.",
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
            "role": "Create all required HTML templates with exact element IDs, page layouts, and navigation as specified in design_spec.md including all 7 pages.",
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
            "role": "Integrate implementations from app.py and templates/*.html ensuring interface compliance, fix inconsistencies and produce final app.py and templates/*.html for deployment.",
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
            "review_criteria": "Check that backend implementation conforms to the backend portions of design_spec.md and is consistent with frontend.",
            "review_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify frontend templates conform exactly to design_spec.md including element IDs and navigation coherence with backend.",
            "review_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the VirtualMuseum Python Flask web application with seven pages, local text file data management, and precise frontend element IDs as specified",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel backend and frontend design specification creation and merging.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Merged backend and frontend design specification"}
            ]
        },
        {
            "step": 2,
            "description": "Parallel backend and frontend implementation and integration merging.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Merged backend and frontend implementation ready for deployment"}
            ]
        }
    ]
): pass
# Orchestrate_End