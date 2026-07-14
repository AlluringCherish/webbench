# Phase1_Start
def design_specification_phase(
    goal: str = "Debate the detailed design specification for the 'VirtualMuseum' Flask web application respecting all user requirements and produce a complete design_spec.md",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = (
        "DesignDebaterA and DesignDebaterB independently draft design_debate_a.md and design_debate_b.md respectively in round 1, "
        "then each revises their draft once informed by the other's draft in round 2; "
        "DesignJudge then adjudicates both final design drafts and writes the canonical design_spec.md."
    ),
    team: list = [
        {
            "agent_name": "DesignDebaterA",
            "role": "Produce a comprehensive design document draft detailing the Flask routes, templates, local text storage schema, and precise page element mapping for the 'VirtualMuseum' app, following the user requirements; revise based on peer draft.",
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
            "role": "Independently create a competing design document draft for the VirtualMuseum Flask application detailing adaptive web routes, templates, and local text file handling; revise informed by DesignDebaterA's draft.",
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
            "role": "Review final design drafts from DesignDebaterA and DesignDebaterB, adjudicate discrepancies, ensure full compliance with the user specification, and produce the canonical design_spec.md document describing exact Flask routes, templates with element IDs, local text data management, and navigation flow.",
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
            "review_criteria": (
                "Approve if design_debate_a.md exists, is non-empty, well-structured, relevant to the user requirements, "
                "and free from catastrophic format or logical errors; completeness at this stage not mandatory."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "source_agent": "DesignDebaterB",
            "reviewer_agent": "DesignJudge",
            "review_criteria": (
                "Approve if design_debate_b.md exists, is non-empty, well-structured, relevant to the user requirements, "
                "and free from catastrophic format or logical errors; completeness at this stage not mandatory."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "source_agent": "DesignJudge",
            "reviewer_agent": "DesignDebaterA",
            "review_criteria": (
                "Approve when design_spec.md exists, is non-empty, readable, broadly usable, "
                "and captures all required design elements without feature additions."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Debate two full implementations of the VirtualMuseum Flask app including app.py and templates/*.html for two total rounds, then adjudicate the final canonical implementation",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = (
        "ImplementationDebaterA and ImplementationDebaterB independently develop full candidate app.py and corresponding templates/*.html "
        "based on design_spec.md in round 1, then revise once informed by peer artifacts in round 2; ImplementationJudge adjudicates "
        "both bundles and produces the final app.py and templates/*.html set."
    ),
    team: list = [
        {
            "agent_name": "ImplementationDebaterA",
            "role": (
                "Implement the VirtualMuseum Flask application according to the design_spec.md, including all routes, "
                "templates with exact element IDs, local text file data management, and local text pipe-delimited persistence; "
                "revise implementation once in round 2 based on ImplementationDebaterB's candidate."
            ),
            "tools": ["write_text_file"],
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
            "role": (
                "Produce an independent implementation of the VirtualMuseum Flask app with all specified pages, routes, templates, "
                "and local text file handling per design_spec.md; revise once informed by ImplementationDebaterA's candidate."
            ),
            "tools": ["write_text_file"],
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
            "role": (
                "Evaluate the final candidates from ImplementationDebaterA and ImplementationDebaterB for completeness, correctness, "
                "and adherence to the design_spec.md, then merge the best supported elements into a final canonical app.py and templates/*.html."
            ),
            "tools": ["write_text_file"],
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
            "review_criteria": (
                "Approve when app_debate_a.py and associated templates exist, are syntactically valid, meet design_spec.md requirements, "
                "and exhibit no catastrophic format or logical errors."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationDebaterB",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": (
                "Approve when app_debate_b.py and associated templates exist, are syntactically valid, meet design_spec.md requirements, "
                "and exhibit no catastrophic format or logical errors."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationJudge",
            "reviewer_agent": "ImplementationDebaterA",
            "review_criteria": (
                "Approve when the canonical app.py and templates/*.html exist, are non-empty, readable, usable, and strictly adhere to design_spec.md."
            ),
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
    goal: str = "Design and implement the 'VirtualMuseum' Python Flask web application according to the detailed user requirements with exact web interface contract and local text data persistence.",
    workflow: list = [
        {
            "step": 1,
            "description": "Design specification debate and adjudication for the VirtualMuseum app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Debate and produce comprehensive design_spec.md for the web app."}
            ]
        },
        {
            "step": 2,
            "description": "Implementation debate and adjudication producing the final app.py and templates/*.html.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Debate and produce full code and templates, finalize the canonical implementation."}
            ]
        }
    ]
): pass
# Orchestrate_End