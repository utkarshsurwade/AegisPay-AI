"""
AegisPay-AI: 1-Click Master Demo & Web Prototype Launcher
Mastercard Innovation Challenge 2026 @ Global Fintech Fest (GFF 2026), Mumbai
"""
import os
import sys
import time
import uvicorn

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from benchmarks.benchmark_suite import BenchmarkPipeline
from benchmarks.fidelity_tests import FidelityTestSuite
from generate_submission_doc import create_submission_docx


def main():
    print("""
========================================================================================
   ___   ______ _____ _____ ____   ___ __   __     _    ___ 
  / _ \ |  ____/ ____|_   _/ ___| | _ \\ \ / /    / \  |_ _|
 / /_\ \| |__ | |  __  | || |__   |  _/ \ V /    / _ \  | | 
 |  _  ||  __|| | |_ | | ||___ \  |_|    |_|    / ___ \ | | 
 |_| |_||_|    \_____|_____|___) |              /_/   \_\___|
========================================================================================
  Mastercard Innovation Challenge 2026 @ Global Fintech Fest (GFF 2026), Mumbai
  Project: AegisPay-AI (Autonomous Closed-Loop Red Teaming & Multi-Modal Payment Defense)
========================================================================================
""")

    print("\n[STEP 1/3] Running Statistical Fidelity & Empirical Goodness-of-Fit Tests...")
    fid = FidelityTestSuite(seed=42)
    fid_res = fid.run_full_fidelity_suite(sample_size=1000)
    print(f"  [+] Fidelity Validation: {'PASSED (Statistically Sound)' if fid_res['fidelity_passed'] else 'FAILED'}")
    print(f"  [+] Amount KS Test p-value: {fid_res['metrics']['amount_lognormal_p_value']}")
    print(f"  [+] Amount Wasserstein Distance: {fid_res['metrics']['amount_wasserstein_dist']}")
    print(f"  [+] Keystroke Cadence KS p-value: {fid_res['metrics']['keystroke_hold_p_value']}")

    print("\n[STEP 2/3] Generating Official Solution Walkthrough Document (.docx)...")
    doc_path = create_submission_docx("AegisPay_AI_Mastercard_Solution_Walkthrough.docx")
    print(f"  [+] Generated: {doc_path} ({os.path.getsize(doc_path):,} bytes)")

    print("\n[STEP 3/3] Launching AegisPay-AI Interactive Web Prototype Dashboard...")
    print("  [+] Server running at: http://127.0.0.1:8000")
    print("  [+] Open your browser to explore the Threat Taxonomy, Attack Studio, Fraud Graph, and Closed-Loop Arena.")
    print("  [+] Press CTRL+C to stop the server.\n")

    uvicorn.run("web_prototype.server:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
