import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_ollama import ChatOllama

load_dotenv(override=True)

print("🔗 [1/3] Connecting to Neo4j Database...")
# Use LangChain's built-in Neo4jGraph (No need to manually manage Neo4j driver!)
URI = os.getenv("NEO4J_URI")
AUTH = (
    os.getenv("NEO4J_USERNAME"),
    os.getenv("NEO4J_PASSWORD"),
)
graph = Neo4jGraph(url=URI, username=AUTH[0], password=AUTH[1])

# LangChain automatically scans the DB and understands the Schema!
print("✅ Automatically detected Graph Schema:")
print(graph.schema)

print("\n🧠 [2/3] Initializing AI (Llama 3.2) and GraphCypherQAChain...")
llm = ChatOllama(
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=0,
    model=os.getenv("OLLAMA_MODEL"),
)

from langchain_core.prompts import PromptTemplate

CYPHER_GENERATION_TEMPLATE = """Task: Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
CRITICAL: The proper name of an entity (like 'Apple', 'Steve Jobs') is stored in the 'id' property, NOT the 'label' property. Always use {{id: "Entity Name"}} in your MATCH clauses.

Schema:
{schema}

Question:
{question}"""

cypher_prompt = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

# THE POWER OF FRAMEWORKS: Combines Cypher Generation & QA into 1 Chain
chain = GraphCypherQAChain.from_llm(
    cypher_llm=llm,  # LLM responsible for translating text to Cypher
    qa_llm=llm,  # LLM responsible for answering based on DB results
    graph=graph,
    verbose=True,  # Set to True to watch it write Cypher queries in real-time
    allow_dangerous_requests=True,  # Required by newer LangChain versions to allow DB queries
    cypher_prompt=cypher_prompt,  # Dạy AI cách dùng đúng Property
)

question = "Who co-founded Apple?"
print(f"\n❓ [3/3] User Question: {question}")
print("⏳ Waiting for LangChain to process (Text -> Cypher -> Result -> Answer)...\n")

try:
    response = chain.invoke({"query": question})
    print("\n============================================================")
    print("🤖 LANGCHAIN'S ANSWER:")
    print("============================================================")
    print(response["result"])
except Exception as e:
    print(
        f"\n❌ Error (Likely because small Llama 3.2 generated invalid Cypher syntax): {e}"
    )
