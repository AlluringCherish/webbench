# Phase1_Start
def design_specification_phase(
    goal: str = "Debate the adaptive design of the MusicStreaming Flask web app with exact page routes, elements, data formats, and no-authentication contract; deliver design_spec.md.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = (
        "DesignDebaterA and DesignDebaterB independently draft design_debate_a.md and design_debate_b.md respectively "
        "in round 1, revising once in round 2 informed by each other's artifacts. DesignJudge adjudicates and writes "
        "design_spec.md consolidating exact Flask routes, HTTP methods, templates with specified element IDs, form fields, "
        "actions, and local-text persistence behavior compliant with the adaptive Web contract."
    ),
    team: list = [
        {
            "agent_name": "DesignDebaterA",
            "role": (
                "Use SystemArchitect role to create a complete design_debate_a.md capturing all pages, routes, elements, and local-text "
                "data management as per requirements, adhering strictly to the adaptive Web contract for no-authentication apps."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"},
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "agent_name": "DesignDebaterB",
            "role": (
                "Use SystemArchitect role to create design_debate_b.md focusing on page contracts, element IDs, and data flow for the "
                "MusicStreaming web app, ensuring compliance with the fixed Web workflow and local text files."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "agent_name": "DesignJudge",
            "role": (
                "Adjudicate design_debate_a.md and design_debate_b.md by cross-validating all specified pages, routes, element IDs, "
                "form field names, HTTP methods, navigation flows, and local-text file persistence behavior; produce canonical design_spec.md."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_debate_a.md", "source": "DesignDebaterA"},
                {"type": "text_file", "name": "design_debate_b.md", "source": "DesignDebaterB"},
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignDebaterA",
            "reviewer_agent": "DesignJudge",
            "review_criteria": (
                "Approve when design_debate_a.md exists, is non-empty, readable, relevant, and has no catastrophic format errors; "
                "partial completeness acceptable."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "source_agent": "DesignDebaterB",
            "reviewer_agent": "DesignJudge",
            "review_criteria": (
                "Approve when design_debate_b.md exists, is non-empty, readable, relevant, and has no catastrophic format errors; "
                "partial completeness acceptable."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "source_agent": "DesignJudge",
            "reviewer_agent": "DesignDebaterA",
            "review_criteria": (
                "Approve when design_spec.md exists, is non-empty, readable, broadly usable, and satisfies the adaptive Web contract for "
                "MusicStreaming app; minor omissions and polish allowed."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Debate complete, valid Flask app implementation and templates for MusicStreaming web app with local-text persistence and exact UI contract; deliver app.py and templates/*.html.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = (
        "ImplementationDebaterA and ImplementationDebaterB independently implement full Flask app.py and templates sets (templates_debate_a and templates_debate_b) "
        "in round 1, revise once in round 2 informed by peer artifacts; ImplementationJudge adjudicates and writes canonical app.py and templates/*.html with strict conformance."
    ),
    team: list = [
        {
            "agent_name": "ImplementationDebaterA",
            "role": (
                "Implement full MusicStreaming Flask backend (app.py) and frontend templates_debate_a/*.html based on design_spec.md; "
                "ensure root route '/', all declared page routes, HTTP methods, elements with exact IDs, form field names, POST actions with local-text file persistence, "
                "and user navigation flow with no authentication."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignJudge"},
                {"type": "text_file", "name": "app_debate_a.py", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "templates_debate_a/*.html", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "app_debate_b.py", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "templates_debate_b/*.html", "source": "ImplementationDebaterB"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"},
            ]
        },
        {
            "agent_name": "ImplementationDebaterB",
            "role": (
                "Implement full MusicStreaming Flask backend (app.py) and frontend templates_debate_b/*.html applying the same requirements and contract; "
                "revise from round 1 outputs once peer-informed."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignJudge"},
                {"type": "text_file", "name": "app_debate_b.py", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "templates_debate_b/*.html", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "app_debate_a.py", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "templates_debate_a/*.html", "source": "ImplementationDebaterA"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"},
            ]
        },
        {
            "agent_name": "ImplementationJudge",
            "role": (
                "Review and adjudicate candidate implementations app_debate_a.py, app_debate_b.py and templates sets against design_spec.md; "
                "produce final canonical app.py and templates/*.html ensuring no features beyond requirements."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignJudge"},
                {"type": "text_file", "name": "app_debate_a.py", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "templates_debate_a/*.html", "source": "ImplementationDebaterA"},
                {"type": "text_file", "name": "app_debate_b.py", "source": "ImplementationDebaterB"},
                {"type": "text_file", "name": "templates_debate_b/*.html", "source": "ImplementationDebaterB"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "ImplementationDebaterA",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": (
                "Approve when app_debate_a.py and templates_debate_a/*.html exist, readable, relevant, syntactically valid, and broadly conforming "
                "to design_spec.md; minor incompleteness allowed."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"},
            ]
        },
        {
            "source_agent": "ImplementationDebaterB",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": (
                "Approve when app_debate_b.py and templates_debate_b/*.html exist, readable, relevant, syntactically valid, and broadly conforming "
                "to design_spec.md; minor incompleteness allowed."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"},
            ]
        },
        {
            "source_agent": "ImplementationJudge",
            "reviewer_agent": "ImplementationDebaterA",
            "review_criteria": (
                "Approve when final app.py and templates/*.html exist, are readable, syntactically correct, and usable to run MusicStreaming app per spec."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
            ]
        }
    ]
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Design and implement the MusicStreaming Flask web application with exact adaptive Web interface contract for specified pages and local text file persistence without authentication.",
    workflow: list = [
        {
            "step": 1,
            "description": "Debate design specification and adaptive web contract for MusicStreaming app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Adaptive design debate and adjudication producing design_spec.md."}
            ]
        },
        {
            "step": 2,
            "description": "Debate full Flask app implementation and templates; adjudicate final app.py and templates.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Adaptive implementation debate and adjudication producing app.py and templates."}
            ]
        }
    ]
): pass
# Orchestrate_End