# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend designs for the 'OnlineCourse' app and produce a merged design specification document.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect specifies Flask routes, data schema, and business logic from the user task description; "
        "FrontendDesignArchitect specifies HTML templates, element IDs, UI structure, and navigation. "
        "DesignMerger reconciles backend_design.md and frontend_design.md into a consistent design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design and specify the Flask backend routes, data file schemas, enrollment and progress logic, and API contracts conforming to the 'OnlineCourse' requirements.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "agent_name": "FrontendDesignArchitect",
            "role": "Design the frontend page layouts, HTML templates with exact element IDs, navigation flow, and UI details for the nine 'OnlineCourse' pages per requirements.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        },
        {
            "agent_name": "DesignMerger",
            "role": "Merge backend_design.md and frontend_design.md into one coherent design_spec.md ensuring completeness and no conflicting details.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "backend_design.md", "source": "BackendDesignArchitect"},
                {"type": "text_file", "name": "frontend_design.md", "source": "FrontendDesignArchitect"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "BackendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify backend routes, data schemas, and logic completeness for 'OnlineCourse' against requirements.",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Validate frontend templates, element IDs, and navigation flow for accuracy and completeness.",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend and frontend code artifacts from design_spec.md and integrate them into a consistent final web application.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements app.py backend logic independently from design_spec.md; "
        "FrontendDeveloper implements templates/*.html frontend UI independently using design_spec.md; "
        "IntegrationMerger integrates and reconciles backend and frontend artifacts into final app.py and templates/*.html ensuring interface consistency."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Implement app.py Flask backend covering all routes, data file handling, enrollment, progress updates, certificate generation per design_spec.md.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "agent_name": "FrontendDeveloper",
            "role": "Implement all required HTML templates with page structures, element IDs, buttons, and navigation as specified in design_spec.md.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        },
        {
            "agent_name": "IntegrationMerger",
            "role": "Merge and reconcile app.py and templates/*.html to ensure interface conformity, fix interface mismatches, and produce final deployable code artifacts.",
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
            "review_criteria": "Check backend app.py for correct route implementations, data file management, and business logic conformity.",
            "review_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify frontend templates/*.html adhere to design_spec.md including all element IDs and navigation correctness.",
            "review_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop a complete Python Flask web application 'OnlineCourse' with local text file data storage, multiple interactive pages, and full backend/frontend integration based on the user requirements document.",
    workflow: list = [
        {
            "step": 1,
            "description": "Create backend and frontend design specifications and merge into a unified design document.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Merged comprehensive backend and frontend design for OnlineCourse."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement backend and frontend code independently from design; merge and reconcile into final deployable artifacts.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Final integrated backend and frontend implementation for OnlineCourse."
                }
            ]
        }
    ]
): pass
# Orchestrate_End