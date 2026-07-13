# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the adaptive design specification for the MusicStreaming web app, producing design_spec.md and gated design_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator writes design_spec.md describing all pages, navigation, UI elements, and data storage format; DesignCritic reviews design_spec.md and produces design_feedback.md with either [APPROVED] or NEED_MODIFY, iterating at most twice.",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Generate or revise a detailed design_spec.md for the MusicStreaming app covering all ten pages, exact element IDs, navigation flow starting from dashboard, and local text file data formats",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "agent_name": "DesignCritic",
            "role": "Review design_spec.md for completeness, correctness, and alignment with user requirements; produce design_feedback.md with exact markers [APPROVED] or NEED_MODIFY",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_feedback.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignGenerator",
            "reviewer_agent": "DesignCritic",
            "review_criteria": "Check design_spec.md for adherence to all specified pages, elements, navigation starting at dashboard, data format, and absence of authentication",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Refine the combined backend and frontend implementation of the MusicStreaming app with app.py and templates/*.html, gated by code_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator writes or revises app.py and all HTML templates per design_spec.md and code_feedback.md; CodeCritic reviews all produced files for functionality, page elements and IDs, data handling from text files, and produces code_feedback.md with [APPROVED] or NEED_MODIFY at most twice.",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Implement or revise app.py and templates/*.html fully implementing the MusicStreaming app features, pages, navigation, exact element IDs, and local text file data management as specified in design_spec.md",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"},
                {"type": "text_file", "name": "code_feedback.md", "source": "CodeCritic"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        },
        {
            "agent_name": "CodeCritic",
            "role": "Review app.py and templates/*.html against design_spec.md for correctness, completeness, exact page and element IDs, local text file data access, and produce gated code_feedback.md with [APPROVED] or NEED_MODIFY",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "code_feedback.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "AppGenerator",
            "reviewer_agent": "CodeCritic",
            "review_criteria": "Gate app.py and templates/*.html for conformance to design_spec.md including page elements, navigation, data file usage, and required exact element IDs",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the MusicStreaming Python web application with exact page elements, local text file data storage, and navigation starting at dashboard page",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the adaptive design specification for MusicStreaming web app for at most two iterations",
            "phases": [
                {
                    "phase_name": "design_specification_phase", 
                    "role": "Adaptive design refinement for MusicStreaming app pages and data formats"
                }
            ]
        },
        {
            "step": 2,
            "description": "Refine the combined backend and frontend implementation for MusicStreaming for at most two iterations",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase", 
                    "role": "Adaptive implementation refinement producing app.py and templates/*.html"
                }
            ]
        }
    ]
): pass
# Orchestrate_End