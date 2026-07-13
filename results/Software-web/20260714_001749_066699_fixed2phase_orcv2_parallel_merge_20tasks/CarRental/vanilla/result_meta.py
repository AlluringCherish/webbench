# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend designs covering Flask routes, data schemas, and all 9 CarRental pages with exact element IDs and local text file data format; produce a consistent merged design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = "BackendDesignArchitect specifies Flask backend routes, data management, and business logic in backend_design.md; FrontendDesignArchitect specifies HTML templates, element IDs, layout, and navigation in frontend_design.md; DesignMerger consolidates these two documents into a unified design_spec.md meeting all user requirements.",
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design the Flask backend architecture covering routes for all required pages, data reading/writing from local text files, and business logic for search, booking, reservations, insurance, and special requests.",
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
            "role": "Design the frontend HTML templates specifying the exact element IDs, page layouts, and UI components for all 9 CarRental pages with navigation and data placeholders.",
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
            "role": "Merge backend_design.md and frontend_design.md to produce one coherent design_spec.md ensuring consistency of routes, page elements, naming conventions, and data schemas without adding new features.",
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
            "review_criteria": "Validate completeness and correctness of backend routes and data schema design per user requirements.",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Validate frontend element IDs, page structure, and compliance with all UI requirements.",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend app.py and frontend templates for all 9 pages based on design_spec.md and merge them into a working CarRental application with matching interfaces and pages",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = "BackendDeveloper implements app.py following backend design rules; FrontendDeveloper creates templates/*.html for all pages per frontend design; IntegrationMerger integrates both producing final app.py and templates/*.html ensuring interface consistency.",
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Implement app.py with Flask routes, business logic, and local text file data handling as specified in design_spec.md for vehicle management, bookings, reservations, insurance, and special requests.",
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
            "role": "Implement HTML templates for all CarRental pages with exact element IDs, page structure, and UI per design_spec.md in templates/*.html files.",
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
            "role": "Merge app.py and templates/*.html ensuring consistent interfaces, matching element IDs, route correctness and write final app.py and templates/*.html files for deployment without adding new features.",
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
            "review_criteria": "Verify app.py implementation correctly follows design_spec.md, including routes and data handling.",
            "review_artifacts": [{"type": "text_file", "name": "app.py"}, {"type": "text_file", "name": "design_spec.md"}]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify templates/*.html match design_spec.md element IDs and page layouts exactly.",
            "review_artifacts": [{"type": "text_file", "name": "templates/*.html"}, {"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the CarRental Flask web application with backend and frontend fully integrated from the user requirements with local text data storage",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel design of backend and frontend specifications, merged into one design document.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Create complete backend and frontend design and merge into one spec."}
            ]
        },
        {
            "step": 2,
            "description": "Parallel implementation of backend and frontend, merged into the final working app and templates.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Implement and integrate backend and frontend code based on the design spec."}
            ]
        }
    ]
): pass
# Orchestrate_End