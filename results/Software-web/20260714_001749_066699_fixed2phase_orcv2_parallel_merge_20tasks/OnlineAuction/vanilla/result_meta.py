# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend designs for the OnlineAuction web app and merge into one consistent design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect specifies Flask routes, data models from auctions, bids, winners, and items, and data management logic into backend_design.md. "
        "FrontendDesignArchitect defines HTML templates with exact element IDs and page structures for the 9 application pages into frontend_design.md. "
        "DesignMerger consumes backend_design.md and frontend_design.md plus the user task description to reconcile and write a coherent design_spec.md without deviation."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Specify Flask backend route architecture, data file access, data schemas, and logic for managing auction, bid, winner, and trending text files.",
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
            "role": "Design HTML template structure, element IDs, navigation flow, and page layout for dashboard, auction catalog, bid history, and other pages with given element details.",
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
            "role": "Reconcile backend_design.md and frontend_design.md creating one internal-consistent design_spec.md that fulfills all user requirements without adding new ones.",
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
            "review_criteria": "Check backend design completeness and correctness against user task and compatibility with frontend design.",
            "review_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend design adherence to user requirements and backend design integration feasibility.",
            "review_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend logic and frontend templates in parallel from design_spec.md, then integrate into final app.py and templates/*.html",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements app.py with routing, data loading, and business logic per design_spec.md. "
        "FrontendDeveloper implements all HTML templates for 9 pages with specified element IDs and navigation per design_spec.md. "
        "IntegrationMerger integrates app.py and frontend templates ensuring interface correctness and produces the final app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Implement app.py including all Flask routes, business logic for auctions, bids, winners, categories, trending, and file data management from design_spec.md.",
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
            "role": "Develop all HTML templates for the 9 described pages using exact element IDs and layout specified in design_spec.md.",
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
            "role": "Merge app.py and templates/*.html correcting interface mismatches and produce final executable app.py and frontend templates bundle.",
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
            "review_criteria": "Verify backend implementation matches route, data handling, and business logic in design_spec.md precisely.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify frontend templates conform to design_spec.md element IDs, layout, and navigation requirements.",
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
    goal: str = "Develop the OnlineAuction Python Flask web application with local text file data management, full frontend templates, and backend logic per user requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel backend and frontend design followed by merging into a single consistent specification.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce a coherent merged design specification document for backend and frontend."}
            ]
        },
        {
            "step": 2,
            "description": "Parallel implementation of backend logic and frontend templates followed by integration into final executable files.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Produce final integrated backend app.py and frontend templates per design specification."}
            ]
        }
    ]
): pass
# Orchestrate_End