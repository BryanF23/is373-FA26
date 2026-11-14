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

## Checks and feedback status

- **Completed for this Plan draft:** Identified the intended users and problem, listed candidate source types, reviewed vector and graph approaches, selected a vector-first direction, compared pgvector and Neo4j documentation, and outlined architecture and evaluation stories.
- **Not yet completed:** Installing pgvector, importing documents, generating embeddings, implementing retrieval, connecting a language model, hosting the app, and running the five tests.
- **Peer feedback:** Not added yet. I will record feedback and any changes after receiving a review.
- **Evidence links:** The documentation links above support the initial research. Add links to implementation commits, test results, and a hosted demo during the Build and Release stages.
