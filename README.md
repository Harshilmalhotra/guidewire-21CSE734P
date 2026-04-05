# Unified Multimodal Claims Decision Engine (UCDE)

## Project Overview

This project implements a **Unified Claims Decision Engine (UCDE)** designed to sit on top of traditional insurance systems (e.g., Guidewire ClaimCenter) and **optimize claim decisions using multimodal AI signals**.

Unlike existing InsurTech solutions that operate as **isolated AI components**, this system introduces a **centralized decision intelligence layer** that:

* Fuses outputs from multiple AI models (NLP, CV, Fraud)
* Resolves conflicting signals
* Produces a **single optimized decision**
* Generates **explainable reasoning**
* Learns continuously from human feedback

---

## Core Problem

Current insurance AI systems are:

* Fragmented (multiple vendors, no unified reasoning)
* Locally optimized (each model solves a narrow task)
* Lacking global decision intelligence
* Weak in handling conflicting signals

### Example Failure Case

| Signal       | Output       |
| ------------ | ------------ |
| CV Model     | Minor damage |
| Fraud Model  | High risk    |
| Triage Model | Low severity |

**Current systems:**

* Pass outputs downstream
* Rely on manual intervention

**UCDE:**

* Detects contradiction
* Resolves conflict
* Produces a **justified decision**

---

## System Objectives

* Minimize claim processing cost
* Reduce fraud leakage
* Improve claim turnaround time
* Maintain explainability (regulatory requirement)
* Enable system-level optimization

---

## Key Features

### 1. Multimodal Feature Fusion

* Combines:

  * Text (claim description)
  * Image (damage evidence)
  * Structured data (policy, history)
* Produces unified feature representation

---

### 2. Decision Engine (Core)

* Multi-objective decision system:

  * Fraud risk
  * Severity
  * Claim value
  * Historical behavior

* Outputs:

  * Action (approve / escalate / investigate)
  * Confidence score
  * Decision rationale

---

### 3. Conflict Detection Engine

Detects inconsistencies such as:

* Low visual damage vs high claim amount
* Description vs image mismatch

Flags:

* `CONFLICT_DETECTED`

---

### 4. GenAI Reasoning Layer

* Uses LLM for:

  * Decision justification
  * Context-aware reasoning
  * Natural language explanations

---

### 5. Explainability Layer

Provides:

* Reason codes
* Feature importance
* Decision trace

---

### 6. Feedback Loop (Learning System)

* Captures:

  * Model decision
  * Human override
* Enables:

  * Threshold tuning
  * Model retraining

---

### 7. Guidewire-Compatible Integration Layer

* Simulates:

  * Claim creation
  * Status updates
* Designed to integrate with enterprise systems

---

## System Architecture

```
[Frontend (FNOL UI)]
        |
        v
[API Gateway]
        |
        v
[Ingestion Service]
        |
        v
[Feature Extraction Layer]
  ├── NLP Service
  ├── CV Service
  ├── Fraud Model Service
        |
        v
[Feature Store]
        |
        v
[Decision Engine]
  ├── Rule Layer
  ├── Optimization Layer
  ├── LLM Reasoning Layer
        |
        v
[Decision API]
        |
        v
[Integration Layer (Claim System)]
        |
        v
[Feedback Loop]
```

---

## Tech Stack

### Backend

* FastAPI (Python)

### ML / AI

* NLP: DistilBERT / HuggingFace
* CV: YOLOv8 (or mocked service)
* Fraud Model: XGBoost / LightGBM

### GenAI

* Gemini

### Data Layer

* PostgreSQL (structured data)
* Redis (feature store)

### Messaging (Optional but recommended)

* Kafka (event-driven pipeline)

### Frontend

* React / Next.js

### Infra

* Docker
* Kubernetes (optional for scaling)

---

## API Design (Sample)

### POST /fnol

```
{
  "policyId": "P123",
  "description": "Rear-end collision",
  "images": ["base64"],
  "location": "Chennai"
}
```

### Response

```
{
  "claimId": "C001",
  "decision": "INVESTIGATE",
  "confidence": 0.82,
  "reason": [
    "High fraud probability",
    "Damage inconsistent with claim value"
  ]
}
```

---

## Components Breakdown

### 1. Ingestion Service

* Handles FNOL input
* Validates payload

---

### 2. NLP Service

* Extracts:

  * Incident type
  * Severity hints

---

### 3. CV Service

* Detects:

  * Damage severity
* Can be mocked initially

---

### 4. Fraud Service

* Predicts fraud probability
* Based on structured features

---

### 5. Feature Store

* Aggregates all signals
* Ensures low-latency access

---

### 6. Decision Engine (MOST IMPORTANT)

Sub-components:

* Rule-based logic
* Scoring function
* Conflict detection
* LLM reasoning

---

### 7. Explainability Engine

* Converts outputs into:

  * Human-readable reasoning
  * Audit logs

---

### 8. Integration Layer

* Simulates external system (e.g., claims platform)

---

### 9. Feedback Module

* Captures post-decision outcomes
* Enables iterative improvement

---

## What Makes This Project Non-Trivial

* Not just ML → **Decision system**
* Not just APIs → **Architecture design**
* Not just outputs → **Explainable reasoning**
* Not just static → **Feedback-driven learning**

---

# Phase-Wise Build Plan (STRICT EXECUTION)

## ⚠️ RULE: DO NOT SKIP PHASES

Each phase must:

* Work independently
* Be testable
* Be committed before moving forward

---

## Phase 1 — Project Setup & Data Simulation

### Goals

* Set up repo
* Create synthetic dataset
* Define schemas

### Tasks

* Create project structure
* Define claim JSON schema
* Generate 1000+ synthetic claims
* Store in PostgreSQL

### Output

* Working data layer

---

## Phase 2 — Individual Model Services

### Goals

* Build independent AI services

### Tasks

* NLP API (text → structured output)
* CV API (mock or real)
* Fraud model training + API

### Output

* 3 working microservices

---

## Phase 3 — Feature Fusion Layer

### Goals

* Combine all signals

### Tasks

* Create feature aggregation service
* Normalize outputs
* Store in Redis/Postgres

### Output

* Unified feature vector per claim

---

## Phase 4 — Decision Engine (CORE)

### Goals

* Implement decision logic

### Tasks

* Rule-based engine
* Scoring function
* Conflict detection
* Threshold tuning

### Output

* Deterministic decision system

---

## Phase 5 — GenAI Integration

### Goals

* Add reasoning capability

### Tasks

* Design LLM prompts
* Feed structured features
* Generate:

  * Decision explanation
  * Conflict reasoning

### Output

* Human-like reasoning layer

---

## Phase 6 — API Layer + Integration

### Goals

* End-to-end flow

### Tasks

* Build `/fnol` endpoint
* Connect all services
* Simulate claim system integration

### Output

* Full pipeline working

---

## Phase 7 — Frontend Demo

### Goals

* Visualize system

### Tasks

* FNOL submission UI
* Show:

  * Model outputs
  * Final decision
  * Explanation

### Output

* Demo-ready UI

---

## Phase 8 — Feedback Loop

### Goals

* Enable learning

### Tasks

* Capture human override
* Store feedback
* Adjust thresholds or retrain model

### Output

* Closed-loop system

---

## Phase 9 — Optimization & Polish

### Goals

* Improve system quality

### Tasks

* Add logging
* Add metrics
* Improve latency
* Refactor code

---

# How to Build This Correctly (Critical Guidance)

## 1. Build Vertically, Not Horizontally

Wrong:

* Build all services partially

Correct:

* Complete one pipeline end-to-end first

---

## 2. Keep ML Simple

Focus on:

* System design
* Decision logic

NOT:

* Model accuracy

---

## 3. Treat Decision Engine as Product Core

Spend most time on:

* Conflict handling
* Multi-objective scoring
* Explainability

---

## 4. Add GenAI Late

Do NOT start with LLMs.

Add only after:

* Structured system works

---

## 5. Test Each Phase Independently

Before moving on:

* Validate outputs
* Log everything
* Ensure determinism

---

## 6. Demonstration Strategy

Final demo must show:

1. Input claim
2. Individual model outputs
3. Conflict detection
4. Final decision
5. Explanation
6. Integration output

---

# Final Positioning

This is NOT:

* A chatbot
* A simple ML pipeline
* A dashboard

This IS:

> A **decision intelligence system for insurance claims**, designed to address fragmentation in current AI ecosystems.

---

If executed correctly, this project demonstrates:

* Enterprise system design
* AI + architecture integration
* Understanding of insurance workflows
* Ability to solve real industry gaps

---
