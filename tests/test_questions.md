# Aegis grounded Q&A test questions

Hand-crafted questions covering different parts of the EU AI Act, used to spot-check whether `src/aegis/grounded_qa.py` retrieves relevant passages and produces answers that cite real page numbers.

These are not the formal evaluation set. The Week 8 evaluation harness will hand-label 30 to 50 system descriptions against a known-correct risk tier and measure classifier and citation accuracy properly. This file is the informal "does it look right" set used during Week 3 development.

Each entry says what good retrieval should pull and what a good answer should reference. Verified manually on 31 May 2026 by running the script and reading the output.

## Question 1: Article 13 transparency

What does Article 13 require for transparency in high-risk AI systems?

Good retrieval should pull: Article 13 itself, Recital 72 (the transparency rationale for high-risk systems), the instructions-for-use requirement.

Good answer should cite: pages in the Article 13 area (around page 56) or Recital 72 (around page 21). Should mention instructions for use, deployer understanding, characteristics and limitations.

Observed 31 May 2026: passages from pages 21, 34, 35, 46, 114. Answer cited page 21 consistently. Honest about not having the full text of Article 13 in the retrieved chunks. No fabricated citations.

## Question 2: General-purpose AI obligations

What are the obligations on providers of general-purpose AI models?

Good retrieval should pull: Articles 53 and 54 (the GPAI obligations chapter), the open-source carve-out, the authorised representative requirement.

Good answer should cite: pages in the 80s (Articles 53-54 area). Should mention technical documentation, copyright, summary of training content, and the authorised representative obligation for third-country providers.

Observed 31 May 2026: passages from pages 26, 27, 31, 67, 85. Answer cited pages 31 and 85. Mentioned authorised representative requirement (real, from Article 54). Did not cover technical documentation or training-content summary in this run; would benefit from a follow-up question.

## Question 3: Article 5 prohibited practices

Which AI practices are prohibited under Article 5?

Good retrieval should pull: Article 5 directly, ideally page 51 onwards. This is the question that Week 2 retrieval missed at top-3.

Good answer should cite: page 51 or nearby. Should list at least the four canonical Article 5(1) categories: subliminal manipulation, exploitation of vulnerabilities, social scoring, and predictive policing based on profiling alone.

Observed 31 May 2026: passages from pages 4, 8, 12, 51. Top passage was Article 4 (literacy), not Article 5 (prohibitions). The model produced a correct list of four Article 5 prohibitions citing page 51, but the retrieved passages do not contain the full Article 5 text. The model used a combination of one partial passage and its training knowledge of the Act. This is a partial-grounding case and is flagged for the Week 8 evaluation harness.

## Question 4 to 10: planned but not yet run

These are queued for the evaluation harness in Week 8, not for the Week 3 spot-check.

4. Who is the AI Office and what are its powers?
5. What is the definition of a high-risk AI system?
6. What are the conformity assessment requirements before placing a high-risk AI system on the market?
7. When does enforcement begin under the Act?
8. What are the obligations on deployers of high-risk AI systems?
9. What penalties can be imposed for non-compliance?
10. How does the Act define a "provider" versus a "deployer"?

## Known limitations

- pypdf produces letter-spacing artefacts in the source text ("high-r isk", "Ar ticle"). The model is robust enough to handle this in its outputs but the retrieved chunks themselves remain noisy. Week 8 evaluation will decide whether to swap to pdfplumber or pymupdf.
- Top-5 retrieval is currently the setting. Week 8 will test 3, 5, and 10 chunks against a hand-labelled set to measure which gives the best accuracy.
- The model occasionally fills gaps in retrieval with general knowledge of the Act (see Question 3). Citation accuracy testing in Week 8 will catch and quantify this.
- All similarity scores currently sit between 0.35 and 0.50. This is the loosely-related band. Better retrieval (better PDF extraction, larger embedding model, or hybrid search with BM25) is queued for Week 8.