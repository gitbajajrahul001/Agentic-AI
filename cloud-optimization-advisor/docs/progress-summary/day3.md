# Cloud Optimization Advisor – Day Progress Log

**Date:** 2026-07-03

---

# Objective

Today's primary objective was to evolve the Cloud Optimization Advisor from a simple CPU/Memory recommendation engine into the foundation of an explainable AI optimization engine.

The focus shifted from simply producing recommendations to ensuring that every recommendation can eventually be justified with technical reasoning suitable for an AI agent.

---

# Work Completed

## 1. Azure Resource Graph Inventory Enhancement

Expanded the Azure Resource Graph query to collect significantly richer VM inventory.

### Newly Collected Properties

- Operating System
- OS Disk Type
- OS Disk Size
- Data Disk Count
- NIC Count
- Security Type
- Power State
- Managed Identity
- Availability Zone

The KQL query is now embedded directly inside the `ResourceGraphConnector` instead of maintaining a separate query file.

### Design Decision

Keep inventory collection close to the connector instead of introducing unnecessary abstraction for the MVP.

---

# 2. VM Domain Model Enrichment

Introduced profile-based modeling for virtual machines.

Instead of storing everything directly inside `AzureVirtualMachine`, the model now contains dedicated capability profiles.

## Storage Profile

File:

```text
app/models/azure_storage_profile.py
```

Captures:

- OS Disk Type
- OS Disk Size
- Data Disk Count
- Premium SSD
- Ultra SSD

---

## Network Profile

File:

```text
app/models/azure_network_profile.py
```

Captures:

- NIC Count
- Accelerated Networking

---

## Security Profile

File:

```text
app/models/azure_security_profile.py
```

Captures:

- Security Type

---

## Compute Profile

File:

```text
app/models/azure_compute_profile.py
```

Created as the foundation for future capability validation.

Currently stores:

- VM Size
- vCPUs
- Memory
- Premium Storage Support
- Max Data Disks
- Network Bandwidth

Although not fully utilized yet, it prepares the project for future validation rules.

---

# 3. Azure SKU Inventory

Completed the Azure Resource SKU integration.

Connector:

```text
app/connectors/azure/vm_sku_connector.py
```

Implemented:

- Azure Resource SKU API integration
- Duplicate SKU removal
- Conversion into `AzureVmSku`
- Capability dictionary

Examples of collected capabilities:

- vCPUs
- MemoryGB
- PremiumIO
- MaxDataDiskCount
- MaxNetworkInterfaces
- UltraSSDAvailable
- EncryptionAtHostSupported
- AcceleratedNetworkingEnabled

---

# 4. Supported SKU Loader

Introduced organization-controlled supported VM SKUs.

Concept:

Azure defines capabilities.

Organization defines which VM sizes are allowed.

Example:

```yaml
supported_vm_sizes:

- Standard_B1s

- Standard_B2s

- Standard_B2ms

- Standard_B4ms

- Standard_B8ms
```

No Azure capabilities are hardcoded inside the application.

---

# 5. VM Sizing Engine

Implemented the first version of the sizing engine.

Responsibilities:

- Receive recommendation
- Locate current VM size
- Select next supported SKU

Current behavior:

```text
Current VM

↓

Supported SKU List

↓

Candidate SKU
```

---

# 6. Recommendation Engine Improvements

Began migrating from simple observations toward explainable recommendations.

Created:

```text
RecommendationReason
```

Model:

```text
category

message
```

Current work:

Recommendation engine now records structured reasons instead of simple text observations.

Examples:

```text
CPU

Average CPU utilization (10.91%)
exceeds configured upsize threshold (15%).

Memory

Average memory utilization
is below configured threshold.
```

Migration is still in progress.

---

# 7. Validation Engine

Validation framework remains intentionally separate from recommendation.

Current architecture:

```text
Recommendation

↓

Candidate SKU

↓

Validation

↓

Final Recommendation
```

This separation was identified as a key architectural decision.

---

# 8. Inventory Mapping Validation

Verified that Azure inventory is now correctly populated.

Example:

```text
Storage

OS Disk Type

OS Disk Size

Data Disk Count

Network

NIC Count

Security

Trusted Launch
```

Successfully fixed:

- duplicate VM mapping
- profile population
- Resource Graph mapping

---

# 9. Test Environment Enhancement

Modified Azure environment to simulate realistic scenarios.

## VM-1

Purpose:

General recommendation testing.

## VM-2

Modified:

- Resized to Standard_B2s
- Attached four Premium data disks

Purpose:

Storage capability validation.

Also modified recommendation thresholds to intentionally produce different recommendation paths.

---

# 10. Validation Gap Identified

Discovered an important architectural limitation.

Current flow:

```text
Recommendation

↓

Candidate

↓

Validation

↓

Return
```

Example:

Current VM

```text
B2s

4 Data Disks
```

Candidate:

```text
B1s

Supports only 2 data disks
```

Expected:

Reject candidate.

Current behavior:

Candidate still returned.

Conclusion:

Validation currently validates only one candidate instead of iterating through supported SKUs until a compatible candidate is found.

---

# Important Architectural Decisions

## Recommendation Engine Responsibilities

Responsible for answering:

```text
Should this VM change size?
```

Inputs:

- CPU
- Memory
- Telemetry
- Policy

Does NOT evaluate:

- Premium SSD
- Data Disks
- NIC Count
- Trusted Launch

---

## Validation Engine Responsibilities

Responsible for answering:

```text
Can this candidate host the workload?
```

Validation will eventually include:

- Premium SSD
- Max Data Disks
- Max NIC Count
- Trusted Launch
- Encryption at Host
- Compute Compatibility

---

## Azure as Source of Truth

Decided not to maintain Azure VM capability data inside the application.

Azure Resource SKU API remains the authoritative source.

Only organization-specific supported SKUs are maintained locally.

---

# Lessons Learned

Several architectural insights emerged today.

## Recommendation != Validation

These must remain independent systems.

Recommendation determines intent.

Validation determines technical feasibility.

---

## Explainability is a First-Class Feature

The long-term goal is not merely to resize virtual machines.

The goal is to produce recommendations that can be fully explained by an AI assistant using structured reasoning.

---

## AI Will Not Make Decisions

The optimization engine remains the decision-making component.

Future AI responsibilities:

- Tool calling
- Reading structured results
- Producing natural language explanations

The LLM should never perform optimization calculations itself.

---

# Next Steps

## Immediate

- Complete Validation Engine
- Implement Max Data Disk validation
- Implement Premium SSD validation
- Implement Max NIC validation
- Iterate through candidate SKUs until a valid recommendation is found

---

## After Validation

Complete structured explainability.

Every recommendation should explain:

- CPU evaluation
- Memory evaluation
- Validation results
- Final recommendation

---

## MVP Target

The MVP will be considered complete once the project contains:

- Azure Inventory
- Azure Monitor Metrics
- Azure SKU Inventory
- Recommendation Engine
- VM Sizing Engine
- Validation Engine
- Explainability
- Cost Estimation
- JSON API

Only after achieving this milestone will development shift toward integrating an Agentic AI workflow using LLM tool calling.