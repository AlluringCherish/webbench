# Phase1_Start
def design_specification_phase(
    goal: str = "Refine and produce a comprehensive design specification document for the RealEstate Python web app, delivering design_spec.md and gated design_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "DesignGenerator creates or revises design_spec.md detailing the architecture, pages, elements with exact IDs, "
        "and data storage model from user_task_description and design_feedback.md; DesignCritic reviews the design_spec.md "
        "against the user requirements and writes design_feedback.md to be either [APPROVED] or NEED_MODIFY, "
        "enabling iterative refinement up to two iterations."
    ),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": "Architect and specify the detailed Python web app design including the dashboard start page, all eight pages with exact element IDs, user interactions, data storage structure using local text files, and navigation flows; produce design_spec.md.",
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
            "role": "Critically evaluate the design_spec.md to ensure full coverage of all specified pages, elements, and data model requirements; provide actionable feedback in design_feedback.md starting with [APPROVED] or NEED_MODIFY.",
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
            "review_criteria": "Validate comprehensive coverage of all 8 pages, accurate element IDs, data file formats, and logical navigation flows; ensure design is fully aligned with user requirements without missing any constraint.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "design_feedback.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Refine the Python Flask web app implementation including app.py and templates/*.html for the RealEstate site, plus gated code_feedback.md for correctness and completeness.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "AppGenerator writes or revises app.py and all required templates/*.html files implementing the RealEstate app functionality "
        "based on design_spec.md and previous code_feedback.md; CodeCritic reviews the code and templates for full adherence to design, "
        "correct element IDs, functionality, and data file integration; then writes code_feedback.md with either [APPROVED] or NEED_MODIFY, "
        "allowing up to two iterations of refinement."
    ),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": "Develop and iteratively refine the full Python Flask app implementation including app.py and HTML templates with precise element IDs for all 8 pages, enable browsing, searching, viewing details, inquiries, favorites, agents directory, and locations page, integrating with local text data files as specified.",
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
            "role": "Review the app.py and HTML templates for complete and accurate implementation per design_spec.md, verify usage of exact element IDs, validate integration with local text files for properties, inquiries, favorites, agents and locations, and write detailed code_feedback.md starting with [APPROVED] or NEED_MODIFY.",
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
            "review_criteria": "Review for complete functional implementation of all required pages with correct element IDs, full data access and manipulation, navigation correctness, and absence of errors or deviations from design_spec.md.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the RealEstate Python Flask web app with specified pages, functionality, and local text data integration in two refinement phases.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the detailed design specification for the RealEstate application.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce and refine the comprehensive design specification document."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement and verify the RealEstate web application per the approved design.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Develop and refine the full Python Flask app implementation including templates."
                }
            ]
        }
    ]
): pass
# Orchestrate_End