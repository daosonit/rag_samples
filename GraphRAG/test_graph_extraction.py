import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_neo4j import Neo4jGraph, LLMGraphTransformer
from langchain_ollama import ChatOllama

# 1. Load biến môi trường
load_dotenv()

# 2. Kết nối Neo4j
print("🔗 Đang kết nối tới Neo4j (192.168.1.99)...")
NEO4J_URI = "bolt://192.168.1.99:7687"
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "SecurePassword_123!")

try:
    graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
    print("✅ Đã kết nối Neo4j thành công!")
except Exception as e:
    print(f"❌ LỖI Kết nối Neo4j: {e}")
    exit(1)

# 3. Khởi tạo LLM (Ollama trên server 192.168.1.99)
# Bóc tách thông tin (NER) cần khả năng tư duy logic tốt. Llama 3.2 8B làm khá ổn.
llm = ChatOllama(
    base_url="http://192.168.1.99:11434", temperature=0, model="llama3.2-vision:latest"
)

# 4. Tạo LLMGraphTransformer
# Đây là công cụ ma thuật tự động gọi AI để đọc Text và nhả ra Graph Documents
print("🤖 Đang thiết lập LLM Graph Transformer...")
llm_transformer = LLMGraphTransformer(llm=llm)

# 5. Cung cấp một đoạn văn bản thô
text = """
Tố Hữu tên khai sinh là Nguyễn Kim Thành. Ông sinh ngày 4 tháng 10 năm 1920 tại Thừa Thiên (nay là thành phố Huế), là con út trong gia đình. Đến năm 9 tuổi, ông cùng cha trở về sống tại làng Phù Lai, nay thuộc xã Quảng Điền, thành phố Huế. Cha ông là một nhà nho nghèo, không đỗ đạt và phải kiếm sống rất chật vật nhưng lại thích thơ, thích sưu tập ca dao tục ngữ. Ông đã dạy Tố Hữu làm thơ cổ. Mẹ ông cũng là con của một nhà nho nghèo nhưng thuộc nhiều ca dao dân ca Huế và rất yêu thương con. Cha mẹ đã góp phần nuôi dưỡng tâm hồn thơ Tố Hữu.
"""
print("\n📄 Văn bản gốc:")
print(text)

# Đóng gói text thành dạng Document của LangChain
documents = [Document(page_content=text)]

# 6. Biến đổi Text thành Graph (Triples)
print(
    "\n⏳ AI đang đọc và bóc tách thực thể... (có thể mất vài chục giây do phải sinh ra JSON format)"
)
try:
    # Bước này là bước tốn thời gian nhất vì AI phải đọc kỹ và nhặt ra từng chủ ngữ, vị ngữ
    graph_documents = llm_transformer.convert_to_graph_documents(documents)

    # In ra kết quả để xem AI đã "hiểu" được gì
    print("\n--- KẾT QUẢ BÓC TÁCH ---")
    for i, doc in enumerate(graph_documents):
        print(f"\nNodes (Thực thể):")
        for node in doc.nodes:
            print(f"  - [{node.type}] {node.id}")

        print(f"\nRelationships (Mối quan hệ):")
        for rel in doc.relationships:
            print(f"  - ({rel.source.id}) -[:{rel.type}]-> ({rel.target.id})")

    # 7. Lưu thẳng vào Neo4j Database
    print("\n💾 Đang lưu dữ liệu vào Neo4j...")
    # Hàm này tự động sinh ra các lệnh UNWIND MERGE để lưu vào Neo4j với tốc độ cực nhanh
    graph.add_graph_documents(graph_documents)
    print("🎉 Thành công! Dữ liệu đã nằm gọn trong Neo4j của bạn.")
    print(
        "💡 Gợi ý: Hãy mở Neo4j Browser (http://localhost:7474) và chạy lệnh: MATCH (n) RETURN n LIMIT 50 để xem các thực thể VinFast, Vingroup trên đồ thị!"
    )

except Exception as e:
    print(f"\n❌ Lỗi khi bóc tách: {e}")
