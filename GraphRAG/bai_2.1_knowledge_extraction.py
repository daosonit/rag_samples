import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# 1. Load environment variables
load_dotenv(override=True)


# 2. Define desired JSON output structure (Schema) using Pydantic
class Node(BaseModel):
    id: str = Field(
        description="Specific proper noun or entity name. Warning: Must be a short noun phrase (e.g., 'Steve Jobs', 'Apple'). Do NOT extract full sentences."
    )
    type: str = Field(
        description="Entity category (e.g., Person, Company, Location, Product)"
    )


class Edge(BaseModel):
    source: str = Field(description="Source node (subject, must match a Node id above)")
    target: str = Field(description="Target node (object, must match a Node id above)")
    relation: str = Field(
        description="Relationship between source and target. Use UPPERCASE verbs (e.g., FOUNDED, CEO_OF, CREATED)"
    )


class KnowledgeGraph(BaseModel):
    """Knowledge Graph containing a list of Nodes and Edges"""

    nodes: List[Node] = Field(description="List of extracted entities")
    edges: List[Edge] = Field(description="List of relationships between entities")


# 3. Initialize LLM
llm = ChatOllama(
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=0,
    model=os.getenv("OLLAMA_MODEL"),
)

structured_llm = llm.with_structured_output(KnowledgeGraph)

# 4. Sample text for extraction
text = """
Steve Jobs and Steve Wozniak co-founded Apple on April 1, 1976 in Cupertino, California.
Apple is famous for creating the iPhone.
In 2011, Tim Cook became the CEO of Apple after Steve Jobs resigned.
"""

print(f"📄 ORIGINAL TEXT:\n{text}\n")
print("⏳ AI is reading and extracting the Knowledge Graph... (please wait)\n")

# 5. Execute with Prompt Engineering
try:
    # System Prompt to guide the AI
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an excellent graph data expert. 
Your task is to read the text and extract entities (Nodes) and relationships (Edges).
STRICT RULES:
1. Node ID must be a short proper noun (e.g., "Steve Jobs", "Apple", "iPhone", "Tim Cook"). DO NOT extract full sentences.
2. Edge Relation MUST be in UPPERCASE ENGLISH, separated by underscores (e.g., CO_FOUNDED, CREATED, BECAME_CEO).
Be extremely accurate!""",
            ),
            ("human", "Text to extract:\n{text}"),
        ]
    )

    # Connect Prompt with LLM
    chain = prompt_template | structured_llm

    result = chain.invoke({"text": text})

    print("✅ EXTRACTION RESULT AFTER PROMPT ENGINEERING:")
    print("\n--- List of Nodes ---")
    for node in result.nodes:
        print(f"  [{node.type}] {node.id}")

    print("\n--- List of Edges (Triples) ---")
    for edge in result.edges:
        print(f"  ({edge.source}) -[{edge.relation}]-> ({edge.target})")

except Exception as e:
    print(f"❌ Extraction error: {e}")
