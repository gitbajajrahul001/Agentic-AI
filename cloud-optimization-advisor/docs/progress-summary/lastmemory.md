# Cloud Optimization Advisor - Project Context & Continuation Guide

> **Purpose**
>
> This document serves as the primary context for future ChatGPT sessions. It captures the complete vision, architecture, design decisions, implementation status, and roadmap of the Cloud Optimization Advisor project.
>
> At the beginning of a future conversation, I will provide:
>
> 1. This markdown document
> 2. The latest architecture diagram
>
> ChatGPT should use these as the authoritative context and continue the project without requiring me to explain everything again.

---

# Project Vision

The objective is to build an enterprise-grade Cloud Optimization Advisor that continuously analyzes Azure infrastructure and converts cloud optimization recommendations into durable enterprise knowledge.

Unlike traditional optimization tools that generate recommendations on demand, this platform continuously produces structured knowledge documents that become the organization's cloud optimization knowledge repository.

The knowledge repository will later be consumed by Agentic AI to answer natural language questions from FinOps teams, Enterprise Architects, CIOs, CFOs and Cloud Operations teams.

The architecture intentionally minimizes LLM token usage.

Instead of allowing the LLM to query Azure directly, the application performs all expensive Azure discovery, telemetry collection, pricing analysis and recommendation generation ahead of time.

The LLM should only perform reasoning over already generated knowledge documents.

---

# Overall Vision

Azure Resources

↓

Collect Inventory

↓

Collect Metrics

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

Knowledge Generation

↓

Azure Blob Storage

↓

Azure AI Search

↓

Agentic AI

---

# Design Principles

The project follows several architectural principles.

## 1. Separation of Responsibilities

Azure connectors only communicate with Azure services.

Business engines contain recommendation logic.

Renderers display information.

Exporters persist information.

Serializers transform internal domain models into knowledge documents.

No component should perform responsibilities outside its domain.

---

## 2. Configuration Driven

Business logic should not be hardcoded.

Recommendation thresholds come from YAML.

Metadata tags come from YAML.

Supported VM SKUs come from YAML.

Storage configuration comes from config.yaml.

Future optimization policies should also remain configuration driven.

---

## 3. Knowledge First

The application does not optimize infrastructure for immediate display.

Instead it generates structured enterprise knowledge.

Knowledge is the primary output.

Console rendering is secondary.

---

## 4. AI First Architecture

Every architectural decision should support future AI consumption.

Knowledge documents should be:

- structured
- deterministic
- explainable
- machine readable
- searchable
- versioned

---

# Current Repository Structure

The repository currently contains:

- Azure Connectors
- Recommendation Engine
- Sizing Engine
- Validation Engine
- Cost Analysis
- Metadata Engine
- Knowledge Serializer
- JSON Exporter
- Blob Storage Connector
- Console Renderer

The repository structure should be treated as the source of truth.

---

# Current Processing Flow

Configuration

↓

Authenticate to Azure

↓

Discover Subscriptions

↓

Discover Virtual Machines

↓

Collect Azure Monitor Metrics

↓

Analyze CPU

↓

Analyze Memory

↓

Generate Recommendation

↓

Find Candidate VM Sizes

↓

Validate Candidates

↓

Perform Cost Analysis

↓

Extract Metadata

↓

Build VMOptimizationReport

↓

Serialize into Knowledge Document

↓

Export JSON

↓

Upload to Azure Blob Storage

---

# Azure Services Used

Current implementation uses:

- Azure Resource Graph
- Azure Monitor
- Azure Retail Pricing API
- Azure Blob Storage

Future implementation:

- Azure AI Search

---

# Current Knowledge Repository

Knowledge documents are exported locally to:

output/json/YYYY-MM-DD/

and automatically uploaded to:

Azure Storage Account

Container:

finops-repo

Blob layout:

json/YYYY-MM-DD/

One JSON document represents one Azure Virtual Machine.

---

# Current Knowledge Document Structure

Every VM produces one structured knowledge document.

Current top-level schema:

Execution

Inventory

Metadata

Observability

Analysis

Inside Analysis:

Recommendation

Validation

Cost

This schema should remain stable unless new optimization domains require extension.

---

# VMOptimizationReport

VMOptimizationReport is the canonical domain object.

It combines:

Inventory

Metrics

Analysis

Validation

Cost

Metadata

Execution metadata

including:

- generated_at
- execution_id
- policy_version

Every downstream component uses this object.

---

# Metadata

Metadata extraction is configuration driven.

Configured in:

config/metadata_configuration.yaml

Current metadata fields:

- Owner
- Cost Center
- Environment
- Application

Future metadata additions should require only YAML changes.

---

# Cost Analysis

Pricing comes from Azure Retail Pricing API.

Current calculations include:

Current hourly cost

Recommended hourly cost

Monthly cost

Monthly savings

Annual savings

---

# Validation

Recommendation validation currently evaluates:

Storage

Network

Platform

Candidate validation results are preserved in the knowledge document.

The AI should be able to explain WHY recommendations failed.

---

# Knowledge Serializer

KnowledgeSerializer converts VMOptimizationReport into an AI-ready knowledge document.

The serializer intentionally maps fields explicitly.

It should not simply dump internal models.

The knowledge schema is independent from internal implementation.

---

# JSON Export

The exporter creates:

output/json/YYYY-MM-DD/

Filename format:

YYYYMMDDTHHMMSSZ_<resource_name>.json

Example:

20260706T123015Z_vm-agentic-ai.json

---

# Blob Storage

Blob Storage acts as the enterprise knowledge repository.

Current storage account:

staccagenticai

Current container:

finops-repo

Folder structure:

json/YYYY-MM-DD/

Blob Storage should be considered the source of truth.

---

# Current Implementation Status

Completed

- Azure Authentication
- Subscription Discovery
- VM Discovery
- Metrics Collection
- Recommendation Engine
- Sizing Engine
- Validation Engine
- Cost Analysis
- Metadata Engine
- Console Renderer
- Knowledge Serializer
- JSON Export
- Azure Blob Storage Upload

Not Started

- Azure AI Search
- Agentic AI Integration
- CSV Export
- Execution Manifest
- Scheduled Execution
- Historical Trend Analysis

---

# Long-Term Architecture

Azure

↓

Knowledge Generation

↓

Blob Storage

↓

Azure AI Search

↓

Agentic AI

↓

Natural Language Q&A

The Agent should never query Azure directly.

It should answer using enterprise knowledge.

---

# Typical Future Questions

Which VMs failed downsizing because of storage?

Which Cost Center has the highest optimization opportunity?

Show recommendations generated by Policy Version 1.0.

Which VM owners have the highest annual savings?

Which recommendations have High confidence?

Which VMs violate Premium Storage requirements?

Show all recommendations for Environment = Production.

---

# Development Philosophy

The project emphasizes architecture over shortcuts.

Preference order:

1. Clean architecture
2. Maintainability
3. Extensibility
4. Readability
5. Performance

The codebase intentionally favors explicit business logic over clever abstractions.

Future implementations should preserve this philosophy.

---

# Next Planned Milestone

The next phase is Azure AI Search.

Expected flow:

Azure Blob Storage

↓

Azure AI Search Indexer

↓

Search Index

↓

AEX Agentic Platform

↓

LLM

↓

Natural Language Answers

Azure AI Search will become the retrieval layer.

Blob Storage will remain the durable knowledge repository.

---

# Architecture Diagram

Along with this document, I will provide the latest architecture diagram.

The diagram represents the implementation state of Version 1.0.

Treat both this document and the architecture diagram as the authoritative reference for future work.

---

# Instruction for Future ChatGPT Sessions

When this document and the accompanying architecture diagram are provided:

- Assume the project context has already been established.
- Do not redesign existing architecture unless explicitly requested.
- Preserve the existing separation of responsibilities.
- Continue implementation from the current milestone.
- Favor incremental, production-quality enhancements over major rewrites.
- Maintain the project's coding style and architectural principles.
- Consider the current implementation as Version 1.0 and build future capabilities on top of it.