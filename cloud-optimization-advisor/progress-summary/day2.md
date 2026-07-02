# Cloud Optimization Advisor - Progress Summary (Day 2)

## Date

2026-07-02

---

# Objective

Continue building the MVP Cloud Optimization Advisor by moving beyond telemetry collection and introducing a policy-driven recommendation engine.

The goal was **not** to build a production-grade platform, but to create an end-to-end working MVP demonstrating:

- Azure resource discovery
- Runtime telemetry collection
- Policy evaluation
- Recommendation generation
- Console presentation

---

# Completed Today

## 1. Azure Monitor Metrics Connector

Successfully completed CPU telemetry collection using Azure Monitor Metrics API.

Metrics collected:

- CPU Average
- CPU Maximum
- CPU P95
- Sample Count

---

## 2. Azure Log Analytics Integration

Integrated Log Analytics to collect memory utilization.

### Data Source

Perf table

Counter:

```
Memory
% Committed Bytes In Use
```

### Important Discovery

Azure Resource Graph returns Resource IDs as:

```
/subscriptions/.../resourceGroups/.../providers/Microsoft.Compute/virtualMachines/...
```

However Log Analytics stores `_ResourceId` in lowercase:

```
/subscriptions/.../resourcegroups/.../providers/microsoft.compute/virtualmachines/...
```

Therefore the query must use:

```python
vm.id.lower()
```

Otherwise zero rows are returned.

---

## 3. Memory Statistics

Successfully implemented:

- Memory Average
- Memory Maximum
- Memory P95

using the existing Statistics utility.

---

## 4. AzureVirtualMachineMetrics Model

The runtime telemetry model now contains:

### CPU

- cpu_average_percent
- cpu_max_percent
- cpu_p95_percent

### Memory

- memory_average_percent
- memory_max_percent
- memory_p95_percent

### Network

(placeholders)

- network_in_average_bytes
- network_out_average_bytes

### Disk

(placeholders)

- disk_read_average_bytes
- disk_write_average_bytes

### Telemetry

- sample_count
- telemetry_coverage_percent

---

## 5. Recommendation Policy

Created a dedicated policy file.

Current structure:

```yaml
telemetry:

  observation_window_days: 30

  minimum_sample_count: 10

  minimum_coverage_percent: 5

  allow_low_confidence: true

decision:

  cpu:

    upsize_threshold: 80

    downsize_threshold: 20

  memory:

    upsize_threshold: 80

    downsize_threshold: 40

confidence:

  high: 90

  medium: 70

  low: 30
```

> Note:
>
> `minimum_sample_count` was temporarily reduced from **24** to **10** because the test VM had only existed for one day.

---

# Recommendation Engine

Implemented the first version of the recommendation engine.

Location

```
app/recommendation/
```

Responsibilities

- Evaluate telemetry
- Compare against policy
- Produce recommendation
- Produce confidence
- Produce observations

The engine is intentionally independent of:

- Azure SDK
- Console rendering
- HTTP
- REST APIs

It contains only business logic.

---

# Recommendation Rules (MVP)

Evaluation order:

```
Enough telemetry?

        ↓

CPU above threshold?

        ↓

Memory above threshold?

        ↓

CPU AND Memory below thresholds?

        ↓

KEEP CURRENT SIZE
```

Safety rule:

> Any resource under pressure blocks a downsize recommendation.

This was intentionally chosen over weighted scoring for the MVP.

---

# VirtualMachineAnalysis Model

Created a dedicated domain model representing the decision.

Current responsibilities:

- Recommendation
- Confidence
- Observations
- Current VM Size
- Recommended VM Size (reserved for future use)

This model intentionally contains **no telemetry**.

Telemetry and recommendations remain separate concerns.

---

# Recommendation Enums

Created:

```
RecommendationAction
```

Values

- UPSIZE
- DOWNSIZE
- KEEP_CURRENT_SIZE
- INSUFFICIENT_DATA

Created:

```
RecommendationConfidence
```

Values

- HIGH
- MEDIUM
- LOW

---

# Console Renderer

Added a dedicated renderer.

```
render_vm_analysis()
```

Displays

- Recommendation
- Confidence
- Current VM Size
- Observations

Presentation is now completely separated from business logic.

---

# Current MVP Flow

```
Azure Authentication
        │
        ▼
Subscription Discovery
        │
        ▼
Azure Resource Graph
        │
        ▼
VM Inventory
        │
        ▼
Azure Monitor Metrics API
        │
        ├── CPU
        │
        ▼
Azure Monitor Agent
        │
        ▼
Log Analytics
        │
        ├── Memory
        │
        ▼
Statistics
        │
        ▼
Recommendation Engine
        │
        ▼
Rich Console Renderer
```

---

# Current Output

Current VM

```
Standard_B1s
```

Telemetry

```
CPU Average
12.74%

Memory Average
85.25%
```

Recommendation

```
UPSIZE
```

Confidence

```
HIGH
```

Observation

```
Average memory utilization (85.25%) exceeds the configured threshold.
```

---

# Architectural Decisions Finalized

## Connectors

Responsible only for Azure communication.

Never contain business logic.

---

## Models

Represent data.

Contain no Azure SDK logic.

Contain no rendering logic.

---

## Recommendation Engine

Contains only business rules.

Knows nothing about:

- Azure SDK
- Rich
- Console
- REST
- HTTP

---

## Renderer

Responsible only for presentation.

Consumes domain models.

Contains no recommendation logic.

---

## Main

Acts only as the orchestrator.

Responsibilities:

- Authenticate
- Collect
- Analyze
- Render

---

# Important Lessons Learned

## Azure Monitor Metrics

CPU metrics are available directly through Azure Monitor Metrics API.

---

## Memory

Memory metrics require:

Azure Monitor Agent

+

Log Analytics Workspace

Memory is **not** available through Azure Monitor Metrics API.

---

## Resource IDs

Resource Graph

```
ResourceGroups
Microsoft.Compute
```

Log Analytics

```
resourcegroups
microsoft.compute
```

Always compare using:

```python
vm.id.lower()
```

---

## Azure Monitor Query SDK

The SDK requires:

```python
timespan=(
    observation_start,
    observation_end,
)
```

Using timezone-aware datetimes introduced issues with Azure Metrics API because the code appended an additional `Z`.

For the MVP we intentionally retained:

```python
datetime.utcnow()
```

This keeps the implementation simple.

---

# Remaining MVP Work

## High Priority

### 1. Process every VM

Replace

```python
virtual_machines[0]
```

with

```python
for vm in virtual_machines
```

---

### 2. VM SKU Recommendation

Current output

```
UPSIZE
```

Target output

```
Current SKU

Standard_B1s

Recommended SKU

Standard_B2s
```

This will require:

- Azure VM SKU catalogue
- VM family awareness
- Simple sizing algorithm

---

### 3. Cost Impact

Show

- Current monthly cost
- Recommended monthly cost
- Estimated savings

---

# Future Enhancements

- Network utilization
- Disk utilization
- Azure Advisor integration
- Cost Management integration
- Reserved Instance recommendations
- Spot VM suitability
- AI-generated recommendation explanations
- REST API
- Web UI
- HTML/PDF reports

---

# MVP Status

Completed

- Azure authentication
- Subscription discovery
- VM discovery
- CPU telemetry
- Memory telemetry
- Statistics engine
- Policy engine
- Recommendation engine
- Rich console renderer

Remaining before MVP v1.0

- Multi-VM processing
- VM SKU recommendation
- Cost estimation

After these are complete, the project will represent a complete Cloud Optimization Advisor MVP capable of discovering Azure virtual machines, collecting runtime telemetry, evaluating policy-driven recommendations, and presenting actionable optimization guidance.