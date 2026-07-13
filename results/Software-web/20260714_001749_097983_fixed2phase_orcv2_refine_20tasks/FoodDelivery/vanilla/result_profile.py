# Phase1_Start
def design_specification_phase(
    goal: str = "Refine the FoodDelivery web application design specification with detailed page layouts, element IDs, and data storage formats; deliver design_spec.md and gated design_feedback.md.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "DesignGenerator writes design_spec.md based on user_task_description and design_feedback.md; DesignCritic reviews design_spec.md and writes design_feedback.md starting with [APPROVED] or NEED_MODIFY."
    ),
    team: list = [
        {
            "agent_name": "DesignGenerator",
            "prompt": """You are a Software Architect specializing in Python web application design specifications.

Your goal is to create and iteratively revise a complete design specification for a FoodDelivery web application, focusing on page layouts, element IDs, navigation flow, and data storage formats.

Task Details:
- Read the full user_task_description from CONTEXT to capture all functional and data requirements.
- Read the current design_spec.md and design_feedback.md artifacts from CONTEXT, if present.
- On the first iteration, produce a full design_spec.md document covering all pages and data formats.
- If design_feedback.md begins with NEED_MODIFY, incorporate all requested changes and overwrite design_spec.md.
- Cease iterations after two or on receiving [APPROVED] feedback.

**Section 1: Page Layouts and Element IDs**
- Specify each page with its exact title and a container element ID.
- Detail all UI elements per page with their element IDs, types, and brief purpose.
- Maintain consistency of element ID naming and map navigation controls explicitly.

**Section 2: Navigation Flow**
- Define how users navigate between pages, referencing button IDs and expected actions.
- Ensure the Dashboard page is the application’s start point.
- Provide a clear mapping of page transitions via UI elements.

**Section 3: Data Storage Formats**
- List all local data files with exact file names.
- Specify file data schemas by field names, separators, and data types.
- Include example data rows consistent with the specification.

CRITICAL SUCCESS CRITERIA:
- Use the write_text_file tool to save design_spec.md.
- Keep the design_spec.md artifact self-contained and authoritative for implementation.
- Follow the Refinement Loop protocol with two iterations max.
- Produce clear, unambiguous, and comprehensive specifications aligned with user_task_description.
- Do not include status markers inside design_spec.md.

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
            "prompt": """You are a Design Reviewer specializing in Python web application specifications.

Your goal is to review the design_spec.md artifact for completeness, clarity, and alignment with the FoodDelivery user requirements and provide gated feedback for at most two iterations.

Task Details:
- Read user_task_description and design_spec.md from CONTEXT.
- Verify all specified pages contain page titles and required element IDs with types and purposes.
- Confirm navigation flow matches the described UI controls and starts with the Dashboard page.
- Validate all data storage files include filename, exact field schemas, separators, types, and example records.
- Write feedback in design_feedback.md starting exactly with [APPROVED] if complete and consistent.
- If incomplete, unclear, or missing details, begin feedback with NEED_MODIFY followed by concrete, itemized corrections.

Review Criteria:
1. Completeness of page layouts and all UI element IDs per provided user task.
2. Clarity in navigation scheme and correctness of page transition mappings.
3. Accuracy and consistency of all data storage file specifications with example data.
4. No contradictions or ambiguities relative to user_task_description.
5. No additional requirements beyond original user task.

CRITICAL REQUIREMENTS:
- The first bytes of design_feedback.md MUST be exactly [APPROVED] or NEED_MODIFY.
- Do not add headings or whitespace before the status marker.
- Use write_text_file tool to save the full review feedback.
- Adhere strictly to the two-iteration refinement loop and stop upon approval.

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
            "review_criteria": "Verify design_spec.md fully addresses all features, page elements, element IDs, navigation scheme, and data storage requirements without missing or ambiguous details.",
            "review_artifacts": [
                {"type": "text_file", "name": "design_spec.md"}
            ]
        }
    ]
): pass
# Phase1_End
# Phase2_Start
def implementation_and_verification_phase(
    goal: str = "Refine the full Python implementation and verification of the FoodDelivery app including app.py, HTML templates and gated code_feedback.md for at most two iterations.",
    collab_pattern_name: str = "Refinement Loop",
    collab_pattern_description: str = (
        "AppGenerator develops and revises app.py and templates/*.html from design_spec.md and code_feedback.md; CodeCritic reviews the implementation for correctness, completeness, adherence to design, and produces code_feedback.md starting with [APPROVED] or NEED_MODIFY."
    ),
    team: list = [
        {
            "agent_name": "AppGenerator",
            "prompt": """You are a Python Flask Developer specialized in web applications using local text file data storage.

Your goal is to implement and iteratively refine the full FoodDelivery application including app.py and all HTML templates for dashboard, restaurants listing, menus, cart, orders, delivery tracking, and reviews.

Task Details:
- Read design_spec.md describing detailed page designs and data file formats from CONTEXT.
- Read existing app.py, templates/*.html, and prior code_feedback.md for iterative refinement.
- On first iteration, create full app.py and templates/*.html implementing all specified pages and features.
- On NEED_MODIFY feedback, apply all corrections and overwrite app.py and templates/*.html completely.
- On [APPROVED] feedback, preserve approved implementation.

**Implementation Requirements:**
- Implement Flask routes and view functions for all 9 pages: Dashboard, Restaurant Listing, Restaurant Menu, Item Details, Shopping Cart, Checkout, Active Orders, Order Tracking, Reviews.
- Use local text files in 'data' directory exactly as specified for Restaurants, Menus, Cart, Orders, Order Items, Deliveries, Reviews.
- Preserve all element IDs exactly as per design_spec.md in templates for correct navigation and UI interaction.
- Implement button actions, search/filter inputs, quantity updates, and page navigations as described.
- Ensure no authentication; all pages are publicly accessible.

**Data Persistence Requirements:**
- Read and write data files with correct parsing and formatting preserving exact field orders and types.
- Implement adding to cart, updating quantities, placing orders, tracking deliveries, and managing reviews with file modifications.
- Ensure data consistency between files and UI.

**Refinement Loop Instructions:**
- Use write_text_file tool to write final app.py and all templates/*.html.
- Run at most two iterations; stop immediately upon receiving [APPROVED] in code_feedback.md.

Output: app.py, templates/*.html""",
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
            "prompt": """You are a Software Test Engineer specialized in verifying Python Flask web applications with local file-based data management.

Your goal is to review the FoodDelivery app.py and HTML templates for syntax correctness, runtime behavior, and conformance to design_spec.md, producing gated feedback in code_feedback.md.

Task Details:
- Read design_spec.md describing required pages, elements, IDs, navigation, and data formats.
- Read the submitted app.py and all templates/*.html from CONTEXT.
- Do not assume undocumented features beyond design_spec.md.
- Validate that all specified element IDs exist exactly as documented.
- Check Flask routes and handlers are complete, consistent, and correctly linked to templates.
- Verify data file interactions correctly read and write expected fields and formats.
- Verify no syntax or runtime errors in app.py.
- On complete conformance, write feedback starting with [APPROVED].
- On any issues or incomplete features, write feedback starting with NEED_MODIFY and detailed corrections.

Review Checklist:
1. Complete implementation of all 9 pages with correct routes and templates.
2. Exact match of all element IDs in HTML templates.
3. Correct implementation of user actions (search, filters, add to cart, checkout).
4. Proper reading/writing of specified text data files per documented formats.
5. Syntax and runtime validation of app.py (use testing or code inspection).
6. Consistency and correctness of navigation flows and button actions.
7. No additional features or undocumented deviations from design_spec.md.

CRITICAL REQUIREMENTS:
- Begin written feedback file code_feedback.md with exactly [APPROVED] or NEED_MODIFY at byte 1.
- Use write_text_file tool to save the complete feedback for review.
- Conduct at most two review iterations; approve immediately if no issues.

Output: code_feedback.md""",
            "tools": ["write_text_file"], "llm_model": "gpt-4.1-mini",
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
            "review_criteria": "Verify app.py and templates/*.html fully implement design_spec.md web pages and features with correct element IDs and data file interactions, free of syntax or runtime errors.",
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
    goal: str = "Develop the FoodDelivery Python Flask web application with local text file data storage and exact page/elements implementation according to user requirements.",
    workflow: list = [
        {
            "step": 1,
            "description": "Refine the complete design specification with exact page elements, layout, IDs, and data storage formats.",
            "phases": [
                {
                    "phase_name": "design_specification_phase",
                    "role": "Produce and verify the detailed design specification document."
                }
            ]
        },
        {
            "step": 2,
            "description": "Implement and verify the full Python Flask app with HTML templates based on design specification.",
            "phases": [
                {
                    "phase_name": "implementation_and_verification_phase",
                    "role": "Produce and validate the production-ready Python Flask web app code and templates."
                }
            ]
        }
    ]
): pass
# Orchestrate_End