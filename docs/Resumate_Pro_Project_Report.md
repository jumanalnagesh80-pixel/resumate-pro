<!--
================================================================================
  RESUMATE PRO — AI POWERED RESUME BUILDER
  BCA FINAL YEAR PROJECT REPORT

  FORMATTING GUIDE (apply when converting this Markdown to Word / PDF):
    • Font ............ Times New Roman
    • Chapter Heading . 16 pt, Bold, Centered / Left
    • Subheading ...... 14 pt, Bold
    • Body Text ....... 12 pt
    • Line Spacing .... 1.5
    • Margins ......... Left 1.5", Right 1", Top 1", Bottom 1" (university standard)
    • Alignment ....... Justified for body paragraphs
    • Page Numbers .... Bottom-centre; front matter in roman numerals (i, ii, iii)
  Each "---PAGE BREAK---" marker indicates a recommended page break.
================================================================================
-->

# RESUMATE PRO – AI POWERED RESUME BUILDER

### A Project Report Submitted in Partial Fulfilment of the Requirements for the Award of the Degree of

## BACHELOR OF COMPUTER APPLICATIONS (BCA)

**Submitted by**

`<Student Name>`
`<University Register / Roll Number>`

**Under the Guidance of**

`<Guide Name & Designation>`

**Department of Computer Applications**
`<College / Institution Name>`
`<University Name>`
`<Academic Year 2025–2026>`

---PAGE BREAK---

## CERTIFICATE

This is to certify that the project report entitled **"Resumate Pro – AI Powered Resume Builder"** is a bonafide record of the project work carried out by **`<Student Name>`** bearing register number **`<Register Number>`** in partial fulfilment of the requirements for the award of the degree of **Bachelor of Computer Applications (BCA)** of `<University Name>` during the academic year **2025–2026**.

The work presented in this report is the original work of the candidate and has not been submitted, either in part or in full, to any other university or institution for the award of any degree or diploma.

<br><br>

| | |
|---|---|
| **Signature of the Guide** | **Signature of the Head of the Department** |
| `<Guide Name>` | `<HOD Name>` |
| Designation | Department of Computer Applications |

<br><br>

**Submitted for the University Project Viva-Voce Examination held on: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**

<br><br>

| | |
|---|---|
| **Internal Examiner** | **External Examiner** |
| Signature & Date | Signature & Date |

---PAGE BREAK---

## DECLARATION

I, **`<Student Name>`**, bearing register number **`<Register Number>`**, hereby declare that the project report entitled **"Resumate Pro – AI Powered Resume Builder"**, submitted to `<University Name>` in partial fulfilment of the requirements for the award of the degree of **Bachelor of Computer Applications (BCA)**, is a record of original and independent work carried out by me under the supervision and guidance of **`<Guide Name>`**, `<Designation>`, Department of Computer Applications.

I further declare that this project, and the source code, design and documentation associated with it, has been developed by me, and that the work has not been submitted, in part or in full, to any other university or institution for the award of any degree, diploma or other similar title. All external sources, libraries and references used during the development of this project have been duly acknowledged in the references section of this report.

<br><br>

**Place:** `<City>`
**Date:** `<DD / MM / YYYY>`

<br><br>

**Signature of the Candidate**
`<Student Name>`

---PAGE BREAK---

## ACKNOWLEDGEMENT

The successful completion of any project is never the result of a single individual's effort; it is the outcome of guidance, encouragement and support extended by many people. I take this opportunity to express my sincere gratitude to all those who contributed, directly or indirectly, to the completion of this project.

First and foremost, I express my deep sense of gratitude to **`<Principal Name>`**, Principal of `<College Name>`, for providing an excellent academic environment and the infrastructure necessary to carry out this project.

I am profoundly thankful to **`<HOD Name>`**, Head of the Department of Computer Applications, for the constant encouragement and for permitting me to undertake this project.

I owe my sincere thanks to my internal guide **`<Guide Name>`**, `<Designation>`, whose valuable guidance, constructive criticism and continuous motivation were instrumental at every stage of this project. The technical insights and timely suggestions provided by my guide helped me transform an idea into a complete, working software product.

I also extend my gratitude to all the **teaching and non-teaching staff** of the Department of Computer Applications for their cooperation and support throughout the course of my study.

Finally, I would like to thank my **family and friends** for their unconditional support, patience and encouragement, without which this project would not have reached its successful completion.

<br>

`<Student Name>`

---PAGE BREAK---

## ABSTRACT

**Project Introduction.** *Resumate Pro – AI Powered Resume Builder* (internally versioned as *ResuMate AI v3*) is a full-stack web application that helps job seekers create, optimise and export professional, Applicant Tracking System (ATS) friendly resumes. The system combines a modern, token-authenticated web application programming interface (API) with an intelligent text-processing engine that rewrites weak resume statements, generates professional summaries and cover letters, scores resumes against industry keyword sets, and measures how well a resume matches a specific job description. The application is delivered as a single deployable server that exposes both a documented REST API and a lightweight browser-based front end, supported by a complete administrative back office for user and content management.

**Problem Solved.** A large proportion of resumes are rejected before a human recruiter ever sees them because they are filtered out by automated ATS software. Traditional resume creation tools such as word processors and graphic design platforms focus on visual appearance and provide no objective feedback on the content quality, keyword relevance or machine-readability of a resume. Job seekers, especially students and early-career professionals, frequently use weak, passive phrasing, omit quantified achievements, and fail to tailor their resume to each job description. Resumate Pro directly addresses these problems by providing real, measurable, content-level feedback together with one-click intelligent rewriting and tailoring tools.

**Technologies Used.** The back end is built with **Python 3** and the **FastAPI** web framework served by the **Uvicorn** ASGI server. Data is persisted through the **SQLAlchemy 2.0** Object Relational Mapper (ORM) over **SQLite** in development and **PostgreSQL** in production. Authentication is implemented using **JSON Web Tokens (JWT)** via *python-jose* with **bcrypt** password hashing. The intelligence layer uses the **OpenAI API** when an API key is configured, and otherwise falls back to a fully self-contained, deterministic local engine that uses **scikit-learn** TF-IDF vectorisation for job-description matching. Portable Document Format (PDF) output is produced with **ReportLab**, and uploaded resumes are parsed with **PyPDF2** and **python-docx**. The front end is composed of semantic **HTML5**, **Alpine.js** for reactivity and **Tailwind CSS** for styling, with authentication tokens stored in the browser's `localStorage`.

**Features.** The platform offers secure registration and login; full create, read, update and delete (CRUD) management of multiple resumes per user; real-time automatic saving; four ATS-friendly PDF templates (Modern, Classic, Minimal and Creative); AI-assisted bullet-point rewriting; automatic professional-summary and cover-letter generation; an ATS score computed across six weighted dimensions; job-description matching with skill-gap analysis; resume file import (PDF, DOCX, TXT, MD); public read-only resume sharing with view counting; a career-advice chat assistant; and a complete administrative dashboard with statistics, a user-growth chart, user management, resume oversight and a full activity audit trail.

**Benefits.** Resumate Pro shortens the time required to produce a high-quality resume from hours to minutes, raises the probability of passing automated screening, offers objective and explainable scoring rather than subjective opinion, works completely offline through its local engine, and is free of per-template paywalls. Its single-server architecture makes deployment straightforward and inexpensive.

**Future Scope.** Planned enhancements include deeper large-language-model integration, multi-language resume support, an interview-question generator, LinkedIn profile import, a dedicated mobile application, and cloud-native deployment with object storage and managed databases for horizontal scalability.

---PAGE BREAK---

## TABLE OF CONTENTS

| Sl. No. | Particulars | Page No. |
|---|---|---|
| | Certificate | i |
| | Declaration | ii |
| | Acknowledgement | iii |
| | Abstract | iv |
| | Table of Contents | v |
| | List of Figures | vi |
| | List of Tables | vii |
| | List of Abbreviations | viii |
| **1** | **INTRODUCTION** | 1 |
| 1.1 | Project Overview | 1 |
| 1.2 | Objectives | 3 |
| 1.3 | Scope of the Project | 4 |
| **2** | **SYSTEM ANALYSIS** | 6 |
| 2.1 | Problem Statement | 6 |
| 2.2 | Existing System | 7 |
| 2.3 | Proposed System | 9 |
| 2.4 | Feasibility Study | 10 |
| **3** | **SYSTEM SPECIFICATION** | 12 |
| 3.1 | Hardware Requirements | 12 |
| 3.2 | Software Requirements | 12 |
| 3.3 | Functional & Deployment Requirements | 14 |
| **4** | **TECHNOLOGY USED** | 15 |
| **5** | **SYSTEM DESIGN** | 23 |
| **6** | **MODULE DESCRIPTION** | 33 |
| **7** | **SCREENSHOTS** | 40 |
| **8** | **ALGORITHM / PSEUDOCODE** | 45 |
| **9** | **TESTING & IMPLEMENTATION** | 51 |
| **10** | **CONCLUSION** | 56 |
| | **REFERENCES** | 58 |
| | **APPENDIX** | 60 |

---PAGE BREAK---

## LIST OF FIGURES

| Figure No. | Description | Page No. |
|---|---|---|
| 5.1 | Overall System Architecture | 23 |
| 5.2 | System Workflow | 25 |
| 5.3 | Data Flow Diagram – Level 0 (Context Diagram) | 26 |
| 5.4 | Data Flow Diagram – Level 1 | 27 |
| 5.5 | Entity Relationship Diagram | 28 |
| 5.6 | Use Case Diagram | 29 |
| 5.7 | Activity Diagram – Resume Optimisation | 30 |
| 5.8 | Sequence Diagram – Authentication & AI Enhancement | 31 |
| 5.9 | Component Diagram | 32 |
| 5.10 | Class Diagram (Domain Model) | 32 |
| 7.1 – 7.18 | Application Screenshots | 40–44 |

## LIST OF TABLES

| Table No. | Description | Page No. |
|---|---|---|
| 2.1 | Comparison of Existing Resume Tools | 8 |
| 2.2 | Technical Feasibility Assessment | 10 |
| 2.3 | Economic Feasibility Assessment | 10 |
| 2.4 | Operational Feasibility Assessment | 11 |
| 2.5 | Schedule Feasibility (Project Timeline) | 11 |
| 3.1 | Hardware Requirements | 12 |
| 3.2 | Software Requirements | 13 |
| 3.3 | Python Dependency Matrix | 13 |
| 4.1 | Technology Stack Summary | 15 |
| 5.1 | REST API Endpoint Catalogue | 23 |
| 5.2 | Database Schema – `users` | 28 |
| 5.3 | Database Schema – `resumes` | 28 |
| 5.4 | Database Schema – `activity_logs` | 28 |
| 6.1 | ATS Scoring Dimensions and Weights | 36 |
| 9.1 – 9.6 | Test Case Tables | 52–55 |

## LIST OF ABBREVIATIONS

| Abbreviation | Expansion |
|---|---|
| AI | Artificial Intelligence |
| API | Application Programming Interface |
| ASGI | Asynchronous Server Gateway Interface |
| ATS | Applicant Tracking System |
| CORS | Cross-Origin Resource Sharing |
| CRUD | Create, Read, Update, Delete |
| CSS | Cascading Style Sheets |
| DFD | Data Flow Diagram |
| DOCX | Microsoft Word Open XML Document |
| ER | Entity Relationship |
| HTML | HyperText Markup Language |
| HTTP | HyperText Transfer Protocol |
| JD | Job Description |
| JSON | JavaScript Object Notation |
| JWT | JSON Web Token |
| LLM | Large Language Model |
| ML | Machine Learning |
| NLP | Natural Language Processing |
| ORM | Object Relational Mapper |
| PDF | Portable Document Format |
| REST | Representational State Transfer |
| SQL | Structured Query Language |
| TF-IDF | Term Frequency – Inverse Document Frequency |
| UI / UX | User Interface / User Experience |
| URL | Uniform Resource Locator |

---PAGE BREAK---

# CHAPTER 1
# INTRODUCTION

## 1.1 Project Overview

### 1.1.1 What is Resumate Pro

*Resumate Pro* is an Artificial-Intelligence-assisted, full-stack web application for building, analysing and exporting professional resumes. It is engineered as a single, self-contained server application that simultaneously serves a documented REST API and a browser-based user interface. The product allows a registered user to maintain a personal library of multiple resumes, edit them through a structured editor, receive automated content feedback, generate supporting documents such as cover letters, and finally export the finished resume as a polished PDF in one of several professionally designed templates.

Unlike conventional document editors that treat a resume merely as a formatted page, Resumate Pro treats a resume as **structured data**. Every resume is stored as a normalised JSON document containing well-defined sections: personal details, professional summary, work experience (with bullet points), education, skills, projects, certifications, languages and awards. Because the content is structured, the system is able to *reason* about it — counting quantified achievements, detecting weak phrasing, measuring keyword coverage for a target industry, and comparing the resume against a pasted job description. This data-centric design is the conceptual foundation that distinguishes Resumate Pro from purely visual tools.

The application is the third major iteration of the product, internally labelled *ResuMate AI v3*. This version adds a complete administrative back office, real-time automatic saving, profile management, an activity audit log, persisted ATS scores, public-share view counting and dedicated editor sections for projects and certifications, building upon the core resume-building and AI capabilities of earlier iterations.

### 1.1.2 Why It Was Developed

The motivation behind Resumate Pro arises from a well-documented disconnect in modern recruitment. Most medium and large organisations rely on Applicant Tracking Systems to filter incoming applications before they ever reach a human recruiter. These systems parse the resume's text, extract keywords, and rank candidates according to how closely the document matches the job requirement. A resume that is visually impressive but poorly structured, keyword-sparse, or written in passive language is frequently discarded automatically, regardless of the candidate's actual merit.

At the same time, the tools most commonly used to write resumes — word processors and graphic-design platforms — provide no insight into this hidden layer of evaluation. They help a user make a document *look* good but offer no answer to the far more important question: *will this resume actually pass an automated screen, and how strong is its content?* Resumate Pro was developed precisely to close this feedback gap, by giving the job seeker objective, explainable, content-level analysis combined with concrete tools to act on that analysis immediately.

A secondary motivation is **accessibility**. Many high-quality resume platforms place their best templates and AI features behind recurring subscription paywalls. Resumate Pro was built to provide an equivalent capability that runs locally, without mandatory paid services: its intelligence engine is designed to work fully offline through a deterministic local fallback, so that the cost of producing a strong resume is not a barrier for students and early-career applicants.

### 1.1.3 The AI Resume Builder Concept

An *AI resume builder* augments the traditional act of writing a resume with automated language intelligence. In Resumate Pro this is realised through several cooperating capabilities. The **bullet enhancer** takes a weak, passive statement such as *"Was responsible for the deployment pipeline"* and rewrites it into a strong, action-verb-led form such as *"Owned the deployment pipeline … (quantify impact: by X%, $K saved, N users reached)"*, automatically detecting and removing weak openers and prompting the user to add measurable impact. The **summary generator** synthesises a concise three-sentence professional summary from the structured resume, inferring years of experience, top skills and the most likely industry. The **cover-letter generator** drafts a tailored letter for a specific company and job description, weaving in the skills that overlap between the candidate and the role.

A defining architectural decision is the **dual-mode intelligence engine**. When an OpenAI API key is configured, the system delegates these language tasks to a large language model for the highest-quality output. When no key is present, it transparently falls back to a built-in deterministic engine driven by curated knowledge bases — a categorised action-verb library, a skills database and industry-keyword sets — so that the product never depends on an external paid service to function. This makes Resumate Pro both powerful and resilient.

### 1.1.4 Resume Optimisation

Resume optimisation in Resumate Pro is built around the **ATS analyser**, which scores a resume out of 100 across six weighted dimensions: contact completeness, section coverage, keyword density, action-verb strength, quantification and length/formatting. Crucially, each dimension does not merely produce a number — it produces a list of human-readable, actionable suggestions. For example, the analyser might report that only 40% of the user's bullets begin with a strong action verb, that the skills section is light, or that a particular set of industry keywords is missing. The user can then act on each suggestion using the AI tools, re-run the analysis, and watch the score improve. Optimisation is therefore an *iterative, feedback-driven loop* rather than a single static report.

### 1.1.5 ATS-Friendly Resumes

Every PDF template shipped with Resumate Pro is deliberately a **single-column layout** that avoids multi-column tables, text boxes and graphics placed behind text — the very elements that cause ATS parsers to scramble or drop content. The four templates (Modern, Classic, Minimal and Creative) differ only in typography, colour and header treatment, never in machine-readability. This guarantees that an attractive resume produced in Resumate Pro remains reliably parseable by the automated systems that will read it first.

### 1.1.6 Modern Resume Creation

The creation experience is intentionally modern and frictionless. The browser front end is reactive, supports light and dark themes, and saves the user's changes automatically a short interval after they stop typing, displaying a live save indicator. Users can import an existing resume file to bootstrap their data, duplicate a resume to create tailored variants for different roles, and share a read-only public link whose views are counted. The entire workflow — from import or blank start, through editing and AI enhancement, to scoring, matching and PDF export — is unified within a single workspace.

---PAGE BREAK---

## 1.2 Objectives

The project was undertaken with the following clearly defined objectives:

1. **To design and develop a secure, full-stack web application** that enables users to create, store, edit and manage multiple professional resumes from a single account, using token-based authentication to protect user data.

2. **To represent resumes as structured data** rather than free-form documents, so that the content can be programmatically analysed, scored and transformed by the system.

3. **To implement an intelligent content-enhancement engine** capable of rewriting weak, passive bullet points into strong, action-verb-led statements and prompting the user to quantify their achievements.

4. **To provide automated generation of professional summaries and tailored cover letters** derived from the user's own resume data and a target job description, without inventing facts.

5. **To build an objective ATS scoring system** that evaluates a resume across six weighted dimensions and returns both an overall grade and specific, actionable improvement suggestions.

6. **To develop a job-description matching feature** that quantifies how well a resume aligns with a particular vacancy using TF-IDF similarity, keyword coverage and skill-gap analysis.

7. **To offer multiple ATS-friendly PDF export templates**, ensuring that visually distinct resumes nonetheless remain reliably machine-readable.

8. **To support importing of existing resumes** from PDF, DOCX, TXT and Markdown files, automatically parsing them into the structured editor to reduce data-entry effort.

9. **To enable public, read-only resume sharing** through unique share tokens, including view-count tracking for shared documents.

10. **To incorporate a dual-mode AI architecture** that uses an external large language model when available but degrades gracefully to a self-contained local engine, guaranteeing offline functionality and eliminating mandatory dependency on paid services.

11. **To deliver a comprehensive administrative module** that provides platform statistics, a user-growth chart, user management (activation, ban, promotion and deletion), resume oversight and a complete activity audit trail.

12. **To ensure maintainability and verifiability** by organising the codebase into clearly separated layers (routes, ORM models, schemas, core engines, data knowledge bases and utilities) and by providing an automated end-to-end smoke test that exercises every public endpoint.

---PAGE BREAK---

## 1.3 Scope of the Project

### 1.3.1 Present Scope

The present scope of Resumate Pro encompasses a fully functional, deployable resume-building platform with the following capabilities that are implemented and verified in the current codebase:

**User Management and Security.** The system supports user registration and login with email and password. Passwords are hashed using bcrypt and never stored in plain text. Sessions are managed through stateless JWT access tokens with a configurable expiry. Users can update their display name and avatar colour and change their password. Every significant action — registration, login, password change and resume operations — is recorded in an activity log together with the originating IP address.

**Resume Lifecycle.** Authenticated users can create an unlimited number of resumes, each stored as a structured JSON document with an associated title and template. Resumes can be listed, retrieved, updated, duplicated and deleted. Each resume tracks its creation and update timestamps, a view count, a persisted ATS score, a public/private flag and a unique share token.

**Intelligence Features.** The system can enhance individual resume bullets, generate professional summaries, draft tailored cover letters, suggest additional relevant skills based on the detected industry, and provide a rule-based career-advice chat assistant. All of these operate through the dual-mode engine described earlier.

**Analysis Features.** The ATS analyser scores resumes across six dimensions and returns detailed feedback, while the job matcher computes a blended match score against any pasted job description, reporting matched skills, missing skills, missing keywords and concrete recommendations.

**Document Generation and Import.** Resumes can be exported as PDF documents in four templates, cover letters can be exported as PDF, and existing resume files can be uploaded and parsed into the editor.

**Public Sharing.** A user may mark a resume as public, generating a read-only shareable link that tracks how many times the resume has been viewed.

**Administration.** A privileged administrator (the first registered user is automatically promoted) can view aggregate platform statistics, a daily signup-growth dataset, a searchable and paginated user list with the ability to activate, ban, promote, demote or delete users, a list of all resumes across all users with the ability to delete any of them, and a full chronological activity log.

### 1.3.2 Boundaries and Limitations of the Present Scope

To keep the project focused and achievable within the academic timeline, the following items are explicitly **outside** the present scope: a native mobile application; real-time multi-user collaborative editing of a single resume; integration with external job boards for automatic application submission; payment or subscription handling; and email-based notification or password-reset flows. The default development database is file-based SQLite, although the system is explicitly designed to switch to PostgreSQL for production through a single environment variable.

### 1.3.3 Future Scope

The architecture has been intentionally layered so that the following enhancements can be added with minimal disruption to existing code:

- **Deeper LLM integration** — richer, conversation-driven editing and section-by-section rewriting.
- **Multi-language resumes** — localisation of the interface and language-aware content generation.
- **Interview preparation** — automatic generation of likely interview questions from the resume and a target job description.
- **LinkedIn and external profile import** — bootstrapping a resume from an existing professional profile.
- **Mobile application** — a companion native or progressive-web application for on-the-go editing.
- **Cloud-native deployment** — containerised deployment with a managed PostgreSQL database and object storage for uploaded files, enabling horizontal scalability.
- **Analytics for users** — personal dashboards showing how a user's ATS score and match rate evolve over time.

These directions are revisited in detail in Chapter 10.

---PAGE BREAK---


# CHAPTER 2
# SYSTEM ANALYSIS

System analysis is the disciplined study of an existing situation with the aim of understanding the problem thoroughly and specifying what a new system must do to solve it. This chapter examines the difficulties associated with conventional resume creation, surveys the tools currently used for the purpose, defines the proposed solution embodied by Resumate Pro, and establishes the feasibility of the project across technical, economic, operational, legal and schedule dimensions.

## 2.1 Problem Statement

The act of writing a resume appears deceptively simple, yet it is one of the most common points of failure in a job search. Several distinct problems combine to make traditional resume creation ineffective:

**1. Invisible automated filtering.** A substantial majority of job applications submitted to medium and large employers are first processed by Applicant Tracking Systems that parse, keyword-match and rank resumes before any human involvement. Candidates are rarely aware of how their resume is being machine-evaluated, and conventional editing tools provide no visibility into this process. As a result, qualified candidates are frequently rejected for reasons that have nothing to do with their ability — poor keyword alignment, unparseable formatting, or missing standard sections.

**2. Weak, passive language.** Inexperienced writers tend to describe their work using passive, low-impact constructions such as *"responsible for"*, *"helped with"*, *"worked on"* or *"duties included"*. These phrases dilute the perceived contribution of the candidate and provide no sense of ownership or outcome. Identifying and rewriting such phrasing manually requires writing skill that many applicants do not possess.

**3. Lack of quantification.** Strong resume statements follow the formula *action verb + task + measurable result*. In practice, most applicants omit the measurable result entirely, producing bullets that describe activity but not impact. Without numbers — percentages, monetary amounts, counts, time saved — a resume fails to communicate the scale of a candidate's achievements.

**4. Poor tailoring.** A single, generic resume is rarely competitive. Each application ideally requires the resume to be tailored to the specific job description, mirroring its language and emphasising relevant skills. Manual tailoring for every application is tedious and error-prone, so most candidates submit the same document everywhere.

**5. Formatting that breaks machine parsing.** Visually rich resumes built with multi-column layouts, tables, text boxes and background graphics often confuse ATS parsers, causing them to misread or drop content. The very design choices that make a resume look impressive to a human can make it illegible to the machine that screens it first.

**6. No objective feedback.** Perhaps most fundamentally, traditional tools offer no objective measure of resume quality. The applicant is left to guess whether the resume is good, with no score, no benchmark and no specific guidance on what to improve.

Resumate Pro is designed specifically to dissolve each of these problems through structured data, intelligent rewriting, objective scoring, job-description matching and guaranteed ATS-friendly output.

## 2.2 Existing System

Before designing the proposed system, the prevailing tools and methods used for resume creation were studied. The four most representative approaches are discussed below.

### 2.2.1 Microsoft Word and Word Processors

General-purpose word processors such as Microsoft Word, Google Docs and LibreOffice Writer are the most widely used resume tools. They offer pre-built resume templates and complete control over formatting.

- **Advantages:** Universally available; familiar interface; complete formatting freedom; offline use.
- **Disadvantages:** No content intelligence whatsoever; many built-in templates use multi-column layouts and text boxes that break ATS parsing; no scoring or feedback; no job-description matching; tailoring is entirely manual.

### 2.2.2 Canva and Graphic Design Platforms

Canva and similar design platforms provide visually striking, designer-made resume templates with drag-and-drop editing.

- **Advantages:** Beautiful, modern visual designs; very easy to use; large template gallery.
- **Disadvantages:** Optimised for visual appeal at the direct expense of ATS-readability; heavy use of graphics, columns and decorative elements that automated parsers cannot read reliably; no content analysis, scoring or matching; premium templates and exports are typically paywalled.

### 2.2.3 Manual / Hand-written Resume Writing

Some applicants write resumes from scratch in a plain text editor or by hand, sometimes with the help of online example resumes.

- **Advantages:** Full control; no tool dependency; naturally simple and parseable if kept plain.
- **Disadvantages:** Extremely time-consuming; entirely dependent on the writer's own skill; no feedback, scoring, intelligence or formatting assistance; very easy to introduce inconsistency and errors.

### 2.2.4 Existing Online Resume Builders

A number of dedicated online resume builders exist. Many provide templates and some provide limited AI suggestions.

- **Advantages:** Purpose-built for resumes; structured section editors; some provide basic suggestions.
- **Disadvantages:** Best features (AI rewriting, downloads, premium templates) are typically locked behind recurring subscriptions; user data is stored on third-party servers; scoring, where present, is often opaque; offline operation is generally impossible; many do not transparently combine objective ATS scoring with job-description matching.

### 2.2.5 Comparison of Existing Tools

**Table 2.1 — Comparison of Existing Resume Tools**

| Capability | MS Word | Canva | Manual | Online Builders | **Resumate Pro** |
|---|:---:|:---:|:---:|:---:|:---:|
| Structured section editor | Partial | Yes | No | Yes | **Yes** |
| ATS-friendly output guaranteed | No | No | Partial | Partial | **Yes** |
| Objective ATS score + feedback | No | No | No | Partial | **Yes (6 dimensions)** |
| AI bullet rewriting | No | No | No | Partial (paid) | **Yes** |
| Auto summary & cover letter | No | No | No | Partial (paid) | **Yes** |
| Job-description matching | No | No | No | Rare | **Yes (TF-IDF)** |
| Resume file import / parsing | No | No | No | Partial | **Yes** |
| Works fully offline | Yes | No | Yes | No | **Yes (local engine)** |
| Free of mandatory paywall | Yes | No | Yes | No | **Yes** |
| Admin / audit capability | No | No | No | N/A | **Yes** |

## 2.3 Proposed System

The proposed system, **Resumate Pro**, integrates the strengths of the existing approaches while systematically eliminating their weaknesses. It is a unified, full-stack web application in which resume creation, intelligent enhancement, objective analysis and reliable export are part of a single, continuous workflow.

The proposed system solves the identified problems as follows:

- **Against invisible filtering**, it provides an explicit ATS analyser that scores the resume across six dimensions and explains exactly what to fix, making the hidden machine evaluation visible and actionable.
- **Against weak language**, it provides a bullet enhancer that detects weak openers from a curated list and rewrites them with contextually chosen strong action verbs.
- **Against missing quantification**, it detects bullets that contain no numbers and explicitly prompts the user to add measurable impact, factoring quantification directly into the ATS score.
- **Against poor tailoring**, it provides a job-description matcher that computes a blended similarity score and lists the exact skills and keywords missing from the resume relative to the target role.
- **Against parser-breaking formatting**, it offers only single-column, ATS-safe PDF templates, so visual variety never compromises machine-readability.
- **Against the absence of feedback**, every analysis returns a concrete, prioritised list of suggestions rather than a bare number.

In addition, the proposed system is architected with a **dual-mode intelligence engine** so that it remains fully functional offline and free of mandatory paid services, and it includes a **complete administrative module** for platform governance — a capability absent from all the surveyed alternatives.

## 2.4 Feasibility Study

A feasibility study evaluates whether the proposed system can be realistically developed and operated. The following assessments were carried out.

### 2.4.1 Technical Feasibility

The project relies entirely on mature, well-documented, open-source technologies that are freely available and run on commodity hardware. FastAPI, SQLAlchemy, scikit-learn, ReportLab and the supporting libraries are widely adopted in industry and have large communities. The dual-mode AI engine removes any hard dependency on a paid external service. The system therefore presents no significant technical risk.

**Table 2.2 — Technical Feasibility Assessment**

| Factor | Assessment | Conclusion |
|---|---|---|
| Availability of technology | All components open-source and freely available | Feasible |
| Team skill requirement | Python, web fundamentals, basic ML — within BCA scope | Feasible |
| Hardware requirement | Runs on a standard laptop / low-cost server | Feasible |
| External service dependency | Optional only (graceful local fallback) | Feasible |
| Integration complexity | Single deployable server, no microservice sprawl | Feasible |

### 2.4.2 Economic Feasibility

The development cost of the project is effectively limited to the developer's time, since the entire technology stack is open-source and licence-free. Development was carried out on an existing personal computer. Hosting can be achieved on a low-cost virtual server, and the default SQLite database incurs no licensing or hosting cost during development. The optional OpenAI integration is the only potential recurring expense, and it is strictly optional.

**Table 2.3 — Economic Feasibility Assessment**

| Cost Component | Estimated Cost | Remark |
|---|---|---|
| Software licences | ₹0 | Entirely open-source stack |
| Development hardware | Existing PC | No new purchase |
| Database (development) | ₹0 | File-based SQLite |
| Hosting (production) | Low / minimal | Single small VM sufficient |
| AI service (optional) | Pay-per-use, optional | Local engine avoids this cost |

The project is therefore highly economically feasible.

### 2.4.3 Operational Feasibility

Operationally, the system is designed for ease of use by non-technical job seekers: a clean web interface, structured section editors, one-click AI actions, automatic saving and clear scoring. Administrators interact through a dedicated dashboard. The single-server deployment model means operation requires only running one process and serving one database, which is well within the operational capability of a small team or an individual.

**Table 2.4 — Operational Feasibility Assessment**

| Factor | Assessment |
|---|---|
| Ease of use for end users | High — guided, structured workflow |
| Training required | Minimal — intuitive web UI |
| Administrative effort | Low — single dashboard, automated logging |
| Deployment effort | Low — one server process |
| User acceptance likelihood | High — solves a real, felt problem |

### 2.4.4 Legal Feasibility

The project uses only permissively licensed open-source libraries and does not redistribute any proprietary content. User passwords are stored only as bcrypt hashes, and personal data is confined to the fields the user voluntarily enters. The system can restrict cross-origin access through configurable allowed origins, and production deployments are expected to operate over HTTPS and to comply with applicable data-protection norms. No legal impediment to development or operation was identified.

### 2.4.5 Schedule Feasibility

The project was decomposed into incremental phases, each producing working functionality, which kept the schedule realistic and trackable.

**Table 2.5 — Schedule Feasibility (Indicative Project Timeline)**

| Phase | Activity | Duration |
|---|---|---|
| 1 | Requirement study & system analysis | 1 week |
| 2 | Database & backend architecture design | 1 week |
| 3 | Authentication & resume CRUD implementation | 2 weeks |
| 4 | Core engines (AI, ATS, matcher, parser, PDF) | 3 weeks |
| 5 | Front-end workspace & admin panel | 2 weeks |
| 6 | Integration, smoke testing & bug fixing | 2 weeks |
| 7 | Documentation & report preparation | 1 week |
| | **Total** | **≈ 12 weeks** |

The project was completed within the academic timeline, confirming schedule feasibility.

---PAGE BREAK---


# CHAPTER 3
# SYSTEM SPECIFICATION

This chapter specifies the hardware and software environment required to develop, run and deploy Resumate Pro. The specifications are derived directly from the project's actual dependency manifest (`requirements.txt`) and configuration files, and they reflect the minimum and recommended resources for comfortable operation.

## 3.1 Hardware Requirements

Resumate Pro is a lightweight server application with modest resource needs. Because the heaviest computation (TF-IDF vectorisation and PDF rendering) is performed in short, request-scoped bursts, even a small server is sufficient for development and moderate production loads.

**Table 3.1 — Hardware Requirements**

| Component | Minimum | Recommended |
|---|---|---|
| Processor | Dual-core 2.0 GHz (x86-64) | Quad-core 2.5 GHz or higher |
| RAM | 4 GB | 8 GB or higher |
| Storage | 1 GB free disk space | 5 GB free (SSD preferred) |
| Display | 1366 × 768 | 1920 × 1080 |
| Network | Broadband internet (for optional AI / CDN assets) | Stable broadband |
| Server (production) | 1 vCPU, 1 GB RAM VM | 2 vCPU, 2–4 GB RAM VM |

## 3.2 Software Requirements

### 3.2.1 Operating System

The application is operating-system independent because it is written in pure Python and standard web technologies. It has been developed and tested on Linux and runs equally on the following:

- **Linux** (Ubuntu 22.04+ / Debian / any modern distribution) — recommended for deployment
- **Microsoft Windows** 10 / 11
- **macOS** 12 (Monterey) or later

### 3.2.2 Software Requirement Summary

**Table 3.2 — Software Requirements**

| Category | Software / Technology | Version |
|---|---|---|
| Programming Language | Python | 3.10 or higher (3.12 recommended) |
| Web Framework | FastAPI | ≥ 0.110.0 |
| ASGI Server | Uvicorn (standard) | ≥ 0.27.0 |
| ORM | SQLAlchemy | ≥ 2.0.25 |
| Database (development) | SQLite | Bundled with Python |
| Database (production) | PostgreSQL | 13+ (via `DATABASE_URL`) |
| Authentication | python-jose (JWT), bcrypt | ≥ 3.3.0, ≥ 4.0.0 |
| PDF Generation | ReportLab | ≥ 4.0.0 |
| File Parsing | PyPDF2, python-docx | ≥ 3.0.0, ≥ 1.1.0 |
| Machine Learning | scikit-learn, NumPy | ≥ 1.3.0, ≥ 1.26.0 |
| Optional AI | openai, python-dotenv | ≥ 1.10.0, ≥ 1.0.0 |
| Form / Upload handling | python-multipart, email-validator | ≥ 0.0.9, ≥ 2.1.0 |
| Legacy UI (optional) | Streamlit, Pandas, Plotly, Jinja2 | ≥ 1.32.0, ≥ 2.0.0, ≥ 5.17.0, ≥ 3.1.0 |
| Front-end | HTML5, Alpine.js, Tailwind CSS | — (CDN-delivered) |
| Web Browser | Chrome / Edge / Firefox / Safari | Latest two versions |

### 3.2.3 Python Dependency Matrix and Roles

**Table 3.3 — Python Dependency Matrix**

| Dependency | Role in the Project |
|---|---|
| `fastapi` | Declares the REST API, request validation, dependency injection and auto-generated docs |
| `uvicorn[standard]` | High-performance ASGI server that runs the FastAPI application |
| `python-multipart` | Parses multipart form data for file uploads (resume import) |
| `bcrypt` | Hashes and verifies user passwords securely |
| `python-jose[cryptography]` | Encodes and decodes JWT access tokens |
| `email-validator` | Validates email addresses in Pydantic schemas |
| `SQLAlchemy` | Object-relational mapping for `User`, `Resume` and `ActivityLog` entities |
| `reportlab` | Renders structured resume data into styled, single-column PDF documents |
| `PyPDF2` | Extracts text from uploaded PDF resumes |
| `python-docx` | Extracts text from uploaded DOCX resumes |
| `scikit-learn` | TF-IDF vectorisation and cosine similarity for job-description matching |
| `numpy` | Numerical support underlying scikit-learn operations |
| `openai` | Optional large-language-model integration for higher-quality generation |
| `python-dotenv` | Loads configuration from a local `.env` file |
| `streamlit`, `pandas`, `plotly`, `Jinja2` | Power the optional legacy Streamlit prototype UI (`app.py`) |

## 3.3 Development Environment

- **Code editor / IDE:** Any modern editor (e.g., VS Code, PyCharm).
- **Version control:** Git, with the project hosted on GitHub (`jumanalnagesh80-pixel/resumate-pro`).
- **Package management:** `pip` with a pinned `requirements.txt`.
- **API exploration & testing:** FastAPI's auto-generated interactive documentation at `/docs` (Swagger UI), plus the bundled `smoke_test.py` end-to-end test harness using FastAPI's `TestClient`.
- **Configuration:** Environment variables via a `.env` file (template provided as `.env.example`).

## 3.4 Functional and Deployment Requirements

### 3.4.1 Configuration (Environment Variables)

| Variable | Default | Purpose |
|---|---|---|
| `JWT_SECRET` | placeholder | Secret used to sign JWT tokens; **must** be changed in production |
| `JWT_EXPIRE_HOURS` | `24` | Validity period of an access token, in hours |
| `OPENAI_API_KEY` | empty | Enables the LLM-backed AI path when set |
| `DATABASE_URL` | SQLite file | Overrides the database; set to a PostgreSQL URL for production |
| `ALLOWED_ORIGINS` | `*` | Comma-separated CORS allow-list; restrict in production |
| `PORT` | `8000` | TCP port on which the server listens |

### 3.4.2 Deployment Requirements

The application is started with a single command, either through Uvicorn directly (`uvicorn server:app --port 8000`) or by running `python server.py`. On startup the application automatically creates all database tables and promotes the first registered user to administrator. For production, the recommended configuration is: a Linux virtual machine, PostgreSQL as the database, a strong `JWT_SECRET`, a restricted CORS allow-list, and an HTTPS-terminating reverse proxy (such as Nginx) placed in front of the Uvicorn process. The static front-end assets are served by the same application from the `frontend/` directory, so no separate web server is strictly required.

---PAGE BREAK---


# CHAPTER 4
# TECHNOLOGY USED

This chapter describes, in detail, every technology actually used in the construction of Resumate Pro, as evidenced by the project's source code and dependency manifest. For each technology, the discussion covers an introduction, its salient features, its advantages, and the specific reasons it was selected for this project. The chapter concludes with an explanation of how these technologies combine to form the overall application architecture.

**Table 4.1 — Technology Stack Summary**

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Web framework / API | FastAPI |
| Application server | Uvicorn (ASGI) |
| Data validation | Pydantic |
| Persistence (ORM) | SQLAlchemy 2.0 |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Authentication | JWT (python-jose) + bcrypt |
| Machine learning | scikit-learn + NumPy |
| Optional AI | OpenAI API |
| PDF generation | ReportLab |
| File parsing | PyPDF2, python-docx |
| Front-end | HTML5, Alpine.js, Tailwind CSS |
| Legacy prototype UI | Streamlit, Pandas, Plotly |
| Architecture style | REST API + static SPA-style front end |

## 4.1 Python

**Introduction.** Python is a high-level, general-purpose, interpreted programming language renowned for its readable, expressive syntax. It is the primary implementation language of Resumate Pro; every backend module, core engine and data knowledge base is written in Python 3.

**Features.** Dynamic typing with optional type hints; an enormous standard library; first-class support for asynchronous programming; a vast third-party ecosystem (PyPI); and excellent suitability for both web development and machine learning, which made it uniquely appropriate for a project that combines both.

**Advantages.** Rapid development; concise and maintainable code; cross-platform portability; strong community support; and the rare ability to host the web layer and the intelligence layer within a single language and process.

**Why Selected.** Resumate Pro deliberately unifies a web API and a text-intelligence engine. Python is one of the very few languages in which both halves can be written naturally and idiomatically, allowing the ATS analyser, matcher and AI engine to share data structures and utilities directly with the web layer without serialisation boundaries.

## 4.2 FastAPI

**Introduction.** FastAPI is a modern, high-performance Python web framework for building APIs, built on top of Starlette (for the web layer) and Pydantic (for data validation). In Resumate Pro, FastAPI defines the entire REST API surface, organised into routers for authentication, resumes, AI, analysis, export, parsing and administration.

**Features.** Declarative path operations using Python decorators; automatic request and response validation from type-annotated Pydantic models; built-in dependency injection (used in this project for database sessions and authentication guards); automatic, interactive OpenAPI/Swagger documentation at `/docs`; native asynchronous support; and a startup/shutdown lifecycle hook (used here to create tables and promote the first admin).

**Advantages.** Extremely fast development with very little boilerplate; validation and serialisation handled automatically; self-documenting endpoints; and strong editor support thanks to type hints.

**Why Selected.** FastAPI's combination of speed, automatic validation and auto-generated documentation makes it ideal for a data-driven application. The dependency-injection system in particular allowed clean, reusable authentication and admin guards (`get_current_user`, `get_admin_user`) to be applied across dozens of endpoints with a single line each, dramatically reducing repetitive security code.

## 4.3 Uvicorn (ASGI Server)

**Introduction.** Uvicorn is a lightning-fast Asynchronous Server Gateway Interface (ASGI) server. It is the process that actually runs the FastAPI application and handles incoming HTTP connections.

**Features.** High concurrency through an asynchronous event loop; hot-reload during development; production-grade performance; and simple command-line invocation.

**Advantages.** Minimal configuration; excellent throughput; and seamless integration with FastAPI.

**Why Selected.** FastAPI is an ASGI framework and therefore requires an ASGI server. Uvicorn is the de-facto standard companion, offering both a convenient `--reload` development mode and the performance characteristics needed for production, all from a single command.

## 4.4 Pydantic (Data Validation)

**Introduction.** Pydantic is a data-validation library that uses Python type annotations to define data schemas. In Resumate Pro it defines every request and response model in `backend/schemas.py` — for example `UserCreate`, `ResumeCreate`, `ResumeUpdate`, `AtsRequest` and the admin schemas.

**Features.** Automatic type coercion and validation; clear, structured validation errors; constrained fields (e.g., minimum password length, maximum name length); specialised types such as `EmailStr`; and effortless serialisation to and from JSON.

**Advantages.** Guarantees that data entering the system is well-formed before any business logic runs; eliminates large quantities of manual validation code; and produces consistent, machine-readable error responses.

**Why Selected.** Validating user input is a security and reliability necessity. By expressing the rules declaratively in Pydantic models, Resumate Pro enforces, for instance, valid email formats and a minimum six-character password automatically, with FastAPI returning a precise error if the rules are violated.

## 4.5 SQLAlchemy 2.0 (ORM)

**Introduction.** SQLAlchemy is the most widely used Object Relational Mapper in the Python ecosystem. It maps Python classes to database tables, allowing the application to manipulate rows as objects. Resumate Pro uses the modern SQLAlchemy 2.0 declarative style with `Mapped` and `mapped_column` typing to define the `User`, `Resume` and `ActivityLog` models.

**Features.** Declarative, typed model definitions; relationship management with cascading deletes; a powerful query interface; transaction and session management; and database independence — the same models work on SQLite and PostgreSQL.

**Advantages.** Eliminates hand-written SQL for the majority of operations; prevents SQL-injection by parameterising queries; keeps the schema and the code in one place; and allows the underlying database to be switched without changing application logic.

**Why Selected.** The project needed to store relational data (users own resumes; users generate activity logs) and to be able to migrate from a zero-configuration development database to a production database effortlessly. SQLAlchemy's database-agnostic ORM, combined with cascading relationships (deleting a user deletes their resumes and logs), made it the natural choice. The JSON column type also allows the entire structured resume document to be stored compactly in a single field.

## 4.6 SQLite and PostgreSQL (Database)

**Introduction.** SQLite is a serverless, file-based relational database engine bundled with Python; PostgreSQL is a powerful, open-source, client-server relational database used for production workloads. Resumate Pro uses SQLite by default and switches to PostgreSQL through the `DATABASE_URL` environment variable.

**Features.** *SQLite* — zero configuration, single-file storage, perfect for development and testing. *PostgreSQL* — concurrency, robustness, advanced indexing, JSON support and proven scalability.

**Advantages.** The pairing gives the project the convenience of a configuration-free development database and the strength of an industrial production database, with no code changes required to move between them thanks to the SQLAlchemy abstraction.

**Why Selected.** During development and demonstration, SQLite means the application runs instantly with no database server to install. For real-world deployment, PostgreSQL provides the concurrency and durability a multi-user web application requires. Supporting both maximises both convenience and production-readiness.

## 4.7 JWT Authentication (python-jose) and bcrypt

**Introduction.** JSON Web Tokens (JWT) provide stateless authentication: upon login the server issues a cryptographically signed token that the client presents on subsequent requests. *python-jose* encodes and decodes these tokens, while *bcrypt* securely hashes user passwords. Both are used in `backend/auth.py`.

**Features.** *JWT* — self-contained, signed, expiring tokens carrying the user's identity (`sub`), issued-at (`iat`) and expiry (`exp`) claims. *bcrypt* — a deliberately slow, salted hashing algorithm designed to resist brute-force attacks, with a configurable work factor (12 rounds in this project).

**Advantages.** Stateless tokens require no server-side session store, simplifying scaling; signing prevents tampering; expiry limits the damage from a leaked token; and bcrypt ensures that even if the database is compromised, plaintext passwords are never exposed.

**Why Selected.** A modern API benefits from stateless authentication that scales horizontally without sticky sessions. JWT was chosen for exactly this reason, and bcrypt — implemented directly to avoid a well-known `passlib`/`bcrypt` version incompatibility — provides the secure, salted password storage that responsible authentication demands. The implementation also safely truncates passwords to bcrypt's 72-byte limit.

## 4.8 scikit-learn and NumPy (Machine Learning)

**Introduction.** scikit-learn is the standard Python machine-learning library; NumPy provides the numerical array foundation it builds upon. In Resumate Pro, scikit-learn powers the job-description matcher in `core/job_matcher.py`.

**Features.** A `TfidfVectorizer` that converts text into Term Frequency–Inverse Document Frequency feature vectors (with English stop-word removal and unigram/bigram features), and a `cosine_similarity` function that measures the angular similarity between two such vectors.

**Advantages.** A mathematically principled, well-tested way to quantify textual similarity; extraction of the most informative terms from a job description; and robust, fast computation.

**Why Selected.** Measuring how closely a resume matches a job description is fundamentally a text-similarity problem. TF-IDF cosine similarity is a classic, explainable and dependency-light technique well suited to it. Importantly, the project also implements a pure-Python TF-IDF fallback so that matching still works even if scikit-learn is unavailable — reinforcing the system's resilience.

## 4.9 OpenAI API (Optional AI)

**Introduction.** The OpenAI API provides access to large language models capable of high-quality natural-language generation. Resumate Pro integrates it optionally in `core/ai_engine.py` for bullet enhancement, summary writing, cover-letter drafting and the chat assistant.

**Features.** Chat-completion models; controllable temperature and token limits; and instruction-following through system and user prompts. The integration uses a configurable model (defaulting to a compact, cost-efficient model).

**Advantages.** State-of-the-art language quality; natural, context-aware rewriting; and tailored, fluent generated text.

**Why Selected.** When the highest possible output quality is desired and an API key is available, an LLM produces superior summaries and cover letters. Critically, the integration is **strictly optional**: the engine checks for the API key at runtime and, if it is absent or a call fails, transparently falls back to the deterministic local engine. The product therefore gains LLM quality when configured without ever depending on it.

## 4.10 ReportLab (PDF Generation)

**Introduction.** ReportLab is a mature Python library for programmatically generating PDF documents. Resumate Pro uses it in `core/pdf_generator.py` to render structured resume data into polished, downloadable PDFs.

**Features.** The high-level *platypus* flowable system (paragraphs, spacers, horizontal rules, keep-together blocks); precise control over fonts, colours and layout; custom flowables (the project defines a coloured `HeaderBanner` and a `SidebarHeader`); and direct generation to an in-memory byte stream.

**Advantages.** Pixel-precise, reproducible output; no external rendering engine or headless browser required; and the ability to drive multiple visual templates from one rendering routine.

**Why Selected.** Producing a clean, consistent, ATS-friendly PDF is a core deliverable. ReportLab allows the four templates (Modern, Classic, Minimal, Creative) to be defined as data (colours, fonts, header style) and rendered by a single, single-column flowable pipeline — guaranteeing that every template stays machine-readable while remaining visually distinct.

## 4.11 PyPDF2 and python-docx (File Parsing)

**Introduction.** PyPDF2 extracts text from PDF files and python-docx extracts text from Microsoft Word DOCX files. Both are used by the resume parser in `core/resume_parser.py`.

**Features.** Page-by-page text extraction from PDFs; paragraph-level extraction from DOCX documents; and tolerant error handling so that a malformed file degrades gracefully rather than crashing.

**Advantages.** Enables the import feature, allowing users to bootstrap a structured resume from an existing file and avoid re-typing their entire history.

**Why Selected.** Resume import is a major usability feature. Since resumes commonly exist as PDF or Word files, these two libraries cover the overwhelming majority of real-world inputs; plain-text and Markdown are handled directly by Python's built-in decoding.

## 4.12 HTML5, Alpine.js and Tailwind CSS (Front-End)

**Introduction.** The browser front end is built from semantic HTML5 pages (`index.html`, `auth.html`, `app.html`, `admin.html`, `share.html`), made reactive with **Alpine.js** — a lightweight declarative JavaScript framework — and styled with **Tailwind CSS**, a utility-first CSS framework. A hand-written API client (`frontend/js/api.js`) wraps all server calls.

**Features.** Alpine.js provides declarative reactivity directly in HTML attributes without a build step; Tailwind provides composable utility classes and supports native dark mode; the API client centralises token handling (stored in `localStorage`), toast notifications, theme toggling and date formatting.

**Advantages.** No heavy front-end build pipeline; fast page loads; small bundle footprint; and a clean separation between the static UI and the JSON API.

**Why Selected.** For a project whose intelligence lives on the server, a lightweight front end is ideal. Alpine.js and Tailwind (delivered via CDN) allow a polished, reactive, themeable interface to be built quickly without the complexity of a single-page-application framework or a Node.js build toolchain, keeping the entire project deployable as one Python server.

## 4.13 REST API Architecture

**Introduction.** Representational State Transfer (REST) is an architectural style for networked applications in which resources are addressed by URLs and manipulated using standard HTTP verbs. Resumate Pro exposes its entire functionality as a REST API.

**Features.** Resource-oriented endpoints grouped by domain (`/api/auth`, `/api/resumes`, `/api/ai`, `/api/analyze`, `/api/export`, `/api/parse`, `/api/admin`); correct use of HTTP methods (GET, POST, PUT, PATCH, DELETE) and status codes (201 Created, 204 No Content, 401 Unauthorised, 403 Forbidden, 404 Not Found, 409 Conflict); and JSON request/response bodies.

**Advantages.** A clean contract between front end and back end; reusability of the API by any client (web, future mobile, third-party); statelessness; and self-documentation through OpenAPI.

**Why Selected.** A REST API cleanly decouples the user interface from the business logic, which is what allows the same backend to power the web workspace, the admin panel, the public share page and the automated test suite — and to power a future mobile client without modification.

## 4.14 Streamlit (Legacy Prototype UI)

**Introduction.** Streamlit is a Python framework for rapidly building data applications. The project retains an optional legacy prototype interface (`app.py`, `ui/pages.py`, `ui/styles.py`) built with Streamlit, Pandas and Plotly.

**Features.** Pure-Python UI definition; instant widgets; and integrated charting through Plotly.

**Why Selected.** Streamlit was used in the earliest prototyping phase to validate the core engines (builder, enhance, ATS, match, templates, cover letter, import, export) quickly before the production FastAPI + HTML front end was built. It is retained as an optional developer tool but is not the primary interface.

## 4.15 Overall Architecture Explanation

Resumate Pro follows a **layered, single-process, API-centric architecture**:

1. **Presentation layer** — static HTML pages enhanced by Alpine.js and Tailwind, communicating exclusively through the JSON REST API via the `api.js` client. The same FastAPI process also serves these static files.
2. **API / routing layer** — FastAPI routers in `backend/routes/` that validate input (Pydantic), enforce authentication and authorisation (dependency-injected guards), and orchestrate calls into the core engines.
3. **Domain / service layer** — the `core/` engines (`ai_engine`, `ats_analyzer`, `job_matcher`, `resume_parser`, `pdf_generator`, `templates`) that contain the actual intelligence and document-processing logic, supported by the `data/` knowledge bases and `utils/` helpers.
4. **Persistence layer** — SQLAlchemy ORM models (`User`, `Resume`, `ActivityLog`) mapped onto SQLite or PostgreSQL.
5. **Cross-cutting concerns** — JWT authentication, bcrypt hashing, CORS configuration, activity logging and the optional OpenAI integration with local fallback.

This separation means each layer can evolve independently: the engines can be improved without touching the API, the database can be swapped without touching the engines, and a new front end (such as a mobile app) can be added by consuming the same API. The architecture is depicted in detail in Chapter 5.

---PAGE BREAK---


# CHAPTER 5
# SYSTEM DESIGN

System design translates the requirements established during analysis into a concrete blueprint for implementation. This chapter presents the overall architecture, the system workflow, data-flow diagrams at two levels, the entity-relationship and database design, behavioural diagrams (use case, activity, sequence), structural diagrams (component and class), and detailed explanations of the folder structure, the front-end and back-end architecture, and the principal workflows (API, authentication, AI and resume generation).

## 5.1 Overall System Architecture

Resumate Pro is organised as a layered architecture in which a browser-based client communicates with a FastAPI application server that in turn calls a set of core engines and a relational database.

**Figure 5.1 — Overall System Architecture**

```
+===========================================================================+
|                              CLIENT (BROWSER)                             |
|  index.html  auth.html  app.html  admin.html  share.html                  |
|        |            Alpine.js (reactivity) + Tailwind CSS (style)         |
|        |            api.js  -> JWT token in localStorage                   |
+========|==================================================================+
         |  HTTPS / JSON  (REST)
         v
+===========================================================================+
|                      FastAPI APPLICATION  (server.py)                     |
|  CORS middleware  |  Static file serving  |  Lifespan: init_db + 1st admin|
|---------------------------------------------------------------------------|
|                              ROUTING LAYER  (backend/routes)              |
|  auth | resumes | ai | analyze | export | parse | admin                   |
|---------------------------------------------------------------------------|
|   Dependencies (deps.py): get_current_user (JWT)  /  get_admin_user       |
|   Validation (schemas.py): Pydantic request & response models             |
+========|=====================================================|============+
         |                                                     |
         v                                                     v
+===============================+               +===========================+
|     CORE ENGINES (core/)      |               |   PERSISTENCE (SQLAlchemy)|
|  ai_engine    ats_analyzer    |               |   models: User, Resume,   |
|  job_matcher  resume_parser   |               |           ActivityLog     |
|  pdf_generator  templates     |               |   database.py (engine)    |
|        |  uses                |               +============|==============+
|        v                      |                            |
|  DATA (data/)  +  UTILS       |                            v
|  skills_db  action_verbs      |               +===========================+
|  industry_keywords  helpers   |               |  SQLite (dev)             |
+===============|===============+               |  PostgreSQL (prod)        |
                |                               +===========================+
                v  (optional)
        +-----------------------+
        |  OpenAI API (LLM)     |  <-- used only if OPENAI_API_KEY is set;
        +-----------------------+      otherwise deterministic local fallback
```

**Table 5.1 — REST API Endpoint Catalogue**

| Group | Method & Path | Purpose | Auth |
|---|---|---|---|
| Auth | `POST /api/auth/register` | Create account, return token | Public |
| Auth | `POST /api/auth/login` | Authenticate, return token | Public |
| Auth | `GET /api/auth/me` | Current user profile | User |
| Auth | `PUT /api/auth/profile` | Update name / avatar colour | User |
| Auth | `POST /api/auth/change-password` | Change password | User |
| Resumes | `GET /api/resumes` | List own resumes | User |
| Resumes | `POST /api/resumes` | Create resume | User |
| Resumes | `GET /api/resumes/{id}` | Get one resume | User |
| Resumes | `PUT /api/resumes/{id}` | Update resume | User |
| Resumes | `DELETE /api/resumes/{id}` | Delete resume | User |
| Resumes | `POST /api/resumes/{id}/duplicate` | Duplicate resume | User |
| Share | `GET /api/resumes/share/{token}` | Public read-only resume (+view count) | Public |
| AI | `POST /api/ai/enhance-bullet` | Rewrite a weak bullet | User |
| AI | `POST /api/ai/summary` | Generate professional summary | User |
| AI | `POST /api/ai/cover-letter` | Generate tailored cover letter | User |
| AI | `GET /api/ai/skill-suggestions` | Full skills DB (autocomplete) | User |
| AI | `POST /api/ai/suggest-skills` | Suggest skills for this resume | User |
| AI | `POST /api/ai/chat` | Career-advice chat | User |
| Analyze | `POST /api/analyze/ats` | Compute ATS score | User |
| Analyze | `POST /api/analyze/match` | Match resume to job description | User |
| Export | `GET /api/export/pdf/{id}` | Download resume PDF | User |
| Export | `POST /api/export/cover-letter/pdf` | Download cover-letter PDF | User |
| Parse | `POST /api/parse` | Upload & parse resume file | User |
| Admin | `GET /api/admin/stats` | Platform statistics | Admin |
| Admin | `GET /api/admin/growth` | Daily signup growth | Admin |
| Admin | `GET /api/admin/users` | List / search users | Admin |
| Admin | `GET /api/admin/users/{id}` | User detail + activity | Admin |
| Admin | `PATCH /api/admin/users/{id}` | Ban / promote user | Admin |
| Admin | `DELETE /api/admin/users/{id}` | Delete user | Admin |
| Admin | `GET /api/admin/resumes` | List all resumes | Admin |
| Admin | `DELETE /api/admin/resumes/{id}` | Delete any resume | Admin |
| Admin | `GET /api/admin/activity` | Activity audit log | Admin |
| Meta | `GET /api/health` | Health & counts | Public |

## 5.2 System Workflow

**Figure 5.2 — System Workflow**

```
   START
     |
     v
[ Visit landing page ] ---- no account ----> [ Register ] --+
     |                                                       |
  has account                                                v
     |                                              [ Auto-login + JWT ]
     v                                                       |
[ Login ] --------------------------------------------------+
     |
     v
[ Dashboard: list of resumes ]
     |
     +--> [ Import existing file ] --> parse --> structured data --+
     |                                                             |
     +--> [ Create new / blank ] ----------------------------------+
                                                                   |
                                                                   v
                                                       [ Resume Editor ]
                                                                   |
              +----------------+----------------+-----------------+----------------+
              v                v                v                 v                v
       [ AI Enhance ]   [ Generate     ]  [ ATS Score ]    [ Job Match ]    [ Choose template ]
       (rewrite bullets) [ summary/cover]  (6 dimensions)  (vs JD)          (Modern/Classic/...)
              |                |                |                 |                |
              +----------------+--------+-------+-----------------+----------------+
                                        |  (auto-save every ~1.5s)
                                        v
                              [ Export as PDF ] / [ Share public link ]
                                        |
                                        v
                                       END
```

## 5.3 Data Flow Diagram — Level 0 (Context Diagram)

The context diagram shows Resumate Pro as a single process interacting with its external entities: the Job Seeker, the Administrator and the optional OpenAI service.

**Figure 5.3 — DFD Level 0 (Context Diagram)**

```
                credentials, resume data,            resume PDF, ATS score,
                job description, files               match report, suggestions
   +-------------+ -------------------------->  +------------------------+ --------------------> +-------------+
   | JOB SEEKER  |                               |                        |                       | JOB SEEKER  |
   +-------------+ <--------------------------   |     RESUMATE PRO       |                       +-------------+
                                                 |   (Resume Builder      |
   +-------------+   admin actions               |     System)            |   stats, user list,
   | ADMINISTRATOR| -------------------------->  |                        | --------------------> | ADMINISTRATOR|
   +-------------+ <--------------------------   |                        |   activity log
                                                 +-----------+------------+
                                                             |  ^
                                          prompt (optional)  |  |  generated text
                                                             v  |
                                                    +------------------+
                                                    |   OpenAI API     |
                                                    +------------------+
```

## 5.4 Data Flow Diagram — Level 1

The Level-1 diagram decomposes the single process into the major functional processes and shows the data stores (D1 Users, D2 Resumes, D3 Activity Logs).

**Figure 5.4 — DFD Level 1**

```
  +-----------+
  | JOB SEEKER|
  +-----+-----+
        | credentials
        v
  (1.0 Authentication) <----> [ D1: Users ]
        | token              writes login -> [ D3: Activity Logs ]
        v
  (2.0 Resume Management) <----> [ D2: Resumes ]
        |   ^                     logs CRUD -> [ D3: Activity Logs ]
        |   | structured resume
        v   |
  (3.0 AI Enhancement) ---- uses ----> [ data: skills, verbs, keywords ]
        |   (enhance / summary / cover / suggest / chat)   (optional: OpenAI)
        v
  (4.0 Analysis: ATS + Match) ---- uses ----> [ data: keywords ] + scikit-learn
        |   returns score / report
        v
  (5.0 Parsing) <---- file upload ---- [ JOB SEEKER ]   (PyPDF2 / python-docx)
        |   returns structured resume
        v
  (6.0 Export / Share) ---- ReportLab ----> resume PDF / cover-letter PDF
        |                                    public link -> increments view_count in [ D2 ]
        v
  +-----------+        +---------------+
  | JOB SEEKER|        | ADMINISTRATOR | --> (7.0 Administration) <--> D1, D2, D3
  +-----------+        +---------------+         stats / growth / manage / audit
```

## 5.5 Entity Relationship Diagram

The data model comprises three entities. A `User` owns many `Resume` records and generates many `ActivityLog` records; both child relationships cascade on delete.

**Figure 5.5 — Entity Relationship Diagram (text notation)**

```
      +---------------------------+
      |           USER            |
      +---------------------------+
      | PK id                     |
      |    email (unique)         |
      |    name                   |
      |    password_hash          |
      |    is_active              |
      |    is_admin               |
      |    last_login             |
      |    login_count            |
      |    avatar_color           |
      |    created_at / updated_at|
      +-------------+-------------+
                    | 1
        +-----------+-----------+
        |                       |
      owns (1..N)            generates (1..N)
        |                       |
        v N                     v N
+----------------------+   +----------------------------+
|        RESUME        |   |        ACTIVITY_LOG        |
+----------------------+   +----------------------------+
| PK id                |   | PK id                      |
| FK user_id           |   | FK user_id                 |
|    title             |   |    action                  |
|    template          |   |    detail                  |
|    data (JSON)       |   |    ip_address              |
|    ats_score         |   |    created_at              |
|    view_count        |   +----------------------------+
|    is_public         |
|    share_token (uniq)|
|    created_at/updated|
+----------------------+

Relationships:
  USER (1) ──── owns ────< (N) RESUME           [cascade delete]
  USER (1) ──── logs ────< (N) ACTIVITY_LOG     [cascade delete]
```

## 5.6 Use Case Diagram

**Figure 5.6 — Use Case Diagram**

```
        +--------------------------- RESUMATE PRO ---------------------------+
        |                                                                    |
        |   (Register)        (Login)        (Manage Profile)                |
        |   (Create Resume)   (Edit Resume)  (Duplicate Resume)              |
   (Job |   (Delete Resume)   (Import Resume File)                           |
  Seeker)--(Enhance Bullet)   (Generate Summary)   (Generate Cover Letter)   |
    O   |   (Suggest Skills)  (Chat with Assistant)                          |
   /|\  |   (Compute ATS Score) (Match to Job Description)                   |
   / \  |   (Export PDF)      (Share Public Link)                            |
        |                                                                    |
        |   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  |
        |                                                                    |
 (Admin)|   (View Statistics) (View Growth Chart) (Manage Users)            |
    O   |   (Ban/Promote User)(Delete User) (View All Resumes)               |
   /|\ -|   (Delete Any Resume)(View Activity Log)                           |
   / \  |                                                                    |
        |                                                                    |
        |  <<external>> OpenAI API  - - participates in - - (AI use cases)   |
        +--------------------------------------------------------------------+

Note: The Admin actor inherits all Job Seeker use cases (an admin is also a user).
```

## 5.7 Activity Diagram — Resume Optimisation Loop

**Figure 5.7 — Activity Diagram (Resume Optimisation)**

```
        (●) start
         |
         v
   [ Open / create resume ]
         |
         v
   [ Edit sections (personal, experience, skills...) ]
         |
         v
   [ Run ATS analysis ] ---------------------------+
         |                                          |
         v                                          |
     < score >= target ? >                          |
        /         \                                 |
      yes          no                               |
       |            |                               |
       |            v                               |
       |   [ Read suggestions ]                     |
       |            |                               |
       |            v                               |
       |   [ Apply AI Enhance / add metrics /       |
       |     add keywords / fix sections ]          |
       |            |                               |
       |            +-------- auto-save ------------+
       |                     (re-run analysis)
       v
   [ (optional) Match against job description ]
       |
       v
   [ Choose template & Export PDF / Share ]
       |
       v
      (◉) end
```

## 5.8 Sequence Diagram — Login and AI Bullet Enhancement

**Figure 5.8 — Sequence Diagram (Authentication & AI Enhancement)**

```
 User    Browser(api.js)   FastAPI Route     deps/auth      ai_engine     OpenAI(opt)   DB
  |            |                |                |              |             |          |
  |--login---->|                |                |              |             |          |
  |            |--POST /login-->|                |              |             |          |
  |            |                |--verify_password (bcrypt)----------------------------->|
  |            |                |<--user row-------------------------------------------- |
  |            |                |--create_access_token (JWT)-->|              |          |
  |            |<--token+user---|                |              |             |          |
  |  (token stored in localStorage)             |              |             |          |
  |            |                |                |              |             |          |
  |--enhance-->|                |                |              |             |          |
  |            |--POST /ai/enhance-bullet (Bearer token)------->|             |          |
  |            |                |--get_current_user-->decode_token (verify)   |          |
  |            |                |<--authenticated user--------- |             |          |
  |            |                |--enhance_bullet(text)-------->|             |          |
  |            |                |                |   if OPENAI_API_KEY:       |          |
  |            |                |                |     -------- prompt ------>|          |
  |            |                |                |     <------ rewritten -----|          |
  |            |                |                |   else: local deterministic rewrite   |
  |            |                |<--enhanced bullet------------ |             |          |
  |            |<--{original, enhanced}----------|              |             |          |
  |<--shown----|                |                |              |             |          |
```

## 5.9 Component Diagram

**Figure 5.9 — Component Diagram**

```
+-------------------+        +------------------------------------------+
|  Front-end SPA    |  HTTP  |              FastAPI Server              |
|  (HTML/Alpine/    |<------>|  +------------------------------------+  |
|   Tailwind)       |  JSON  |  |  Routers: auth, resumes, ai,       |  |
|  api.js client    |        |  |  analyze, export, parse, admin     |  |
+-------------------+        |  +------------------+-----------------+  |
                             |          |          |                    |
                             |          v          v                    |
                             |  +-------------+  +---------------------+ |
                             |  | Core Engines|  | Persistence (ORM)   | |
                             |  | ai_engine   |  | models + database   | |
                             |  | ats_analyzer|  +----------+----------+ |
                             |  | job_matcher |             |            |
                             |  | resume_parser|            v            |
                             |  | pdf_generator|   +-----------------+   |
                             |  | templates   |    | SQLite/Postgres |   |
                             |  +------+------+     +-----------------+   |
                             |         | uses                            |
                             |         v                                 |
                             |  +-------------------------------+        |
                             |  | data: skills_db, action_verbs,|        |
                             |  | industry_keywords; utils      |        |
                             |  +-------------------------------+        |
                             +------------------------------------------+
                                         | optional
                                         v
                                  +--------------+
                                  |  OpenAI API  |
                                  +--------------+
```

## 5.10 Class Diagram (Domain Model)

**Figure 5.10 — Class Diagram (Persistence Layer)**

```
+-------------------------------+        +-------------------------------+
|             User              | 1    N |            Resume             |
+-------------------------------+--------+-------------------------------+
| - id: int (PK)                |        | - id: int (PK)                |
| - email: str (unique)         |        | - user_id: int (FK)           |
| - name: str                   |        | - title: str                  |
| - password_hash: str          |        | - template: str               |
| - is_active: bool             |        | - data: dict (JSON)           |
| - is_admin: bool              |        | - ats_score: int?             |
| - last_login: datetime?       |        | - view_count: int             |
| - login_count: int            |        | - is_public: bool             |
| - avatar_color: str           |        | - share_token: str (unique)   |
| - created_at/updated_at       |        | - created_at/updated_at       |
+---------------+---------------+        +-------------------------------+
                | 1
                | N
+-------------------------------+
|          ActivityLog          |
+-------------------------------+
| - id: int (PK)                |
| - user_id: int (FK)           |
| - action: str                 |
| - detail: str                 |
| - ip_address: str             |
| - created_at: datetime        |
+-------------------------------+

Service classes (stateless modules, not ORM):
  ai_engine      :: enhance_bullet(), generate_summary(), generate_cover_letter(), suggest_skills()
  ats_analyzer   :: analyze(resume) -> {overall, grade, breakdown, suggestions}
  job_matcher    :: match(resume, jd) -> {match_score, matched/missing, recommendations}
  resume_parser  :: parse_resume(bytes, filename) -> structured resume dict
  pdf_generator  :: render_pdf(resume, template), render_cover_letter_pdf(text)
```

## 5.11 Database Schema

The three tables are defined by the SQLAlchemy models in `backend/models.py`.

**Table 5.2 — `users`**

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | Primary Key |
| email | VARCHAR(255) | Unique, Indexed, Not Null |
| name | VARCHAR(120) | Default '' |
| password_hash | VARCHAR(255) | Not Null |
| created_at | DATETIME | Default now |
| updated_at | DATETIME | Default now, on update |
| is_active | BOOLEAN | Default True |
| is_admin | BOOLEAN | Default False |
| last_login | DATETIME | Nullable |
| login_count | INTEGER | Default 0 |
| avatar_color | VARCHAR(20) | Default '#6366f1' |

**Table 5.3 — `resumes`**

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key → users.id, Indexed, Not Null |
| title | VARCHAR(160) | Default 'Untitled Resume' |
| template | VARCHAR(40) | Default 'modern' |
| data | JSON | Default {} |
| created_at / updated_at | DATETIME | Default now / on update |
| view_count | INTEGER | Default 0 |
| ats_score | INTEGER | Nullable |
| is_public | BOOLEAN | Default False |
| share_token | VARCHAR(40) | Unique, Indexed, auto-generated |

**Table 5.4 — `activity_logs`**

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key → users.id, Indexed, Not Null |
| action | VARCHAR(80) | Not Null (e.g., `resume_created`) |
| detail | VARCHAR(255) | Default '' |
| ip_address | VARCHAR(45) | Default '' |
| created_at | DATETIME | Default now, Indexed |

## 5.12 Folder Structure Explanation

```
resumate-pro/
├── server.py              FastAPI entry point; mounts routers, serves frontend,
│                          runs init_db() and first-admin promotion on startup.
├── app.py                 Optional legacy Streamlit prototype UI entry point.
├── smoke_test.py          End-to-end test exercising every endpoint via TestClient.
├── requirements.txt       Pinned Python dependencies.
├── .env.example           Template for environment configuration.
├── app.db                 SQLite database file (development).
│
├── backend/               The web application layer.
│   ├── database.py        SQLAlchemy engine/session, Base, init_db().
│   ├── models.py          ORM models: User, Resume, ActivityLog.
│   ├── schemas.py         Pydantic request/response models.
│   ├── auth.py            bcrypt hashing + JWT encode/decode helpers.
│   ├── deps.py            Auth dependencies: get_current_user, get_admin_user.
│   └── routes/            One router per domain:
│       ├── auth.py        register, login, me, profile, change-password.
│       ├── resumes.py     CRUD, duplicate, public share (+view count).
│       ├── ai.py          enhance, summary, cover letter, suggest, chat.
│       ├── analyze.py     ATS score, JD match.
│       ├── export.py      PDF resume + cover-letter PDF.
│       ├── parse.py       Upload & parse resume files.
│       └── admin.py       Stats, growth, users, resumes, activity.
│
├── core/                  Domain/intelligence engines:
│   ├── ai_engine.py       Bullet enhancement, summary, cover letter, suggestions.
│   ├── ats_analyzer.py    Six-dimension ATS scoring.
│   ├── job_matcher.py     TF-IDF cosine + coverage match scoring.
│   ├── resume_parser.py   PDF/DOCX/TXT/MD text extraction & section parsing.
│   ├── pdf_generator.py   ReportLab rendering for four templates.
│   └── templates.py       Template metadata (colours, fonts, header style).
│
├── data/                  Knowledge bases:
│   ├── skills_db.py        Categorised skills + extraction.
│   ├── action_verbs.py     Power verbs by category + weak-phrase detection.
│   └── industry_keywords.py 7 industry keyword sets + detection.
│
├── utils/helpers.py       Tokenizing, number detection, empty_resume schema.
│
├── frontend/              Static client:
│   ├── index.html / auth.html / app.html / admin.html / share.html
│   ├── css/styles.css      Design system (dark mode).
│   └── js/api.js, app.js, auth.js   API client and controllers.
│
└── ui/                    Legacy Streamlit pages and styles.
    ├── pages.py
    └── styles.py
```

## 5.13 Front-End Architecture

The front end is a set of static HTML pages served directly by the FastAPI process. Each page declares its interactive behaviour using Alpine.js directives and styles itself with Tailwind utility classes. A single shared module, `api.js`, exposes the `window.API` object that encapsulates all server communication. This module is responsible for attaching the JWT bearer token (read from `localStorage`) to every request, transparently redirecting to the login page on a `401` response, surfacing toast notifications, toggling the light/dark theme and formatting dates. Page-specific controllers (`auth.js`, `app.js`) implement the behaviour of the authentication screen and the main workspace respectively. Because all state changes flow through the API client, the front end remains a thin presentation layer over the REST API.

## 5.14 Back-End Architecture

The back end follows the **router → dependency → service → model** pattern. Each HTTP request enters through a FastAPI router function, which first runs Pydantic validation on the request body. Authentication and authorisation are injected as dependencies: `get_current_user` decodes and validates the JWT and loads the corresponding user, while `get_admin_user` additionally enforces the admin flag. The router then delegates to a core engine (for intelligence operations) or directly manipulates ORM models within a request-scoped database session. Responses are again shaped by Pydantic models. Significant actions write an `ActivityLog` row before the transaction is committed, providing a complete audit trail.

## 5.15 API Workflow

A typical authenticated API call proceeds as follows: (1) the client attaches `Authorization: Bearer <token>`; (2) FastAPI resolves the route and runs the `get_current_user` dependency, which decodes the token, extracts the subject (user id), and loads an active user from the database — rejecting the request with `401` if any step fails; (3) the request body is validated against the route's Pydantic schema; (4) the route executes its logic, calling engines and/or the database; (5) the result is serialised through a response model and returned as JSON with an appropriate HTTP status code. Admin routes insert the extra `get_admin_user` check, returning `403` for non-admins.

## 5.16 Authentication Workflow

On registration, the submitted password is hashed with bcrypt (12 rounds, truncated safely to 72 bytes), a `User` row is created, the registration is logged with the originating IP, and a JWT is issued. The very first registered user is automatically promoted to administrator during the application's startup lifespan hook. On login, the supplied password is verified against the stored hash; on success, `last_login` and `login_count` are updated, the login is logged, and a fresh JWT is returned. The token carries the user id as its subject and an expiry claim (24 hours by default). All protected endpoints validate this token on every request; there is no server-side session, making the scheme stateless and horizontally scalable.

## 5.17 AI Workflow

When an AI endpoint is invoked, the `ai_engine` first checks whether an OpenAI API key is configured. If it is, the engine constructs a carefully bounded prompt (with explicit instructions not to invent achievements) and requests a completion; if the call succeeds, the model's text is returned. If no key is present, or the call fails, the engine seamlessly falls back to its deterministic local implementation. For bullet enhancement, the local path strips recognised weak openers (e.g., *"responsible for"*), infers an impact category from the bullet's content, deterministically selects a strong action verb from the corresponding category, and appends a quantification hint if the bullet contains no numbers. For summaries it synthesises three sentences from inferred years of experience, top skills and detected industry; for cover letters it composes a structured letter highlighting overlapping skills. This dual path guarantees a useful result in every case.

## 5.18 Resume Generation (Export) Workflow

To export a resume, the export route loads the resume (verifying ownership), selects the template metadata by key, and invokes the ReportLab-based `pdf_generator`. The generator builds an ordered list of flowables — a header (rendered as a coloured banner, sidebar accent, minimal heading or underlined heading depending on the template), followed by summary, experience, projects, education, skills, certifications, awards and languages sections. All text is HTML-escaped for safety, bullets are rendered with proper indentation, and related blocks are kept together to avoid awkward page breaks. The document is written to an in-memory buffer and returned as a downloadable PDF with a sanitised filename derived from the resume title. The same generator renders cover letters from plain text using the chosen template's typography.

---PAGE BREAK---


# CHAPTER 6
# MODULE DESCRIPTION

This chapter describes each functional module of Resumate Pro in detail. For every module the purpose, inputs, internal processing, outputs, advantages and workflow are presented, based directly on the implemented source code.

## 6.1 User Authentication Module

**Purpose.** To securely register new users, authenticate returning users, manage user profiles, and protect every other module behind token-based access control. Implemented in `backend/routes/auth.py`, `backend/auth.py` and `backend/deps.py`.

**Input.** Email, name and password for registration; email and password for login; name and avatar colour for profile updates; current and new password for password changes; a JWT bearer token for all protected requests.

**Processing.** Registration normalises the email, rejects duplicates with a `409 Conflict`, hashes the password with bcrypt, creates the user, logs the event with the client IP, and issues a JWT. Login verifies the password, blocks disabled accounts, updates `last_login` and `login_count`, logs the login and returns a JWT. The `get_current_user` dependency decodes and validates the token on every protected call; `get_admin_user` additionally enforces the admin flag.

**Output.** A signed JWT access token plus a sanitised user object (which never includes the password hash); for profile and password operations, a confirmation response.

**Advantages.** Passwords are never stored in plain text; sessions are stateless and scalable; all authentication events are auditable; and a single reusable dependency secures the entire API.

**Workflow.** `Register/Login → validate → (hash/verify) → log activity → issue JWT → client stores token → token sent on every subsequent request → validated by dependency.`

## 6.2 Dashboard Module

**Purpose.** To present each authenticated user with an overview of their resume library and act as the launch point for all editing and analysis actions.

**Input.** The user's JWT; implicitly, the user's identity resolved from the token.

**Processing.** The dashboard calls `GET /api/resumes`, which returns all resumes belonging to the user ordered by most recently updated, including each resume's title, template, timestamps, public flag, share token, view count and persisted ATS score.

**Output.** A list of resume summary cards from which the user can open, duplicate, delete, share or export each resume, and a control to create or import a new resume.

**Advantages.** Centralised management of multiple tailored resumes; at-a-glance visibility of ATS scores and share status; quick access to all actions.

**Workflow.** `Login → fetch resume summaries → render cards → user selects an action (open / create / import / duplicate / delete / share).`

## 6.3 Resume Builder (Editor) Module

**Purpose.** To allow structured creation and editing of all resume sections. Backed by the resume CRUD endpoints in `backend/routes/resumes.py`.

**Input.** Structured resume data: personal details, summary, experience entries (role, company, dates, location, bullets), education, skills, projects, certifications, languages and awards; a title and a chosen template.

**Processing.** New resumes are created via `POST /api/resumes`, defaulting to the standard empty-resume schema when no data is supplied. Edits are persisted through `PUT /api/resumes/{id}`, which updates only the fields provided (title, template, data, public flag, ATS score). The front end auto-saves changes a short interval after the user stops typing. Ownership is enforced on every operation, and each change is recorded in the activity log.

**Output.** The persisted resume object with updated timestamps; a live save indicator in the UI.

**Advantages.** Structured data enables analysis and AI features; partial updates are efficient; auto-save prevents data loss; ownership checks guarantee privacy.

**Workflow.** `Open editor → edit a section → debounce → PUT update → log → confirmation indicator.`

## 6.4 AI Content Generator Module

**Purpose.** To improve resume content using language intelligence — rewriting bullets, generating summaries, drafting cover letters and suggesting skills. Implemented in `core/ai_engine.py` and exposed via `backend/routes/ai.py`.

**Input.** For bullet enhancement: a single bullet and an optional role hint. For summary and skill suggestions: the structured resume. For cover letters: the resume, a job description and an optional company name.

**Processing.** Each function follows the dual-mode pattern (OpenAI when configured, deterministic local engine otherwise). Bullet enhancement detects and strips weak openers, infers an impact category, selects a strong action verb, and adds a quantification hint when no number is present. Summary generation infers years of experience, top skills and industry. Skill suggestion extracts recognised skills and tops up with industry keywords the resume lacks.

**Output.** An enhanced bullet (with the original preserved); a three-sentence summary; a tailored cover letter; or a list of suggested skills.

**Advantages.** Converts weak writing into strong, action-led statements instantly; works offline; never fabricates achievements; tailors output to the detected industry and the target role.

**Workflow.** `Select text/section → call AI endpoint → engine chooses LLM or local path → return improved text → user reviews and accepts.`

## 6.5 ATS Score Module

**Purpose.** To objectively evaluate a resume's machine-readability and content strength and to return actionable feedback. Implemented in `core/ats_analyzer.py` via `POST /api/analyze/ats`.

**Input.** The structured resume.

**Processing.** The analyser scores six weighted dimensions and aggregates them into a total out of 100, then assigns a letter grade and compiles up to twelve prioritised suggestions.

**Table 6.1 — ATS Scoring Dimensions and Weights**

| Dimension | Weight | What it measures |
|---|---|---|
| Contact completeness | 15 | Name, valid email, phone, location, professional link |
| Section coverage | 15 | Summary, experience, education, skills, extras present |
| Keyword density | 20 | Coverage of detected-industry keywords + recognised skills |
| Action-verb strength | 15 | Proportion of bullets starting with strong verbs (penalises weak openers) |
| Quantification | 15 | Proportion of bullets containing numbers/metrics |
| Length & formatting | 20 | Word count range, bullet length, summary length |

**Output.** A JSON report containing the overall score, the grade, a per-dimension breakdown (with detected industry, keyword hits and missing keywords), and the suggestion list.

**Advantages.** Makes hidden machine evaluation visible and explainable; turns vague "is my resume good?" anxiety into a concrete, improvable number; drives the optimisation loop.

**Workflow.** `Submit resume → score 6 dimensions → aggregate → grade → collect suggestions → return report → user acts → re-run.`

## 6.6 Job Match Module

**Purpose.** To quantify how well a resume aligns with a specific job description and to identify the gaps. Implemented in `core/job_matcher.py` via `POST /api/analyze/match`.

**Input.** The structured resume and a job-description string.

**Processing.** The resume is flattened to text and compared with the job description using TF-IDF cosine similarity (scikit-learn, with a pure-Python fallback). The most informative job-description terms are extracted and classified as matched or missing. Recognised skills in the job description are checked against the resume to produce a skill gap. A blended score is computed as `0.3 × cosine + 0.4 × keyword-coverage + 0.3 × skill-coverage`, scaled to 0–100.

**Output.** A match score; the component cosine, keyword-coverage and skill-coverage figures; matched and missing keywords; matched and missing (gap) skills; the top job-description terms; and concrete recommendations.

**Advantages.** Replaces guesswork with a measurable alignment figure; tells the user exactly which skills and phrases to add; encourages honest tailoring ("only if you genuinely have them").

**Workflow.** `Paste JD → flatten resume → compute cosine + coverage + skill gap → blend → recommend → user tailors → re-match.`

## 6.7 Resume Preview and Template Module

**Purpose.** To let the user choose among professionally designed, ATS-friendly templates and preview the result. Template metadata lives in `core/templates.py`.

**Input.** A template key (`modern`, `classic`, `minimal`, `creative`) stored on the resume.

**Processing.** Each template defines primary/secondary/muted colours, main and bold fonts, type sizes and a header style. The PDF generator consumes this metadata to render the chosen look while keeping every layout single-column.

**Output.** A styled rendering of the resume in the selected template.

**Advantages.** Visual variety for different industries (Modern for tech, Classic for finance/law/academia, Minimal for design/PM, Creative for marketing) without ever sacrificing ATS-readability.

**Workflow.** `Select template → metadata loaded → generator applies styling → preview / export.`

## 6.8 Download (PDF Export) Module

**Purpose.** To produce a downloadable, polished PDF of a resume or a cover letter. Implemented in `core/pdf_generator.py` via `backend/routes/export.py`.

**Input.** A resume id (for resume export) or cover-letter text plus a name and template (for cover-letter export).

**Processing.** Ownership of the resume is verified, the template is resolved, and ReportLab assembles the document from flowables — header, summary, experience, projects, education, skills, certifications, awards, languages — with all content escaped and grouped to avoid bad page breaks. The PDF is generated into an in-memory buffer.

**Output.** A `application/pdf` response with a `Content-Disposition: attachment` header and a sanitised filename.

**Advantages.** Consistent, reproducible, print-ready output; no external rendering engine; ATS-safe single-column structure.

**Workflow.** `Request export → verify ownership → resolve template → render flowables → stream PDF download.`

## 6.9 Import / Parse Module

**Purpose.** To let users bootstrap a structured resume from an existing file. Implemented in `core/resume_parser.py` via `backend/routes/parse.py`.

**Input.** An uploaded file (PDF, DOCX, TXT or MD), limited to 5 MB and validated by extension.

**Processing.** Text is extracted (PyPDF2 for PDF, python-docx for DOCX, direct decoding for text). The parser heuristically locates section headings using an alias table, splits the document into sections, and extracts personal details (name, title, email, phone, links, location via regular expressions), experience blocks, education, skills (cross-referenced against the skills database), projects, certifications, languages and awards.

**Output.** A partial structured resume dict ready to load into the editor (the raw text is stripped before returning).

**Advantages.** Eliminates re-typing an entire resume; tolerant of messy real-world formatting; jump-starts the editing workflow.

**Workflow.** `Upload file → validate type/size → extract text → split sections → extract fields → return structured resume.`

## 6.10 Public Share Module

**Purpose.** To allow a user to publish a read-only version of a resume at a unique, unguessable URL, and to count its views. Implemented in `backend/routes/resumes.py`.

**Input.** A public/private toggle on the resume; for viewers, the resume's share token.

**Processing.** Each resume is created with a unique, randomly generated share token. Setting `is_public` true exposes the resume at `GET /api/resumes/share/{token}` (no authentication required). Each successful public view increments the resume's `view_count`. If the resume is private, the public endpoint returns `404`.

**Output.** A read-only resume payload for viewers; an incrementing view count for the owner.

**Advantages.** Easy sharing with recruiters via a link; privacy preserved by default; basic engagement analytics through view counts.

**Workflow.** `Owner toggles public → share link generated → viewer opens link → resume served read-only → view_count++ → owner sees count.`

## 6.11 Career-Advice Chat Module

**Purpose.** To answer the user's resume-related questions conversationally. Implemented in `backend/routes/ai.py`.

**Input.** A free-text question and an optional resume snapshot.

**Processing.** When OpenAI is configured, the question and a truncated resume snapshot are sent to the model with a career-coach system prompt. Otherwise a rule-based responder pattern-matches the question (summaries, bullets, ATS, matching, cover letters, templates) and returns targeted advice — for example counting the user's weak bullet openers when asked about experience.

**Output.** A short, actionable text reply.

**Advantages.** Contextual guidance without leaving the app; works offline; gently steers users toward the relevant tool.

**Workflow.** `Ask question → LLM or rule-based responder → return concise advice.`

## 6.12 Profile and Settings Module

**Purpose.** To let users personalise their account. Implemented in `backend/routes/auth.py`.

**Input.** Updated display name and/or avatar colour; or current and new password.

**Processing.** Profile updates modify the relevant fields; password changes verify the current password before storing a new bcrypt hash and logging the change.

**Output.** The updated user object or a success confirmation.

**Advantages.** User control over identity and security; auditable password changes.

**Workflow.** `Open profile → edit name/colour or change password → validate → persist → confirm.`

## 6.13 Admin Module

**Purpose.** To provide platform governance: statistics, growth tracking, user management, resume oversight and a full audit trail. Implemented in `backend/routes/admin.py`; access is restricted by the `get_admin_user` guard.

**Input.** Admin JWT; query parameters for pagination/search; user or resume identifiers and update payloads.

**Processing.** The stats endpoint aggregates totals (users, resumes, active users, new today/this week, public resumes, total logins). The growth endpoint groups signups by day. User management supports searching, paginating, banning/unbanning (`is_active`), promoting/demoting (`is_admin`) and deleting users — with safeguards preventing an admin from removing their own privileges or deleting their own account. Resume management lists all resumes with owner information and can delete any of them. The activity endpoint returns the chronological audit log. Every administrative action is itself logged.

**Output.** Statistics objects, a growth dataset for charting, paginated user and resume lists, and the activity log.

**Advantages.** Complete operational visibility and control; protected against accidental self-lockout; full accountability through logging.

**Workflow.** `Admin opens /admin → load stats + growth chart → manage users/resumes → review activity log; non-admins are redirected to /app.`

---PAGE BREAK---


# CHAPTER 7
# SCREENSHOTS

This chapter presents the user interface of Resumate Pro through annotated screenshot placeholders. When compiling the final report, replace each `[ Insert Screenshot ]` block with an actual capture taken from a running instance of the application (landing page at `/`, authentication at `/login`, workspace at `/app`, admin at `/admin`, and a public share link at `/share/{token}`). Each figure is accompanied by a description of what it demonstrates.

---

**Figure 7.1 — Landing Page**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|              ResuMate AI — landing / index.html                  |
+------------------------------------------------------------------+
```
*Description:* The public landing page introducing Resumate Pro, its key value proposition (AI-powered, ATS-friendly resume building) and a call to action directing visitors to register or sign in.

---

**Figure 7.2 — Registration Page**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|         Sign-up form (name, email, password) — auth.html         |
+------------------------------------------------------------------+
```
*Description:* The registration screen where a new user enters name, email and password. On submission the account is created, a JWT is issued and the user is taken into the workspace. The first registered user is automatically granted administrator rights.

---

**Figure 7.3 — Login Page**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|              Sign-in form (email, password)                      |
+------------------------------------------------------------------+
```
*Description:* The login screen validating credentials against the bcrypt-hashed password and returning an access token on success.

---

**Figure 7.4 — Dashboard / Resume Library**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|        Grid of resume cards with title, ATS score, actions       |
+------------------------------------------------------------------+
```
*Description:* The dashboard listing all of the user's resumes ordered by last update, showing each resume's template, persisted ATS score, share status and view count, with actions to open, duplicate, delete, share or export.

---

**Figure 7.5 — Resume Editor (Personal & Summary)**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     Structured editor — personal details and summary section     |
+------------------------------------------------------------------+
```
*Description:* The structured editor capturing personal information (name, title, contact details, links) and the professional summary, with auto-save active.

---

**Figure 7.6 — Resume Editor (Experience & Bullets)**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     Experience entries with editable bullet points               |
+------------------------------------------------------------------+
```
*Description:* The experience section where each role contains editable bullet points, each with a "Rewrite" action that invokes the AI bullet enhancer.

---

**Figure 7.7 — AI Bullet Enhancement Result**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     Before/after view of an enhanced bullet point                |
+------------------------------------------------------------------+
```
*Description:* A weak bullet (e.g., "Was responsible for the deploy pipeline") rewritten into a strong, action-verb-led statement with a quantification hint.

---

**Figure 7.8 — AI Summary Generator**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     Generated three-sentence professional summary                |
+------------------------------------------------------------------+
```
*Description:* The automatically generated professional summary derived from the user's experience, skills and detected industry.

---

**Figure 7.9 — ATS Score Report**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     Overall score, grade, six-dimension breakdown, suggestions   |
+------------------------------------------------------------------+
```
*Description:* The ATS analysis screen showing the overall score out of 100, the letter grade, the per-dimension breakdown and the prioritised list of improvement suggestions.

---

**Figure 7.10 — Job Description Match**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     Match score with matched/missing skills and recommendations  |
+------------------------------------------------------------------+
```
*Description:* The job-match screen where a pasted job description yields a blended match score together with matched keywords, the skill gap and tailoring recommendations.

---

**Figure 7.11 — Cover Letter Generator**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     Generated cover letter for a target company / role           |
+------------------------------------------------------------------+
```
*Description:* A tailored cover letter generated from the resume and job description, with an option to export it as a PDF.

---

**Figure 7.12 — Template Selection**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     Modern / Classic / Minimal / Creative template chooser       |
+------------------------------------------------------------------+
```
*Description:* The template gallery offering four ATS-friendly single-column designs, each suited to a different industry.

---

**Figure 7.13 — Resume Import / Parse**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     File upload dialog and parsed-data preview                   |
+------------------------------------------------------------------+
```
*Description:* The import feature where an uploaded PDF/DOCX/TXT/MD file is parsed into the structured editor.

---

**Figure 7.14 — Exported PDF (Modern Template)**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     Rendered single-column PDF resume                            |
+------------------------------------------------------------------+
```
*Description:* The final exported PDF demonstrating the Modern template's coloured header banner and clean single-column layout.

---

**Figure 7.15 — Public Shared Resume**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     Read-only public view at /share/{token}                      |
+------------------------------------------------------------------+
```
*Description:* The read-only public view of a shared resume, accessible without login, with its view count incremented on each visit.

---

**Figure 7.16 — Profile & Settings**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     Profile tab: name, avatar colour, change password            |
+------------------------------------------------------------------+
```
*Description:* The profile management screen for updating display name and avatar colour and changing the account password.

---

**Figure 7.17 — Admin Dashboard (Overview)**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     Stat cards + user-growth chart                               |
+------------------------------------------------------------------+
```
*Description:* The administrator overview showing total users, resumes, logins and today's signups, along with a user-growth chart.

---

**Figure 7.18 — Admin User Management & Activity Log**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     User table (ban/promote/delete) + activity audit log         |
+------------------------------------------------------------------+
```
*Description:* The administrator user-management table with ban/unban, promote/demote and delete controls, alongside the chronological activity audit log.

---

**Figure 7.19 — Interactive API Documentation (Swagger UI)**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     Auto-generated OpenAPI docs at /docs                          |
+------------------------------------------------------------------+
```
*Description:* FastAPI's automatically generated interactive documentation listing and allowing testing of every endpoint.

---

**Figure 7.20 — Dark Mode**

```
+------------------------------------------------------------------+
|                       [ Insert Screenshot ]                      |
|     The workspace rendered in dark theme                         |
+------------------------------------------------------------------+
```
*Description:* The application's native dark theme, toggled and persisted through the API client.

---PAGE BREAK---


# CHAPTER 8
# ALGORITHM / PSEUDOCODE

This chapter presents the algorithms and pseudocode for the principal operations of Resumate Pro. The pseudocode reflects the logic actually implemented in the source code while remaining language-neutral and easy to follow.

## 8.1 Algorithm: User Signup (Registration)

```
ALGORITHM Register(email, name, password)
BEGIN
    email <- normalise_lowercase_trim(email)
    IF user_exists(email) THEN
        RETURN error(409, "An account with this email already exists")
    END IF
    IF length(password) < 6 THEN
        RETURN error(422, "Password too short")     // enforced by schema
    END IF
    hash <- bcrypt_hash(truncate_72_bytes(password), rounds = 12)
    user <- create_user(email, name OR derive_from_email(email), hash)
    user.last_login  <- now()
    user.login_count <- 1
    write_activity_log(user, action = "register", ip = client_ip)
    commit()
    token <- create_jwt(subject = user.id, expiry = now + JWT_EXPIRE_HOURS)
    RETURN { access_token: token, user: sanitise(user) }   // status 201
END
```

## 8.2 Algorithm: User Login

```
ALGORITHM Login(email, password)
BEGIN
    user <- find_user_by_email(lowercase_trim(email))
    IF user IS NULL OR NOT bcrypt_verify(password, user.password_hash) THEN
        RETURN error(401, "Invalid email or password")
    END IF
    IF NOT user.is_active THEN
        RETURN error(403, "Account is disabled")
    END IF
    user.last_login  <- now()
    user.login_count <- user.login_count + 1
    write_activity_log(user, action = "login", ip = client_ip)
    commit()
    token <- create_jwt(subject = user.id)
    RETURN { access_token: token, user: sanitise(user) }   // status 200
END
```

## 8.3 Algorithm: Token Authentication (Request Guard)

```
ALGORITHM GetCurrentUser(authorization_header)
BEGIN
    IF header missing OR scheme != "bearer" THEN
        RETURN error(401, "Not authenticated")
    END IF
    payload <- jwt_decode(token, JWT_SECRET, algorithm = HS256)
    IF payload IS NULL THEN
        RETURN error(401, "Invalid or expired token")
    END IF
    user_id <- to_int(payload.sub)
    user <- db_get(User, user_id)
    IF user IS NULL OR NOT user.is_active THEN
        RETURN error(401, "User not found")
    END IF
    RETURN user
END

ALGORITHM GetAdminUser(user)              // builds on GetCurrentUser
BEGIN
    IF NOT user.is_admin THEN
        RETURN error(403, "Admin access required")
    END IF
    RETURN user
END
```

## 8.4 Algorithm: Resume Creation

```
ALGORITHM CreateResume(user, payload)
BEGIN
    data     <- payload.data IF payload.data NOT empty ELSE empty_resume_schema()
    resume   <- new Resume(
                    user_id  = user.id,
                    title    = payload.title OR "Untitled Resume",
                    template = payload.template OR "modern",
                    data     = data,
                    share_token = random_url_safe_token() )
    db_add(resume)
    write_activity_log(user, "resume_created", detail = resume.title)
    commit()
    RETURN sanitise(resume)                // status 201
END
```

## 8.5 Algorithm: Save / Update Resume (Auto-save)

```
ALGORITHM UpdateResume(user, resume_id, payload)
BEGIN
    resume <- db_get(Resume, resume_id)
    IF resume IS NULL OR resume.user_id != user.id THEN
        RETURN error(404, "Resume not found")     // ownership guard
    END IF
    IF payload.title    PRESENT THEN resume.title    <- payload.title OR "Untitled Resume"
    IF payload.template PRESENT THEN resume.template <- payload.template
    IF payload.data     PRESENT THEN resume.data     <- payload.data
    IF payload.is_public PRESENT THEN resume.is_public <- payload.is_public
    IF payload.ats_score PRESENT THEN resume.ats_score <- payload.ats_score
    resume.updated_at <- now()
    write_activity_log(user, "resume_updated", detail = resume.title)
    commit()
    RETURN sanitise(resume)
END

// Front-end auto-save trigger
ON user_stops_typing FOR 1.5 seconds:
    show_indicator("Saving...")
    UpdateResume(current_user, current_resume_id, changed_fields)
    show_indicator("Saved")
```

## 8.6 Algorithm: AI Bullet Enhancement (Dual Mode)

```
ALGORITHM EnhanceBullet(bullet, role_hint)
BEGIN
    IF bullet is empty THEN RETURN bullet

    IF OPENAI_API_KEY is set THEN
        prompt <- build_rewrite_prompt(bullet, role_hint)   // forbids inventing facts
        result <- openai_chat(prompt)
        IF result is not empty THEN
            RETURN clean(result)
        END IF
    END IF

    // ---- Deterministic local fallback ----
    text          <- trim_and_strip_trailing_period(bullet)
    (body, weak)  <- strip_weak_prefix(text)         // e.g. removes "responsible for"
    IF weak recognised THEN
        category <- WEAK_TO_CATEGORY[weak]
    ELSE
        category <- infer_category(body + role_hint) // keyword-rule scoring
    END IF
    seed   <- char_sum(body[0..40])
    verb   <- pick_verb(category, seed)              // deterministic choice
    result <- verb + " " + lowercase_first(body)
    IF result has no number THEN
        result <- result + quantification_hint(seed) // prompt to add a metric
    END IF
    RETURN ensure_terminal_punctuation(result)
END
```

## 8.7 Algorithm: AI Summary Generation

```
ALGORITHM GenerateSummary(resume)
BEGIN
    IF OPENAI_API_KEY is set THEN
        out <- openai_chat(summary_prompt(resume))   // <= 60 words, no fabrication
        IF out not empty THEN RETURN out
    END IF

    // Local fallback
    title      <- resume.personal.title OR "Professional"
    years      <- estimate_years(resume.experience)  // from year ranges
    skills     <- first_5(resume.skills)
    industry   <- detect_industry(all_text(resume))
    company    <- resume.experience[0].company OR "leading organizations"
    line1 <- title + " with " + years_phrase(years) + " delivering impact in " + industry
    line2 <- "Proven track record at " + company + ", with expertise in " + skills
    line3 <- "Known for translating complex problems into measurable outcomes ..."
    RETURN line1 + " " + line2 + " " + line3
END
```

## 8.8 Algorithm: ATS Scoring

```
ALGORITHM AnalyzeATS(resume)
BEGIN
    (c_score, c_issues) <- score_contact(resume)        // max 15
    (s_score, s_issues) <- score_sections(resume)       // max 15
    (k_score, k_issues, meta) <- score_keywords(resume) // max 20
    (v_score, v_issues) <- score_action_verbs(resume)   // max 15
    (q_score, q_issues) <- score_quantification(resume) // max 15
    (f_score, f_issues) <- score_formatting(resume)     // max 20

    overall <- c_score + s_score + k_score + v_score + q_score + f_score
    grade   <- assign_grade(overall)                    // A+ .. F
    suggestions <- concat(all issue lists)[0..12]
    RETURN { overall, grade, breakdown, suggestions, industry: meta.industry }
END

FUNCTION score_action_verbs(resume)
    bullets <- flatten_bullets(experience + projects)
    strong  <- count(bullets where first_word in ACTION_VERBS)
    weak    <- count(bullets where starts_with any WEAK_PHRASE)
    ratio   <- max(0, strong/total - 0.5 * weak/total)
    RETURN min(ratio * 1.2, 1.0) * 15
```

## 8.9 Algorithm: Job-Description Matching

```
ALGORITHM Match(resume, job_description)
BEGIN
    IF job_description empty THEN RETURN zero_match_report

    resume_text  <- flatten_to_text(resume)
    cosine       <- tfidf_cosine(resume_text, job_description)   // sklearn or local

    jd_skills      <- extract_known_skills(job_description)
    matched_skills <- jd_skills present in resume
    missing_skills <- jd_skills - matched_skills
    skill_cov      <- |matched_skills| / |jd_skills|

    top_terms <- tfidf_top_k(job_description, k = 20)
    matched_kw, missing_kw <- classify(top_terms by presence in resume_text)
    keyword_cov <- |matched_kw| / |top_terms|

    score <- (cosine*0.3 + keyword_cov*0.4 + skill_cov*0.3) * 100
    score <- min(round(score,1), 100)
    RETURN { match_score: score, cosine, keyword_cov, skill_cov,
             matched_keywords, missing_keywords, skill_gap: missing_skills,
             recommendations: build_recommendations(score, missing_skills, missing_kw) }
END
```

## 8.10 Algorithm: Resume File Parsing (Import)

```
ALGORITHM ParseResume(file_bytes, filename)
BEGIN
    ext <- lower(extension(filename))
    IF ext NOT IN {.pdf,.docx,.txt,.md} THEN RETURN error(400)
    IF size(file_bytes) > 5MB THEN RETURN error(413)

    text     <- extract_text(file_bytes, ext)     // PyPDF2 / python-docx / decode
    sections <- split_by_heading_aliases(text)    // summary/experience/education/...
    resume   <- empty_resume_schema()
    resume.personal       <- extract_personal(sections.header, text)  // regex
    resume.summary        <- sections.summary
    resume.experience     <- extract_experience(sections.experience)
    resume.education       <- extract_education(sections.education)
    resume.skills         <- extract_skills(sections.skills OR text)
    resume.projects/certs/languages/awards <- extract_simple_lists(...)
    RETURN resume (without raw text)
END
```

## 8.11 Algorithm: PDF Export (Download)

```
ALGORITHM ExportPDF(user, resume_id)
BEGIN
    resume <- db_get(Resume, resume_id)
    IF resume IS NULL OR resume.user_id != user.id THEN RETURN error(404)
    template <- get_template(resume.template)
    flowables <- []
    flowables += build_header(resume.personal, template)   // banner/sidebar/minimal/underline
    flowables += build_summary(resume.summary)
    flowables += build_experience(resume.experience)
    flowables += build_projects(resume.projects)
    flowables += build_education(resume.education)
    flowables += build_skills(resume.skills)
    flowables += build_sections(certifications, awards, languages)
    pdf_bytes <- reportlab_build(flowables, page = LETTER)
    RETURN pdf_response(pdf_bytes, filename = safe(resume.title) + ".pdf")
END
```

## 8.12 Algorithm: Profile Update and Password Change

```
ALGORITHM UpdateProfile(user, payload)
BEGIN
    IF payload.name PRESENT         THEN user.name <- payload.name OR user.name
    IF payload.avatar_color PRESENT THEN user.avatar_color <- payload.avatar_color
    commit()
    RETURN sanitise(user)
END

ALGORITHM ChangePassword(user, current_password, new_password)
BEGIN
    IF NOT bcrypt_verify(current_password, user.password_hash) THEN
        RETURN error(400, "Current password is incorrect")
    END IF
    user.password_hash <- bcrypt_hash(new_password)
    write_activity_log(user, "password_changed")
    commit()
    RETURN { message: "Password updated successfully" }
END
```

## 8.13 Algorithm: Generic Authenticated API Call (Client)

```
ALGORITHM ApiRequest(path, method, body)
BEGIN
    headers <- {}
    token   <- localStorage.get("arb_token")
    IF token THEN headers.Authorization <- "Bearer " + token
    IF body is FormData THEN attach as multipart
    ELSE headers["Content-Type"] <- "application/json"; body <- json(body)
    response <- fetch(path, method, headers, body)
    IF response.status == 401 THEN
        clear_auth(); redirect("/login"); THROW Unauthorized
    END IF
    IF NOT response.ok THEN THROW error(response.detail)
    IF response.status == 204 THEN RETURN null
    RETURN parse(response)        // json or text
END
```

## 8.14 Algorithm: Database Operations (ORM Session Lifecycle)

```
ALGORITHM WithDbSession(operation)            // FastAPI dependency get_db()
BEGIN
    session <- SessionLocal()                 // request-scoped
    TRY
        result <- operation(session)
        session.commit()                      // persist changes
        RETURN result
    EXCEPT error
        session.rollback()                    // atomicity preserved
        RAISE error
    FINALLY
        session.close()                       // always release the connection
    END
END

// Application startup
ALGORITHM InitDatabase()
BEGIN
    import all ORM models                      // register on metadata
    Base.metadata.create_all(engine)           // create tables if absent
    first <- query(User) ordered by id, first  // promote first user to admin
    IF first EXISTS AND NOT first.is_admin THEN first.is_admin <- true; commit()
END
```

---PAGE BREAK---


# CHAPTER 9
# TESTING AND IMPLEMENTATION

Testing is the process of evaluating a system to verify that it satisfies its specified requirements and to detect defects. This chapter describes the testing strategy applied to Resumate Pro, the categories of testing performed, representative test cases with expected and actual outcomes, the defects identified and resolved, and the implementation and deployment processes.

## 9.1 Testing Approach

Resumate Pro was tested using a combination of automated and manual techniques. The centrepiece of automated verification is `smoke_test.py`, an end-to-end test harness that boots the FastAPI application in-process using FastAPI's `TestClient` and exercises every public endpoint against an isolated, temporary SQLite database. This guarantees that the real application code paths — routing, validation, authentication, the core engines and the database — are tested together exactly as they run in production, without affecting the live database. Manual testing through the browser and the interactive `/docs` interface complemented the automated suite for user-experience verification.

## 9.2 Types of Testing

### 9.2.1 Unit Testing

Unit testing verifies individual functions in isolation. The deterministic nature of the local engines makes them highly unit-testable. For example, the bullet enhancer is verified to remove weak openers (an enhanced bullet must not begin with "was responsible"), the ATS analyser is verified to return an overall score within the valid 0–100 range, and the matcher is verified to return a bounded match score. The skills database is checked to contain more than fifty recognised skills.

### 9.2.2 Integration Testing

Integration testing verifies that modules cooperate correctly. The smoke test performs true integration testing: it registers a user, logs in, creates and updates a resume, runs AI enhancement, generates a summary and cover letter, computes the ATS score, matches against a job description, exports a PDF, parses an uploaded file and toggles public sharing — confirming that the routing, authentication, engine and persistence layers work together end-to-end.

### 9.2.3 System Testing

System testing evaluates the complete, integrated application against its requirements. The whole workflow — from registration through editing, optimisation and export — was executed both automatically and through the browser, including the administrative panel and the public share page, to confirm the system behaves as a coherent whole.

### 9.2.4 Acceptance Testing

Acceptance testing confirms the system meets user expectations. The end-to-end scenario in the smoke test mirrors a realistic user journey and asserts business-meaningful outcomes (for example, that a shared resume is readable without authentication when public and returns `404` when private, and that the exported file genuinely begins with the `%PDF` signature).

### 9.2.5 Performance Testing

Performance testing assessed response times for the principal operations. The TF-IDF matching and ReportLab PDF rendering both complete within sub-second timeframes for typical single-page resumes on commodity hardware, and the stateless JWT design avoids any session-store bottleneck.

### 9.2.6 Security Testing

Security testing verified that passwords are stored only as bcrypt hashes, that protected endpoints reject requests lacking a valid token (`401`), that admin endpoints reject non-admins (`403`), that resume operations enforce ownership (a user cannot access another user's resume — returns `404`), that the public share endpoint blocks private resumes, and that an administrator cannot remove their own privileges or delete their own account through the admin panel.

## 9.3 Test Cases

The following tables present representative test cases, each derived from the actual end-to-end checks performed.

**Table 9.1 — Authentication Test Cases**

| TC | Test Case | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| TC-01 | Register new user | Valid email, name, password | 201 + access token | 201 + token | Pass |
| TC-02 | Register duplicate email | Existing email | 409 Conflict | 409 Conflict | Pass |
| TC-03 | Register weak password | Password < 6 chars | 422 Validation error | 422 | Pass |
| TC-04 | Login valid credentials | Correct email/password | 200 + token | 200 + token | Pass |
| TC-05 | Login wrong password | Incorrect password | 401 Unauthorised | 401 | Pass |
| TC-06 | Access /me with token | Valid bearer token | 200 + user matches email | 200 + match | Pass |
| TC-07 | Access protected route without token | No Authorization header | 401 Unauthorised | 401 | Pass |

**Table 9.2 — Resume Management Test Cases**

| TC | Test Case | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| TC-08 | Create resume | Title, template, data | 201 + resume id | 201 + id | Pass |
| TC-09 | List resumes | Authenticated user | 200 + exactly 1 resume | 200 + 1 | Pass |
| TC-10 | Update (rename) resume | New title | 200 + updated title | 200 + match | Pass |
| TC-11 | Duplicate resume | Resume id | 201 + new id | 201 + id | Pass |
| TC-12 | Delete resume | Resume id | 204 No Content | 204 | Pass |
| TC-13 | Access another user's resume | Foreign resume id | 404 Not Found | 404 | Pass |

**Table 9.3 — AI Feature Test Cases**

| TC | Test Case | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| TC-14 | Enhance weak bullet | "Was responsible for the deploy pipeline" | Non-empty; not starting with "was responsible" | Strong rewrite | Pass |
| TC-15 | Generate summary | Resume dict | Non-empty summary | 3-sentence summary | Pass |
| TC-16 | Generate cover letter | Resume + JD + company | Letter containing company name | Contains "Acme" | Pass |
| TC-17 | Suggest skills | Resume dict | List of suggestions | List returned | Pass |
| TC-18 | Skills DB list | — | > 50 skills | > 50 skills | Pass |
| TC-19 | Chat assistant | "How do I improve my ATS score?" | Non-empty advice reply | Advice returned | Pass |

**Table 9.4 — Analysis Test Cases**

| TC | Test Case | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| TC-20 | ATS score | Resume dict | overall in [0,100] + grade | Valid score + grade | Pass |
| TC-21 | Job match | Resume + JD | match_score in [0,100] | Valid score | Pass |

**Table 9.5 — Export, Parse and Share Test Cases**

| TC | Test Case | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| TC-22 | Export resume PDF | Resume id | 200 + bytes starting with %PDF | %PDF bytes | Pass |
| TC-23 | Export cover-letter PDF | Cover text | 200 + %PDF | %PDF bytes | Pass |
| TC-24 | Parse uploaded file | demo.txt with skills | 200 + "Python" in skills | Skills parsed | Pass |
| TC-25 | Make resume public | is_public = true | 200 + is_public true | is_public true | Pass |
| TC-26 | Read shared resume (no auth) | Share token (public) | 200 + correct title | 200 + match | Pass |
| TC-27 | Read shared resume when private | Share token (private) | 404 Not Found | 404 | Pass |

**Table 9.6 — Administration & Health Test Cases**

| TC | Test Case | Input | Expected Output | Actual Output | Status |
|---|---|---|---|---|---|
| TC-28 | First user is admin | First registration | is_admin = true | true | Pass |
| TC-29 | Admin stats | Admin token | Totals object | Stats returned | Pass |
| TC-30 | Non-admin admin access | User token | 403 Forbidden | 403 | Pass |
| TC-31 | Health check | — | 200 + status "ok" | "ok" | Pass |
| TC-32 | Frontend served | GET / | 200 + "ResuMate" in body | Served | Pass |

The complete automated smoke test reports **all checks passing**, confirming the integrated correctness of the application.

## 9.4 Bug Fixes

Several defects were identified and resolved during development:

1. **bcrypt / passlib incompatibility.** The well-known issue where `passlib` reads `bcrypt.__about__` (removed in bcrypt 4.x) was eliminated by calling the `bcrypt` library directly instead of through `passlib`, as documented in `backend/auth.py`.
2. **bcrypt 72-byte limit.** Passwords longer than 72 bytes caused bcrypt to raise an error; this was fixed by safely truncating the input at the byte level before hashing and verifying.
3. **SQLite cross-thread access.** SQLite raised threading errors under FastAPI's worker model; this was resolved by configuring the engine with `check_same_thread=False` for SQLite connections only.
4. **scikit-learn optional dependency.** To prevent matching from failing if scikit-learn is unavailable, a pure-Python TF-IDF cosine fallback was implemented in the matcher.
5. **PDF markup injection.** User text containing `&`, `<` or `>` could corrupt ReportLab paragraphs; all text is now HTML-escaped before rendering.
6. **Weak-prefix capitalisation.** After stripping a weak opener and prepending a strong verb, the remaining clause is correctly re-cased to read naturally.

## 9.5 Implementation Process

Implementation proceeded incrementally and in a layered order so that each layer could be verified before the next was built:

1. **Database and models** were defined first (`User`, `Resume`, `ActivityLog`), establishing the data foundation.
2. **Authentication** (hashing, JWT, dependencies) was implemented and tested next, since every other feature depends on it.
3. **Resume CRUD** was added, followed by the **core engines** (AI, ATS, matcher, parser, PDF) which were developed and validated independently against the structured resume schema.
4. **API routers** were wired to the engines, and the **front end** was built against the resulting REST API.
5. The **admin module** and **enhancements** (auto-save, profile, activity logging, sharing) were layered on last.
6. Throughout, the **smoke test** was extended to cover each new endpoint, ensuring no regression as the system grew.

## 9.6 Deployment Process

The deployment process for a production environment is as follows:

1. **Provision** a Linux virtual machine and install Python 3.10+.
2. **Clone** the repository and install dependencies with `pip install -r requirements.txt`.
3. **Configure** environment variables — set a strong `JWT_SECRET`, a PostgreSQL `DATABASE_URL`, a restricted `ALLOWED_ORIGINS`, and optionally `OPENAI_API_KEY`.
4. **Launch** the application with Uvicorn (`uvicorn server:app --host 0.0.0.0 --port 8000`); the startup hook automatically creates the database tables and promotes the first user to administrator.
5. **Front** the server with an HTTPS-terminating reverse proxy (such as Nginx) and a process manager to keep it running.
6. **Verify** the deployment by calling `GET /api/health`, which reports status, version, AI-enablement and current user/resume counts.

Because the FastAPI application also serves the static front end, no separate web-server deployment is required, keeping the operational footprint minimal.

---PAGE BREAK---


# CHAPTER 10
# CONCLUSION

## 10.1 Project Summary

Resumate Pro – AI Powered Resume Builder is a complete, full-stack web application that reimagines resume creation as a data-driven, feedback-rich process rather than a purely visual exercise. By representing every resume as structured data, the system is able to analyse content objectively, rewrite weak phrasing intelligently, score machine-readability across six dimensions, and measure alignment against any job description. The application is delivered as a single, self-contained FastAPI server that exposes a documented REST API, serves a lightweight reactive front end, persists data through SQLAlchemy onto SQLite or PostgreSQL, and secures every operation with JWT authentication and bcrypt password hashing. A defining characteristic of the design is its dual-mode intelligence engine, which uses a large language model when one is configured but otherwise falls back to a fully self-contained, deterministic engine — guaranteeing that the product remains useful, free and private even without any external service. The system is rounded out by document export in four ATS-friendly templates, resume file import, public sharing with view tracking, and a comprehensive administrative back office.

## 10.2 Achievements

The project successfully met all of its stated objectives. The principal achievements are:

- A secure, stateless, token-authenticated API with full audit logging.
- A structured resume model enabling automated analysis and transformation.
- An intelligent, dual-mode content engine for bullet enhancement, summary and cover-letter generation, and skill suggestion.
- An explainable six-dimension ATS scoring system that drives an iterative optimisation loop.
- A TF-IDF-based job-description matcher with skill-gap analysis and actionable recommendations.
- Four ATS-safe PDF templates rendered from a single, escaping-safe generator.
- Tolerant resume import from PDF, DOCX, TXT and Markdown files.
- Public read-only sharing with view counting.
- A complete administrative module with statistics, growth data, user and resume management, and an activity audit trail.
- A comprehensive automated end-to-end smoke test confirming correctness across the entire stack.

## 10.3 Advantages

Resumate Pro offers clear advantages over conventional resume tools: it provides objective, explainable feedback rather than subjective guesswork; it guarantees ATS-readable output; it converts hours of manual writing and tailoring into minutes; it operates fully offline and without mandatory paywalls; and its layered, single-process architecture makes it inexpensive to deploy and easy to maintain and extend.

## 10.4 Limitations

The current implementation has a number of acknowledged limitations. The local fallback engine, while robust and deterministic, produces less nuanced prose than a large language model. The resume parser relies on heuristics and may require manual correction for unconventionally formatted source files. Real-time collaborative editing, email-based password recovery, payment handling and a native mobile client are outside the present scope. The default development database is file-based SQLite, which, although easily switched to PostgreSQL, is not itself suited to high-concurrency production use.

## 10.5 Future Enhancements

### 10.5.1 AI Improvements

Future work will deepen the language intelligence: section-by-section conversational rewriting, automatic tailoring of an entire resume to a pasted job description in a single action, tone and seniority controls, and an interview-question generator derived from the resume and target role. The chat assistant can be extended into a guided, stateful coaching experience.

### 10.5.2 Cloud Deployment

The system is well positioned for cloud-native deployment. Planned improvements include containerisation, a managed PostgreSQL database, object storage for uploaded files, horizontal scaling behind a load balancer (enabled by the stateless JWT design), and continuous-integration pipelines that run the smoke test on every change.

### 10.5.3 Mobile Application Version

Because all functionality is exposed through a clean REST API, a companion mobile application — native or as a progressive web app — can be built to consume the same backend without modification, offering on-the-go editing, scoring and sharing.

### 10.5.4 Additional Enhancements

Further directions include multi-language resume support and localisation, LinkedIn and external-profile import, personal analytics dashboards that track how a user's ATS score and match rate evolve over time, additional templates, and richer export formats. The deliberately layered architecture ensures these can be introduced with minimal disruption to existing functionality.

## 10.6 Concluding Remarks

Resumate Pro demonstrates how a thoughtfully layered architecture, structured data modelling, and a pragmatic dual-mode intelligence strategy can combine to solve a genuine, widely felt problem. It is a complete, tested and deployable system that not only fulfils its academic requirements but also stands as a practical tool capable of measurably improving a job seeker's prospects. The project provided substantial experience across the full software-development lifecycle — analysis, design, implementation, testing and deployment — and across a modern technology stack spanning web development, databases, machine learning and document processing.

---PAGE BREAK---

# REFERENCES

The following sources, presented in APA citation style, were consulted during the design, development and documentation of this project. Online documentation was last accessed in June 2026.

### Books

1. Sommerville, I. (2016). *Software engineering* (10th ed.). Pearson Education.
2. Pressman, R. S., & Maxim, B. R. (2020). *Software engineering: A practitioner's approach* (9th ed.). McGraw-Hill Education.
3. Lutz, M. (2013). *Learning Python* (5th ed.). O'Reilly Media.
4. Percival, H., & Gregory, B. (2020). *Architecture patterns with Python: Enabling test-driven development, domain-driven design, and event-driven microservices*. O'Reilly Media.
5. Géron, A. (2019). *Hands-on machine learning with Scikit-Learn, Keras, and TensorFlow* (2nd ed.). O'Reilly Media.
6. Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.

### Research Papers

7. Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval. *Information Processing & Management, 24*(5), 513–523.
8. Provost, F., & Fawcett, T. (2013). Data science and its relationship to big data and data-driven decision making. *Big Data, 1*(1), 51–59.
9. Jones, K. S. (1972). A statistical interpretation of term specificity and its application in retrieval. *Journal of Documentation, 28*(1), 11–21.

### Official Documentation

10. FastAPI. (2026). *FastAPI documentation*. https://fastapi.tiangolo.com/
11. SQLAlchemy. (2026). *SQLAlchemy 2.0 documentation*. https://docs.sqlalchemy.org/
12. Pydantic. (2026). *Pydantic documentation*. https://docs.pydantic.dev/
13. Uvicorn. (2026). *Uvicorn documentation*. https://www.uvicorn.org/
14. scikit-learn developers. (2026). *scikit-learn user guide*. https://scikit-learn.org/stable/
15. ReportLab. (2026). *ReportLab user guide*. https://docs.reportlab.com/
16. SQLite. (2026). *SQLite documentation*. https://www.sqlite.org/docs.html
17. PostgreSQL Global Development Group. (2026). *PostgreSQL documentation*. https://www.postgresql.org/docs/
18. OpenAI. (2026). *OpenAI API reference*. https://platform.openai.com/docs/
19. Alpine.js. (2026). *Alpine.js documentation*. https://alpinejs.dev/
20. Tailwind CSS. (2026). *Tailwind CSS documentation*. https://tailwindcss.com/docs

### Standards and Specifications

21. Internet Engineering Task Force. (2015). *RFC 7519: JSON Web Token (JWT)*. https://datatracker.ietf.org/doc/html/rfc7519
22. Mozilla. (2026). *MDN Web Docs — HTTP, HTML and JavaScript references*. https://developer.mozilla.org/

### Online Communities and Repositories

23. Stack Overflow. (2026). *Developer Q&A community*. https://stackoverflow.com/
24. GitHub. (2026). *Resumate Pro project repository*. https://github.com/jumanalnagesh80-pixel/resumate-pro
25. Python Software Foundation. (2026). *The Python language reference*. https://docs.python.org/3/

---PAGE BREAK---

# APPENDIX

## Appendix A — Empty Resume Data Schema

Every resume in Resumate Pro conforms to the following structured JSON shape, which is the contract shared between the editor, the engines and the PDF generator:

```json
{
  "personal": {
    "name": "", "title": "", "email": "", "phone": "",
    "location": "", "linkedin": "", "github": "", "website": ""
  },
  "summary": "",
  "experience": [
    { "role": "", "company": "", "start": "", "end": "",
      "location": "", "bullets": [] }
  ],
  "education": [
    { "school": "", "degree": "", "field": "", "start": "",
      "end": "", "gpa": "", "details": "" }
  ],
  "projects": [
    { "name": "", "description": "", "link": "", "tech": [], "bullets": [] }
  ],
  "skills": [],
  "certifications": [ { "name": "", "issuer": "", "year": "" } ],
  "languages": [ { "name": "", "level": "" } ],
  "awards": [ { "name": "", "year": "", "description": "" } ]
}
```

## Appendix B — Environment Configuration Template

```
JWT_SECRET=change-me-to-a-long-random-string-in-production
OPENAI_API_KEY=
# DATABASE_URL=postgresql+psycopg://user:pass@localhost/resumate
# ALLOWED_ORIGINS=https://yourdomain.com
# JWT_EXPIRE_HOURS=24
# PORT=8000
```

## Appendix C — Quick Start Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy and edit the environment file
cp .env.example .env          # set a strong JWT_SECRET

# 3. Start the server
uvicorn server:app --reload --port 8000     # or: python server.py

# 4. Open in a browser
#    Landing : http://localhost:8000/
#    App     : http://localhost:8000/app
#    Admin   : http://localhost:8000/admin
#    API docs: http://localhost:8000/docs

# 5. Run the end-to-end smoke test
python smoke_test.py
```

## Appendix D — ATS Scoring Reference

| Grade | Score Range | Interpretation |
|---|---|---|
| A+ | 90–100 | Excellent |
| A | 80–89 | Strong |
| B | 70–79 | Good, with room to improve |
| C | 60–69 | Needs work |
| D | 45–59 | Weak |
| F | 0–44 | Major rework required |

## Appendix E — Action-Verb Categories (Local Engine)

The deterministic engine selects strong verbs from ten impact categories — *leadership, achievement, improvement, creation, analysis, communication, management, collaboration, growth* and *reduction* — and detects weak openers such as *responsible for, helped, worked on, duties included, assisted, supported, handled* and *involved in*, mapping each to an appropriate strong-verb category for rewriting.

## Appendix F — Supported Industries (Keyword Detection)

The keyword engine recognises and scores seven industry profiles: *software engineering, data science, product management, marketing, finance, design* and *sales*, each backed by a curated keyword set used in both ATS scoring and content suggestions.

<!-- END OF REPORT -->
