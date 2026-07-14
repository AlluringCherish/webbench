# Phase1_Start
def design_specification_phase(
    goal: str = "Debate and finalize a comprehensive adaptive design_spec.md for the TravelPlanner Flask web application with exact page routes, method contracts, element IDs, and data storage formats.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = (
        "DesignDebaterA and DesignDebaterB independently draft their candidate design_spec.md documents in round 1 based on user requirements, "
        "then each revises their documents in round 2 by incorporating or rebutting peer artifacts. DesignJudge adjudicates and synthesizes the final "
        "design_spec.md reflecting the adaptive Web Contract and user requirements."
    ),
    team: list = [
        {
            "agent_name": "DesignDebaterA",
            "role": "Produce the first candidate design_spec.md detailing Flask route mappings, HTTP methods, template files, and exact element IDs for all TravelPlanner pages, "
                    "plus data file formats based on the user requirements, performing round 1 independent draft and round 2 revision using peer input.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_debate_a.md"}
            ]
        },
        {
            "agent_name": "DesignDebaterB",
            "role": "Produce the second candidate design_spec.md detailing Flask route mappings, data persistence behavior, template filenames, and exact HTML element IDs for the TravelPlanner application, "
                    "independently in round 1 and revise incorporating peer feedback in round 2.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_debate_b.md"}
            ]
        },
        {
            "agent_name": "DesignJudge",
            "role": "Adjudicate and synthesize the final canonical design_spec.md for the TravelPlanner application from both Debaters' final artifacts ensuring full coverage of the adaptive Web interface contract, "
                    "route definitions, element IDs, page templates, local text data persistence, and compliance with user requirements.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignDebaterA",
            "reviewer_agent": "DesignJudge",
            "review_criteria": "Approve if design_debate_a.md exists, is complete, non-empty, readable, aligned with user requirements, and has no formatting errors.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "source_agent": "DesignDebaterB",
            "reviewer_agent": "DesignJudge",
            "review_criteria": "Approve if design_debate_b.md exists, is complete, non-empty, readable, aligned with user requirements, and has no formatting errors.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "source_agent": "DesignJudge",
            "reviewer_agent": "DesignDebaterA",
            "review_criteria": "Approve if design_spec.md exists, is non-empty, broadly usable, well-structured, and sufficient for implementation without minor omissions.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Debate complete implementation bundles of app.py and templates/*.html for the TravelPlanner Flask application with exact adaptive web contract compliance and local text data management, then finalize canonical artifacts.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = (
        "ImplementationDebaterA and ImplementationDebaterB independently create complete app.py source and all required HTML templates in separate directories in round 1, "
        "revise once from peer artifacts in round 2, and ImplementationJudge adjudicates and combines them into canonical app.py and templates/*.html."
    ),
    team: list = [
        {
            "agent_name": "ImplementationDebaterA",
            "role": "Implement the TravelPlanner Flask application combining backend routes, local text-based data handling (read/write), and frontend templates with exact element IDs as per design_spec.md, "
                    "first draft independently and then revise after peer review.",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignJudge"},
                {"type": "text_file", "name": "app_debate_a.py", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "templates_debate_a/*.html", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "app_debate_b.py", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "templates_debate_b/*.html", "source": "ImplementationDebaterB"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"}
            ]
        },
        {
            "agent_name": "ImplementationDebaterB",
            "role": "Implement an independent candidate version of the TravelPlanner application backend and frontend templates following design_spec.md, then revise after peer review.",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignJudge"},
                {"type": "text_file", "name": "app_debate_b.py", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "templates_debate_b/*.html", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "app_debate_a.py", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "templates_debate_a/*.html", "source": "ImplementationDebaterA"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"}
            ]
        },
        {
            "agent_name": "ImplementationJudge",
            "role": "Evaluate and adjudicate both debate implementations for correctness, adherence to design_spec.md, and adaptive Web interface contract compliance, then produce canonical app.py and templates/*.html.",
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignJudge"},
                {"type": "text_file", "name": "app_debate_a.py", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "templates_debate_a/*.html", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "app_debate_b.py", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "templates_debate_b/*.html", "source": "ImplementationDebaterB"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "ImplementationDebaterA",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": "Approve if app_debate_a.py and templates_debate_a/*.html exist, are syntactically correct, readable, relevant to design_spec.md, and without critical errors.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationDebaterB",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": "Approve if app_debate_b.py and templates_debate_b/*.html exist, are syntactically correct, readable, relevant to design_spec.md, and without critical errors.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationJudge",
            "reviewer_agent": "ImplementationDebaterA",
            "review_criteria": "Approve if app.py and templates/*.html exist as canonical deliverables, are readable, well-structured, and suitable for deployment with no blocking issues.",
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
    goal: str = "Develop a complete TravelPlanner Flask web app with local text data storage according to user requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Design phase: debate and finalize detailed adaptive design specification.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Debate and adjudicate the adaptive design specification for TravelPlanner."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implementation phase: debate, revise, and adjudicate the full Flask app and templates implementations.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Debate and adjudicate complete TravelPlanner app.py and templates/*.html implementation."
                }
            ]
        }
    ]
): pass
# Orchestrate_End