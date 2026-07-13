# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend Flask design specifications and merge them into a unified design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect and FrontendDesignArchitect independently write their respective design sections based on the user task description; "
        "DesignMerger consumes both design documents and user task to produce a consolidated design_spec.md with consistent backend and frontend contracts."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": (
                "Design Flask backend routes, data handling logic, and text-file data access patterns "
                "required by the GymMembership user stories, ensuring endpoints support all pages and features."
            ),
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
            "role": (
                "Design HTML template structure, element IDs, navigation, and interactive elements "
                "to fulfill all GymMembership page requirements, matching backend routes and data context."
            ),
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
            "role": (
                "Reconcile backend_design.md and frontend_design.md against the user task description "
                "to produce a single internally consistent design_spec.md ensuring no feature or element conflicts."
            ),
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
            "review_criteria": "Merge backend design ensuring all backend endpoints and data access conform to user requirements.",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Merge frontend design ensuring all pages, element IDs, and navigation match backend contracts and user requirements.",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend Flask app and frontend templates from design_spec.md and merge into final app.py and HTML templates",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper and FrontendDeveloper independently implement the backend app.py and frontend HTML templates respectively using design_spec.md; "
        "IntegrationMerger combines both implementations correcting interface inconsistencies and produces the canonical app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": (
                "Implement the Flask app.py backend using design_spec.md, including all routes, "
                "local text file data management, and business logic for GymMembership functionalities."
            ),
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
            "role": (
                "Implement HTML templates (*.html) using design_spec.md, including all required pages, element IDs, buttons, navigation, "
                "and UI components for GymMembership frontend."
            ),
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
            "role": (
                "Combine app.py and templates/*.html implementations with design_spec.md, resolving interface inconsistencies, "
                "ensuring backend and frontend harmony, and producing final app.py and templates/*.html files."
            ),
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
            "review_criteria": "Verify backend app.py conforms to design_spec.md routes, data access, and logic correctness.",
            "review_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify frontend templates/*.html conform to design_spec.md element IDs, navigation, and layout.",
            "review_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        }
    ]
): pass
# Phase2_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the GymMembership Python Flask web application with local text file data handling and multi-page UI as per requirements",
    workflow: list = [
        {
            "step": 1,
            "description": "Create complementary backend and frontend design specifications and merge into unified design.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce unified design_spec.md for backend and frontend."}
            ]
        },
        {
            "step": 2,
            "description": "Implement backend Flask app and frontend templates in parallel, then integrate into final application files.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Produce final app.py and templates/*.html implementations."}
            ]
        }
    ]
): pass
# Orchestrate_End