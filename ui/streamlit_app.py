"""Streamlit demo UI for the Deterministic Decisioning Engine."""

import os
import json
from dataclasses import dataclass
from typing import Any

import requests
import streamlit as st


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

@dataclass
class ApiError(Exception):
    status_code: int
    body: Any
    message: str = ""

    def __str__(self) -> str:
        base = f"HTTP {self.status_code}"
        return f"{base}: {self.message}" if self.message else base


def _parse_response(resp: requests.Response) -> Any:
    ct = (resp.headers.get("content-type") or "").lower()
    if "application/json" in ct:
        try:
            return resp.json()
        except Exception:
            pass
    return resp.text


def post_apply(payload: dict) -> dict:
    resp = requests.post(f"{API_BASE_URL}/apply", json=payload, timeout=10)
    body = _parse_response(resp)

    if not resp.ok:
        msg = ""
        if isinstance(body, dict) and "detail" in body:
            msg = "Validation failed" if resp.status_code == 422 else "Request failed"
        raise ApiError(resp.status_code, body, msg)

    return body


def get_audit(audit_id: str) -> dict:
    resp = requests.get(f"{API_BASE_URL}/audit/{audit_id}", timeout=10)
    body = _parse_response(resp)

    if not resp.ok:
        raise ApiError(resp.status_code, body, "Request failed")

    return body


st.set_page_config(
    page_title="Deterministic Decisioning Engine",
    layout="centered",
)

# ── Section 1: Application Form ──────────────────────────────────────────────

st.header("Credit Decision Application")

with st.form("apply_form"):
    income_monthly = st.number_input("Monthly Income", step=100)
    dti = st.number_input(
        "Debt-to-Income Ratio", step=0.01, format="%.2f"
    )
    employment_months = st.number_input("Employment Duration (months)", step=1)
    age = st.number_input("Age", step=1)
    has_defaults = st.checkbox("Has Payment Defaults")
    submitted = st.form_submit_button("Evaluate")

if submitted:
    payload = {
        "income_monthly": income_monthly,
        "dti": dti,
        "employment_months": employment_months,
        "age": age,
        "has_defaults": has_defaults,
    }
    try:
        data = post_apply(payload)

        decision = data["decision"]
        if decision == "APPROVE":
            st.success(f"Decision: {decision}")
        elif decision == "REVIEW":
            st.warning(f"Decision: {decision}")
        else:
            st.error(f"Decision: {decision}")

        st.metric("Score", data["score"])
        st.write("**Reason Codes:**", ", ".join(data["reason_codes"]))
        st.write("**Explanation:**", data["explanation"])
        st.write("**Audit ID:**", data["audit_id"])

        with st.expander("Raw response"):
            st.json(data)
    except ApiError as e:
        if e.status_code == 422 and isinstance(e.body, dict) and "detail" in e.body:
            st.error("Backend rejected the request (422). Fix these fields:")
            details = e.body["detail"]

            if isinstance(details, list):
                for err in details:
                    loc = " → ".join(str(x) for x in err.get("loc", []))
                    msg = err.get("msg", "Invalid")
                    inp = err.get("input", None)

                    line = f"- **{loc}**: {msg}"
                    if inp is not None:
                        line += f" (got: `{inp}`)"
                    st.write(line)
            else:
                st.json(e.body)
        else:
            st.error(str(e))
            if isinstance(e.body, (dict, list)):
                st.json(e.body)
            else:
                st.code(str(e.body))



st.divider()

# ── Section 2: Audit Retrieval ───────────────────────────────────────────────

st.header("Retrieve Audit Record")

audit_id_input = st.text_input("Audit ID")

if st.button("Retrieve"):
    if not audit_id_input.strip():
        st.error("Please enter an Audit ID.")
    else:
        try:
            record = get_audit(audit_id_input.strip())
            st.json(record)
        except Exception as e:
            st.error(str(e))
