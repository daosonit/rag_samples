import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from pydantic import BaseModel, Field
from typing import List
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv(override=True)

# ============================================================
# AI AND NEO4J CONFIGURATION
# ============================================================
llm = ChatOllama(
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=0,
    model=os.getenv("OLLAMA_MODEL"),
)

URI = os.getenv("NEO4J_URI")
AUTH = (
    os.getenv("NEO4J_USERNAME"),
    os.getenv("NEO4J_PASSWORD"),
)


class EntitiesExtraction(BaseModel):
    names: List[str] = Field(
        description="List of proper nouns, names of people or organizations in the question"
    )


entity_extractor = llm.with_structured_output(EntitiesExtraction)

# ============================================================
# RUN ENTITY RETRIEVAL PIPELINE (SUB-GRAPH EXTRACTION)
# ============================================================

# Simulate user asking a question
question = "According to the data, what is the relationship between Hồ Chí Minh, Nguyễn Tất Thành, and Việt Nam?"
print(f"❓ USER QUESTION: {question}\n")

# STEP 1: Extract Entities from the question Mục đích: Bắt AI đọc câu hỏi và "nhặt" ra các danh từ riêng quan trọng.
print("⏳ [1/4] Using AI to extract Keywords from the question...")
extractor_prompt = f"Extract the names of people or companies from the following sentence: '{question}'"
extracted = entity_extractor.invoke(extractor_prompt)
print(f"✅ Found Entities: {extracted.names}\n")

# STEP 2: Find "neighbors" on Neo4j (Graph Traversal) Tìm những Node nào có tên khớp với Keyword, sau đó bốc toàn bộ các Node và Mối quan hệ xung quanh nó (trong bán kính 1 bước nhảy / depth 1).
print("🔗 [2/4] Scanning Neo4j to retrieve Sub-graph...")
context_triples = []

try:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        for entity_name in extracted.names:
            # Fixed Cypher query: Find Nodes containing the keyword, get all relationships at depth 1
            query = """
            MATCH (n:Entity)-[r]-(m:Entity)
            WHERE n.id CONTAINS $name OR m.id CONTAINS $name
            RETURN n.id AS source, type(r) AS relation, m.id AS target
            """
            result = session.run(query, name=entity_name)
            for record in result:
                triple = f"({record['source']}) -[{record['relation']}]-> ({record['target']})"
                print(triple)
                if triple not in context_triples:
                    context_triples.append(triple)
    driver.close()
except Exception as e:
    print(f"❌ Neo4j Error: {e}")

print("✅ Context retrieved from Graph:")
if not context_triples:
    print("  (No relevant data found)")
for t in context_triples:
    print(f"  - {t}")
print()

# STEP 3: Force AI to answer based on Graph Context
print("🧠 [3/4] Synthesizing final answer...")
context_text = "\n".join(context_triples)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a smart AI assistant. Answer the user's question BASED ONLY ON THE PROVIDED DATA.
Do not hallucinate or make things up. If the data is insufficient, say you don't know.
DATA (Extracted from Knowledge Graph):
{context}""",
        ),
        ("human", "{question}"),
    ]
)

qa_chain = qa_prompt | llm | StrOutputParser()
answer = qa_chain.invoke({"context": context_text, "question": question})

print("\n============================================================")
print("🤖 GRAPHRAG SYSTEM ANSWER:")
print("============================================================")
print(answer)
