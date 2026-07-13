# Phase1_Start
def design_specification_phase(
    goal: str = "Design comprehensive backend routes and frontend HTML templates reflecting all pages and specified element IDs; produce merged design specification document.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect defines the Flask routes, data handling flows, and input/output data schemas for all specified pages and data files;"
        "FrontendDesignArchitect specifies HTML templates, with correct element IDs, page layouts, and navigation for all application pages;"
        "DesignMerger reviews and merges backend_design.md and frontend_design.md into a single, consistent design_spec.md ensuring coherence and compliance to the user requirements."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design Flask backend architecture including routes, local text file data management, input/output schemas, and route-based logic for all pages with necessary route parameters.",
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
            "role": "Design frontend HTML templates defining page structure, exact element IDs for components, navigation flows, and data-binding placeholders for all specified pages.",
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
            "role": "Consolidate backend_design.md and frontend_design.md into a consistent, complete design_spec.md reflecting all functionalities, UI elements, and data flows without adding new requirements.",
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
            "review_criteria": "Verify backend design covers all routes, data storage schema, and specifications as per user requirements.",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend design matches element IDs, page layouts, and navigation requirements.",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend Flask app.py and frontend HTML templates in parallel from design_spec.md, then merge and integrate them into a consistent working web application.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements the Flask app.py file with routes, logic, and data file management strictly following design_spec.md;"
        "FrontendDeveloper creates all required HTML templates with correct element IDs and structures as specified in design_spec.md;"
        "IntegrationMerger reconciles the backend and frontend components, resolves interface mismatches, and produces integrated app.py and templates/*.html ensuring functional consistency."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Develop the app.py Flask backend implementing all routes, data file interactions, form handling, and required logic following design_spec.md.",
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
            "role": "Create all HTML templates with correct element IDs, page layouts, and navigation patterns following design_spec.md.",
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
            "role": "Merge app.py and HTML templates per design_spec.md; resolve interface mismatches, correct minor inconsistencies, and produce final integrated app.py and templates/*.html files.",
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
            "review_criteria": "Check app.py conforms precisely to design_spec.md routes, data access, and requirements.",
            "review_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Check HTML templates conform completely to design_spec.md element IDs, structure, and navigation.",
            "review_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        }
    ]
): pass
# Phase2_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the 'PetAdoptionCenter' Python Flask web application with all specified pages, elements, and local text file data management as detailed in user requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel comprehensive design of backend architecture and frontend templates followed by merged design specification creation.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Merged backend and frontend design specification."}
            ]
        },
        {
            "step": 2,
            "description": "Parallel implementation of backend and frontend followed by integration merging into final app.py and templates.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Merged implementation of backend Flask app and frontend HTML templates."}
            ]
        }
    ]
): pass
# Orchestrate_End