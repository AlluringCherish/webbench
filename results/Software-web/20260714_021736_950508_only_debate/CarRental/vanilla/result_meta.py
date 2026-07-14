# Phase1_Start
def design_specification_phase(
    goal: str = "Debate adaptive Web design contract for CarRental app with specified pages, elements, routes, and local text file data format; produce design_spec.md",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = "DesignDebaterA and DesignDebaterB independently draft design_debate_a.md and design_debate_b.md in round 1; revise including peer outputs in round 2; DesignJudge adjudicates and merges final design_spec.md.",
    team: list = [
        {
            "agent_name": "DesignDebaterA",
            "role": "Create first complete design specification draft addressing all 9 pages, element IDs, Flask routing, and data file contracts; produce design_debate_a.md in round 1 and revise it incorporating DesignDebaterB's draft in round 2.",
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
            "role": "Create second independent complete design specification draft with full adaptive Web contract compliance and detailed local text data storage format; produce design_debate_b.md in round 1 and revise it incorporating DesignDebaterA's draft in round 2.",
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
            "role": "Adjudicate and synthesize final comprehensive design_spec.md from both Debater outputs ensuring full coverage of adaptive Web interface contract, pages, routes, element IDs, and local text file data storage as per user requirements; produce canonical design_spec.md.",
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
            "review_criteria": "Approve when design_debate_a.md exists, is non-empty, readable, relevant, and consistent with adaptive Web contract; do not require final completeness.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "source_agent": "DesignDebaterB",
            "reviewer_agent": "DesignJudge",
            "review_criteria": "Approve when design_debate_b.md exists, is non-empty, readable, relevant, and consistent with adaptive Web contract; do not require final completeness.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "source_agent": "DesignJudge",
            "reviewer_agent": "DesignDebaterA",
            "review_criteria": "Approve when design_spec.md exists, is non-empty, readable, broadly usable, and aligns with user requirements; allow minor omissions or polish issues.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Debate full implementation of CarRental Flask app with templates for all pages, strict local text file data handling per design_spec.md; produce app.py and templates/*.html",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = "ImplementationDebaterA and ImplementationDebaterB independently create complete app.py and templates candidates in round 1; revise from peer candidates in round 2; ImplementationJudge integrates and finalizes canonical app.py and templates/*.html.",
    team: list = [
        {
            "agent_name": "ImplementationDebaterA",
            "role": "Implement Flask app and Jinja2 templates for all 9 pages with exact routes, HTTP methods, element IDs, form specifications, and local text file data persistence per design_spec.md; produce app_debate_a.py and templates_debate_a/*.html in round 1; revise once from ImplementationDebaterB's artifacts in round 2.",
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
            "role": "Independently implement Flask app and templates matching adaptive Web contract for CarRental with local text file backend per design_spec.md; produce app_debate_b.py and templates_debate_b/*.html in round 1; revise once from ImplementationDebaterA's work in round 2.",
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
            "role": "Evaluate both implementation candidates against design_spec.md for correctness, completeness, Flask route fidelity, element ID compliance, local text file data handling; produce canonical app.py and templates/*.html.",
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
            "review_criteria": "Approve when app_debate_a.py and templates_debate_a/*.html exist, are non-empty, follow design_spec.md, are readable, and free of catastrophic errors; partial completeness allowed.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationDebaterB",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": "Approve when app_debate_b.py and templates_debate_b/*.html exist, are non-empty, follow design_spec.md, are readable, and free of catastrophic errors; partial completeness allowed.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationJudge",
            "reviewer_agent": "ImplementationDebaterA",
            "review_criteria": "Approve when canonical app.py and templates/*.html exist, are non-empty, readable, broadly usable, and preserve adaptive Web contract; minor omissions allowed.",
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
    goal: str = "Design and implement the CarRental adaptive Python Flask web application with local text file data storage according to user requirements",
    workflow: list = [
        {
            "step": 1,
            "description": "Debate and adjudicate the comprehensive adaptive Web design and data storage specification for CarRental app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce final design_spec.md for CarRental app adaptive Web contract and local text file data formats."}
            ]
        },
        {
            "step": 2,
            "description": "Debate and adjudicate the full implementation of Flask backend and Jinja2 templates for CarRental app following the design specification.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Produce final app.py and templates/*.html for CarRental app, implementing exact routes, element IDs, forms, and local text file persistence."}
            ]
        }
    ]
): pass
# Orchestrate_End