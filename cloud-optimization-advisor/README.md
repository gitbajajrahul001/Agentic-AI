# Cloud Optimization Advisor

An enterprise-grade Python application that analyzes Azure Virtual Machines using live Azure telemetry, generates explainable FinOps optimization recommendations, and transforms the results into a hierarchical knowledge repository for AI-driven cloud operations.

Unlike traditional optimization tools that produce reports for immediate consumption, Cloud Optimization Advisor generates structured knowledge objects at multiple levels of the Azure hierarchy. These knowledge documents become durable enterprise assets that can be consumed by AI agents, search platforms, dashboards, APIs, and automation workflows.

The project is intentionally designed as the foundation of an enterprise cloud optimization platform where Azure discovery, optimization logic, knowledge generation, and AI-powered reasoning are independent architectural components.

---

# Architecture Overview

The application implements a layered optimization pipeline followed by hierarchical knowledge generation.

```text
Azure

↓

Configuration

↓

Resource Discovery

↓

Metrics Collection

↓

Recommendation Engine

↓

Sizing Engine

↓

Validation Engine

↓

Cost Analysis

↓

Metadata Enrichment

↓

VM Optimization Report

↓

Knowledge Serialization

↓

Hierarchical Knowledge Aggregation

    VM
      ↓
Resource Group
      ↓
Subscription
      ↓
Enterprise

↓

Knowledge Repository

    ├── Local JSON Repository
    └── Azure Blob Storage
```

The architecture separates optimization from knowledge generation, allowing downstream AI systems to consume structured knowledge rather than raw operational data.

---

# Core Capabilities

## Azure Discovery

Discovers Azure infrastructure using live Azure APIs.

Current capabilities include:

- Azure Authentication
- Subscription Discovery
- Azure Resource Graph Inventory
- Azure VM SKU Discovery
- Azure Monitor Metrics
- Azure Retail Pricing API

---

## Recommendation Engine

Evaluates Azure Virtual Machines using configurable optimization policies.

Current recommendation types:

- Downsize
- Upsize
- Keep Current Size
- Insufficient Data

Every recommendation includes:

- Recommendation
- Confidence
- Human-readable reasoning
- Validation outcome

The recommendation engine is completely policy driven.

---

## VM Sizing Engine

Identifies candidate VM sizes based on configurable supported SKU definitions.

The sizing engine determines:

- Direction (Upsize / Downsize)
- Candidate ordering
- SKU compatibility

---

## Validation Engine

Before recommending any resize operation, every candidate VM is validated against Azure platform constraints.

Current validation covers:

### Storage

- Maximum Data Disks
- Premium SSD Support
- Ultra SSD Support

### Network

- Maximum Network Interfaces

### Platform

- Hyper-V Generation
- CPU Architecture
- Ephemeral OS Disk Support

Only candidates that pass all validation checks are recommended.

---

## Cost Analysis

Integrates with the Azure Retail Pricing API to calculate:

- Current Hourly Cost
- Recommended Hourly Cost
- Monthly Savings
- Annual Savings

Cost calculations are embedded directly into every knowledge document.

---

## Metadata Enrichment

Business metadata is dynamically extracted from Azure resource tags.

Current metadata includes:

- Owner
- Cost Center
- Environment
- Application

Metadata mappings are configuration-driven and require no code changes.

---

# Hierarchical Knowledge Architecture

The application follows a knowledge-first architecture.

Instead of generating isolated reports, optimization results are transformed into structured knowledge objects.

## Level 1 — Virtual Machine Knowledge

One knowledge document is generated per Azure Virtual Machine.

Contains:

- Inventory
- Performance metrics
- Recommendation
- Validation
- Cost analysis
- Metadata
- Execution metadata

---

## Level 2 — Resource Group Knowledge

VM knowledge is aggregated into Resource Group knowledge.

Contains:

- VM count
- Recommendation summary
- Optimization score
- Financial summary
- Resource Group insights

---

## Level 3 — Subscription Knowledge

Resource Group knowledge is aggregated into Subscription knowledge.

Contains:

- Resource Group count
- VM count
- Optimization statistics
- Financial rollups
- Subscription-level insights

---

## Level 4 — Enterprise Knowledge

Subscription knowledge is aggregated into a single Enterprise knowledge document.

Provides:

- Estate-wide optimization summary
- Total subscriptions
- Total resource groups
- Total virtual machines
- Overall optimization score
- Enterprise savings
- Executive summary

---

# Knowledge Repository

The generated knowledge hierarchy is persisted in two locations.

## Local Repository

```
output/

├── vm-knowledge/

├── resource-group-knowledge/

├── subscription-knowledge/

└── enterprise-knowledge/
```

---

## Azure Blob Storage

Each knowledge level is stored in its own container.

```
vm-knowledge

resource-group-knowledge

subscription-knowledge

enterprise-knowledge
```

Each resource maintains a single authoritative knowledge document representing its latest state.

Historical versions can be retained using Azure Blob Versioning.

---

# Repository Structure

```
cloud-optimization-advisor/

├── app/
│
├── aggregation/
│   ├── aggregation_engine.py
│   ├── resource_group_aggregator.py
│   ├── subscription_aggregator.py
│   └── enterprise_aggregator.py
│
├── config/
│
├── connectors/
│   └── azure/
│
├── exporters/
│
├── knowledge/
│
├── metadata/
│
├── models/
│
├── optimization/
│
├── recommendation/
│
├── renderers/
│
├── sizing/
│
├── validation/
│
├── config/
├── policies/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Design Principles

## Knowledge First

Knowledge documents are the primary output of the application.

Console rendering is simply one presentation layer.

This allows the same optimization results to power:

- AI Agents
- Dashboards
- Search
- APIs
- Reports
- Automation

---

## Hierarchical Aggregation

Knowledge is aggregated rather than repeatedly analyzed.

```
VM

↓

Resource Group

↓

Subscription

↓

Enterprise
```

This dramatically reduces retrieval cost and token consumption for downstream LLMs.

---

## Explainability

Recommendations are never black boxes.

Every recommendation includes:

- Recommendation
- Confidence
- Business reasoning
- Validation summary
- Financial impact

---

## Configuration Driven

Business behavior is controlled through YAML configuration.

Current configurable components include:

- Recommendation policies
- Metadata mappings
- Supported VM sizes

---

## Separation of Concerns

The application intentionally separates:

- Azure Connectors
- Recommendation Logic
- Validation
- Cost Analysis
- Metadata
- Knowledge Serialization
- Knowledge Aggregation
- Export
- Presentation

Each component has a single responsibility.

---

# Technology Stack

- Python
- Azure Resource Graph
- Azure Monitor
- Azure Retail Pricing API
- Azure Blob Storage
- Azure SDK for Python
- Pydantic
- PyYAML
- Rich

---

# Current Features

- Azure Authentication
- Subscription Discovery
- Resource Graph Integration
- Azure Monitor Metrics
- Azure VM SKU Discovery
- Recommendation Engine
- VM Sizing Engine
- Validation Engine
- Cost Analysis
- Metadata Extraction
- Knowledge Serialization
- Hierarchical Knowledge Aggregation
- JSON Knowledge Repository
- Azure Blob Storage Integration
- Console Rendering

---

# Current Architecture Status

| Capability | Status |
|------------|--------|
| Azure Discovery | ✅ Complete |
| Recommendation Engine | ✅ Complete |
| VM Sizing | ✅ Complete |
| Validation Engine | ✅ Complete |
| Cost Analysis | ✅ Complete |
| Metadata Engine | ✅ Complete |
| VM Knowledge | ✅ Complete |
| Resource Group Knowledge | ✅ Complete |
| Subscription Knowledge | ✅ Complete |
| Enterprise Knowledge | ✅ Complete |
| Local Knowledge Repository | ✅ Complete |
| Azure Blob Knowledge Repository | ✅ Complete |

---

# Roadmap

## Phase 1 — Knowledge Platform

Completed

- Azure Discovery
- Optimization Engine
- Knowledge Generation
- Hierarchical Aggregation
- Blob Storage Repository

---

## Phase 2 — Cloud Native Foundation

- Docker
- Docker Compose
- GitHub Actions
- Containerized Development

---

## Phase 3 — Service Platform

- FastAPI
- REST APIs
- Background Jobs
- Authentication
- OpenAPI

---

## Phase 4 — Cloud Deployment

- Azure Container Apps
- Azure Kubernetes Service (AKS)
- Azure Container Registry
- CI/CD Pipeline
- Infrastructure as Code

---

## Phase 5 — Enterprise AI

- Azure AI Search
- Hybrid Search
- Retrieval Planner
- Agentic AI
- Natural Language Query Interface
- AI-Powered Cloud Optimization Assistant

---

# Vision

The long-term vision is to build an AI-native Cloud Optimization Platform where structured operational knowledge replaces static reports.

Instead of requiring large language models to process thousands of raw infrastructure objects, hierarchical knowledge enables deterministic retrieval of only the most relevant optimization context.

This architecture significantly reduces token consumption, improves response quality, and provides a scalable foundation for enterprise AI use cases.

---

# License

This project is maintained as a personal engineering and learning initiative focused on enterprise architecture, cloud optimization, and AI-native systems design.