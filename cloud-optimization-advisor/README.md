# Cloud Optimization Advisor

An enterprise-oriented Python application that analyzes Azure Virtual Machines using live Azure telemetry, generates explainable optimization recommendations, enriches them with business context and pricing information, and persists the results as structured knowledge documents.

The project is designed around a **knowledge-first architecture**. Instead of generating recommendations only for immediate display, it converts optimization results into durable JSON knowledge documents that can be searched, indexed and consumed by downstream AI systems.

The long-term vision is to evolve this application into a cloud-native optimization platform where Azure discovery, optimization logic and AI-powered insights are decoupled into independently deployable services.

---

## Project Objectives

The project has four primary objectives:

- Analyze Azure Virtual Machines using live Azure APIs.
- Produce explainable optimization recommendations.
- Persist recommendations as structured enterprise knowledge.
- Build a foundation for future Agentic AI and Azure AI Search integration.

Unlike many proof-of-concept FinOps projects, this application deliberately separates:

- Azure connectivity
- Business logic
- Recommendation policies
- Validation
- Knowledge generation
- Data persistence

This separation allows each component to evolve independently.

---

# Current Architecture

The current implementation follows this processing pipeline.

```text
Azure

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

VMOptimizationReport

↓

Knowledge Serializer

↓

JSON Export

↓

Azure Blob Storage
```

Each stage has a clearly defined responsibility.

---

# Features

## Azure Resource Discovery

- Azure Authentication
- Subscription Discovery
- Resource Graph Inventory
- Azure VM SKU Discovery

---

## Metrics Collection

Collects live Azure Monitor telemetry including:

- CPU utilization
- Memory utilization
- Sample count

---

## Recommendation Engine

Generates recommendations based on configurable policies.

Current recommendation types include:

- Downsize
- Upsize
- Keep Current Size
- Insufficient Data

Recommendations include confidence levels and human-readable reasoning.

---

## VM Sizing

Identifies candidate VM sizes using configurable supported SKU definitions.

---

## Validation Engine

Validates recommendations against Azure platform constraints before presenting them.

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

---

## Cost Analysis

Uses the Azure Retail Pricing API to calculate:

- Current hourly cost
- Recommended hourly cost
- Estimated monthly savings
- Estimated annual savings

---

## Metadata Enrichment

Business metadata is extracted dynamically from Azure resource tags.

Metadata is configuration driven.

Current fields include:

- Owner
- Cost Center
- Environment
- Application

Additional metadata can be added without changing application code.

---

## Knowledge Generation

The application produces structured JSON knowledge documents instead of only console output.

Each document contains:

- Execution metadata
- Inventory
- Observability
- Recommendation
- Validation
- Cost analysis
- Business metadata

These documents become durable optimization knowledge that can later be indexed and queried by AI systems.

---

## Azure Blob Storage Integration

Generated knowledge documents are automatically uploaded to Azure Blob Storage.

Blob Storage acts as the enterprise knowledge repository.

---

# Repository Structure

```text
app/
├── config/
├── connectors/
├── exporters/
├── knowledge/
├── metadata/
├── models/
├── optimization/
├── recommendation/
├── renderers/
├── sizing/
├── validation/
```

The project intentionally separates:

- Azure integrations
- Business engines
- Domain models
- Rendering
- Export
- Knowledge generation

---

# Design Principles

The application follows several architectural principles.

## Configuration Driven

Recommendation policies, metadata mappings and supported VM sizes are maintained outside the application using YAML configuration.

---

## Separation of Concerns

Azure connectors communicate with Azure services.

Business engines implement optimization logic.

Serializers generate knowledge documents.

Exporters persist knowledge.

Renderers display results.

Each component has a single responsibility.

---

## Explainability

Recommendations are not treated as black boxes.

Every recommendation includes:

- confidence
- reasoning
- validation outcome

This enables operators and downstream AI systems to understand *why* a recommendation was generated.

---

## Knowledge First

Console output is considered a presentation layer.

The primary output of the application is structured knowledge suitable for long-term storage and future AI consumption.

---

# Technology Stack

- Python
- Azure Resource Graph
- Azure Monitor
- Azure Retail Pricing API
- Azure Blob Storage
- Pydantic
- PyYAML
- Rich

---

# Current Status

Implemented:

- Azure Authentication
- Azure Resource Discovery
- Azure Monitor Integration
- Recommendation Engine
- VM Sizing
- Validation Engine
- Cost Analysis
- Metadata Extraction
- Knowledge Serialization
- JSON Export
- Azure Blob Storage Upload

Planned:

- Azure AI Search
- Agentic AI Integration
- Containerization
- REST API
- Kubernetes Deployment
- CI/CD Pipeline

---

# Roadmap

The project is intended to evolve through several phases.

## Phase 1

Knowledge Generation

Completed

---

## Phase 2

Cloud-Native Foundation

- Git workflow
- Docker
- Containerization

---

## Phase 3

Service Platform

- FastAPI
- REST APIs
- Microservices

---

## Phase 4

Cloud Deployment

- Kubernetes
- Azure Kubernetes Service
- CI/CD

---

## Phase 5

Enterprise AI

- Azure AI Search
- Agentic AI
- Natural Language Querying

---

# Project Philosophy

This project is intentionally built as an engineering exercise rather than a prototype.

The focus is on:

- clean architecture
- maintainable code
- explicit business logic
- configuration-driven behavior
- explainable recommendations
- AI-ready knowledge generation

Every implementation decision is made with long-term extensibility in mind.

---

# License

This project is currently maintained as a personal learning and engineering project.