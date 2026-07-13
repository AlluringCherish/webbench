# Phase1_Start
def design_specification_phase(
    goal: str = "Create a detailed adaptive design specification for the WeatherForecast web app with page layouts, element IDs, navigation, and data storage formats as explicit deliverables.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "DesignGenerator writes design_spec.md, laying out all page designs, element IDs, navigation structure, "
        "and data storage format based on the user_task_description string. DesignCritic reviews design_spec.md, "
        "writes design_feedback.md beginning with [APPROVED] or NEED_MODIFY providing detailed feedback for improvements. "
        "Data flow is design_spec.md from DesignGenerator to DesignCritic, design_feedback.md from DesignCritic to DesignGenerator."
    ),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "role": (
                "Interpret user_task_description to produce a comprehensive design_spec.md defining all eight pages "
                "(Dashboard, Current Weather, Weekly Forecast, Location Search, Weather Alerts, Air Quality, Saved Locations, Settings), "
                "with exact element IDs, navigation flow, and local text file data schema as described."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        },
        {
            "agent_name": "DesignCritic",
            "role": (
                "Review design_spec.md for completeness, consistency, adherence to requirements, clear navigation paths, "
                "correct page element IDs, and proper integration of local text file data schemas; write design_feedback.md "
                "starting with [APPROVED] if no issues or NEED_MODIFY listing required changes."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_feedback.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignGenerator",
            "reviewer_agent": "DesignCritic",
            "review_criteria": (
                "Ensure design_spec.md fully covers all stated requirements including page structure, element IDs, "
                "navigation logic, and correct specification of local text file data formats as per the requirements document. "
                "Check for clarity, completeness, and absence of contradictions."
            ),
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Develop and iteratively refine an executable Python Flask web app (app.py, templates/*.html) implementing WeatherForecast design_spec.md and successfully passing code validation.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "AppGenerator creates or revises app.py and templates/*.html implementing the comprehensive web app based on design_spec.md and code_feedback.md. "
        "CodeCritic reviews the generated code and templates for functional correctness, syntax, integration with data files, adherence to element IDs, "
        "and writes code_feedback.md starting with [APPROVED] or NEED_MODIFY. Artifact flow: app.py and templates/*.html authored by AppGenerator, "
        "code_feedback.md authored by CodeCritic."
    ),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "role": (
                "Translate design_spec.md into a complete Python Flask application with templates, implementing all eight pages, local text file data ingestion, "
                "routing, UI elements with exact IDs, and user navigation starting from Dashboard; revise based on code_feedback.md."
            ),
            "tools": ["write_text_file", "validate_python_file"],
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
            "role": (
                "Critically analyze app.py and templates/*.html for syntax errors, runtime issues, architectural adherence to design_spec.md, "
                "correct element IDs, page routing, data file correctness, and overall quality; produce code_feedback.md with gating feedback marker."
            ),
            "tools": ["write_text_file", "validate_python_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "code_feedback.md"}]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "AppGenerator",
            "reviewer_agent": "CodeCritic",
            "review_criteria": (
                "Verify that app.py and templates/*.html fully implement the design_spec.md requirements without adding unauthorized features, "
                "ensure code correctness, functional accuracy, proper use of element IDs, and seamless data file integration."
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
    goal: str = "Deliver a complete, validated Python Flask WeatherForecast web application with specified pages and local text file data management as per requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Develop and iteratively improve the design specification for the WeatherForecast web app.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Refine detailed design spec covering all page UI and data file formats."}
            ]
        },
        {
            "step": 2,
            "description": "Develop and iteratively refine the Python Flask implementation and verify its correctness.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Build and validate the web app code and templates fully conforming to design."}
            ]
        }
    ]
): pass
# Orchestrate_End