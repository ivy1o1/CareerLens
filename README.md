# CareerLens

> AI-powered resume-to-job matching and fit analysis.

CareerLens analyzes how well a user's resume fits a specific job description.

## V1

**Input:**

* Resume (PDF)
* Job description / job posting

**Output:**

* Matched requirements
* Missing / weak requirements
* Supporting resume evidence
* Requirement-level evaluation
* Overall fit score

### Core Flow

```text
Resume ──────────────┐
                     ↓
              CareerLens Backend
                     ↑
Job Description ─────┘
                     │
                     ↓
            Extract Requirements
                     ↓
             Resume Evidence
                     ↓
          Semantic Retrieval
                     ↓
            Gemini Evaluation
                     ↓
          ┌──────────┴──────────┐
          ↓                     ↓
      Matched                Missing
   Requirements           Requirements
          └──────────┬──────────┘
                     ↓
                Fit Score
```

## Architecture

```text
Frontend
   │
   ↓
FastAPI
   │
   ├── Resume Parser ──→ Structured Resume
   ├── Database ───────→ Supabase/PostgreSQL
   │
   └── Matching Engine
          │
          ├── Evidence Builder
          ├── Embeddings
          ├── Semantic Retrieval
          └── Gemini Evaluator
                    │
                    ↓
              Match Analysis
```

## Implemented

### Backend

* ✅ Resume PDF text extraction
* ✅ Structured resume parsing
* ✅ Resume evidence construction
* ✅ Local embeddings with `all-MiniLM-L6-v2`
* ✅ Semantic evidence retrieval
* ✅ Gemini-based requirement evaluation
* ✅ Matched / missing requirement detection
* ✅ Requirement-level explanations
* ✅ Overall fit score
* ✅ Supabase database integration
* ✅ Matching API

### Frontend

* 🚧 Not implemented yet

## Planned

These are **not implemented in V1** and will be built later:

* 🔲 Web frontend
* 🔲 Job-specific resume generation
* 🔲 Resume rewriting and tailoring
* 🔲 ATS-oriented optimization
* 🔲 Cover letter generation
* 🔲 Job discovery and recommendations
* 🔲 Application tracking
* 🔲 Skill-gap learning recommendations

## Matching Logic

```text
Job Requirement
      ↓
Embedding
      ↓
Retrieve relevant resume evidence
      ↓
Gemini evaluates evidence
      ↓
Matched / Missing + Explanation
```

Retrieval finds potentially relevant evidence.
Gemini determines whether that evidence actually satisfies the requirement.

The overall score is calculated by the backend:

```text
matched requirements
───────────────────── × 100
total requirements
```

## Tech Stack

* **Backend:** Python, FastAPI, Pydantic
* **Database:** Supabase / PostgreSQL
* **PDF:** PyMuPDF
* **Embeddings:** all-MiniLM-L6-v2 + ONNX Runtime
* **LLM:** Google Gemini
* **Frontend:** React / Next.js — planned

## V1 Principle

> **CareerLens analyzes what the candidate has actually demonstrated — it does not invent qualifications.**

**Current scope: Resume ↔ Job matching.**

