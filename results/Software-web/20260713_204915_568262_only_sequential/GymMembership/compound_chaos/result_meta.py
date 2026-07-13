# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the GymMembership requirements and produce a detailed design_spec.md outlining pages, elements, navigation, and data formats.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first writes requirements_analysis.md detailing all pages, elements, and data storage; "
        "then WebArchitect reads requirements_analysis.md and produces design_spec.md defining Flask routes, templates, page IDs, "
        "navigation flows, data file use, and context variable contracts."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Analyze the user requirements comprehensively to enumerate all pages, UI elements with IDs, navigation flows, "
                "and local data file specifications in requirements_analysis.md."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        },
        {
            "agent_name": "WebArchitect",
            "role": (
                "Convert requirements_analysis.md into a detailed design_spec.md for the Flask GymMembership app, including route-to-template mappings, "
                "exact page element IDs, data file read/write methods, context variable structures, and navigation logic with Dashboard as root."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md", "source": "RequirementsAnalyst"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "RequirementsAnalyst",
            "reviewer_agent": "WebArchitect",
            "review_criteria": "Verify that requirements_analysis.md captures every page, element ID, navigation button, and data file structure exactly as requested without omissions.",
            "review_artifacts": [
                {"type": "user", "name": "user_task_description"},
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_phase(
    goal: str = "Implement the GymMembership Flask application as app_draft.py and templates_draft/*.html consistent with design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "DraftEngineer writes app_draft.py and all templates_draft/*.html following design_spec.md, implementing exact routes,"
        "page titles, element IDs, local text-file data access, and navigation flows; IntegrationEngineer then refines these into final app.py and "
        "templates/*.html, removing draft artifacts and ensuring readiness for validation."
    ),
    team: list = [
        {
            "agent_name": "DraftEngineer",
            "role": (
                "Write the Flask app draft in app_draft.py and all corresponding templates_draft/*.html, strictly respecting design_spec.md's "
                "page IDs, button routes, data file accesses, and Dashboard root route; read/write plaintext data files as specified."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationEngineer",
            "role": (
                "Convert app_draft.py and templates_draft/*.html into finalized app.py and templates/*.html, eliminating draft placeholders, polishing code,"
                "and enforcing all design_spec.md requirements, including the root Dashboard page and exact UI element IDs."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app_draft.py", "source": "DraftEngineer"},
                {"type": "text_file", "name": "templates_draft/*.html", "source": "DraftEngineer"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DraftEngineer",
            "reviewer_agent": "IntegrationEngineer",
            "review_criteria": "Check accuracy of app_draft.py and templates_draft/*.html against design_spec.md for route correctness, element IDs, data file handling, and navigation.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app_draft.py"},
                {"type": "text_file", "name": "templates_draft/*.html"}
            ]
        }
    ]
): pass
# Phase2_End

# Phase3_Start
def verification_phase(
    goal: str = "Validate and fix the final Flask application producing a fully runnable app.py and templates/*.html that meet all requirements.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator validates the final app.py and templates/*.html for runtime errors, route availability, data file accesses, and UI element presence, "
        "then SequentialFixer applies corrections based on validation_report.md ensuring full functionality and compliance."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "role": (
              "Perform syntax and runtime validation of app.py, check all Flask routes exist and respond correctly, verify templates/*.html "
              "contain all requested pages and element IDs, and generate a validation_report.md detailing issues and improvements."
            ),
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "SequentialFixer",
            "role": (
                "Analyze validation_report.md and produce corrected app.py and templates/*.html resolving all functionality, routing, and UI element issues "
                "to meet original GymMembership requirements exactly."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "user", "name": "user_task_description", "source": "User"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "WebValidator",
            "reviewer_agent": "SequentialFixer",
            "review_criteria": "Ensure validation_report.md identifies all runtime, routing, and UI element inconsistencies for repair.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": "Confirm that fixed app.py and templates/*.html fully implement the original user requirements and design specifications.",
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase3_End

# Orchestrate_Start
def orchestrate(
    goal: str = "Develop a complete GymMembership Python Flask application managing all specified pages and local text file storage.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze requirements and produce detailed design specifications.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce a detailed design_spec.md covering all app design aspects."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the GymMembership app draft and finalize source and templates.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Produce a complete Flask app.py and templates as per design_spec.md."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and fix the final Flask app producing a fully functional GymMembership application.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Deliver a validated and corrected runnable Flask app with templates."}
            ]
        }
    ]
): pass
# Orchestrate_End