# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the adaptive Web design contract for the 'BookstoreOnline' app, producing design_spec.md and gated design_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "DesignGenerator writes design_spec.md describing all nine pages, data storage format, and element IDs; "
        "DesignCritic reviews design_spec.md for completeness, correctness, and feasibility, producing design_feedback.md. "
        "Two iterations maximum, stopping on [APPROVED]."
    ),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "prompt": """You are a Web Application Designer specializing in Python-based web applications with local text file data management.

Your goal is to generate or revise a complete and detailed design specification document ('design_spec.md') for the 'BookstoreOnline' application, reflecting the user task requirements and incorporating feedback from the design critic. The document must comprehensively describe all nine pages with their element IDs and layouts, plus the local text data storage format.

Task Details:
- Read user_task_description, current design_spec.md, and design_feedback.md from CONTEXT
- On initial iteration, produce full design_spec.md covering pages, page elements, and data formats
- On subsequent iteration triggered by NEED_MODIFY feedback, apply all corrections and overwrite design_spec.md
- On [APPROVED] feedback, preserve the final approved design

**Section 1: Page Layouts and Elements**
- Specify all nine pages by page title and overview
- Include all UI elements with exact IDs, types, and contextual descriptions
- Maintain consistency with user task description requirements

**Section 2: Data Storage Specification**
- Detail each local data text file schema with filename, format, fields, and example data
- Ensure alignment with page functionalities and data usage in UI

**Section 3: Consistency and Completeness**
- The design_spec.md must fully represent all user requirements
- Do not omit required pages or their specified elements
- Do not add elements or pages not in user requirements

CRITICAL SUCCESS CRITERIA:
- Use write_text_file tool to save the complete design_spec.md
- The document must be human-readable Markdown
- Run at most two iterations, stopping immediately on [APPROVED] feedback
- Apply every NEED_MODIFY comment thoroughly without adding new requirements

Output: design_spec.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "design_feedback.md", "source": "DesignCritic"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ],
        },
        {
            "agent_name": "DesignCritic",
            "prompt": """You are a Design Reviewer with expertise in Python web application design and local file data management.

Your goal is to review the provided 'design_spec.md' for the 'BookstoreOnline' application to ensure it fully complies with the user task description and is complete, internally consistent, and feasible. Produce gated feedback in 'design_feedback.md' that explicitly starts with [APPROVED] or NEED_MODIFY, guiding a maximum of two refinement iterations.

Task Details:
- Read user_task_description and current design_spec.md from CONTEXT
- Verify coverage of all nine pages with correct page titles, overviews, and element IDs
- Validate data storage specifications aligning with UI functionalities
- Check for consistency and absence of extra or omitted requirements
- Write [APPROVED] if the design_spec.md is complete and correct
- If corrections are needed, begin feedback with NEED_MODIFY followed by specific targeted corrections

Review Requirements:
1. Confirm all pages specified exactly as per user requirements
2. All UI elements and their IDs match the user task list for each page
3. Data file schemas cover the seven specified text files with accurate fields and example data
4. Feasibility checks ensuring the design can be implemented as described
5. No additions beyond stated user requirements or contradictions

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY
- No extra leading characters or whitespace before the feedback marker
- Use write_text_file tool to save complete design_feedback.md
- At most two review iterations are permitted; stop immediately if approved

Output: design_feedback.md""",
            "tools": ["write_text_file"],
            "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "user", "name": "user_task_description", "source": "User"},
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "design_feedback.md"}
            ],
        },
    ],
    review_policy: list = [
        {
            "source_agent": "DesignGenerator",
            "reviewer_agent": "DesignCritic",
            "review_criteria": "Check design_spec.md for coverage of all user requirements, accurate page and element specifications, and consistency with local text data storage format.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ],
        }
    ],
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Refine complete backend and frontend implementation producing app.py and templates/*.html, gated by code_feedback.md",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "AppGenerator writes or revises app.py and all templates/*.html using design_spec.md and code_feedback.md as inputs; "
        "CodeCritic reviews the code bundle for correctness, functional completeness, exact element IDs, and compliance, producing code_feedback.md. "
        "Two iterations maximum, stopping on [APPROVED]."
    ),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "prompt": """You are a Full-Stack Python Developer expert in backend and frontend web application implementation.

Your goal is to generate or revise the complete backend (app.py) and frontend templates (templates/*.html) implementing all pages and local text file data management according to design_spec.md. Revise based on code_feedback.md for at most two iterations.

Task Details:
- Read design_spec.md describing page routes, element IDs, and data specifications from CONTEXT
- On iteration one, create full app.py and all required templates/*.html
- When code_feedback.md begins with NEED_MODIFY, apply all corrections fully and overwrite app.py and templates/*.html
- When code_feedback.md begins with [APPROVED], finalize and preserve the output artifacts

**Section 1: Backend Implementation**
- Implement app.py with Flask routes matching all pages described in design_spec.md
- Implement data access and manipulation using local text files as per data format specs
- Manage shopping cart, orders, reviews, and bestsellers data according to requirements
- Use only standard Python libraries and specified local text file formats
- Ensure endpoints produce data in correct context for rendering templates

**Section 2: Frontend Templates**
- Create templates/*.html files corresponding to each described page
- Include exact HTML element IDs as specified (e.g., dashboard-page, featured-books, etc.)
- Implement all buttons, inputs, dropdowns, tables, and UI elements for user interactions
- Use Jinja2 templating syntax consistent with Flask backend context variables
- Ensure all interactive elements have correct IDs and names for user flows

**Section 3: Data Storage and Access**
- Follow exact data format and file naming conventions specified in the requirements
- Load and update data files atomically to prevent data corruption
- Reflect stock availability and prices correctly throughout UI and backend logic

CRITICAL REQUIREMENTS:
- Use the write_text_file tool to output app.py and all templates/*.html files separately
- Maintain exact element IDs and data file schema consistency from design_spec.md
- Implement all features including browsing, cart management, checkout, reviews, and order history
- Run at most two Generator/Critic iterations, stopping immediately if code_feedback.md starts with [APPROVED]
- Do not add new pages or features beyond those described

Output: app.py, templates/*.html""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"},
                {"type": "text_file", "name": "code_feedback.md", "source": "CodeCritic"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
            ],
        },
        {
            "agent_name": "CodeCritic",
            "prompt": """You are a Software Test Engineer specializing in web application backend and frontend code reviews.

Your goal is to review app.py and templates/*.html for correctness, functional completeness, accurate element IDs, and compliance with design_spec.md, providing gated feedback for at most two iterations.

Task Details:
- Read design_spec.md, app.py, and templates/*.html from CONTEXT
- Verify backend routes, data file integrations, and logic completeness
- Verify frontend templates contain all specified pages with exact element IDs and UI elements
- Confirm all user flows and interactive elements function as designed
- Write code_feedback.md starting with [APPROVED] if complete and correct, or NEED_MODIFY followed by detailed corrections

Review Criteria:
1. All routes and pages conform to design_spec.md specification exactly
2. Local text file data formats and handling match the requirements document
3. Element IDs in HTML templates are all present and correct as specified
4. User interaction flows (cart, checkout, reviews, orders) are fully implemented
5. No missing or extraneous features beyond user_task specification

CRITICAL REQUIREMENTS:
- code_feedback.md MUST begin with exactly [APPROVED] or NEED_MODIFY at byte 1
- Provide actionable, detailed correction instructions when NEED_MODIFY
- Use the write_text_file tool to output the complete code_feedback.md file

Output: code_feedback.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
            "input_artifacts": [
                {"type": "text_file", "name": "design_spec.md", "source": "DesignGenerator"},
                {"type": "text_file", "name": "app.py", "source": "AppGenerator"},
                {"type": "text_file", "name": "templates/*.html", "source": "AppGenerator"},
            ],
            "output_artifacts": [
                {"type": "text_file", "name": "code_feedback.md"},
            ],
        },
    ],
    review_policy: list = [
        {
            "source_agent": "AppGenerator",
            "reviewer_agent": "CodeCritic",
            "review_criteria": "Check implementation correctness, completeness against design_spec.md, and adherence to element ID conventions.",
            "review_artifacts": [
                {"type": "text_file", "name": "app.py"},
                {"type": "text_file", "name": "templates/*.html"},
            ],
        }
    ],
): pass
# Phase2_End
# Orchestrate_Start
def orchestrate(
    goal: str = "Develop the 'BookstoreOnline' Python web application with specified pages, features, exact element IDs, using local text file data, enforcing quality through two-phase refinement.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the complete adaptive design specification for the BookstoreOnline app.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce and refine the complete design specification document."
                }
            ]
        },
        {
            "step": 2,
            "description": "Refine the full backend and frontend implementation including app.py and templates/*.html.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Produce and refine the complete implementation and verification."
                }
            ]
        }
    ]
): pass
# Orchestrate_End