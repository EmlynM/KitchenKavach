# KitchenKavach — AI-Powered FSSAI Compliance Assistant

> An evidence-based AI assistant that helps cloud kitchen owners understand FSSAI regulations, prepare for inspections, and avoid misleading regulatory advice.

## Problem

Small cloud kitchen owners struggle to understand FSSAI licensing requirements, food labelling regulations, packaging standards, and hygiene rules. Generic AI chatbots may provide inaccurate or outdated answers, potentially leading to failed inspections, penalties, and compliance issues. KitchenKavach uses Retrieval-Augmented Generation (RAG) to answer questions using official FSSAI documents, with citations to supporting regulatory passages. When reliable evidence is unavailable, it explicitly acknowledges uncertainty instead of inventing an answer.

## Who it is for

- Owners of multi-brand cloud kitchens in Velachery, Chennai, who need reliable licensing guidance and inspection-ready hygiene checklists.
- Small food business operators who need to understand FSSAI regulations, maintain compliance records, and prepare for food safety inspections.

## Signature feature

**Inspection-ready checklist with source-level citations:** One tap generates a cloud kitchen hygiene and compliance checklist, with every applicable item linked to the relevant FSSAI regulation, section, or source passage.

## Hardest problem (my interview story)

The hardest problem is preventing AI hallucinations in food safety and regulatory guidance, where an incorrect answer can have real consequences. I am building an evaluation dataset to measure answer faithfulness against retrieved FSSAI passages and testing whether citations actually support the generated claims. I am also implementing an abstention guardrail that responds with “I couldn't find sufficient supporting evidence in the available FSSAI documents” when evidence is weak, missing, or contradictory. My target is at least 90% faithfulness and at least 90% correct abstention across 30 out-of-scope questions.

## Dataset

| Source | Link | Documents | Pages | Licence / terms |
|---|---|---:|---:|---|
| FSSAI — Food Safety and Standards Authority of India | https://www.fssai.gov.in/ | To be counted after collection | Target: 1,500+ | Check the applicable terms for each document and its permitted reuse |
| Food Safety and Standards Act, 2006 | https://www.fssai.gov.in/ | 1 Act | To be verified | Official government legislation; verify the applicable reproduction terms |
| FSSAI regulations, notifications, orders and FAQs | https://www.fssai.gov.in/ | To be counted after collection | Included in overall target | Check source-specific terms, amendments, and document status |

*Dataset note: The target is 1,500+ relevant pages. Actual document and page counts must be reported after downloading, deduplicating, and validating the dataset. The listed sources are collection targets, not confirmation that all documents have already been ingested.*

## 10 real questions

See [docs/QUESTIONS.md](docs/QUESTIONS.md).

The evaluation set will include questions such as:

1. Does a cloud kitchen with ₹15 lakh annual turnover need registration or a state licence?
2. What must be printed on a takeaway food label?
3. How often must a food business conduct pest control under Schedule 4?
4. What hygiene practices must food handlers follow?
5. What records should a cloud kitchen maintain for food safety inspections?
6. What are the applicable requirements for cleaning and sanitising food-contact surfaces?
7. What requirements apply to safe food storage and temperature monitoring?
8. Which FSSAI licence or registration details must be displayed at the premises?
9. Has a relevant FSSAI regulation been amended, and what is its current applicable version?
10. What should the assistant do when no official document supports an answer?

## Run it

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements-dev.txt

# Linux / macOS
cp .env.example .env

# Windows PowerShell
# Copy-Item .env.example .env

uvicorn app.main:app --reload

# In another terminal
curl http://localhost:8000/health
```

*These commands assume the FastAPI application, dependency files, environment template, and health endpoint have been implemented.*

## Live link

Coming soon — planned for Week 2.

