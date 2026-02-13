# Frontend Guidelines Documentation

## 1. Frontend Overview

### UI Type
Streamlit-based demo interface (Python-only).

### Purpose
Provide a minimal, professional interface for:
- Submitting applications
- Viewing decision outputs
- Retrieving audit records
- Demonstrating deterministic behavior

This is a prototype UI, not a production design system.

---

## 2. Design Principles

1. Clarity over visual complexity  
2. Functional minimalism  
3. Audit transparency  
4. Determinism visibility  
5. Accessibility by default  

The UI should feel neutral, technical, and evaluation-ready.

---

## 3. UI Architecture

### Layered Interaction Model

User Interaction (Streamlit Form)
        ↓
HTTP Call to FastAPI
        ↓
Display Structured JSON Response

Streamlit acts as a thin client.  
All business logic resides in FastAPI.

---

## 4. Core Screens & States

### 4.1 Application Form Screen

Purpose:
- Collect structured input

Fields:
- income_monthly (numeric)
- dti (decimal)
- employment_months (numeric)
- age (numeric)
- has_defaults (boolean)

States:
- Default
- Validation error
- Submitting (loading)
- Successful submission

---

### 4.2 Decision Result Section

Displays:
- Decision (APPROVE / REVIEW / REJECT)
- Score (0–1000)
- Reason codes
- Explanation text
- audit_id

Visual Emphasis:
- Decision displayed prominently
- Score displayed using metric component
- Explanation in readable block text

---

### 4.3 Audit Record Display

Displays:
- Stored request payload
- Stored response payload
- rule_version
- created_at timestamp

Must reflect stored data (not recomputed).

---

### 4.4 Determinism Check Section

Purpose:
- Demonstrate identical output for identical inputs

Behavior:
- Submit same payload twice
- Compare decision, score, reason codes
- Display deterministic validation result

---

## 5. Layout Guidelines

### Layout Type
Single-column layout

### Width
Centered content block
Optimized for readability over density

### Spacing
Use consistent vertical spacing between:
- Form inputs
- Sections
- Results
- Audit output

---

## 6. Interaction Guidelines

### Button Behavior
- Clear primary action (“Evaluate”)
- Disabled state during submission
- Visual feedback during loading

### Error Handling
- Display validation errors clearly
- Avoid technical stack traces in UI
- Preserve user input when possible

### Feedback Mechanisms
- Status message for success/failure
- Clear display of HTTP response status (optional for technical demo)

---

## 7. Accessibility Considerations

- All inputs labeled clearly
- Numeric inputs constrained to valid ranges
- Sufficient spacing for readability
- Clear contrast between headings and body text
- Keyboard navigation supported (Streamlit default)

---

## 8. Responsive Behavior

Streamlit handles responsiveness automatically.

UI optimized for:
- Laptop demo environment
- Tablet viewing
- Basic mobile usability

No custom CSS breakpoints required in MVP.

---

## 9. Explicitly Out of Scope

- Custom CSS frameworks
- React / Vue / Angular frontend
- Theming engines
- Dark mode
- Marketing pages
- Authentication screens
- Admin dashboards
- Data visualizations (charts)
- Multi-step forms

---

## 10. Future Enhancements

Potential extensions:
- Role-based UI views
- Batch simulation interface
- Decision distribution dashboard
- Styled audit timeline view
- Embedded API logs panel

---

## 11. Design Intent Summary

The frontend exists to:

- Demonstrate backend functionality clearly
- Make audit storage visible
- Validate deterministic guarantees
- Support technical evaluation

It is intentionally minimal and Python-native to reduce complexity and maintain alignment with MVP constraints.

---

**Last Updated**: 2026-02-12
