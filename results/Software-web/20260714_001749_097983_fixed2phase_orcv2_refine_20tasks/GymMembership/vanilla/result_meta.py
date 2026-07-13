# Phase1_Start
def design_specification_phase(
    goal: str = "Create a detailed design specification document for the GymMembership web application's UI, page structure, element IDs, navigation flow, and data handling, delivering 'design_spec.md' and gated 'design_feedback.md'.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = ("DesignGenerator writes 'design_spec.md' describing the full UI design, page layout with exact element IDs, navigation logic, and data storage format based on the user task. "
                                      "DesignCritic reviews 'design_spec.md' against the user task and writes 'design_feedback.md' starting with [APPROVED] or NEED_MODIFY. "
                                      "The loop iterates at most twice until approval or stopping after two iterations."),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Produce or revise the GymMembership web application design_spec.md detailing page titles, element IDs, navigation structure, and local text file data management according to user requirements.",
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
            "role": "Review design_spec.md ensuring completeness, correctness, and conformance to requirements; produce design_feedback.md starting with [APPROVED] or NEED_MODIFY.",
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
            "review_criteria": "Check that design_spec.md fully covers all required pages, element IDs, navigation flows, data storage formats, and no contradictions or missing details.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Develop and refine the complete GymMembership web application with app.py and templates/*.html implementing all pages, exact element IDs, local text file data handling, starting from dashboard, delivering app.py, templates/*.html, and code_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = ("AppGenerator writes or revises app.py and templates/*.html implementing the GymMembership application following design_spec.md and addressing code_feedback.md. "
                                      "CodeCritic reviews the implementation for correctness, element ID accuracy, navigation, and data handling consistency; produces code_feedback.md starting with [APPROVED] or NEED_MODIFY. "
                                      "Iterations run at most twice until approval or stopping after two iterations."),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Implement or revise the GymMembership app.py and templates/*.html implementing all pages, element IDs, navigation, and local text file data storage per design_spec.md and code_feedback.md.",
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
            "role": "Review app.py and templates/*.html ensuring all page elements, exact element IDs, navigation, data persistence with local text files, and user task requirements are met; produce code_feedback.md starting with [APPROVED] or NEED_MODIFY.",
            "tools": ["write_text_file"],
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
            "review_criteria": "Gate implementation accuracy for app.py and templates/*.html based on design_spec.md, focusing on element ID correctness, page navigation, data storage, and completeness.",
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
    goal: str = "Develop the GymMembership Python web application delivering app.py and templates/*.html implementing the specified pages, navigation with exact element IDs, and local text file data management.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the design specification document for the GymMembership application for at most two iterations.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Create and refine the GymMembership application design specification."}
            ]
        },
        {
            "step": 2,
            "description": "Develop and refine the GymMembership application implementation for at most two iterations.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Implement and verify the GymMembership web application based on design specification."}
            ]
        }
    ]
): pass
# Orchestrate_End