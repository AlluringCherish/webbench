# Phase1_Start
def design_specification_phase(
    goal: str = "Analyze the NewsPortal requirements document and produce a complete design_spec.md specifying Flask routes, pages, elements, data contracts, and navigation flows.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "RequirementsAnalyst first creates requirements_analysis.md tracing every requested page, route, element ID, data file format, navigation path, and feature; "
        "then WebArchitect consumes that to produce design_spec.md detailing Flask route methods, exact page titles, element IDs, directory layout, and data contracts."
    ),
    team: list = [
        {
            "agent_name": "RequirementsAnalyst",
            "role": (
                "Analyze the user task and produce requirements_analysis.md, tracing every page (Dashboard, Catalog, Article Details, Bookmarks, Comments, Write Comment, Trending, Category, Search Results), "
                "routes, exact element IDs, data file formats and example usages, page-to-template mappings, navigation buttons, and bookmark/comment/trending functionality."
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
                "Create design_spec.md defining Flask app architecture for NewsPortal, listing all routes and HTTP methods, exact page titles, all element IDs on each page, "
                "templates folder names, data file parsing details for articles, categories, bookmarks, comments, and trending data, and UI navigation flows."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "requirements_analysis.md", "source": "RequirementsAnalyst"}
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
            "review_criteria": (
                "Verify requirements_analysis.md includes all page elements, exact requested element IDs, all data file formats with examples, and detailed navigation flows."
            ),
            "review_artifacts": [
                {"type": "user", "name": "user_task_description"},
                {"type": "text_file", "name": "requirements_analysis.md"}
            ]
        },
        {
            "source_agent": "WebArchitect",
            "reviewer_agent": "ImplementationEngineer",
            "review_criteria": (
                "Ensure design_spec.md fully implements all requirements from requirements_analysis.md, including precise Flask routes, template names, data file parsing contracts, "
                "page titles, element IDs, and correct navigation button actions."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "requirements_analysis.md"},
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End

# Phase2_Start
def implementation_phase(
    goal: str = "Implement NewsPortal as a Flask application with exact Flask routes, app.py, and templates/*.html files according to design_spec.md.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "ImplementationEngineer writes a complete app.py with all routes and logic per design_spec.md; TemplateDesigner writes all templates/*.html files with exact element IDs and content structure; "
        "IntegrationEngineer integrates app.py and templates ensuring no draft paths remain and all features function as specified."
    ),
    team: list = [
        {
            "agent_name": "ImplementationEngineer",
            "role": (
                "Develop app.py implementing every Flask route specified in design_spec.md with correct HTTP methods, data loading from local text files in 'data' directory, and logic for browsing, "
                "reading, bookmarking, commenting, trending, and filtering."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"}
            ]
        },
        {
            "agent_name": "TemplateDesigner",
            "role": (
                "Create all HTML templates under templates/ directory with exact element IDs and page structure as specified in design_spec.md for Dashboard, Catalog, Article Details, Bookmarks, Comments, "
                "Write Comment, Trending, Category, and Search Results pages."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "templates/*.html"}
            ]
        },
        {
            "agent_name": "IntegrationEngineer",
            "role": (
                "Integrate app.py and templates/*.html into final working NewsPortal application, removing any draft or temporary references, "
                "ensuring correct render_template usage, data parsing from text files, and that navigation buttons redirect properly."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "ImplementationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "TemplateDesigner"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "ImplementationEngineer",
            "reviewer_agent": "IntegrationEngineer",
            "review_criteria": (
                "Verify app.py implements all routes and data loading exactly as design_spec.md requires, especially handling data files, navigation buttons, and page responses."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"}
            ]
        },
        {
            "source_agent": "TemplateDesigner",
            "reviewer_agent": "IntegrationEngineer",
            "review_criteria": (
                "Verify all templates/*.html contain every required element with exact IDs, page titles, and structure, and that navigation buttons and links match design_spec.md."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        },
        {
            "source_agent": "IntegrationEngineer",
            "reviewer_agent": "WebValidator",
            "review_criteria": (
                "Assess the integrated app.py and templates/*.html form a runnable Flask web app adhering to design_spec.md and requirements_analysis.md."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        }
    ]
): pass
# Phase2_End

# Phase3_Start
def verification_phase(
    goal: str = "Validate the NewsPortal Flask application for correctness, completeness, and usability, then produce validation_report.md with actionable fixes.",
    collab_pattern_name: str = "Sequential Flow",
    collab_pattern_description: str = (
        "WebValidator runs full Flask application verification, checking route correctness, page rendering, data loading, navigation, and UI completeness; "
        "SequentialFixer then applies fixes from validation_report.md to finalize app.py and templates."
    ),
    team: list = [
        {
            "agent_name": "WebValidator",
            "role": (
                "Validate the final app.py with templates/*.html against design_spec.md and requirements_analysis.md, verifying Flask syntax, route existence, data file reading, exact element IDs, "
                "navigation buttons, and expected page content; write detailed validation_report.md with findings."
            ),
            "tools": ["validate_python_file", "execute_python_code", "write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "validation_report.md"}
            ]
        },
        {
            "agent_name": "SequentialFixer",
            "role": (
                "Apply all actionable corrections from validation_report.md to improve and finalize app.py and templates/*.html, ensuring all required features and exact IDs are correct and the app is fully functional."
            ),
            "tools": ["write_text_file"],
            "llm_model": "precision",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "WebArchitect"},
                {"type": "text_file", "name": "app.py", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "templates/*.html", "source": "IntegrationEngineer"},
                {"type": "text_file", "name": "validation_report.md", "source": "WebValidator"}
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
            "review_criteria": (
                "Verify validation_report.md comprehensively covers route correctness, data file parsing, element IDs, navigation, and includes clear fix instructions."
            ),
            "review_artifacts": [
                {"type": "text_file", "name": "validation_report.md"},
                {"type": "text_file", "name": "design_spec.md"},
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"}
            ]
        },
        {
            "source_agent": "SequentialFixer",
            "reviewer_agent": "RequirementsAnalyst",
            "review_criteria": (
                "Validate that the finalized app.py and templates/*.html fully resolve all validation issues and meet user requirements completely."
            ),
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
    goal: str = "Build a fully functional NewsPortal Python Flask web application with browsing, bookmarking, commenting, trending, and search features using local text file data storage.",
    workflow: list = [
        {
            "step": 1,
            "description": "Analyze user requirements and design precise design specifications for the NewsPortal application.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Produce detailed architectural design_spec.md and requirements_analysis.md."}
            ]
        },
        {
            "step": 2,
            "description": "Implement the NewsPortal application including app.py and HTML templates as per design specifications.",
            "phases": [
                {"phase_name": "implementation_phase", "role": "Develop final app.py and templates/*.html for NewsPortal."}
            ]
        },
        {
            "step": 3,
            "description": "Validate and fix the NewsPortal application to ensure full requirement compliance and functional correctness.",
            "phases": [
                {"phase_name": "verification_phase", "role": "Produce validation_report.md and final corrected app.py and templates."}
            ]
        }
    ]
): pass
# Orchestrate_End