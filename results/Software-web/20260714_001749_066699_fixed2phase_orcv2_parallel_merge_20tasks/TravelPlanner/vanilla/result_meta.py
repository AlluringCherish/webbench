# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend design specifications for TravelPlanner and merge them into a coherent design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect and FrontendDesignArchitect independently produce backend_design.md and frontend_design.md based on the user task. "
        "DesignMerger consumes both specifications along with the original user task and produces the merged design_spec.md ensuring internal consistency."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design Python Flask backend routes, data models, and local text file data schema for TravelPlanner based on the requirements.",
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
            "role": "Specify HTML templates, element IDs, user interface layout, and navigation flows for TravelPlanner's pages according to the requirements.",
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
            "role": "Merge backend_design.md and frontend_design.md into a unified, internally consistent design_spec.md without adding new requirements or features.",
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
            "review_criteria": "Verify backend design completeness and adherence to user requirements for TravelPlanner backend architecture.",
            "review_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend design completeness and adherence to user requirements for TravelPlanner UI and element IDs.",
            "review_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend Flask app.py and frontend HTML templates in parallel based on design_spec.md and merge them into final runnable files",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements the app.py Flask backend based on design_spec.md; FrontendDeveloper implements templates/*.html based on design_spec.md. "
        "IntegrationMerger reconciles both implementations into final app.py and templates/*.html ensuring interface consistency."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Develop the Python Flask app.py implementing backend routes, data loading, and logic per design_spec.md for TravelPlanner.",
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
            "role": "Create HTML templates in templates/*.html implementing UI structure, exact element IDs, and navigation based on design_spec.md for TravelPlanner.",
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
            "role": "Merge app.py and templates/*.html ensuring their interface is consistent with design_spec.md and produce final deployable files.",
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
            "review_criteria": "Review backend code app.py for conformance with design_spec.md and correct any interface mismatches.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Review frontend templates/*.html for conformance with design_spec.md and correct any interface mismatches.",
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
    goal: str = "Develop the TravelPlanner Python Flask web application with required pages, local text data storage, and exact element IDs",
    workflow: list = [
        {
            "step": 1,
            "description": "Design complementary backend and frontend specifications and merge them into a unified design specification.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Merged backend and frontend design specification for TravelPlanner"
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement backend and frontend from design specification in parallel and merge into final deployable files.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Merged implementation and integration of backend and frontend for TravelPlanner"
                }
            ]
        }
    ]
): pass
# Orchestrate_End