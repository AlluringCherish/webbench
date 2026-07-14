# Phase1_Start
def design_specification_phase(
    goal: str = "Debate and produce a complete design specification for the OnlineAuction Flask web application including exact route, page, element IDs, data files, and local text persistence.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = "DesignDebaterA and DesignDebaterB independently draft design_specification artifacts in round 1, then revise by incorporating peer artifacts in round 2; DesignJudge adjudicates and produces the canonical design_spec.md detailing the Flask app's adaptive web interface contract and data storage design.",
    team: list = [
        {
            "agent_name": "DesignDebaterA",
            "role": "Create a detailed design document specifying Flask routes, HTTP methods, template files with exact HTML element IDs, user navigation flows, form field names with methods/actions, and data storage mappings from the user task description independently for round 1; then in round 2 revise from both own and peer design artifacts.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "agent_name": "DesignDebaterB",
            "role": "Independently produce a complementary detailed design document with the same scope as DesignDebaterA using the user task input in round 1; subsequently revise the artifact in round 2 using both peer and own round 1 artifacts.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "agent_name": "DesignJudge",
            "role": "Adjudicate both final design debate artifacts for completeness, correctness, alignment with user requirements, and produce a consolidated canonical design_spec.md specifying the Flask routes, exact page UI contracts, local text file format storage, and adaptive interface contract.",
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignDebaterA",
            "reviewer_agent": "DesignJudge",
            "review_criteria": "Approve if design_debate_a.md exists, is non-empty, readable, aligned with user requirements, contains all pages with exact element IDs, routes, methods, templates, and data file mappings; allow partial incompleteness but no catastrophic formatting errors.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "source_agent": "DesignDebaterB",
            "reviewer_agent": "DesignJudge",
            "review_criteria": "Approve if design_debate_b.md exists, is non-empty, readable, aligned with user requirements as above; allow partial incompleteness but no catastrophic formatting errors.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "source_agent": "DesignJudge",
            "reviewer_agent": "DesignDebaterA",
            "review_criteria": "Approve if design_spec.md exists and is a broadly usable canonical design specification for the OnlineAuction Flask app preserving all adaptive interface and storage contracts, readable and logically consistent.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Debate two complete, independent candidate implementations of the OnlineAuction Flask app and its templates for exactly two rounds and produce the final canonical app.py and templates/*.html",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = "ImplementationDebaterA and ImplementationDebaterB independently implement app.py and all required HTML templates using the adaptive design_spec.md in round 1; then each revises their own artifacts with full peer artifact context in round 2; ImplementationJudge adjudicates to produce the finalized app.py and templates/*.html reflecting the fully consistent, complete, and runnable app per the design.",
    team: list = [
        {
            "agent_name": "ImplementationDebaterA",
            "role": "Independently implement the full OnlineAuction Flask application backend in app_debate_a.py and all HTML templates in templates_debate_a/*.html according to design_spec.md; revise these in round 2 incorporating peer revised artifacts.",
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
            "role": "Produce an independent, complete implementation of the OnlineAuction Flask backend and templates in app_debate_b.py and templates_debate_b/*.html per design_spec.md; revise from peer round 1 artifacts at round 2.",
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
            "role": "Adjudicate the final implementation artifacts from both debaters for functional completeness, code correctness, adaptive Web contract integrity, and produce the canonical app.py and all templates/*.html files; files must be runnable Flask app matching design_spec.md precisely.",
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
            "review_criteria": "Approve if app_debate_a.py and templates_debate_a/*.html exist, are non-empty, valid in syntax, conform to design_spec.md, and broadly usable; allow minor incompleteness.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationDebaterB",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": "Approve if app_debate_b.py and templates_debate_b/*.html exist, are non-empty, valid, conform to design_spec.md, and broadly usable; allow minor incompleteness.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationJudge",
            "reviewer_agent": "ImplementationDebaterA",
            "review_criteria": "Approve if canonical app.py and templates/*.html exist, are non-empty, readable, runnable, and meet design_spec.md requirements; do not reject for minor omissions or polish.",
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
    goal: str = "Produce the complete OnlineAuction Python Flask web application with local text file data storage and exact user interface and navigation contracts.",
    workflow: list = [
        {
            "step": 1,
            "description": "Design debate and adjudication to produce canonical design_spec.md.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Generate and adjudicate the design specification for the OnlineAuction web app using Multi-Agent Debate."}
            ]
        },
        {
            "step": 2,
            "description": "Implementation debate and adjudication producing final app.py and templates/*.html.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Debate, revise, and adjudicate the implementation of the OnlineAuction app code and HTML templates."}
            ]
        }
    ]
): pass
# Orchestrate_End