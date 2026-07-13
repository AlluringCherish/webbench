# Phase1_Start
def design_specification_phase(
    goal: str = "Create and refine the full design specification for the OnlineAuction Python Flask web app including detailed page structure and data storage contract; deliver design_spec.md and gated design_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator drafts design_spec.md from user_task_description and design_feedback.md; DesignCritic reviews and writes design_feedback.md with [APPROVED] or NEED_MODIFY markers for refinement",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Produce a complete design specification document with page layouts, element IDs, navigation flow, and data file schema based on user requirements and feedback",
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
            "role": "Critically evaluate design_spec.md for completeness, correct element IDs, navigation consistency, and adherence to user requirements; write design_feedback.md starting with [APPROVED] or NEED_MODIFY",
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
            "review_criteria": "Ensure the design_spec.md fully covers all required pages, element IDs, navigation links, and data storage files per user requirements; provide constructive feedback to achieve final approval",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Develop and iteratively refine the OnlineAuction Flask web app source code including app.py and templates/*.html with full functionality and correct element IDs; generate code_feedback.md with validation",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator writes or revises app.py and templates/*.html using design_spec.md and code_feedback.md; CodeCritic evaluates functionality, correctness, completeness, element IDs, and data file integration then writes code_feedback.md starting with [APPROVED] or NEED_MODIFY",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Implement the full OnlineAuction Python Flask application backend and frontend templates according to design_spec.md and iteratively revise them using feedback from code_feedback.md",
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
            "role": "Perform detailed review and validation of app.py and templates/*.html to ensure compliance with design_spec.md, verify element IDs and navigation routes, check local text file data access, and produce code_feedback.md containing approval status or needed modifications",
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
            "review_criteria": "Gate the conformity of app.py and templates/*.html to the design_spec.md and data storage schemes; verify that all required pages and element IDs exist and function correctly; ensure no regression or functionality gaps",
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
    goal: str = "Develop the OnlineAuction Python Flask web application conforming to detailed design and data requirements using at most two refinement iterations per phase",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine OnlineAuction design specification through generator and critic collaboration.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Generate and review the complete design specification."}
            ]
        },
        {
            "step": 2,
            "description": "Implement and verify the OnlineAuction app backend and frontend with iterative feedback.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Build and refine the app.py and templates based on design spec and feedback."}
            ]
        }
    ]
): pass
# Orchestrate_End