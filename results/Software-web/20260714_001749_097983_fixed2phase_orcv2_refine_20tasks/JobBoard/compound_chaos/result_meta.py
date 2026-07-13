# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the comprehensive Python web application design contract for JobBoard covering all 9 pages, data structures, navigation, and exact element IDs; deliver design_spec.md and gated design_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator drafts design_spec.md consolidating user requirements; DesignCritic reviews and writes design_feedback.md with approval or requests modification.",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Generate or revise the full design_spec.md with detailed page layouts, element IDs, navigation flow, and data file structures for the JobBoard web app, based on user_task_description and prior feedback.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        },
        {
            "agent_name": "DesignCritic",
            "role": "Critically review design_spec.md to ensure full coverage of functional pages, exact element IDs, data storage formats, and navigation correctness; produce design_feedback.md starting with [APPROVED] or NEED_MODIFY.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_feedback.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignGenerator",
            "reviewer_agent": "DesignCritic",
            "review_criteria": "Verify design_spec.md completeness, correctness of page elements, data file consistency, navigation flow, and compliance with user requirements without adding new features.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Refine the complete Python web app implementation and verification for JobBoard, producing app.py, templates/*.html, and gated code_feedback.md for at most two iterations",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator writes or revises app.py and templates/*.html based on design_spec.md and previous code_feedback.md; CodeCritic performs technical and functional review producing code_feedback.md with [APPROVED] or NEED_MODIFY.",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Write or completely revise the full JobBoard Python web application source code app.py and HTML templates with accurate page structures, element IDs, navigation, and local text file data management per design_spec.md and code_feedback.md.",
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
            "role": "Perform code review for correctness, adherence to design_spec.md, functionality, and code quality; produce code_feedback.md beginning with [APPROVED] or NEED_MODIFY.",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "code_feedback.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "AppGenerator",
            "reviewer_agent": "CodeCritic",
            "review_criteria": "Validate conformance to design_spec.md, page element correctness including all 9 pages with exact IDs, navigation flow, data file usage per specs, and code syntax/quality.",
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
    goal: str = "Develop a comprehensive Python web application 'JobBoard' with all specified pages, accurate element IDs, local text data management, and user functionalities with no authentication.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the complete design specification for JobBoard covering all pages, element IDs, data formats, and navigation.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Full design refinement and gating"}
            ]
        },
        {
            "step": 2,
            "description": "Refine the implementation of the Python web app and HTML templates with verification against the design.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Combine implementation and code verification"}
            ]
        }
    ]
): pass
# Orchestrate_End