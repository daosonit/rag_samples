import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from pydantic import BaseModel, Field
from typing import List
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(override=True)


# ============================================================
# PART 1: REUSE EXTRACTION CODE FROM LESSON 2.1
# ============================================================
class Node(BaseModel):
    id: str = Field(description="Short proper noun")
    type: str = Field(description="Entity category")


class Edge(BaseModel):
    source: str = Field(description="Source node")
    target: str = Field(description="Target node")
    relation: str = Field(description="Relation (ENGLISH, UPPERCASE)")


class KnowledgeGraph(BaseModel):
    nodes: List[Node]
    edges: List[Edge]


llm = ChatOllama(
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=0,
    model=os.getenv("OLLAMA_MODEL"),
)
structured_llm = llm.with_structured_output(KnowledgeGraph)

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an excellent graph data expert.
STRICT RULES:
1. Node ID: Must be a specific proper noun (e.g., "Steve Jobs", "Apple"). DO NOT EXTRACT SENTENCES.
2. Edge Relation: MUST be translated to ENGLISH UPPERCASE, separated by underscores (e.g., CO_FOUNDED, CREATED).

FEW-SHOT EXAMPLE:
Text: "Elon Musk and JB Straubel co-founded Tesla"
Instruction: You must identify 2 separate subjects acting on 1 object.
Desired Output: 
- Nodes: Elon Musk, JB Straubel, Tesla
- Edges: (Elon Musk) -[CO_FOUNDED]-> (Tesla), (JB Straubel) -[CO_FOUNDED]-> (Tesla)
""",
        ),
        ("human", "{text}"),
    ]
)

chain = prompt_template | structured_llm

text = "Steve Jobs and Steve Wozniak co-founded Apple in 1976."
print("⏳ [1/3] Calling AI to extract Triples from text...")
graph_data = chain.invoke({"text": text})

# ============================================================
# PART 2: SAVE TO NEO4J VIA BULK INSERT (LESSON 2.2)
# ============================================================
print("\n🔗 [2/3] Connecting to Neo4j (192.168.1.99)...")
URI = os.getenv("NEO4J_URI")
AUTH = (
    os.getenv("NEO4J_USERNAME"),
    os.getenv("NEO4J_PASSWORD"),
)

try:
    driver = GraphDatabase.driver(URI, auth=AUTH)

    # Transaction function to write data
    def insert_graph_data(tx, graph):
        # 0. Delete old data (clean up DB for testing)
        tx.run("MATCH (n) DETACH DELETE n")
        print("🧹 Cleared old data in the Database.")

        # 1. Bulk insert Nodes (using UNWIND)
        nodes_list = [{"id": n.id, "label": n.type} for n in graph.nodes]
        tx.run(
            """
            UNWIND $nodes AS n
            MERGE (entity:Entity {id: n.id})
            SET entity.label = n.label
        """,
            nodes=nodes_list,
        )
        print(f"✅ Successfully written {len(nodes_list)} Nodes.")

        # 2. Bulk insert Edges
        # Trick: Group edges by Relation Type, then UNWIND each group
        edges_by_type = {}
        for e in graph.edges:
            if e.relation not in edges_by_type:
                edges_by_type[e.relation] = []
            edges_by_type[e.relation].append({"source": e.source, "target": e.target})

        for rel_type, edges in edges_by_type.items():
            # HACK: Use backticks (`) around rel_type to prevent syntax errors
            query = f"""
            UNWIND $edges AS e
            MERGE (s:Entity {{id: e.source}})
            MERGE (t:Entity {{id: e.target}})
            MERGE (s)-[:`{rel_type}`]->(t)
            """
            tx.run(query, edges=edges)

        print(
            f"✅ Successfully written {len(graph.edges)} Relationships (Including {len(edges_by_type)} types: {list(edges_by_type.keys())})."
        )

    with driver.session() as session:
        print("\n💾 [3/3] Starting data push to Database...")
        session.execute_write(insert_graph_data, graph_data)

    print(
        "\n🎉 SUCCESS! Graph Extraction Pipeline ran seamlessly from Text -> LLM -> Neo4j."
    )

except Exception as e:
    print(f"\n❌ Error: {e}")
finally:
    driver.close()
