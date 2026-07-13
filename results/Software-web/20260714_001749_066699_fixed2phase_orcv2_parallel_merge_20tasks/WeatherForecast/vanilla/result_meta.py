# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend design documents and merge them into a unified design_spec.md for the WeatherForecast web application.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect and FrontendDesignArchitect independently prepare backend and frontend design specs respectively from the user task. "
        "DesignMerger reconciles and merges backend_design.md and frontend_design.md into a single coherent design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": "Specify Flask routes, data schemas, file storage handling, and backend API structure conforming to WeatherForecast requirements.",
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
            "role": (
                "Design HTML templates, element IDs, navigation flow, UI components, and interactive elements "
                "for all 8 pages of the WeatherForecast app based on user requirements."
            ),
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
            "role": (
                "Integrate backend_design.md and frontend_design.md, ensuring no conflicting specs and producing a single comprehensive design_spec.md "
                "that precisely matches the user task without adding or omitting requirements."
            ),
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
            "review_criteria": "Ensure backend_design.md fully covers all backend requirements, adheres to user specifications and data storage formats.",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Validate frontend_design.md for completeness of UI element IDs, page flows, accessibility, and compliance with user task.",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement backend app.py and frontend HTML templates in parallel from design_spec.md and integrate them into a final consistent application bundle.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper and FrontendDeveloper independently implement backend Python app.py and frontend HTML templates respectively using design_spec.md. "
        "IntegrationMerger reconciles and integrates their artifacts into a consistent app.py and templates/*.html set."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": "Implement the backend Python Flask application (app.py) following the backend API design and data contracts defined in design_spec.md.",
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
            "role": "Implement the frontend HTML templates (*.html) with specified element IDs, navigation, and UI components as outlined in design_spec.md.",
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
            "role": (
                "Examine app.py and templates/*.html for interface and routing consistency, merging them into final deployable files, "
                "resolving only inconsistencies without adding new features."
            ),
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
            "review_criteria": (
                "Verify app.py implementation adheres to backend design contracts and data format specifications outlined in design_spec.md."
            ),
            "review_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": (
                "Confirm HTML templates conform exactly to UI element IDs, page structure, and navigation rules specified in design_spec.md."
            ),
            "review_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the Python-based WeatherForecast web application with backend, frontend, and local text data storage as per user requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel design of backend and frontend specifications and merging into a single design document.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce a unified design specification for the complete WeatherForecast web app."
                }
            ]
        },
        {
            "step": 2,
            "description": "Parallel implementation of backend and frontend based on design_spec.md and integration into the final application.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Build and integrate backend app.py and frontend HTML templates into final deployables."
                }
            ]
        }
    ]
): pass
# Orchestrate_End