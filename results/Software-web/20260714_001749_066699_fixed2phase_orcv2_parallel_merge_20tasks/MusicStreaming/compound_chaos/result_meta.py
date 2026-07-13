# Phase1_Start
def design_specification_phase(
    goal: str = "Create complementary backend and frontend design specifications capturing all required Flask routes, data interaction patterns, and HTML template structures with element IDs, then merge into a single consistent design_spec.md document.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDesignArchitect designs detailed Flask route endpoints, data schemas, "
        "and file interaction patterns producing backend_design.md. FrontendDesignArchitect "
        "defines HTML templates, element IDs, UI components, navigation, and filtering mechanisms "
        "producing frontend_design.md. DesignMerger consolidates these two documents into a "
        "unified design_spec.md ensuring consistency and completeness without adding new features."
    ),
    team: list = [
        {
            "agent_name": "BackendDesignArchitect",
            "role": (
                "Design Flask backend structure including routes, data access from local text files, "
                "data schemas based on songs.txt, artists.txt, albums.txt, genres.txt, playlists.txt, "
                "and playlist_songs.txt, API endpoints for searching, playlist management, browsing, "
                "and statistics."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "backend_design.md"}
            ],
        },
        {
            "agent_name": "FrontendDesignArchitect",
            "role": (
                "Design frontend HTML templates with exact element IDs for all ten pages including Dashboard, "
                "catalog, details, playlist management, album browsing, artist profiles, and genre exploration "
                "with navigation and filtering UI."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "frontend_design.md"}
            ],
        },
        {
            "agent_name": "DesignMerger",
            "role": (
                "Merge backend_design.md and frontend_design.md into a coherent design_spec.md, "
                "resolving any inconsistencies, ensuring all required elements and routes are covered "
                "and aligned with the user task."
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
            ],
        }
    ],
    review_policy: list = [
        {
            "source_agent": "BackendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify backend design completeness and correctness per user task and local file data handling.",
            "review_artifacts": [{"type": "text_file", "name": "backend_design.md"}]
        },
        {
            "source_agent": "FrontendDesignArchitect",
            "reviewer_agent": "DesignMerger",
            "review_criteria": "Verify frontend design completeness and correctness of HTML element IDs and page structures.",
            "review_artifacts": [{"type": "text_file", "name": "frontend_design.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Implement the backend app.py and frontend templates/*.html based on design_spec.md and merge into a complete functional Python Flask app with HTML templates.",
    collab_pattern_name: str = "Parallel + Merger",
    collab_pattern_description: str = (
        "BackendDeveloper implements Flask app.py with routes, data loading, and processing per design_spec.md. "
        "FrontendDeveloper implements all HTML templates with specified element IDs and UI features concurrently. "
        "IntegrationMerger reconciles app.py and templates/*.html ensuring interface consistency and writes the final "
        "app.py and all templates."
    ),
    team: list = [
        {
            "agent_name": "BackendDeveloper",
            "role": (
                "Develop the Flask backend in app.py implementing routes, data reading from local text files, "
                "search, playlist management, filters, and statistics as specified in design_spec.md."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"}
            ],
        },
        {
            "agent_name": "FrontendDeveloper",
            "role": (
                "Implement all required HTML templates under templates/*.html with proper element IDs, page layout, "
                "and navigation as per design_spec.md."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignMerger"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "templates/*.html"}
            ],
        },
        {
            "agent_name": "IntegrationMerger",
            "role": (
                "Merge the backend app.py and frontend templates/*.html ensuring interface alignment and consistency "
                "with design_spec.md, correcting integration issues only, and produce final app.py and templates/*.html."
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
            ],
        }
    ],
    review_policy: list = [
        {
            "source_agent": "BackendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify backend implementation correctness and conformance to design_spec.md.",
            "review_artifacts": [{"type": "text_file", "name": "app.py"}]
        },
        {
            "source_agent": "FrontendDeveloper",
            "reviewer_agent": "IntegrationMerger",
            "review_criteria": "Verify frontend template correctness and conformance to design_spec.md.",
            "review_artifacts": [{"type": "text_file", "name": "templates/*.html"}]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop complete Python Flask 'MusicStreaming' web application with frontend templates and backend app.py per user requirements and local text data management.",
    workflow: list = [
        {
            "step": 1,
            "description": "Parallel backend and frontend design specification and merged design.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce merged backend and frontend design specification."
                }
            ],
        },
        {
            "step": 2,
            "description": "Parallel backend and frontend implementation and integration merge.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Produce merged backend app.py and frontend templates/*.html implementation."
                }
            ],
        }
    ]
): pass
# Orchestrate_End