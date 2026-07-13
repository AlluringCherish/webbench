# Phase1_Start
def design_specification_phase(
    goal: str = "Create a detailed design specification document for the GymMembership web application's UI, page structure, element IDs, navigation flow, and data handling, delivering 'design_spec.md' and gated 'design_feedback.md'.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = ("DesignGenerator writes 'design_spec.md' describing the full UI design, page layout with exact element IDs, navigation logic, and data storage format based on the user task. "
                                      "DesignCritic reviews 'design_spec.md' against the user task and writes 'design_feedback.md' starting with [APPROVED] or NEED_MODIFY. "
                                      "The loop iterates at most twice until approval or stopping after two iterations."),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "prompt": """You are a Software Architect specializing in Python web application UI and data design.

Your goal is to produce or revise a complete design specification document for the GymMembership web application, detailing all pages, UI element IDs, navigation flow, and local text file data format, guided by user requirements and critic feedback.

Task Details:
- Read user_task_description, the latest design_spec.md, and design_feedback.md from CONTEXT
- On the first iteration, create a full design_spec.md covering page titles, element IDs, navigation, and data storage format
- Upon feedback beginning with NEED_MODIFY, apply all corrections and completely rewrite design_spec.md
- Upon feedback beginning with [APPROVED], preserve and finalize design_spec.md

**Section 1: Page and UI Element Design**
- Describe each page with its title and overview
- Specify all UI elements precisely with their element IDs and types
- Detail the navigation structure including buttons or links and their target pages

**Section 2: Local Data Storage Format**
- Specify file names, data schema, and field separators for the local text files managing membership, classes, trainers, bookings, and workouts
- Provide example data records matching the schema

**Section 3: Data and Navigation Consistency**
- Ensure element IDs match across pages and navigation buttons connect valid targets
- Verify data storage format aligns with UI elements displaying or modifying the data

CRITICAL SUCCESS CRITERIA:
- Run at most two Generator/Critic iterations until [APPROVED] or two revisions
- Fully cover all nine specified pages and their detailed elements with exact IDs
- Fully specify navigation logic and data text file layouts as per user task
- Use write_text_file tool to output design_spec.md
- Do not include any feedback marker in design_spec.md

Output: design_spec.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
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
            "prompt": """You are a Design Reviewer specializing in Python web application UI and local data design.

Your goal is to review the design_spec.md against the user requirements for GymMembership, ensuring completeness, correctness, consistency, and adherence; provide gated feedback starting with exactly [APPROVED] or NEED_MODIFY for up to two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Check coverage and correctness of all nine specified pages, their element IDs, and navigation flows
- Verify data storage format correctness and alignment with UI design
- Confirm no contradictions, missing pages, or navigation dead ends exist
- Write feedback indexed by starting with [APPROVED] when design_spec.md fully meets requirements, or NEED_MODIFY followed by concrete correction instructions otherwise

Review Criteria:
1. All pages are fully described with required element IDs and types
2. Navigation elements and flows are clearly specified and consistent
3. Data files and their formats match user examples and usage described in UI
4. Design matches user task scope and avoids additions or omissions
5. Feedback begins exactly with [APPROVED] or NEED_MODIFY without prefixes

CRITICAL REQUIREMENTS:
- Feedback files must start with exact marker byte-1 sequences [APPROVED] or NEED_MODIFY
- Save complete feedback text with write_text_file tool

Output: design_feedback.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
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
            "review_criteria": "Check that design_spec.md fully covers all required pages, element IDs, navigation flows, data storage formats, and no contradictions or missing details.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Develop and refine the complete GymMembership web application with app.py and templates/*.html implementing all pages, exact element IDs, local text file data handling, starting from dashboard, delivering app.py, templates/*.html, and code_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = ("AppGenerator writes or revises app.py and templates/*.html implementing the GymMembership application following design_spec.md and addressing code_feedback.md. "
                                      "CodeCritic reviews the implementation for correctness, element ID accuracy, navigation, and data handling consistency; produces code_feedback.md starting with [APPROVED] or NEED_MODIFY. "
                                      "Iterations run at most twice until approval or stopping after two iterations."),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "prompt": """You are a Python Web Developer specializing in building Flask web applications with local text file data handling.

Your goal is to implement or revise a complete GymMembership web application including app.py and templates/*.html, following design_spec.md and incorporating any code_feedback.md, for up to two refinement iterations.

Task Details:
- Read design_spec.md, existing app.py, templates/*.html, and code_feedback.md from CONTEXT.
- On first iteration, produce the full implementation of app.py and all template files.
- On code_feedback.md starting with NEED_MODIFY, carefully revise and overwrite all outputs applying all feedback.
- On code_feedback.md starting with [APPROVED], maintain the approved implementation.
- Output fully implemented and consistent app.py and templates/*.html files.

**Implementation Requirements:**
- Implement all nine pages exactly as specified: Dashboard, Membership Plans, Plan Details, Class Schedule, Trainer Profiles, Trainer Detail, PT Booking, Workout Records, Log Workout.
- Use exact element IDs for each page element as specified in design_spec.md.
- Implement navigation between pages via the specified buttons and links.
- Handle data persistence entirely via local text files in the 'data' directory: memberships.txt, classes.txt, trainers.txt, bookings.txt, workouts.txt.
- Ensure file reading and writing conform to provided data file formats.
- Do not implement user authentication; all features are directly accessible.
- The application must start at the Dashboard page.

**Templates Implementation Details:**
- Each template file corresponds to one page and must contain all required elements with specified IDs.
- Include buttons, dropdowns, tables, inputs with the correct types and IDs.
- Follow naming consistent with app.py route handlers.

**Code Quality:**
- Use concise, clear Python and HTML syntax.
- Include comments using single-quote docstrings or hash comments only.
- Apply robust local file parsing and writing utilities.
- Prepare the app.py and templates for immediate testing.

CRITICAL REQUIREMENTS:
- Use write_text_file tool to save updated app.py and all templates/*.html.
- Run at most two iterations; stop immediately if code_feedback.md begins with [APPROVED].
- Do not add features beyond those described in design_spec.md.
- Preserve exact element IDs and page navigation flows.
- Overwrite app.py and all templates completely on NEED_MODIFY feedback.

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
            "prompt": """You are a Software Test Engineer specializing in Python web application code and HTML template verification.

Your goal is to review app.py and templates/*.html implementing the GymMembership application for correctness, adherence to design specifications, finish conditions, and produce gated feedback code_feedback.md for up to two refinement iterations.

Task Details:
- Read design_spec.md, app.py, and all templates/*.html from CONTEXT.
- Confirm all required page elements for the nine pages exist with exact element IDs as specified.
- Verify navigation buttons and links enable correct page transitions.
- Validate local text file data handling in app.py matches required format and functionality.
- Check that no authentication is implemented and starting page is Dashboard.
- Write feedback starting exactly with [APPROVED] if all criteria pass.
- Otherwise start with NEED_MODIFY followed by explicit, actionable corrections.
- Focus on structural correctness, element IDs, navigation consistency, data file usage, and user task compliance.
- Do not add new feature requests or extraneous comments.

Review Checklist:
1. Page completeness: all pages present with required elements and IDs.
2. Navigation correctness between pages via specified buttons.
3. Accurate reading and writing to local text files with correct fields and formats.
4. Starting the app at the Dashboard page.
5. No authentication implemented.
6. Correct code structure, no syntax errors.
7. Feedback must enable AppGenerator to revise fully within two iterations.

CRITICAL REQUIREMENTS:
- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY.
- No additional formatting or decoration before this marker.
- Use write_text_file tool to save code_feedback.md.
- Limit review scope strictly to user task requirements and design_spec.md compliance.

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
            "review_criteria": "Gate implementation accuracy for app.py and templates/*.html based on design_spec.md, focusing on element ID correctness, page navigation, data storage, and completeness.",
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
    goal: str = "Develop the GymMembership Python web application delivering app.py and templates/*.html implementing the specified pages, navigation with exact element IDs, and local text file data management.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the design specification document for the GymMembership application for at most two iterations.",
            "phases": [
                {"phase_name": "design_specification_phase", "role": "Create and refine the GymMembership application design specification."}
            ]
        },
        {
            "step": 2,
            "description": "Develop and refine the GymMembership application implementation for at most two iterations.",
            "phases": [
                {"phase_name": "implementation_and_verification_phase", "role": "Implement and verify the GymMembership web application based on design specification."}
            ]
        }
    ]
): pass
# Orchestrate_End