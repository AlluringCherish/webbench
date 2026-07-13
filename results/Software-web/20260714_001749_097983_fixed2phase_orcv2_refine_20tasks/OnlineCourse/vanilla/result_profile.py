# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the comprehensive design specification for the 'OnlineCourse' Python web application capturing all pages, UI element IDs, data formats, and user workflows into design_spec.md with gated feedback in design_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "DesignGenerator writes design_spec.md from user_task_description and design_feedback.md; DesignCritic reviews design_spec.md producing design_feedback.md; iteration runs up to two times or stops on [APPROVED].",
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "prompt": """You are a Software Architect specializing in Python web application design specifications.

Your goal is to produce a detailed and complete design specification document capturing UI pages, element IDs, data storage schemas, and user workflows for the 'OnlineCourse' Python web application, refining it through critic feedback for up to two iterations.

Task Details:
- Read user_task_description from CONTEXT
- Read prior versions of design_spec.md and design_feedback.md when available to determine if REWRITE is needed
- On first iteration, create a thorough design_spec.md describing all required pages, UI element IDs, data formats, and functional workflows
- On feedback that begins with NEED_MODIFY, apply every correction fully and overwrite design_spec.md
- On feedback starting with [APPROVED], preserve the approved design

**Section 1: UI Pages and Element IDs**
- Document all 9 application pages with page titles, purpose, and all specified element IDs including repeated elements (e.g. buttons with dynamic IDs)
- Include navigation flows among pages as described
- Ensure element types and IDs match user requirements exactly

**Section 2: Data Storage Formats**
- Specify text file names and exact data field formats per user specification
- Include data field orders, separators, and example rows as structured text
- Confirm data file uses consistent delimiter and encodings

**Section 3: Functional Workflows**
- Detail user interactions such as enrollment, assignment submission, progress tracking, and certificate issuance
- Specify logic for button states, progress calculations, sequential lesson completion, and automatic certificate generation
- Reflect all user objectives and requirements fully

CRITICAL SUCCESS CRITERIA:
- Produce fully comprehensive design_spec.md aligned with user_task_description
- Rewrite entire artifact on NEED_MODIFY feedback, using all supported corrections
- Use write_text_file tool to output design_spec.md
- Run at most two Generator/Critic iterations, stopping immediately on approved status

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
            "prompt": """You are a Design Reviewer specializing in Python web application design specifications.

Your goal is to review the design_spec.md document for completeness, correctness of page layouts, accuracy of UI element IDs, consistency of data formats, and full adherence to the user's functional objectives; provide gated feedback marking completion as [APPROVED] or identify issues as NEED_MODIFY for up to two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT
- Check coverage of all nine required pages with correct titles and exact UI element IDs including repeated dynamic elements
- Verify data storage schemas match the specified local text file formats, field delimiters, and example data
- Confirm functional workflows reflect all required user interactions from enrollment through certificate generation
- Write feedback in design_feedback.md starting with exactly [APPROVED] if all criteria met
- Otherwise, write NEED_MODIFY followed by specific, actionable corrections without adding new requirements beyond user_task_description

Review Criteria:
1. Completeness of page designs and UI element ID accuracy
2. Accuracy and consistency of data file names, field formats, and example entries
3. Fidelity of workflows including button states, progress calculations, and message displays
4. Alignment with stated user objectives and no missing requirements
5. No introduction of unstated functions or data structures

CRITICAL REQUIREMENTS:
- Begin design_feedback.md with byte-1 marker exactly '[APPROVED]' or 'NEED_MODIFY'
- No additional prefixes, whitespace, or headings before marker
- Use write_text_file tool to save full feedback document

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
            "review_criteria": "Ensure the design covers all required pages and UI elements with correct IDs, accurately describes local text data storage formats, and aligns fully with user functional objectives.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Refine complete Python Flask web application source code (app.py and templates/*.html) implementing the 'OnlineCourse' system to specification with gated feedback in code_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = "AppGenerator writes or fully revises app.py and all templates/*.html implementing design_spec.md and code_feedback.md feedback; CodeCritic reviews code correctness, UI element IDs, data file handling, and application functionality, producing code_feedback.md; iteration runs up to two times or stops on [APPROVED].",
    team: list = [
        {
            "agent_name": "AppGenerator",
            "prompt": """You are a Python Flask Developer specializing in web application backend and frontend template development.

Your goal is to develop or fully revise the complete Flask app.py backend and corresponding HTML templates implementing all pages, UI elements with exact IDs, local text file data management, and workflow logic according to design_spec.md and any code_feedback.md for up to two refinement iterations.

Task Details:
- Read design_spec.md to understand full application structure, pages, elements, and data file formats
- Read existing app.py, templates/*.html, and code_feedback.md for requested changes
- On first iteration, create fully functional app.py and templates implementing all specified pages and features
- On feedback starting with NEED_MODIFY, apply all corrections fully and overwrite app.py and templates
- Preserve approval if code_feedback.md begins with [APPROVED]
- Focus on Python backend logic for data files and Flask routes, plus exact HTML templates with specified element IDs

**Section 1: Backend Implementation**
- Implement all Flask routes and view functions for 9 pages with routing and navigation
- Manage local text files (users.txt, courses.txt, enrollments.txt, assignments.txt, submissions.txt, certificates.txt) for CRUD operations
- Implement business logic for enrollment, progress tracking, assignment submissions, and certificate generation
- Enforce sequential lesson completion and progress updates in enrollments.txt
- Include proper date handling for enrollment and submissions

**Section 2: Frontend Templates**
- Create HTML templates for each page with all specified element IDs exactly as declared
- Use Flask templating for dynamic content (user info, course lists, assignments, progress, certificates)
- Include buttons and controls with IDs for navigation and actions
- Ensure consistent navigation links between pages as per design

**Section 3: Refinement and File Output**
- Use write_text_file tool to output complete app.py and templates/*.html files
- Submit fully integrated code reflecting corrections or new implementation each iteration

CRITICAL SUCCESS CRITERIA:
- Run at most two full Generator/Critic iterations or stop immediately on approval
- Apply every NEED_MODIFY item fully and correctly on rewrite iterations
- Maintain exact UI element IDs and data file formats from design_spec.md
- Use write_text_file tool to save output files app.py and templates/*.html

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
            "prompt": """You are a Software Test Engineer specializing in Python Flask applications and HTML frontend verification.

Your goal is to review app.py and HTML templates for syntax correctness, full functional completeness, strict adherence to UI element ID specifications, correct local text file handling, and workflow consistency; provide gated feedback for up to two iterations beginning each code_feedback.md with [APPROVED] or NEED_MODIFY.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Validate Python syntax and runtime correctness using validate_python_file
- Verify all 9 pages' UI elements have exact IDs as specified
- Confirm Flask routes and backend logic fully implement design requirements
- Check proper reading, writing, and updating of local text data files (users, courses, enrollments, assignments, submissions, certificates)
- Verify workflow logic like enrollment handling, progress calculation, assignment submission, and certificate issuance
- Write code_feedback.md starting exactly with [APPROVED] if all criteria met or NEED_MODIFY and specific corrections otherwise

Review Checklist:
1. Syntax and runtime errors absent in app.py
2. All UI element IDs present and correctly named in templates
3. Complete route coverage for all pages with correct navigation links
4. Accurate data file interaction matching design specification format and business logic
5. Correct handling of user interaction flows, statuses, and updates in data files
6. Clear, actionable feedback with specific fix instructions if needed

CRITICAL REQUIREMENTS:
- Use validate_python_file tool for syntax/runtime validation
- The first bytes of code_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY
- Use write_text_file tool to save full feedback text

Output: code_feedback.md""",
            "tools": ["write_text_file", "validate_python_file"],
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
            "review_criteria": "Validate code correctness, full implementation of design_spec.md functional requirements, exact UI element IDs usage, and local text file data integration.",
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
    goal: str = "Build the full 'OnlineCourse' Python web application with specified UI pages, local text data management, and user workflows.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine design specification document describing all UI pages, elements with IDs, data formats, and workflows.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Refine comprehensive design specification for 'OnlineCourse' app."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement and verify the full Python Flask app.py and templates/*.html with feedback loops.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Implement and refine 'OnlineCourse' application code and templates."
                }
            ]
        }
    ]
): pass
# Orchestrate_End