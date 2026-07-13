# Phase1_Start
def design_specification_phase(
    goal: str = "Design the backend data model, Flask routes, and frontend HTML templates with element IDs and page navigation for the ContentPublishingHub application; produce backend_design.md, frontend_design.md, and design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = "BackendDesignArchitect and FrontendDesignArchitect work independently to produce backend_design.md and frontend_design.md respectively based on the user task description; DesignMerger consolidates these into a single consistent design_spec.md document.",
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Design the Flask backend including routes, data models for all data files, and necessary business logic for content management, version control, approvals, scheduling, and analytics.",
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
            "role": "Design HTML templates for all specified pages with exact element IDs, navigation controls, and context variables reflecting the backend design.",
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
            "role": "Combine backend_design.md and frontend_design.md into a single internally consistent design_spec.md that fully addresses user requirements without adding new features.",
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
            "review_criteria": "Check backend_design.md for completeness and clarity in covering routes, data models, and business logic.",
            "review_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Validate frontend_design.md to ensure all page templates, element IDs, and navigation are specified as per user requirements.",
            "review_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement the backend Flask application and frontend templates from design_spec.md, and integrate them into a working ContentPublishingHub application; produce app.py and templates/*.html with fidelity to design",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = "BackendDeveloper and FrontendDeveloper independently implement app.py and HTML templates respectively from design_spec.md; IntegrationMerger reconciles their outputs ensuring interface conformity and produces the final app.py and templates/*.html.",
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Develop app.py implementing all Flask routes, data handling, version control, approvals, content scheduling, and analytics as specified in design_spec.md using local text file data storage.",
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
            "role": "Implement HTML templates with exact element IDs for all described pages in design_spec.md ensuring page structure, navigation, and elements match the specification.",
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
            "role": "Integrate app.py and templates/*.html ensuring routing, context variables, and UI elements interface correctly; resolve inconsistencies and produce the final complete app.py and templates/*.html bundle.",
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
            "review_criteria": "Verify app.py implementation conforms to design_spec.md including correct route handling and local file data management.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify templates/*.html align with design_spec.md including presence of all required element IDs and page navigation structure.",
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
    goal: str = "Build a comprehensive ContentPublishingHub Flask web application with version control, analytics, and scheduling as per the provided specification",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel backend and frontend design and merger.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce merged design_spec.md encapsulating backend and frontend architecture."
                }
            ]
        },
        {
            "step": 2,
            "description": "Parallel implementation of backend and frontend with final integration.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Produce final integrated app.py and templates/*.html that implement the design specification."
                }
            ]
        }
    ]
): pass
# Orchestrate_End