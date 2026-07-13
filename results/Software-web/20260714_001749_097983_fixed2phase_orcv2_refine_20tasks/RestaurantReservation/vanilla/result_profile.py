# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the adaptive Web design contract specifying all page layouts, element IDs, navigation flow and data file schema; deliver design_spec.md and design_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator drafts design_spec.md from user_task_description and prior design_feedback.md; DesignCritic reviews and produces design_feedback.md with gating status.",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "prompt": """You are a Software Designer specializing in Python web application UI/UX and data storage design.

Your goal is to create or revise a comprehensive design specification document covering all page layouts, element IDs, navigation flow, and data file schemas derived from user requirements and prior critic feedback for at most two iterations.

Task Details:
- Read user_task_description, current design_spec.md, and design_feedback.md from CONTEXT
- On first iteration, author complete design_spec.md covering page titles, element IDs, navigation, and data file formats
- On feedback NEED_MODIFY, incorporate all corrections and rewrite the full design_spec.md
- Preserve the approved design if feedback starts with [APPROVED]

**Section 1: Page Layout and Element IDs**
- Specify every page by its title and contain a clear list of element IDs with their HTML types and descriptions
- Include all navigation buttons and their purposes exactly as described in user requirements
- Maintain consistency of element IDs for navigation across pages (e.g., back-to-dashboard)

**Section 2: Navigation Flow**
- Define the navigation logic between pages via button IDs and target pages
- Describe how users transition between pages according to the user task specification

**Section 3: Data File Schema Specification**
- Document all data files stored locally under 'data/' directory exactly as specified
- For each file, specify filename, exact pipe-delimited field structure with field names and data type hints
- Include examples as in user requirements; do not invent additional fields or files

CRITICAL SUCCESS CRITERIA:
- Run at most two cycles of Generator/Critic revisions
- Integrate every supported NEED_MODIFY item fully without omitting details or adding new requirements
- Use write_text_file tool to save design_spec.md
- Do not write any feedback marker in design_spec.md
- Focus exclusively on user requirements for page elements, navigation, and data schema

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        },
        {
            "agent_name": "DesignCritic",
            "prompt": """You are a Design Reviewer specializing in Python web application UI/UX and data storage contracts.

Your goal is to review design_spec.md for completeness, accuracy, and alignment with the user_task_description; provide gated feedback in design_feedback.md to allow at most two refinement iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Assess the completeness and correctness of page titles, required element IDs, navigation flow, and data file schemas against user requirements
- Validate data file schemas match the exact fields, formats, delimiters, and example rows described
- Verify navigation IDs and flows are coherent and complete
- Write feedback starting exactly with [APPROVED] if fully compliant
- Otherwise write NEED_MODIFY followed by explicit, actionable corrections listing missing or inconsistent items

Review Criteria:
1. All nine pages must be specified with correct page titles and element IDs including described button IDs.
2. Navigation buttons and their target pages must be fully and accurately described.
3. Data files under 'data/' directory must be documented with exact field schemas, delimiters, and examples.
4. No extra or omitted requirements beyond user task are permitted.
5. Feedback must be clear and unambiguous to guide full correction.

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY without any prefix or heading
- Use write_text_file tool to save complete feedback
- Stop refinement immediately after approval or max two iterations reached

Output: design_feedback.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_feedback.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "DesignGenerator",
            "reviewer_agent": "DesignCritic",
            "review_criteria": "Verify design_spec.md aligns precisely with all user-stated page structure, element ID requirements, navigation logic, and data file formats.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Develop and refine the full RestaurantReservation Python Flask web app implementation with all specified pages, element IDs, navigation, and data management per design_spec.md; deliver app.py, templates/*.html and gated code_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator writes or revises canonical app.py and templates/*.html from design_spec.md and code_feedback.md; CodeCritic assesses code correctness, page completeness, route correctness, element ID exactness, and data file access, producing code_feedback.md with approval status.",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "prompt": """You are a Python Flask Developer specializing in full-stack web applications using local text file data management.

Your goal is to implement or revise the complete RestaurantReservation Flask application, including app.py and all HTML templates, fully conforming to the design specification and incorporating critic feedback, within at most two iterations.

Task Details:
- Read design_spec.md and the latest code_feedback.md from CONTEXT to guide development and refinement.
- Read current app.py and all templates/*.html as starting points.
- Produce complete app.py and all templates/*.html reflecting all nine pages, exact element IDs, navigation routes, and local text file data usage.
- On first iteration, produce full implementation; on NEED_MODIFY feedback, apply all corrections and overwrite prior artifacts.
- Preserve specified naming, directory structure, and data file integration as per design_spec.md.

**Section 1: Flask Application Structure**
- Implement all specified routes corresponding to each page (Dashboard, Menu, Dish Details, Make Reservation, My Reservations, Waitlist, My Reviews, Write Review, User Profile).
- Each route must render appropriate template with precise context variables.
- Ensure navigation buttons trigger correct route redirects.
- Use local text files in 'data' directory for all data operations (users.txt, menu.txt, reservations.txt, waitlist.txt, reviews.txt) with exact parsing format (pipe-delimited).

**Section 2: HTML Template Requirements**
- Develop one template per page in templates directory (*.html).
- Include all specified page-level container divs with exact IDs.
- Include all required interactive elements with exact IDs and types (buttons, inputs, dropdowns, tables, divs).
- Templates must interact properly with Flask context variables and forms.

**Section 3: Data Integration and Management**
- Read and write data to text files maintaining specified formats.
- Ensure data consistency and correct usage of file-based data in routes and templates.
- Support data operations like browsing menu, submitting reservations and reviews, managing waitlist, and user profile updates.

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to output app.py and all templates/*.html.
- Run at most two iterations; apply all supported NEED_MODIFY corrections fully.
- Output artifacts must exactly match names and folders: app.py, templates/*.html.
- Do not add or omit pages, element IDs, or data files beyond design_spec.md.
- Implement robust navigation and data handling as described.

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
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
            "prompt": """You are a Software Test Engineer specializing in Flask web application code and template verification.

Your goal is to conduct a comprehensive review of app.py and all templates/*.html to verify full implementation compliance with the provided design_spec.md, and produce gated feedback within at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT.
- Review presence and correctness of all nine specified pages and their route handlers.
- Verify every specified element ID within HTML templates is present and matches design_spec.md exactly.
- Validate button and form routes for correctness and navigation accuracy.
- Confirm data file usage (read/write operations) matches specified local text file formats and locations.
- Write code_feedback.md starting with exactly [APPROVED] if implementation meets all criteria or NEED_MODIFY followed by specific actionable corrections.

Review Criteria:
1. All nine pages implemented with full routes and templates.
2. Exact element IDs for containers, buttons, inputs, dropdowns, tables, and divs per page.
3. Navigation flows correctly across pages via buttons and links.
4. Data file handling matches specification; no missing or extraneous data access.
5. Code and templates follow Flask and HTML best practices.

CRITICAL REQUIREMENTS:
- code_feedback.md MUST begin exactly with [APPROVED] or NEED_MODIFY marker, no preceding text or whitespace.
- Provide detailed modification instructions on NEED_MODIFY.
- Use write_text_file tool to save code_feedback.md as the output.

Output: code_feedback.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"}
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "code_feedback.md"}
            ]
        }
    ],
    review_policy: list = [
        {
            "source_agent": "AppGenerator",
            "reviewer_agent": "CodeCritic",
            "review_criteria": "Ensure accuracy and completeness of app.py and templates/*.html against design_spec.md, including correctness of routes, element IDs, and data file handling.",
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
    goal: str = "Build the complete RestaurantReservation Python Flask web application with specified pages, navigation, element IDs, and local text file data handling.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine and finalize the design specification for the RestaurantReservation application.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Create detailed design specifications including page layout, IDs, data storage format."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement the comprehensive Python Flask app and HTML templates, and refine through review cycles.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Develop and refine the implementation of the web application according to design."
                }
            ]
        }
    ]
): pass
# Orchestrate_End