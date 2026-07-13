# Phase1_Start
def design_specification_phase(
    goal: str = "Create backend and frontend design specifications for the NewsPortal application and merge them into a complete design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect and FrontendDesignArchitect work independently to create backend route and data schema "
        "specifications and frontend page templates with element IDs and navigation. DesignMerger receives backend_design.md "
        "and frontend_design.md and produces a reconciled, internally consistent design_spec.md covering all pages, elements, "
        "and data requirements without introducing new features."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design backend Flask routes, data schema, and text file data handling required for NewsPortal including articles, categories, bookmarks, comments, and trending endpoints.",
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
            "role": "Design frontend HTML templates with exact element IDs, page layouts, navigation, and interactive buttons for all nine pages of NewsPortal.",
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
            "role": "Merge backend_design.md and frontend_design.md into one coherent design_spec.md ensuring interface consistency and coverage of all user requirements without adding features.",
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
            "review_criteria": "Verify backend route and data design completeness and correctness before merging.",
            "review_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend template and element ID accuracy before merging.",
            "review_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend app.py and frontend templates based on design_spec.md and integrate them into a complete runnable NewsPortal application bundle",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements app.py with routes, data handling, and logic per design_spec.md. FrontendDeveloper creates HTML templates/*.html "
        "with exact element IDs, layouts, and navigation from design_spec.md. IntegrationMerger reconciles app.py and templates/*.html ensuring interface "
        "compliance and writes final app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Implement backend app.py including Flask routes, local text file data operations, and all server-side logic as per design_spec.md.",
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
            "role": "Implement frontend HTML templates/*.html with exact element IDs, page layouts, and navigation according to design_spec.md.",
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
            "role": "Merge app.py and templates/*.html, verify interface consistency, and write the final complete app.py and templates/*.html bundle for deployment.",
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
            "review_criteria": "Check backend app.py implementation conformance with design_spec.md including routes and data handling.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Check frontend templates/*.html conform to design_spec.md including exact element IDs and navigation.",
            "review_artifacts": [
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop a comprehensive Python Flask NewsPortal web application with specified pages, exact element IDs, local text file data storage, and navigation",
    workflow: list = [
        {
            "step": 1,
            "description": "Design backend routes and data schema and frontend page templates with element IDs, then merge into comprehensive design spec.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Create merged detailed design specification document for backend and frontend."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement backend app.py and frontend HTML templates independently from design spec, then integrate into runnable application bundle.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Merged backend and frontend implementation producing final application files."
                }
            ]
        }
    ]
): pass
# Orchestrate_End