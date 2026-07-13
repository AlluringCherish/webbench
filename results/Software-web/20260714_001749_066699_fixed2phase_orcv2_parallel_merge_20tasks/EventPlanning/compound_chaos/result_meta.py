# Phase1_Start
def design_specification_phase(
    goal: str = "Define backend route/data schemas and frontend templates with exact element IDs for EventPlanning app, merging into a unified design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect specifies Flask app routes, data schema, and local text files for event planning features; "
        "FrontendDesignArchitect specifies the HTML templates, including exact element IDs and navigation flow; "
        "DesignMerger consolidates backend_design.md and frontend_design.md into a coherent design_spec.md ensuring no omissions or conflicts."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design Flask backend routes, data models, and file handling for events, venues, tickets, bookings, participants, and schedules with compliance to user task and data formats.",
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
            "role": "Design frontend HTML templates for all eight pages with specified element IDs and consistent navigation structure per the EventPlanning user requirements.",
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
            "role": "Merge backend_design.md and frontend_design.md into a complete design_spec.md document, ensuring consistency, no conflicts, and fidelity to user requirements without adding features.",
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
            "review_criteria": "Verify backend route and data schema completeness and accuracy against the user task.",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend template coverage, element ID accuracy, and navigation compliance with requirements.",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend Flask app.py and frontend HTML templates for EventPlanning from design_spec.md and integrate them into final deliverables",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements app.py based on backend specifications in design_spec.md; "
        "FrontendDeveloper implements HTML templates for all pages according to design_spec.md; "
        "IntegrationMerger combines app.py and templates/*.html ensuring interface consistency and correctness."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Develop the Flask backend app.py implementing all required routes, data management from local text files, and logic for event, ticket, booking, participant, venue, and schedule features.",
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
            "role": "Implement all HTML templates for EventPlanning's eight pages, respecting element IDs, layout, and navigation as specified in design_spec.md.",
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
            "role": "Integrate app.py backend and frontend templates ensuring consistent routes, data flow, page navigation, and element ID usage per design_spec.md; produce the final app.py and templates/*.html deliverables.",
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
            "review_criteria": "Ensure backend implementation correctly follows design_spec.md routes and data access specifications.",
            "review_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Ensure frontend templates match design_spec.md in element IDs, layout, and navigation.",
            "review_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the EventPlanning Python Flask web application with local text file data storage and specified pages starting at Dashboard",
    workflow: list = [
        {
            "step": 1,
            "description": "Design backend routes/data schemas and frontend templates with exact element IDs, merged into a coherent design_spec.md",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Create a unified design specification document for backend and frontend"}
            ]
        },
        {
            "step": 2,
            "description": "Implement backend app.py and frontend templates from design_spec.md and integrate them into final deployable artifacts",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Implement and integrate backend and frontend"}
            ]
        }
    ]
): pass
# Orchestrate_End