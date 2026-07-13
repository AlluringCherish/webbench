# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the FoodDelivery web application design specification with detailed page layouts, element IDs, and data storage formats; deliver design_spec.md and gated design_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "DesignGenerator writes design_spec.md based on user_task_description and design_feedback.md; DesignCritic reviews design_spec.md and writes design_feedback.md starting with [APPROVED] or NEED_MODIFY."
    ),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Create and revise a comprehensive design specification including page structure, element IDs, navigation flow, and data file formats for the FoodDelivery web application.",
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
            "role": "Critically evaluate the design_spec.md artifact for completeness, clarity, and alignment with user requirements and write design_feedback.md beginning with [APPROVED] or NEED_MODIFY.",
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
            "review_criteria": "Verify design_spec.md fully addresses all features, page elements, element IDs, navigation scheme, and data storage requirements without missing or ambiguous details.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Refine the full Python implementation and verification of the FoodDelivery app including app.py, HTML templates and gated code_feedback.md for at most two iterations.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "AppGenerator develops and revises app.py and templates/*.html from design_spec.md and code_feedback.md; CodeCritic reviews the implementation for correctness, completeness, adherence to design, and produces code_feedback.md starting with [APPROVED] or NEED_MODIFY."
    ),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Implement and iteratively refine the FoodDelivery Python Flask app including dashboard, restaurants listing, menus, cart, orders, delivery tracking, and reviews using local text file data storage as per design_spec.md and code_feedback.md.",
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
            "role": "Review the Python Flask implementation and HTML templates for syntax, runtime errors, conformance to design_spec.md, element ID exactness, navigation correctness, data persistence, and produce gated code_feedback.md.",
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
            "review_criteria": "Verify app.py and templates/*.html fully implement design_spec.md web pages and features with correct element IDs and data file interactions, free of syntax or runtime errors.",
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
    goal: str = "Develop the FoodDelivery Python Flask web application with local text file data storage and exact page/elements implementation according to user requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the complete design specification with exact page elements, layout, IDs, and data storage formats.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce and verify the detailed design specification document."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement and verify the full Python Flask app with HTML templates based on design specification.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Produce and validate the production-ready Python Flask web app code and templates."
                }
            ]
        }
    ]
): pass
# Orchestrate_End