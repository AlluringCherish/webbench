# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend design specifications for SmartHomeManager and merge them into one consistent design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect and FrontendDesignArchitect independently produce backend_design.md and frontend_design.md respectively "
        "based on the user task description. DesignMerger consumes both designs plus the original user task description, "
        "reconciles them, and produces the merged design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design data models, Flask routes, and backend logic for managing smart home devices, automation, energy reports, and activity logs based on user requirements.",
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
            "role": "Design HTML page structure, element IDs, navigation flow, and UI components for the seven application pages as per the user specifications.",
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
            "role": "Merge backend_design.md and frontend_design.md into a unified design_spec.md ensuring internal consistency and full coverage of user requirements.",
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
            "review_criteria": "Verify backend design completeness and conformance with user requirements and frontend design.",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend design completeness and conformance with user requirements and backend design.",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Independently implement backend app.py and frontend templates then integrate them into the final runnable application",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper and FrontendDeveloper independently implement backend app.py and frontend templates/*.html respectively from design_spec.md. "
        "IntegrationMerger reconciles their outputs, ensures interface consistency, and produces the final app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Implement the Flask backend application app.py including data handling, routing, and business logic per the design_spec.md for SmartHomeManager.",
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
            "role": "Develop HTML templates/*.html files with the specified element IDs and UI structure according to design_spec.md for all seven pages.",
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
            "role": "Integrate app.py and frontend templates ensuring their interfaces are consistent and they collectively satisfy the design_spec.md, producing the final deliverables.",
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
            "review_criteria": "Verify backend implementation code for correctness, completeness, and adherence to design_spec.md.",
            "review_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify frontend templates correctness, element ID accuracy, and conformance to design_spec.md.",
            "review_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the SmartHomeManager Python Flask web application with local text file data management as specified.",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel creation of backend and frontend design specifications, followed by merging into one design_spec.md.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Create a merged design specification covering backend and frontend."}
            ]
        },
        {
            "step": 2,
            "description": "Parallel implementation of backend and frontend based on the merged design specification, followed by integration and finalization.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Implement and integrate backend and frontend into final application."}
            ]
        }
    ]
): pass
# Orchestrate_End