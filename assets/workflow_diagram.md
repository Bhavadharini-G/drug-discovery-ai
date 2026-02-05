```mermaid
graph TD;
    subgraph API Layer
        Main[main.py]
    end
    subgraph Agent Layer
        Crew[agents/multi_agent.py]
    end
    subgraph Tool Layer
        PubMedTool[tools/pubmed.py]
        PubChemTool[tools/pubchem.py]
    end
    subgraph Data Layer
        DB[db/mongodb.py]
        DataRaw[data/raw/]
        DataProcessed[data/processed/]
    end
    subgraph Utils
        UtilsNode[app/utils/]
    end
    Main --> Crew
    Crew --> PubMedTool
    Crew --> PubChemTool
    PubMedTool -->|fetches| DataRaw
    PubChemTool -->|fetches| DataRaw
    Crew --> DB
    Main --> UtilsNode
    Crew --> UtilsNode
    Main -->|returns| Main
```
