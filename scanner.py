
import json
import subprocess
import sys
from pathlib import Path


def scan_python_file(file_path):
    """Scan a Python file using Bandit without executing its code."""

    path = Path(file_path).resolve()

    if not path.is_file():
        raise FileNotFoundError("The selected file does not exist.")

    if path.suffix.lower() != ".py":
        raise ValueError("Please select a Python (.py) file.")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "bandit",
            "-f",
            "json",
            str(path),
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )

    # Bandit may return a non-zero code when findings exist.
    if result.returncode not in (0, 1):
        raise RuntimeError(
            "Bandit could not complete the scan: "
            + result.stderr.strip()
        )

    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Could not read the Bandit report."
        ) from exc

    issues = []

    for item in report.get("results", []):
        issues.append({
            "test_id": item.get("test_id", "N/A"),
            "issue": item.get("issue_text", "No description"),
            "severity": item.get("issue_severity", "LOW"),
            "confidence": item.get("issue_confidence", "LOW"),
            "file": item.get("filename", str(path)),
            "line": item.get("line_number", 0),
            "code": item.get("code", ""),
            "cwe": item.get("issue_cwe", {}),
            "recommendation": (
                "Review the flagged code and follow the "
                "recommendation for this Bandit test."
            ),
        })

    return {
        "scanned_file": path.name,
        "total_issues": len(issues),
        "issues": issues,
    }


def save_json_report(report, output_path="scan_report.json"):
    """Save findings to a JSON report."""

    Path(output_path).write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )


if __name__ == "__main__":
    print("CodeShield - Secure Code Assessment")
    file_name = input("Enter the Python file path to scan: ").strip()

    try:
        report = scan_python_file(file_name)
        save_json_report(report)

        print("\nScan completed.")
        print("File:", report["scanned_file"])
        print("Total findings:", report["total_issues"])
        print("Report saved as scan_report.json")

        for issue in report["issues"]:
            print(
                f'\n[{issue["severity"]}] '
                f'{issue["test_id"]}: {issue["issue"]}'
            )
            print("Line:", issue["line"])
            print("Confidence:", issue["confidence"])

    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        print("Scan error:", error)
