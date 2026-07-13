# Phase1_Start
def design_specification_phase(
    goal: str = "Define and merge comprehensive backend and frontend specifications for the JobBoard web application as complementary design documents and a unified design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = "BackendDesignArchitect and FrontendDesignArchitect independently produce backend and frontend design documents describing routes, data schemas, pages, and UI elements. DesignMerger merges these documents into one coherent design_spec.md ensuring internal consistency and alignment with user requirements.",
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design the Flask backend architecture, including route handlers, data schemas reflecting the required local text file formats, and business logic for JobBoard features.",
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
            "role": "Design the frontend layout and HTML templates with explicit element IDs and page structures for all specified JobBoard pages, ensuring navigation flows and UI elements per requirements.",
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
            "role": "Integrate backend_design.md and frontend_design.md into a single, internally consistent design_spec.md covering backend routes, data formats, and frontend templates with element IDs, aligned fully to user requirements without adding new features.",
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
            "review_criteria": "Verify completeness and correctness of backend routes, data schemas, and business logic for JobBoard functionality.",
            "review_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend page designs and element IDs match user requirements and complement the backend architecture.",
            "review_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend and frontend components in parallel per design_spec.md, then integrate into final app.py and templates/*.html files",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = "BackendDeveloper and FrontendDeveloper independently implement backend app.py and frontend templates/*.html from design_spec.md; IntegrationMerger reconciles and integrates their outputs into final deployable artifacts.",
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Develop app.py implementing Flask backend with all routes, data loading/saving from local text files, and business logic as specified in design_spec.md.",
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
            "role": "Develop complete set of HTML templates (*.html) for all JobBoard pages with specified element IDs and navigation, according to design_spec.md.",
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
            "role": "Merge app.py and templates/*.html ensuring consistent interfaces, routing, and UI linkage, producing final integrated backend and frontend codified as app.py and templates/*.html.",
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
            "review_criteria": "Check backend implementation correctness, route completeness, compliance with design_spec.md, and data management accuracy.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify frontend templates match design_spec.md element IDs, page structure, and navigation requirements.",
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
    goal: str = "Design and build the JobBoard Python Flask web application with all specified pages and local text file data management, producing final app.py and templates.",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel backend and frontend design and merge into unified design specification.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce merged backend and frontend design specification for JobBoard"}
            ]
        },
        {
            "step": 2,
            "description": "Parallel backend and frontend implementation followed by integration into deployable artifacts.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Implement merged JobBoard backend and frontend and integrate"}
            ]
        }
    ]
): pass
# Orchestrate_End