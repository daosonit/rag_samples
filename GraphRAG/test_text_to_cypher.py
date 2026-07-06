import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_ollama import ChatOllama

# 1. Load biến môi trường từ file .env
load_dotenv()


print("🔗 Đang kết nối tới Neo4j (192.168.1.99)...")
NEO4J_URI = "bolt://192.168.1.99:7687"
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "SecurePassword_123!")

try:
    # LangChain sẽ tự động gọi db.schema.visualization() ngầm để học sơ đồ
    graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
    print("✅ Đã kết nối Neo4j và tải xong Schema!")
except Exception as e:
    print(f"❌ LỖI Kết nối Neo4j: {e}")
    exit(1)

# 2. Khởi tạo LLM (Sử dụng Ollama trên server 192.168.1.99)
llm = ChatOllama(
    base_url="http://192.168.1.99:11434", temperature=0, model="llama3.2-vision:latest"
)

from langchain_core.prompts import PromptTemplate

# 3. Tạo Prompt tùy chỉnh để "dạy" AI cách map Tiếng Việt vào Schema
CYPHER_GENERATION_TEMPLATE = """Task: Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

Important Vietnamese mapping rules:
- Tỉnh / Thành phố trực thuộc TW = Province
- Quận / Huyện / TP trực thuộc tỉnh = District
- Phường / Xã / Thị trấn = Ward
- Relationship: (Province)-[:HAS_DISTRICT]->(District)-[:HAS_WARD]->(Ward)

Example 1:
Question: Quận 1 có những phường nào?
Cypher: MATCH (d:District)-[:HAS_WARD]->(w:Ward) WHERE d.name CONTAINS 'Quận 1' RETURN w.name

Example 2:
Question: Phường Bến Thành thuộc tỉnh nào?
Cypher: MATCH (p:Province)-[:HAS_DISTRICT]->(d:District)-[:HAS_WARD]->(w:Ward) WHERE w.name CONTAINS 'Bến Thành' RETURN p.name

The question is:
{question}"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

# 4. Tạo QA Prompt (Dùng Tiếng Anh để Llama 3.2 hiểu Logic tốt hơn, nhưng ép trả lời bằng Tiếng Việt)
QA_TEMPLATE = """You are a helpful AI assistant. 
Use the provided information from the database to answer the user's question.
If the provided information is empty or [], say "Dạ, tôi không tìm thấy thông tin này trong cơ sở dữ liệu."
DO NOT use any external knowledge. 

IMPORTANT RULE FOR VIETNAMESE ADMINISTRATIVE UNITS:
The user might ask for "phường" (ward), but the database might return "Xã" or "Thị trấn". 
You MUST treat "Xã", "Phường", and "Thị trấn" as exactly the same thing. 
If the database returns a list of "Xã", you MUST list all of them in your final answer.

Information from Database:
{context}

User Question: {question}
Answer in Vietnamese:"""

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"], template=QA_TEMPLATE
)

# 5. Khởi tạo Chuỗi (Chain) Text-to-Cypher
print("🤖 Đang thiết lập AI Text-to-Cypher Chain...")
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    cypher_prompt=CYPHER_GENERATION_PROMPT,
    qa_prompt=QA_PROMPT,
    verbose=True,  # Bật True để xem log nó sinh lệnh Cypher
    allow_dangerous_requests=True,  # Cần thiết cho phiên bản LangChain mới
)

# 6. Đặt câu hỏi tự nhiên bằng Tiếng Việt
# Bạn có thể thay đổi câu hỏi ở đây
question = "Lục Nam có những phường nào?"

print(f"\n❓ Câu hỏi của người dùng: '{question}'\n")
print("⏳ AI đang suy nghĩ và truy vấn Database...\n" + "-" * 50)

# MATCH (d:District)-[:HAS_WARD]->(w:Ward)
# WHERE d.name CONTAINS "Quận 1"
# RETURN w.name

try:
    response = chain.invoke({"query": question})
    print("-" * 50)
    print(f"\n💡 Trả lời từ AI: {response['result']}\n")
except Exception as e:
    print(f"\n❌ Lỗi khi AI truy vấn: {e}")
