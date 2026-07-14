# Phase1_Start
def design_specification_phase(
    goal: str = "Debate the adaptive Web design contract for the OnlineLibrary app for exactly two total rounds and produce a unified design_spec.md document.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = "DesignDebaterA and DesignDebaterB independently draft design artifacts for the OnlineLibrary app in round 1, revise from each other's drafts in round 2, then DesignJudge adjudicates and synthesizes the final design_spec.md incorporating the user requirements and exact page routes, elements, and file data formats.",
    team: list = [
        {
            "agent_name": "DesignDebaterA",
            "role": "Produce a detailed design_debate_a.md covering the OnlineLibrary app architecture with precise Flask routes, HTTP methods, templates, element IDs, data handling from local text files, and page navigation flows, performing two rounds of drafting.",
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
            "role": "Craft a comprehensive design_debate_b.md for OnlineLibrary emphasizing adaptive Flask route contracts, page context variables, exact element IDs, and local text data integration, performing two rounds of drafting.",
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
            "role": "Adjudicate both design_debate_a.md and design_debate_b.md with respect to user specifications to produce a canonical, complete design_spec.md that specifies all Flask routes, templates, context, element IDs, navigation, and local text data persistence.",
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
            "review_criteria": "Verify design_debate_a.md exists, is non-empty, coherent, follows requirements format, contains Flask route specs for all user-declared pages including element IDs and data persistence.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_a.md"}]
        },
        {
            "source_agent": "DesignDebaterB",
            "reviewer_agent": "DesignJudge",
            "review_criteria": "Check design_debate_b.md exists, is relevant, readable, specifies adaptive web contract conformance including exact routes, forms, and page element IDs.",
            "review_artifacts": [{"type": "text_file", "name": "design_debate_b.md"}]
        },
        {
            "source_agent": "DesignJudge",
            "reviewer_agent": "DesignDebaterA",
            "review_criteria": "Confirm design_spec.md exists, is non-empty, correct, complete with the final canonical web design definition meeting user requirements as specified.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Debate full Python Flask implementation of OnlineLibrary with all defined routes, templates, local text data management, and UI elements for exactly two total rounds and produce final app.py and templates/*.html artifacts.",
    collab_pattern_name: str = "Multi-Agent Debate",
    collab_pattern_description: str = "ImplementationDebaterA and ImplementationDebaterB independently develop candidate app.py and templates sets from design_spec.md in round 1, each revises their versions with peer insights in round 2, then ImplementationJudge combines and adjudicates the final complete app.py and HTML templates without adding features.",
    team: list = [
        {
            "agent_name": "ImplementationDebaterA",
            "role": "Create a full app_debate_a.py and templates_debate_a/*.html implementing all specified Flask routes, page behaviors, local text file data handling, precise element IDs, and navigation flows for OnlineLibrary; revise from peer materials once.",
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
            "role": "Independently produce app_debate_b.py and templates_debate_b/*.html implementing the same complete OnlineLibrary functionality and interface per design_spec.md; revise from peer outputs once.",
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
            "role": "Adjudicate and synthesize app_debate_a.py, app_debate_b.py, and their templates into a canonical, fully functional app.py and templates/*.html set consistent with design_spec.md with no feature additions.",
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
            "review_criteria": "Approve candidate app_debate_a.py and templates_debate_a/*.html presence, readability, adherence to design_spec.md, and absence of catastrophic errors; no full completion required.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_a.py"},
                {"type": "text_file", "name": "templates_debate_a/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationDebaterB",
            "reviewer_agent": "ImplementationJudge",
            "review_criteria": "Approve candidate app_debate_b.py and templates_debate_b/*.html presence, accuracy, conformity to design_spec.md, and no catastrophic mistakes; no full completion required.",
            "review_artifacts": [
                {"type": "text_file", "name": "app_debate_b.py"},
                {"type": "text_file", "name": "templates_debate_b/*.html"}
            ]
        },
        {
            "source_agent": "ImplementationJudge",
            "reviewer_agent": "ImplementationDebaterA",
            "review_criteria": "Confirm final app.py and templates/*.html exist, are readable, fully implement design_spec.md with no feature additions, and are broadly usable as a Flask application.",
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
    goal: str = "Create the OnlineLibrary Python Flask Web application fully implementing the specified pages, local text file data management, and adaptive fixed Web interface contract.",
    workflow: list = [
        {
            "step": 1,
            "description": "Design phase: debate and adjudicate the adaptive Web design contract for OnlineLibrary.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Adaptively design the OnlineLibrary Flask web application architecture and interface."}
            ]
        },
        {
            "step": 2,
            "description": "Implementation phase: debate and adjudicate the full Python Flask app and templates implementation.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Implement and verify the complete OnlineLibrary app and templates per design specification."}
            ]
        }
    ]
): pass
# Orchestrate_End