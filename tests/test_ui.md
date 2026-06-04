# Week 6 UI test plan and results

Manual test pass of the four-screen Streamlit interface, run 3-4 June 2026. Backend logic was tested separately in Weeks 2-5; this pass covers the UI wiring, state sharing, error handling, and the two retrieval paths through the Ask tab.

## Test system

CV-screening tool used as the worked example throughout: "An AI tool that ranks job candidates by scoring their CVs against a job description, and returns a shortlist for a human recruiter to review."

## Cases

1. Inventory accepts a description and classifies it. Result: pass. Returns high-risk, high confidence, reasoning cites Annex III.
2. State carries across tabs. Result: pass. The classified system appears on Classification and Obligations without re-entry.
3. Obligations report renders fully. Result: pass. All ten high-risk Articles, each with page citation, AI note, and checklist question. Page citations match the Week 5 audit (Articles 9, 10, 11, 12, 13, 14, 15, 17, 43, 49 on pages 56, 57, 58, 59, 59, 60, 61, 62, 78, 81).
4. Ask tab, named-Article question. "What does Article 13 require?" Result: pass. Retrieves Article 13 by metadata filter, returns a correct answer cited to page 59.
5. Ask tab, classification question. "What makes an AI system high-risk?" Result: pass after the retrieval fix. Leads with Article 6, returns the two-condition test and the Annex III extension. Page 54 citation for the Annex III amendment power (Article 7(1)) verified against the source PDF.
6. Error handling under a real failure. The Groq free-tier daily token limit was reached during testing. Result: pass. Every screen caught the 429, logged the full traceback to the console, and showed a plain message with inputs preserved, rather than freezing.

## Known limits carried to Week 8

General conceptual questions that name no Article and match no intent pattern rely on plain semantic retrieval (recitals excluded). That path's quality across a wide question set is for the Week 8 evaluation harness to measure systematically. Top-k is fixed at 5.