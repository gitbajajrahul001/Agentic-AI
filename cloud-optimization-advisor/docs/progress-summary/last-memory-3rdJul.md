# Cloud Optimization Advisor -- Project Progress Snapshot

*Date: 2026-07-03*

## Vision

Build an explainable Azure VM optimization engine that becomes the
backend for an AI agent. The optimization logic---not the LLM---makes
decisions. The LLM explains them in natural language.

## Current Architecture

``` text
Azure
 ├── Resource Graph
 ├── Azure Monitor
 └── Resource SKU API
        │
        ▼
Azure Connectors
        │
        ▼
Domain Models
        │
        ▼
Recommendation Engine
        │
        ▼
VM Sizing Engine
        │
        ▼
Validation Engine
        │
        ▼
Optimization Report
        │
        ▼
Future AI Agent
```

## Completed

-   Azure authentication and subscription discovery.
-   Resource Graph inventory for VM metadata, storage, network and
    security.
-   Azure Monitor CPU and memory telemetry.
-   Azure Resource SKU connector with capability mapping.
-   Supported VM SKU loader (organization-owned list).
-   Recommendation Engine (CPU/Memory/Telemetry).
-   VM Sizing Engine.
-   Validation Engine skeleton.
-   Domain models for VM, SKU and profiles.
-   Structured RecommendationReason model introduced.
-   Console reporting.

## Key Decisions

-   Recommendation and Validation are separate stages.
-   Azure Resource SKU API is the source of truth for VM capabilities.
-   Organization only controls supported SKU ordering.
-   Goal is an explainable backend for an AI agent, not just a resize
    script.

## Current Gap

Validation does not yet iterate through candidate SKUs. Example: -
Recommend B1s - Validation should reject because current VM has 4 data
disks. - Engine should automatically evaluate the next supported SKU
until one passes.

## Next Work

1.  Complete Validation Engine:
    -   Premium SSD
    -   MaxDataDiskCount
    -   MaxNetworkInterfaces
    -   Trusted Launch
    -   Encryption at Host
2.  Iterate candidate SKUs until a valid one is found.
3.  Finish structured explainability using RecommendationReason.
4.  Add Azure Retail Prices API for cost estimation.
5.  Produce JSON output suitable for an AI agent.

## Target MVP

-   Inventory
-   Metrics
-   Recommendation Engine
-   VM Sizing Engine
-   Validation Engine
-   Explainability
-   Cost estimation
-   JSON API

## After MVP

Wrap the backend with an AI agent that uses tool calling. The LLM should
explain recommendations using structured results from the optimization
engine rather than making optimization decisions itself.
