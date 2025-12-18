# Report Diagrams

## Diagram 1: High-Level System Architecture
*Caption: The three-tiered architecture of JobMatchAI, separating the User Experience (UX), Agentic Logic, and Data Persistence layers.*

```mermaid
graph TB
    subgraph Client ["Client Layer"]
        Browser["User Browser (React App)"]
    end

    subgraph Server ["Backend Layer (FastAPI)"]
        direction TB
        API[API Gateway]
        
        subgraph Agents ["Agent Swarm"]
            CV[CV Parser]
            ATS[ATS Analyzer]
            Match[Job Matcher]
            Search[Job Aggregator]
            Write[Writer Agent]
        end
        
        API --> Agents
    end

    subgraph Data ["Data Layer"]
        DB[(SQLite Database)]
        Files[File Storage]
    end

    Browser <-->|JSON/HTTP| API
    Agents <--> DB
    CV --> Files
```

---

## Diagram 2: Agent Interaction Sequence (The "Search" Flow)
*Caption: A sequence diagram illustrating the temporal flow of information when a user initiates a job search. Note the asynchronous parallel execution of the Search and Match agents.*

```mermaid
sequenceDiagram
    participant User
    participant ReactUI as Frontend
    participant API as Backend API
    participant Aggregator as "Job Aggregator (Agent 4)"
    participant Matcher as "Job Matcher (Agent 5)"
    participant External as "Adzuna API"

    User->>ReactUI: Click "Find Jobs"
    ReactUI->>API: POST /api/search-jobs
    activate API
    
    API->>Aggregator: fetch_jobs(query)
    activate Aggregator
    Aggregator->>External: GET /jobs (Region=London)
    External-->>Aggregator: Return 50 JSON Objects
    Aggregator-->>API: Return Job List
    deactivate Aggregator

    API->>Matcher: match_jobs(UserCV, JobList)
    activate Matcher
    Matcher->>Matcher: Vectorize Descriptions
    Matcher->>Matcher: Calculate Cosine Similarity
    Matcher-->>API: Return Ranked List
    deactivate Matcher

    API-->>ReactUI: Return JSON {jobs: [...]}
    deactivate API
    ReactUI->>User: Display Ranked Job Cards
```

---

## Diagram 3: Matcher Logic Visualization
*Caption: Visualizing the Vector Space Model used by Agent 5. The User's CV Vector is compared to Job Vectors to find the smallest angle (Cosine Similarity).*

```mermaid
graph LR
    CV["User CV (Vector A)"]
    Job1["Job 1 (Vector B)"]
    Job2["Job 2 (Vector C)"]
    
    CV --"High Similarity (0.9)"--> Job1
    CV --"Low Similarity (0.2)"--> Job2
    
    style CV fill:#d4f1f4,stroke:#333
    style Job1 fill:#97c1a9,stroke:#333
    style Job2 fill:#ff968a,stroke:#333
```
