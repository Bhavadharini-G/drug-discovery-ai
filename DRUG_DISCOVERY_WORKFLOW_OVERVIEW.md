---
title: Drug Discovery Workflow Overview
description: Mermaid diagram linking all parts and chapters of the workflow
---

```mermaid
flowchart TD
    A1[Chapter 1: Gene to Ligand Discovery] --> A2[Chapter 2: Target Identification]
    A2 --> A3[Chapter 3: Target Validation]
    A3 --> B1[Chapter 4: Compound Screening]
    B1 --> B2[Chapter 5: Molecular Properties & ML]
    B2 --> C1[Chapter 6: Docking & Structure]
    C1 --> C2[Chapter 7: Synthesis & Optimization]
    C2 --> D1[Chapter 8+: Downstream Analysis]

    subgraph Part1[Part 1: Target & Ligand Discovery]
        A1
        A2
        A3
    end
    subgraph Part2[Part 2: Screening & Properties]
        B1
        B2
    end
    subgraph Part3[Part 3: Downstream Analysis]
        C1
        C2
        D1
    end
```

This diagram shows the sequential flow and linkage between all major parts and chapters in your drug discovery workflow. Outputs from each chapter become the inputs for the next, forming a reproducible pipeline.