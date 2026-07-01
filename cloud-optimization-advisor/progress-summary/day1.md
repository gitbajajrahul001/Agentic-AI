# Cloud Optimization Advisor - Development Summary (Day 1)

**Date:** 2026-07-01

---

# Objective

Started building the MVP of an enterprise-grade **Cloud Waste Elimination Agent** focused on **Azure Virtual Machines**.

The long-term vision is an AI-powered recommendation engine that:

- Discovers Azure VMs
- Collects utilization metrics
- Evaluates enterprise policies
- Calculates cost savings
- Generates deterministic recommendations
- Uses an LLM only to explain recommendations to business users

---

# Product Scope

## Cloud

Azure only (MVP)

## Resource Type

Azure Virtual Machines only

## Personas

- CIO
- CFO
- FinOps
- Infrastructure Managers

---

# Architectural Principles Agreed

## 1. Azure-first

The MVP is Azure specific.

We intentionally removed cloud-agnostic abstractions.

---

## 2. Business Capability First

We organize the project around business capabilities rather than Azure services.

Business capabilities include:

- Authentication
- Subscription Discovery
- Inventory Discovery
- Metrics Collection
- Cost Collection
- Recommendation Engine

Azure connectors are implementation details.

---

## 3. Connectors Hide Azure

The rest of the application must never understand:

- Azure SDK
- REST responses
- Resource Graph JSON
- KQL

Instead every connector returns domain models.

Example:

```python
vms = resource_graph_connector.get_virtual_machines()
```

instead of

```python
execute_query(query)
```

---

## 4. Domain Models

The application communicates through domain models.

Current model:

```text
AzureVirtualMachine
```

Future models:

```text
VirtualMachineMetrics

VirtualMachineCost

VirtualMachineRecommendation
```

---

## 5. LLM Is NOT The Recommendation Engine

Decision making belongs to deterministic business logic.

The LLM will only:

- Explain recommendations
- Produce business reports
- Answer "Why?" questions
- Provide natural language interaction

---

# Project Structure

Current project structure:

```text
cloud-optimization-advisor/

├── app/
│
├── core/
│   ├── config_loader.py
│   ├── logger.py
│   └── constants.py
│
├── connectors/
│   └── azure/
│       ├── authentication_connector.py
│       ├── subscription_connector.py
│       ├── resource_graph_connector.py
│       ├── monitor_connector.py
│       ├── advisor_connector.py
│       ├── compute_connector.py
│       └── cost_management_connector.py
│
├── models/
│   └── azure_virtual_machine.py
│
├── engines/
│
├── config/
│   └── config.yaml
│
├── policies/
├── tests/
│
├── main.py
└── requirements.txt
```

---

# Components Built

## Configuration Loader

Implemented.

Loads:

- Azure credentials
- Observation window
- Worker threads
- Cache settings
- Logging configuration

---

## Azure Authentication Connector

Implemented.

Responsibilities:

- Create Azure credential
- Validate credential immediately
- Return authenticated credential

Authentication is validated using:

```python
credential.get_token(
    "https://management.azure.com/.default"
)
```

This forces immediate authentication instead of relying on lazy authentication.

---

## Subscription Connector

Implemented.

Responsibilities:

- Discover all subscriptions accessible to the Service Principal

Current public API:

```python
get_subscription_ids()
```

---

## Resource Graph Connector

Implemented.

Responsibilities:

- Execute Azure Resource Graph query
- Convert Azure JSON
- Return

```python
list[AzureVirtualMachine]
```

Current public API:

```python
get_virtual_machines()
```

---

# AzureVirtualMachine Domain Model

Current attributes:

```text
id

name

subscription_id

resource_group

location

vm_size

operating_system

power_state

tags
```

---

# Azure Services Used

Successfully integrated:

- Microsoft Entra ID
- Azure Resource Graph
- Azure Subscription Management API

Authentication is performed using a Service Principal.

---

# Live Validation Completed

Successfully validated:

✅ Configuration loading

✅ Azure authentication

✅ Subscription discovery

✅ Azure Resource Graph inventory

---

Current application output:

```text
Cloud Optimization Advisor

✓ Configuration loaded successfully.

✓ Successfully authenticated to Azure.

✓ Found 1 subscription.

✓ Found 1 virtual machine.

vm-agentic-ai
Standard_B1s
centralindia
```

---

# Azure Environment

Current Azure environment:

- Azure Pay-As-You-Go Subscription
- One Azure Virtual Machine
- Azure Monitor Agent installed
- Data Collection Rule configured
- Memory metrics being collected
- Log Analytics Workspace receiving guest memory metrics
- Azure Resource Graph working

VM Insights is NOT enabled.

Current plan is to continue using:

- Azure Monitor Metrics API
- Log Analytics Workspace

instead of enabling VM Insights.

---

# Recommendation Engine Design

Decision engine will evaluate:

- CPU P95
- Memory P95
- Network
- Disk
- Azure Advisor
- Current SKU
- Available SKUs
- Enterprise Policies
- Environment
- Tags
- Cost

The engine will NOT use an LLM.

Output:

```text
Recommended SKU

Confidence Score

Estimated Savings

Evidence

Reasoning
```

---

# Recommendation Evidence

Every recommendation should include evidence.

Example:

```text
Current SKU

Standard_D16s_v5

Recommended SKU

Standard_D4s_v5

Reason

CPU P95 = 18%

Memory P95 = 42%

Average CPU = 3%

Average Memory = 26%

Azure Advisor Recommendation = Yes

Environment Policy = Allowed

Estimated Monthly Savings = $540
```

---

# Architecture Roadmap

Completed:

```text
Configuration Loader

↓

Authentication

↓

Subscription Discovery

↓

Inventory Discovery
```

Remaining:

```text
Metrics Collection

↓

Cost Collection

↓

Advisor Collection

↓

Recommendation Engine

↓

LLM Explanation Layer

↓

AEX Agent
```

---

# Next Development Session

Primary goal:

Build the Metrics Capability.

Deliverables:

- Monitor Connector
- VirtualMachineMetrics domain model
- CPU metrics
- Memory metrics
- Observation window support
- P95 calculations

Expected output:

```text
VM

vm-agentic-ai

CPU Average

3%

CPU P95

18%

Memory Average

26%

Memory P95

42%

Observation Window

30 Days
```

---

# Key Architectural Decisions

- Azure-specific MVP
- Business capabilities over Azure services
- Domain-driven models
- Connectors encapsulate Azure APIs
- REST-first integration (except Azure Identity)
- Deterministic recommendation engine
- LLM reserved for explanation and conversational interface
- Build one capability at a time
- Prefer current needs over speculative abstractions

---

# Day 1 Milestone

By the end of Day 1, the application evolved from an empty Python project into a working Azure-integrated inventory platform capable of:

- Authenticating with Azure
- Discovering subscriptions
- Discovering virtual machines
- Returning strongly typed domain objects

This establishes the foundation for the Cloud Waste Elimination Agent, with telemetry collection and optimization logic planned for the next development session.