# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend design specifications for 'BookstoreOnline' and merge them into one consistent design_spec.md",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect designs the Flask routes and data schemas, including local text file formats and data handling requirements. "
        "FrontendDesignArchitect designs the HTML templates, element IDs, navigation, and page structure as per the specifications. "
        "DesignMerger consolidates backend_design.md and frontend_design.md ensuring consistency with the user task and outputs design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Specify Flask routes, data management from local text files, and backend logic details matching the 'BookstoreOnline' user requirements.",
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
            "role": "Specify all HTML templates with exact element IDs and page navigation flows including all nine pages specified by the user task.",
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
            "role": "Merge backend_design.md and frontend_design.md into one coherent design_spec.md ensuring all user requirements are met and no contradictions exist.",
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
            "review_criteria": "Ensure backend design completeness and alignment with user requirements.",
            "review_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Ensure frontend design completeness and alignment with user requirements.",
            "review_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend and frontend artifacts from design_spec.md in parallel and integrate them into a consistent 'BookstoreOnline' application",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements app.py using backend specifications from design_spec.md including data management from local text files. "
        "FrontendDeveloper implements all HTML templates (*.html) including all required pages and element IDs. "
        "IntegrationMerger reconciles app.py and templates/*.html ensuring interface consistency and produces final deployable app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Implement the Flask app.py backend logic and routes according to the backend design specified in design_spec.md, managing all local text file data operations.",
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
            "role": "Implement all HTML templates (*.html) with exact element IDs and navigation as specified in design_spec.md for the 'BookstoreOnline' application.",
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
            "role": "Review and merge app.py and templates/*.html outputs to ensure backend and frontend interface consistency; produce final integrated app.py and templates/*.html.",
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
            "review_criteria": "Validate backend implementation against design_spec.md and integration interface.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Validate frontend HTML templates against design_spec.md and integration interface.",
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
    goal: str = "Develop the 'BookstoreOnline' Python Flask web application with complete backend and frontend, integrated and verified",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel complementary design of backend and frontend specifications and merging into design_spec.md.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce a merged backend and frontend design specification"
                }
            ]
        },
        {
            "step": 2,
            "description": "Parallel implementation of backend and frontend from design_spec.md and integration into final app.py and templates/*.html.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Produce final integrated backend and frontend code"
                }
            ]
        }
    ]
): pass
# Orchestrate_End