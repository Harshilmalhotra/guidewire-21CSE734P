# Unified Multimodal Claims Decision Engine (UCDE++)

### *Graph-Driven, Reinforcement Learning Optimized, Agentic Decision Intelligence for Insurance*

---

## Project Overview

This project implements an advanced **Unified Claims Decision Engine (UCDE++)**, a next-generation decision intelligence layer designed to sit above systems like Guidewire ClaimCenter.

Unlike traditional InsurTech architectures that rely on **fragmented AI components**, UCDE++ introduces:

* **Graph-based claim representation**
* **Reinforcement learning-based decision optimization**
* **Agentic AI orchestration layer**
* **Multimodal reasoning across signals**
* **System-level objective optimization**

---

## Core Problem (Reframed)

Current systems (including Guidewire ecosystem):

* Aggregate AI outputs (fraud, triage, CV)
* Do NOT perform **joint reasoning**
* Do NOT optimize **global outcomes**
* Do NOT resolve **conflicting signals**

### Fundamental Gap

> No system exists that treats claim processing as a **sequential decision-making problem under uncertainty**

---

## Key Innovation Layers

---

### 1. Claim Knowledge Graph (NEW — CORE DIFFERENTIATOR)

Each claim is modeled as a **dynamic graph**:

```
Nodes:
- Claim
- Policyholder
- Vehicle
- Location
- Past Claims
- Related Entities

Edges:
- filed_by
- occurred_at
- linked_to
- historically_connected
```

### Why this matters:

* Enables **network-level fraud detection**
* Captures relational dependencies
* Supports graph-based reasoning

---

### 2. Graph Intelligence Layer

* Graph embeddings (Node2Vec / GraphSAGE)
* Detect:

  * Fraud rings
  * Suspicious connections
  * Repeated patterns

---

### 3. Reinforcement Learning Decision Engine (MAJOR UPGRADE)

Instead of static rules:

### Problem Formulation:

```
State (S):
- severity_score
- fraud_score
- graph_risk_score
- claim_amount

Actions (A):
- APPROVE
- INVESTIGATE
- ASSIGN_ADJUSTER

Reward (R):
R = - (fraud_loss + processing_cost + delay_penalty)
```

### Outcome:

* Learns **optimal decision policies**
* Adapts over time
* Simulates real-world tradeoffs

---

### 4. Agentic AI Orchestration Layer (HIGH IMPACT)

Instead of a single pipeline:

You implement **specialized agents**:

| Agent          | Responsibility         |
| -------------- | ---------------------- |
| Intake Agent   | Parses FNOL            |
| Fraud Agent    | Evaluates fraud risk   |
| Severity Agent | Assesses damage        |
| Graph Agent    | Evaluates network risk |
| Decision Agent | Final decision         |

---

### Multi-Agent Coordination:

```
Agents → Share context → Debate/validate → Final decision
```

---

### 5. Multimodal Fusion (Enhanced)

```
Claim Representation =
f(text, image, structured data, graph features)
```

---

### 6. Conflict Detection + Resolution Engine

Detects contradictions:

* Low CV severity + high claim amount
* Clean history + high graph risk
* Text vs image inconsistency

Resolves using:

* RL policy
* Agent consensus
* LLM reasoning

---

### 7. LLM Reasoning Layer (Deterministic Stub)

Currently deployed as a **fallback stub** defining logical extraction outputs to circumvent OpenAI timeouts.
Used for:
* Template-based decision explanation
* Conflict reasoning stubs

NOT used for:
* Core prediction
* FNOL intake

---

### 8. System-Level Objective Optimization

Unlike current systems:

```
Minimize:
- Fraud Loss
- Operational Cost
- Processing Delay

Maximize:
- Customer Satisfaction
```

---

### 9. Continuous Learning Pipeline (Data Collection Layer)

* SQLite `training_store.db` replaces complex streaming event arrays securely offline.
* Captures Adjuster Feedback deterministically tracking Baseline vs RL Parity loops explicitly.
* Extracts arrays exclusively mapped towards Offline Batch Learning pipelines.

---

## System Architecture (Advanced)

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
[Feature Layer]
  ├── NLP Service
  ├── CV Service
  ├── Fraud Model
        |
        v
[Graph Builder Service ⭐]
        |
        v
[Graph DB (Neo4j)]
        |
        v
[Graph Intelligence Engine]
        |
        v
[Feature Fusion Layer]
        |
        v
[Decision Engine]
  ├── Rule Layer (baseline)
  ├── RL Policy Engine ⭐
  ├── Agentic Layer ⭐
  ├── LLM Reasoning Layer
        |
        v
[Decision API]
        |
        v
[Guidewire Adapter]
        |
        v
[Feedback Loop]
```

---

## Tech Stack (Upgraded)

### Backend

* Python (FastAPI)

### Graph Layer

* Neo4j / NetworkX

### ML

* NLP: DistilBERT
* CV: YOLOv8
* Fraud: XGBoost

### Graph ML

* Heuristic-based connection simulations (NetworkX object references over Persistent DB boundaries)

### RL

* Stable-Baselines3 (Offline Data Collection Placeholder)

### GenAI

* OpenAI / Claude (reasoning only)

### Infra

* SQLite Database (Native Persistent Arrays)
* Native FASTAPI Backends

---

## API Design (Enhanced)

### POST /fnol

```
{
  "policyId": "P123",
  "description": "...",
  "images": [...],
  "metadata": {...}
}
```

---

### Response

```
{
  "decision": "INVESTIGATE",
  "confidence": 0.87,
  "graphRisk": 0.65,
  "fraudScore": 0.82,
  "decisionTrace": [
    "Graph shows linkage to prior suspicious claim",
    "Damage inconsistent with description",
    "High fraud probability"
  ]
}
```

---

## Components Breakdown (Updated)

### 1. Graph Builder Service

* Constructs heuristic claim graph bounds utilizing Node mapping lists over object logic natively.

---

### 2. Graph Intelligence Engine

* Computes:
  * Simulated Anomaly limits based on Node tracking.

---

### 3. RL Policy Engine ⭐

* Learns optimal decisions
* Updates from feedback

---

### 4. Agentic Layer ⭐

* Multi-agent orchestration
* Context sharing

---

### 5. Decision Engine (Now Advanced)

Includes:

* Graph signals
* RL decisions
* Agent validation
* LLM explanation

---

## What Makes This Top 1%

* Combines **Graph AI + RL + LLM + System Design**
* Treats claims as:

  * Dynamic system
  * Not static prediction
* Demonstrates:

  * Architecture depth
  * Decision intelligence
  * Real-world constraints

---

# PHASE-WISE BUILD PLAN (STRICT)

## ⚠️ NON-NEGOTIABLE RULES

* Build **incrementally**
* No skipping
* Each phase must produce working output

---

## Phase 1 — Base System (Same as before)

* Data + APIs + basic pipeline

---

## Phase 2 — Decision Engine (Baseline)

* Rule-based + scoring

---

## Phase 3 — Graph Layer ⭐

### Tasks:

* Build claim graph (NetworkX)
* Define node/edge schema
* Compute:

  * degree centrality
  * connected components

### Output:

* Graph-based risk score

---

## Phase 4 — Graph ML (Optional Advanced)

* Node embeddings
* Similarity detection

---

## Phase 5 — RL Engine ⭐

### Tasks:

* Define:

  * state
  * action
  * reward
* Train simple RL agent

### Output:

* Policy-based decision system

---

## Phase 6 — Agentic Layer ⭐

### Tasks:

* Create modular agents
* Implement orchestration logic
* Pass shared context

---

## Phase 7 — LLM Reasoning Layer

* Add explanation
* Add conflict reasoning

---

## Phase 8 — Full Integration

* End-to-end pipeline
* API + frontend

---

## Phase 9 — Feedback Loop

* Store outcomes
* Update RL rewards

---

## Phase 10 — Optimization & Demo

* Structural JSON Rotating Logs
* Cached SQLite Metric extractions
* Feedback Safety Logic

---

## Phase 11 — Model Training & Deployment (TO BE IMPLEMENTED)

* **The Real RL Upgrade Loop**: Offline script extracting `data/training_store.db`.
* Executes `model.learn()` via Batch pipelines.
* Formal Version switching (`v1.0.0` -> `v1.0.1`) smoothly integrated across `AgenticOrchestrator`.

---

# HOW TO BUILD THIS CORRECTLY (CRITICAL)

## 1. DO NOT START WITH RL OR AGENTS

Start simple → then layer complexity

---

## 2. Graph First, RL Second, Agents Third

Correct order:

```
Base → Graph → RL → Agents → LLM
```

---

## 3. Keep Each Layer Independently Testable

* Graph score works?
* RL policy works?
* Agents coordinate?

---

## 4. Focus on Decision Flow, Not Model Accuracy

---

## 5. Demonstrate SYSTEM, Not Components

---

# FINAL POSITIONING (USE THIS EXACTLY)

> “Guidewire integrates multiple AI vendors but lacks a unified decision layer. This system introduces a graph-driven, reinforcement learning-based decision engine that resolves conflicting signals and optimizes claim outcomes end-to-end.”

---

