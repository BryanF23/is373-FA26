# 2. RAG app + technical research

## Project idea

I plan to build an **XR Lab Knowledge Assistant**. It would help students, instructors, and lab staff find answers about approved XR lab equipment and applications, such as Meta Quest headsets, Arkio, VirtualSpeech, setup steps, and common troubleshooting questions.

The goal is to make lab information easier to find and to have answers point back to the source document or guide.

## Intended users and example questions

- A student wants to know how to navigate an imported Revit model in Arkio.
- An instructor wants to know whether an application is supported on a particular headset.
- A lab assistant needs a setup or troubleshooting procedure.
- A user asks about a device or application that is not covered by the approved sources.

## Sources and permissions

Potential sources for the knowledge base:

- Official Meta Quest support pages and manuals.
- Official Arkio documentation and help pages.
- Official VirtualSpeech documentation and support pages.
- Public application manuals and release notes.
- Guides I write myself based on procedures that I am allowed to document.

I will only include internal NJIT documents if I have permission to use them for this project. I will not include student information, private staff information, passwords, access codes, API keys, or other restricted material.

## How RAG works

Retrieval-Augmented Generation (RAG) combines document search with a language model.

1. **Import:** Collect approved documents and extract their text.
2. **Chunk:** Split long documents into smaller sections that can be searched.
3. **Embed:** Convert each chunk into a numerical embedding that represents its meaning.
4. **Store:** Save embeddings and source metadata in a searchable database.
5. **Retrieve:** Search for the chunks most relevant to a user's question.
6. **Generate:** Give the retrieved material to a language model so it can form an answer grounded in those sources.
7. **Cite:** Show which documents or sections support the answer.
8. **Evaluate:** Test whether the answer is relevant, supported, and appropriately cautious when the sources do not contain the answer.

## Vector and graph database research

| Approach | What it stores or helps with | Possible use in this project |
|---|---|---|
| Vector database | Embeddings that support similarity search by meaning. | Find relevant instructions even when a user phrases a question differently from the source. |
| Graph database | Entities and relationships, such as an application being compatible with a headset or a procedure belonging to an application. | Answer questions that depend on connected facts and relationships across documents. |
| Hybrid | Combines vector retrieval with graph relationships or other structured metadata. | Could be useful later if the project needs more complex compatibility and version questions. |

### Initial decision

Start with **vector search and metadata**, rather than building a graph database immediately. The first version mainly needs to retrieve relevant passages from guides and manuals. A graph could be added later if testing shows that questions about relationships between headsets, apps, versions, and procedures are difficult to answer with vector search alone.

## Database options

### PostgreSQL + pgvector

[pgvector](https://github.com/pgvector/pgvector) adds vector similarity search to PostgreSQL. This is a reasonable starting option because I have already worked with PostgreSQL in my self-hosting project. It could keep document metadata and vector data in one database.

### Neo4j GraphRAG

[Neo4j GraphRAG for Python](https://neo4j.com/docs/neo4j-graphrag-python/current/) provides tools for graph-based retrieval workflows. It is a possible option if the project later needs to represent relationships between equipment, applications, versions, and procedures.

**Current choice:** PostgreSQL with pgvector for the first version. This is a research-based decision only; I have not installed or tested pgvector yet.

## Chunking, embeddings, and metadata plan

I will split documents into sections that preserve the meaning of each instruction or topic. I should avoid splitting a procedure in the middle of a step sequence. Each chunk should retain useful metadata, such as:

- Source document title and URL.
- Application or headset name.
- Document type, such as manual, support article, or lab guide.
- Version or publication date when available.
- Section heading or page number when available.

Embeddings will be generated for each chunk so the system can retrieve relevant information based on the meaning of a question, not just exact keyword matches.

## Entities and relationships to consider

Possible entities:

- Headset
- Application
- Software version
- Procedure
- Source document
- Feature or troubleshooting issue

Possible relationships:

- Application **runs on** headset.
- Procedure **explains how to use** application.
- Document **describes** procedure.
- Version **applies to** application or headset.
- Troubleshooting issue **relates to** device or application.

These are planned data concepts. I have not created a graph or populated these relationships yet.

## Proposed architecture

1. A simple web interface accepts a question.
2. A Flask or FastAPI backend receives the question.
3. The backend creates an embedding for the question.
4. PostgreSQL with pgvector retrieves relevant document chunks and metadata.
5. The backend sends the question and retrieved context to a language model API.
6. The model generates an answer based on the retrieved context.
7. The interface displays the answer and source links.

This is a proposed architecture, not a working implementation. I will choose the final framework and model after checking the course requirements and available resources.

## Import plan

- Gather only approved source documents.
- Record each document's title, URL, type, and version/date if available.
- Extract text from PDFs, web pages, and other supported formats.
- Clean up repeated headers, footers, and irrelevant text.
- Split the text into meaningful chunks.
- Generate embeddings and store them with source metadata.
- Keep track of the source each chunk came from so answers can cite it.
- Re-import or update content when a source changes.

## Hosting and resource constraints

I have previously used a DigitalOcean server with Docker, Flask, PostgreSQL, and Traefik. That experience may help with deployment, but the RAG application still needs to be designed and tested separately.

For the first version, I plan to avoid running a large language model locally on a small server. An API-based model may be more practical, depending on course rules, cost, and access. I will need to protect API keys using environment variables and keep them out of GitHub.

## Planned evaluation stories and checks

These are planned tests. They have **not** been run yet.

| # | User story / test question | What I will check |
|---|---|---|
| 1 | A student asks how to navigate an imported Revit model in Arkio. | The answer retrieves the relevant Arkio guide and provides steps supported by that guide. |
| 2 | An instructor asks whether a specific app works on Meta Quest 3. | The answer uses a source that actually confirms compatibility and identifies the relevant device or version. |
| 3 | A user asks about a topic that is not in the knowledge base. | The assistant says it cannot find support in the available sources instead of making up instructions. |
| 4 | A user asks a question that needs information from more than one source. | The answer retrieves and cites the relevant sources without mixing up their claims. |
| 5 | A user asks about an older software version. | The answer identifies version or date limits and does not present outdated steps as current without warning. |

### Evaluation criteria

- **Retrieval relevance:** Did the system find the right source sections?
- **Grounding:** Are the answer's claims supported by the retrieved material?
- **Citations:** Can the user open and verify the sources?
- **Abstention:** Does the system admit when the knowledge base does not contain the answer?
- **Version handling:** Does it distinguish device and software versions when relevant?

## Research sources

- [pgvector — PostgreSQL vector similarity search](https://github.com/pgvector/pgvector)
- [Neo4j GraphRAG for Python documentation](https://neo4j.com/docs/neo4j-graphrag-python/current/)
- [AWS Prescriptive Guidance — Retrieval Augmented Generation options (PDF)](https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/retrieval-augmented-generation-options/retrieval-augmented-generation-options.pdf)
- [Apache Hop — GraphRAG guide](https://hop.apache.org/manual/latest/how-to-guides/graphrag.html)
- [IS373 Project 2 brief](https://njit.instructure.com/courses/70733/pages/project-2-individual-rag-app-and-technical-research)
- [IS373 research review index](https://kaw393939.github.io/is373-studio/templates/project-record.html#research-review-index)



## More detailed technical research

### Chunking strategy

Chunking means splitting a source document into smaller pieces before creating embeddings. The goal is to make each retrieved result focused enough to answer a question, while keeping enough surrounding context that the meaning is not lost.

For this project, I plan to start with **section-aware chunking**:

1. Extract text from a document and keep its headings and section order.
2. Split by headings or logical sections first, rather than cutting every fixed number of characters.
3. If a section is too long, split it into smaller pieces using paragraphs or sentence boundaries.
4. Keep a small overlap between adjacent chunks only when it helps preserve a procedure or explanation that crosses a boundary.
5. Store the original document title, section heading, source URL, page number when available, and version/date with each chunk.

For example, an Arkio guide section called "Navigate a model" should stay together when possible. If it is too long, it can be split into smaller step groups while retaining the same document and section metadata.

**Trade-off:** Very small chunks may lose context, while very large chunks may contain unrelated information and make retrieval less focused. Overlap can preserve context, but too much overlap creates duplicate results and increases storage and embedding work. I will start with a simple section-based approach and adjust it after testing actual questions. I have not tested chunk sizes yet.

### Embeddings

An embedding is a list of numbers representing information in a way that allows similarity comparisons. The ingestion process creates an embedding for each text chunk. When a user asks a question, the system creates an embedding for the question using the same embedding model, then searches for nearby chunk vectors.

This is useful because a student might ask "How do I move around the model?" even if the guide uses wording like "Navigate the 3D scene." Semantic search can find related wording even when the exact keywords differ.

Important implementation details:
- Use the same embedding model and compatible dimensions for document chunks and questions.
- Store the embedding model name and dimensions in configuration or metadata so a future model change is traceable.
- If the embedding model changes, re-embed the existing chunks rather than comparing vectors from incompatible models.
- Keep the source text and metadata; the embedding is for search and does not replace the original text.
- Do not assume a high similarity score proves that a passage answers the question. The retrieved text still needs to be checked.

I have not selected an embedding provider or generated embeddings yet. I will choose after checking course requirements, cost, and API access.

### Vector search and pgvector

A vector database stores numerical embeddings and retrieves items that are close to a query vector. In this project, the query vector represents the student's question and the stored vectors represent chunks from approved XR documentation.

The pgvector extension lets PostgreSQL store vector values and perform similarity search. Its documentation describes distance operators and indexes, including:
- **Cosine distance:** compares vector direction and is a common choice for text embeddings.
- **L2 distance:** measures straight-line distance between vectors.
- **Inner product:** another supported similarity operation.

pgvector supports exact nearest-neighbor search as well as approximate indexes. Its documentation includes **HNSW** and **IVFFlat** index options. Exact search is a useful baseline for a small first corpus. Approximate indexes can make searches faster as data grows, but can trade some recall for speed and require tuning.

**Plan:** Start with ordinary PostgreSQL/pgvector similarity queries and a small document set. Only add an approximate index if performance testing shows it is needed. I should compare the quality of retrieved chunks, not choose an index only because it sounds faster.

### Vector search vs. graph retrieval: example

Consider the question: "Which setup guide should I follow for Arkio on Quest 3, and does it apply to the version installed in the lab?"

- **Vector search** can retrieve passages that discuss Arkio setup, Quest 3, and version details.
- **Graph retrieval** can represent explicit links such as Arkio — runs on — Quest 3, a setup guide — applies to — Arkio version, and a document — describes — a procedure.
- **Hybrid retrieval** can first find relevant passages by vector similarity and then follow structured relationships to gather connected facts.

A graph is more useful when the question depends on relationships across multiple facts or documents. It also adds work: entities and relationships need to be extracted, checked, stored, and kept up to date. For the first version, most expected questions are about finding instructions in a document, so vector search with useful metadata is the simpler starting point. I can reconsider a graph if evaluation shows that relationship-based questions are not being answered well.

### Import and document update design

I will treat the document collection as a small, controlled knowledge base rather than importing everything automatically.

For each source document, I plan to store:
- A stable document ID.
- Title and source URL or file location.
- Publisher or owner.
- Application/headset tags.
- Version, publication date, or last-checked date when available.
- Import date and content checksum or other way to detect a changed file.
- Permission/status note showing that the source is allowed for this project.

For each chunk, I plan to store:
- Chunk ID and document ID.
- Chunk text.
- Section heading and page number if available.
- Embedding and embedding model identifier.
- Version and relevant application/headset metadata.

When a source changes, I should reprocess the changed document's chunks and embeddings, not leave old and new instructions mixed together. If a source becomes outdated or is removed, the system should mark it inactive or remove its chunks from retrieval. Answers should include source title and version/date when available so users can judge whether instructions apply to their device and app version.

### Retrieval and answer-generation controls

The first implementation should be simple and predictable:

1. Accept a question.
2. Generate its embedding.
3. Retrieve a small set of relevant chunks, keeping their source metadata.
4. Optionally filter by headset, application, or version if the user specifies one.
5. Pass the question and retrieved passages to the language model.
6. Instruct the model to answer only from the provided passages, cite the supporting sources, and say when the sources do not contain enough information.
7. Return the answer with clickable source references.

The application should not treat retrieved documents as instructions to the model. They are reference content. The model should not follow commands that happen to appear inside a document. I will also avoid sending private or restricted lab material to an external model API.

## Evaluation plan in more detail

Before testing, I will create a small question set from the documents that are actually imported. Each question should have an expected source or expected answer points. This makes the tests repeatable.

| Check | How I will evaluate it | Evidence to save |
|---|---|---|
| Retrieval relevance | Do the top retrieved chunks contain the section needed to answer the question? | Question, retrieved chunk titles/sections, and ranking |
| Answer grounding | Can each important claim in the response be traced to a retrieved source? | Answer with source links and a short fact-check |
| Citation correctness | Do the links point to the right document and, where possible, the right page or section? | Screenshot or saved response with citations |
| Abstention | For an unsupported question, does the assistant clearly say the knowledge base does not provide the answer? | Unsupported test question and full response |
| Version awareness | Does the assistant identify the relevant version/date and avoid combining conflicting instructions? | Version-specific question, sources retrieved, and response |

I will keep a record of failed tests too. If retrieval selects the wrong section, I can adjust chunking, metadata filters, or retrieval settings. If the right source is retrieved but the answer is wrong, I need to examine the prompt and answer-generation step rather than assuming the database is the problem.

I have not run these evaluations yet. They are planned checks for the Build and Release stages.

## Technical decisions and trade-offs

| Decision | Current plan | Reason | What could make me change it |
|---|---|---|---|
| Retrieval approach | Vector search first | Most questions should locate relevant instructions in manuals and guides. | Questions regularly require joining facts across documents. |
| Database | PostgreSQL + pgvector | I already have experience with PostgreSQL, and pgvector keeps relational metadata and embeddings together. | Performance, hosting limits, or course constraints make another option more practical. |
| Chunking | Section-aware chunks with limited overlap | Keeps instructions together and preserves headings. | Testing shows chunks are too broad or lose important context. |
| Graph database | Not in the first version | Adds entity extraction and relationship maintenance before the need is proven. | Evaluation shows graph relationships would solve important unanswered questions. |
| Model access | Consider an API-based model | More practical than hosting a large model on a small server. | Course rules, cost, privacy, or access require a different setup. |
| Hosting | Reuse familiar Docker/Flask/PostgreSQL deployment patterns if suitable | Builds on my previous self-hosting experience. | The course environment or resource limits require a simpler deployment. |

## Research sources (technical)

- [pgvector — PostgreSQL vector similarity search](https://github.com/pgvector/pgvector) — vector data types, distance operators, exact search, HNSW, and IVFFlat indexes.
- [Neo4j GraphRAG for Python documentation](https://neo4j.com/docs/neo4j-graphrag-python/current/) — graph construction and retrieval options, including vector, hybrid, and graph-aware retrievers.
- [Neo4j GraphAcademy — Knowledge graphs and RAG](https://graphacademy.neo4j.com/knowledge-graph-rag) — explains how vector search finds relevant passages and graph traversal adds connected facts.
- [Neo4j GraphRAG overview](https://neo4j.com/labs/genai-ecosystem/graphrag/) — describes document chunks, entity extraction, relationships, and combining vector and graph retrieval.
- [AWS Prescriptive Guidance — Retrieval Augmented Generation options (PDF)](https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/retrieval-augmented-generation-options/retrieval-augmented-generation-options.pdf)
- [Apache Hop — GraphRAG guide](https://hop.apache.org/manual/latest/how-to-guides/graphrag.html)
- [IS373 Project 2 brief](https://njit.instructure.com/courses/70733/pages/project-2-individual-rag-app-and-technical-research)
- [IS373 research review index](https://kaw393939.github.io/is373-studio/templates/project-record.html#research-review-index)

## Checks and feedback status

- **Completed for this Plan draft:** Identified the intended users and problem, listed candidate source types, reviewed vector and graph approaches, selected a vector-first direction, compared pgvector and Neo4j documentation, and outlined chunking, embeddings, import metadata, retrieval controls, architecture, and evaluation stories.
- **Not yet completed:** Installing pgvector, importing documents, generating embeddings, implementing retrieval, connecting a language model, hosting the app, and running the five tests.
- **Peer feedback:** Not added yet. I will record feedback and any changes after receiving a review.
- **Evidence links:** The documentation links above support the initial research. Add links to implementation commits, test results, and a hosted demo during the Build and Release stages.
