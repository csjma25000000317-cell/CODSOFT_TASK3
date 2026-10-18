
import streamlit as st
from pathlib import Path
from scanner import scan_python_file, save_json_report

st.set_page_config(
    page_title="CodeShield | Security Assessment",
    page_icon="🛡️",
    layout="wide",
)

st.markdown("""
<style>
.stApp {
    background: #0b1120;
    color: #e5e7eb;
}
[data-testid="stHeader"] {
    background: rgba(11, 17, 32, 0.9);
}
[data-testid="stMetric"] {
    background: #151f32;
    border: 1px solid #29374f;
    padding: 18px;
    border-radius: 12px;
}
.stButton > button {
    background: #14b8a6;
    color: #07111e;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    min-height: 42px;
}
.stButton > button:hover {
    background: #5eead4;
    color: #07111e;
}
.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ CodeShield")
st.caption("SECURE CODE ASSESSMENT PLATFORM")
st.write(
    "Analyze Python source code for common security issues "
    "using Bandit static analysis."
)

st.info(
    "Safety: Only scan Python files you own or are authorized "
    "to assess. Uploaded code is analyzed, not executed."
)

uploaded_file = st.file_uploader(
    "Upload a Python source file",
    type=["py"],
)

if uploaded_file is not None:
    st.write(f"**Selected file:** {uploaded_file.name}")

    if st.button("Run Security Scan", use_container_width=True):
        # Store the uploaded source in a temporary local file.
        temp_path = None

        try:
            with __import__("tempfile").NamedTemporaryFile(
                mode="wb",
                suffix=".py",
                delete=False,
            ) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_path = Path(temp_file.name)

            with st.spinner("Analyzing source code..."):
                report = scan_python_file(temp_path)

            report["scanned_file"] = uploaded_file.name
            st.session_state["last_report"] = report

        except Exception as error:
            st.error(f"Scan failed: {error}")

        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

if "last_report" in st.session_state:
    report = st.session_state["last_report"]
    issues = report["issues"]

    st.divider()
    st.subheader("Security Assessment Results")

    high = sum(i["severity"] == "HIGH" for i in issues)
    medium = sum(i["severity"] == "MEDIUM" for i in issues)
    low = sum(i["severity"] == "LOW" for i in issues)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Findings", len(issues))
    col2.metric("High Severity", high)
    col3.metric("Medium Severity", medium)
    col4.metric("Low Severity", low)

    if not issues:
        st.success(
            "Bandit reported no findings for this scan. "
            "This does not guarantee the code is secure."
        )
    else:
        for number, issue in enumerate(issues, start=1):
            with st.expander(
                f'{number}. [{issue["severity"]}] '
                f'{issue["test_id"]} — Line {issue["line"]}'
            ):
                st.write("**Finding:**", issue["issue"])
                st.write("**File:**", issue["file"])
                st.write("**Line:**", issue["line"])
                st.write("**Confidence:**", issue["confidence"])

                if issue["code"]:
                    st.code(issue["code"], language="python")

                cwe = issue.get("cwe", {})
                if isinstance(cwe, dict) and cwe.get("id"):
                    st.write(
                        f'CWE-{cwe["id"]}: '
                        f'{cwe.get("link", "")}'
                    )

                st.write(
                    "**Recommended action:**",
                    issue["recommendation"],
                )

    report_json = __import__("json").dumps(
        report, indent=4
    )
    st.download_button(
        "Download JSON Report",
        data=report_json,
        file_name="codeshield_report.json",
        mime="application/json",
        use_container_width=True,
    )

st.divider()
st.caption(
    "CodeShield | Educational security assessment tool. "
    "Automated findings require human review."
)
