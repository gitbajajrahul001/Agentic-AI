# Cloud Optimization Advisor - Project Status (Day-End Summary)

**Date:** 2026-07-04

## Vision

Build an enterprise-grade Cloud Optimization Advisor that analyzes Azure
Virtual Machines using live Azure telemetry, validates recommendations
against Azure platform constraints, enriches recommendations with
business metadata and pricing, and exports structured knowledge
documents for downstream Agentic AI systems.

Long-term architecture:

Azure → Recommendation Engine → Validation → Cost Analysis → Knowledge
Export → Azure Blob Storage → Azure AI Search → Agentic AI / LLM

The objective is to minimize LLM token consumption by answering
questions primarily from structured knowledge rather than querying Azure
at runtime.

------------------------------------------------------------------------

## Current Architecture

The application currently consists of:

-   app/connectors (Azure integrations)
-   app/recommendation (Recommendation Engine)
-   app/sizing (Candidate selection)
-   app/validation (Constraint validation)
-   app/metadata (Business metadata extraction)
-   app/renderers (Console rendering)
-   app/exporters (Reserved for JSON/CSV export)
-   app/models (Domain models)
-   config (Configuration)
-   policies (Recommendation policy)
-   output (Future exports)

The latest architecture now includes: - Cost Analysis - Metadata
Engine - Report Assembly - Knowledge Export - Future AI integration

------------------------------------------------------------------------

## Implemented

### Azure

-   Authentication
-   Subscription discovery
-   Resource Graph inventory
-   VM SKU discovery
-   Azure Monitor metrics
-   Azure Retail Pricing API

### Recommendation Engine

-   CPU analysis
-   Memory analysis
-   Confidence
-   Recommendation rationale
-   Upsize
-   Downsize
-   Keep Current Size
-   Insufficient Data

### Validation

Storage: - Maximum Data Disks - Premium SSD - Ultra SSD

Network: - Maximum Network Interfaces

Platform: - Hyper-V Generation - CPU Architecture - Ephemeral OS Disk

### Cost Analysis

-   Live Azure Retail pricing
-   Pricing cache
-   Monthly cost
-   Annual savings

### Metadata

Configuration-driven metadata from:

config/metadata_configuration.yaml

Current metadata: - Owner - Cost Center - Environment - Application

### Reporting

VMOptimizationReport now contains: - Inventory - Metrics -
Recommendation - Validation - Cost Analysis - Metadata - generated_at -
policy_version

This is the canonical report object.

------------------------------------------------------------------------

## Architectural Decisions

-   Metadata configuration separated from recommendation policy.
-   Configuration-driven metadata extraction.
-   Validation independent from recommendation logic.
-   Pricing isolated as its own connector.
-   VMOptimizationReport is the single source of truth.
-   Console optimized for operators.
-   Knowledge export will be optimized for AI.

------------------------------------------------------------------------

## Next Milestone

Create:

app/exporters/ - json_exporter.py - csv_exporter.py

JSON becomes the AI knowledge document.

CSV becomes the human-readable analysis report.

------------------------------------------------------------------------

## Future Roadmap

1.  JSON Export
2.  CSV Export
3.  Azure Blob Storage
4.  Azure AI Search
5.  Agentic AI

Typical future questions:

-   Which VMs failed downsizing because of storage?
-   Show recommendations by Cost Center.
-   Which owners have the highest savings?
-   Compare recommendations by policy version.

The future AI will retrieve structured knowledge first and use the LLM
primarily for reasoning.

------------------------------------------------------------------------

## Long-Term Goal

Evolve the project from a VM optimization tool into an Enterprise Cloud
Optimization Knowledge Platform where recommendations become durable,
searchable knowledge assets for FinOps, Enterprise Architecture, CIOs,
CFOs and Agentic AI.
