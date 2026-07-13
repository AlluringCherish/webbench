# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the adaptive Web design contract for the 'BookstoreOnline' app, producing design_spec.md and gated design_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "DesignGenerator writes design_spec.md describing all nine pages, data storage format, and element IDs; "
        "DesignCritic reviews design_spec.md for completeness, correctness, and feasibility, producing design_feedback.md. "
        "Two iterations maximum, stopping on [APPROVED]."
    ),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Generate or revise full detailed design_spec.md of the 'BookstoreOnline' web app including page layouts and data management based on user_task_description and design_feedback.md.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ],
        },
        {
            "agent_name": "DesignCritic",
            "role": "Review design_spec.md for completeness, adherence to requirements, usability, and feasibility; produce design_feedback.md.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_feedback.md"}
            ],
        },
    ],
    review_policy: list = [
        {
            "source_agent": "DesignGenerator",
            "reviewer_agent": "DesignCritic",
            "review_criteria": "Check design_spec.md for coverage of all user requirements, accurate page and element specifications, and consistency with local text data storage format.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ],
        }
    ],
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Refine complete backend and frontend implementation producing app.py and templates/*.html, gated by code_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "AppGenerator writes or revises app.py and all templates/*.html using design_spec.md and code_feedback.md as inputs; "
        "CodeCritic reviews the code bundle for correctness, functional completeness, exact element IDs, and compliance, producing code_feedback.md. "
        "Two iterations maximum, stopping on [APPROVED]."
    ),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Generate or revise the combined backend (Python) and frontend templates implementing all pages and local text file data management strictly following design_spec.md and addressing code_feedback.md.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"},
                {"type": "text_file", "name": "code_feedback.md", "source": "CodeCritic"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
            ],
        },
        {
            "agent_name": "CodeCritic",
            "role": "Review app.py and templates/*.html for implementation correctness, functional completeness, accurate element IDs as specified, interaction with local text file data, and user flows; produce code_feedback.md.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "code_feedback.md"},
            ],
        },
    ],
    review_policy: list = [
        {
            "source_agent": "AppGenerator",
            "reviewer_agent": "CodeCritic",
            "review_criteria": "Check implementation correctness, completeness against design_spec.md, and adherence to element ID conventions.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
            ],
        }
    ],
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the 'BookstoreOnline' Python web application with specified pages, features, exact element IDs, using local text file data, enforcing quality through two-phase refinement.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the complete adaptive design specification for the BookstoreOnline app.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce and refine the complete design specification document."
                }
            ]
        },
        {
            "step": 2,
            "description": "Refine the full backend and frontend implementation including app.py and templates/*.html.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Produce and refine the complete implementation and verification."
                }
            ]
        }
    ]
): pass
# Orchestrate_End