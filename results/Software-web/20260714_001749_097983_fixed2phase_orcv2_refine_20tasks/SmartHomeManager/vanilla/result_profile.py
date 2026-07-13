# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the comprehensive design specification for the SmartHomeManager Flask web application including page structure, navigation, UI elements with exact element IDs, and data file organization, producing design_spec.md and gated design_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator produces design_spec.md detailing pages, element IDs, and data storage contract; DesignCritic reviews this specification and produces design_feedback.md with either [APPROVED] or NEED_MODIFY to guide revision; iteration halts after approval or two cycles.",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "prompt": """You are a System Architect specializing in Flask web application design specifications.

Your goal is to create and iteratively refine a complete design specification for the SmartHomeManager Flask web application, including detailed page structures, element IDs, navigation flows, and data storage formats.

Task Details:
- Read full user_task_description from CONTEXT describing all pages, UI elements with exact IDs, and data files
- Read previous design_spec.md and design_feedback.md when available for refinement
- On first iteration, author the complete design_spec.md covering page design, navigation, element IDs, and data file schemas
- On feedback starting with NEED_MODIFY, apply all indicated corrections thoroughly and overwrite design_spec.md
- When feedback starts with [APPROVED], preserve the final approved design_spec.md

**Section 1: Page and Navigation Design**
- Enumerate all seven pages with their Flask route paths starting at dashboard ('/dashboard')
- Specify each page's title, container div IDs, button IDs, inputs, tables, and UI components as per user_task_description
- Define navigation flow via buttons exactly by ID references (e.g., 'device-list-button' navigates to '/devices')

**Section 2: UI Element ID Specifications**
- Provide exact element IDs and their types (div, button, input, dropdown, table, etc.) for every page element listed
- Maintain consistency in ID naming and type matching user_task_description details

**Section 3: Data Storage Contract**
- Define the 'data' folder usage and detail each data file (name, path)
- Specify file formats with pipe-delimited fields and exact column names matching user_task_description
- Include example rows for each data file as provided
- Keep data isolation by type for efficient management

CRITICAL SUCCESS CRITERIA:
- Must run at most two Generator/Critic iterations and incorporate all NEED_MODIFY feedback
- Use write_text_file tool to save complete design_spec.md after each iteration
- Deliver well-structured design_spec.md enabling implementation and consistent critique
- Reflect accurate Flask routing starting with dashboard page ('/dashboard')

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"}
            ],
            "output_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        },
        {
            "agent_name": "DesignCritic",
            "prompt": """You are a Design Reviewer specializing in Flask web application design specifications.

Your goal is to critically review the design_spec.md against the user_task_description and produce gated feedback that either approves the design or requests revisions with clear actionable details.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Verify every page is defined with exact Flask route paths, beginning with dashboard page ('/dashboard')
- Confirm all UI element IDs, types, and navigation flows fully match user requirements and are unambiguous
- Validate all data storage file definitions, formats, delimiters, field names, and example data accurately reflect the user specification
- Produce feedback starting exactly with [APPROVED] if complete and consistent, or NEED_MODIFY followed by specific corrections required

Review Criteria:
1. All seven pages with their respective IDs and navigation buttons are present and correctly specified
2. Element IDs precisely match those from user_task_description with correct element types
3. Flask routes are appropriate and start at the dashboard
4. Data files are correctly named, formatted using pipe delimiters, with exact field names and example rows
5. No missing or extraneous UI elements or data file fields beyond user specification

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY
- Do not prepend any headings, whitespace, or other markers before the feedback marker
- Use write_text_file tool exclusively to output the full design_feedback.md content
- Feedback must enable generator to fully resolve all requested changes in at most two iterations

Output: design_feedback.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
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
            "review_criteria": "Verify that the design_spec.md fully captures the user requirements, uses exact element IDs for all components, defines the Flask page routing starting at the dashboard, and correctly specifies all data storage files and formats.",
            "review_artifacts": [{"type": "text_file", "name": "design_spec.md"}]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Produce and iteratively refine the complete Flask application code (app.py and templates/*.html) for SmartHomeManager with data handling per design_spec.md, and gated by code_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator creates or revises app.py and all corresponding HTML templates under templates/ directory based on design_spec.md and code_feedback.md; CodeCritic reviews these artifacts for functional correctness, UI compliance, data handling accuracy, and Flask conventions and produces code_feedback.md with [APPROVED] or NEED_MODIFY; up to two iterations per refinement.",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "prompt": """You are a Python Flask Developer specializing in building full-stack web applications with data persisted in local text files.

Your goal is to develop or iteratively refine the complete SmartHomeManager Flask application implementation, including app.py backend and all HTML templates under the templates/ directory, based on design_spec.md and code_feedback.md.

Task Details:
- Read design_spec.md, existing app.py, templates/*.html, and code_feedback.md from CONTEXT
- On initial iteration, produce full app.py and all templates/*.html per design_spec.md requirements
- On feedback NEED_MODIFY, incorporate all corrections fully and rewrite the complete artifacts
- On [APPROVED], preserve approved implementation unchanged
- Focus exclusively on implementing declared pages, exact element IDs, navigation flows starting at dashboard page, data interactions with local text files as specified
- Write app.py and templates/*.html output files precisely with exact naming under expected folders

**Section 1: Flask App Implementation**
- Implement Flask routes for all seven pages named in design_spec.md, starting with dashboard route as root
- Ensure route handlers manage reading and writing to data files in 'data' directory according to specified data schemas
- Handle device control, automation rules, energy reports, and activity logs with correct business logic and persistent storage
- Use proper Flask url_for navigation and POST/GET as appropriate

**Section 2: HTML Templates Requirements**
- Create HTML templates with exactly the specified element IDs (e.g., dashboard-page, device-list-page, add-device-page, etc.)
- Implement button and link navigation that matches route names and element IDs in design_spec.md
- Reflect all UI components for forms, tables, buttons, divs, and inputs as declared

**Section 3: Iterative Refinement**
- On feedback NEED_MODIFY, address all changes comprehensively per CodeCritic comments, rewriting all files
- Use write_text_file tool to save updated app.py and each HTML file in templates/
- Maintain code readability, Flask conventions and UI consistency throughout

CRITICAL SUCCESS CRITERIA:
- Complete implementation covers all functionalities per design_spec.md
- Exact element IDs and navigation routes without omission
- Persistent data stored in text files under 'data' as specified
- Use write_text_file tool strictly to output app.py and templates/*.html files
- Stop after at most two iterations or upon [APPROVED] feedback

Output: app.py and templates/*.html
""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
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
            "prompt": """You are a Software Test Engineer specializing in Flask web applications and code quality assurance.

Your goal is to perform detailed reviews of SmartHomeManager’s app.py and templates/*.html implementation against design_spec.md and produce gated code_feedback.md for at most two refinement iterations.

Task Details:
- Read design_spec.md, app.py, and all templates/*.html from CONTEXT
- Verify compliance with all page requirements, exact element IDs, UI consistency, and correct Flask routing starting at dashboard page
- Validate data handling correctness: local text file reading/writing matching declared formats and storage directory 'data'
- Confirm navigation buttons and links align precisely with route endpoints and element IDs
- Write code_feedback.md beginning exactly with [APPROVED] if fully compliant or NEED_MODIFY followed by clear correction directives if not
- Feedback must guide fixing missing elements, incorrect routes, data handling errors, or UI inconsistencies

Review Requirements:
1. All seven pages exist as Flask routes and correspond to templates/*.html matching design_spec.md
2. Every required UI element ID (buttons, divs, forms, tables) is present and correctly named
3. Data interaction in app.py uses local text files in 'data' folder with exact field parsing per specification
4. Navigation flows through buttons exactly match the specified page transitions
5. No missing functionality or features declared in design_spec.md

CRITICAL REQUIREMENTS:
- code_feedback.md must start with [APPROVED] or NEED_MODIFY with no leading whitespace or extraneous content
- Use write_text_file tool to save complete, precise feedback text
- Limit refinement cycles to two iterations, stop immediately on approval
- Focus feedback exclusively on detail accuracy and completeness without adding new feature requests

Output: code_feedback.md
""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
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
            "review_criteria": "Check that app.py and templates/*.html fully implement the design_spec.md features, use exact element IDs, Flask routes start at dashboard page, and manage local text data files correctly without missing elements.",
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
    goal: str = "Develop the SmartHomeManager Flask web application with precise UI element IDs and local text data storage complying with given requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Iteratively refine the detailed design specification of the SmartHomeManager Flask web app including all pages, elements, and data storage format.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Refine the detailed design specification document for the Flask web app."
                }
            ]
        },
        {
            "step": 2,
            "description": "Iteratively produce and verify the Flask web app implementation (app.py and templates) strictly following the approved design specification.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Produce and refine Flask app code and templates with validation by CodeCritic."
                }
            ]
        }
    ]
): pass
# Orchestrate_End