import requests
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv(override=True)
# ==========================================
# CẤU HÌNH KẾT NỐI NEO4J
# Bạn hãy sửa thông tin đăng nhập nếu cần
# ==========================================
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
# API lấy dữ liệu hành chính Việt Nam (có bao gồm Tỉnh, Huyện, Xã)
API_URL = "https://provinces.open-api.vn/api/?depth=3"


def setup_constraints(session):
    """
    Tạo Unique Constraints (Ràng buộc duy nhất) dựa trên 'code'
    để đảm bảo không bị trùng lặp dữ liệu và truy vấn nhanh hơn.
    """
    print("Đang tạo Constraints...")
    session.run(
        "CREATE CONSTRAINT province_code_unique IF NOT EXISTS FOR (p:Province) REQUIRE p.code IS UNIQUE"
    )
    session.run(
        "CREATE CONSTRAINT district_code_unique IF NOT EXISTS FOR (d:District) REQUIRE d.code IS UNIQUE"
    )
    session.run(
        "CREATE CONSTRAINT ward_code_unique IF NOT EXISTS FOR (w:Ward) REQUIRE w.code IS UNIQUE"
    )
    print("Đã tạo xong Constraints!")


def import_data(session, data):
    """
    Đọc JSON và đẩy vào Neo4j sử dụng MERGE để tránh trùng lặp.
    """
    print(f"Đang xử lý {len(data)} Tỉnh/Thành phố...")

    for province in data:
        # 1. Tạo Node Tỉnh/Thành phố
        session.run(
            """
            MERGE (p:Province {code: $code})
            SET p.name = $name,
                p.codename = $codename,
                p.division_type = $division_type
        """,
            code=province["code"],
            name=province["name"],
            codename=province["codename"],
            division_type=province["division_type"],
        )

        # 2. Lặp qua các Quận/Huyện của Tỉnh này
        districts = province.get("districts", [])
        for district in districts:
            session.run(
                """
                MERGE (d:District {code: $code})
                SET d.name = $name,
                    d.codename = $codename,
                    d.division_type = $division_type
                WITH d
                MATCH (p:Province {code: $province_code})
                MERGE (p)-[:HAS_DISTRICT]->(d)
            """,
                code=district["code"],
                name=district["name"],
                codename=district["codename"],
                division_type=district["division_type"],
                province_code=province["code"],
            )

            # 3. Lặp qua các Phường/Xã của Quận/Huyện này
            wards = district.get("wards", [])
            for ward in wards:
                session.run(
                    """
                    MERGE (w:Ward {code: $code})
                    SET w.name = $name,
                        w.codename = $codename,
                        w.division_type = $division_type
                    WITH w
                    MATCH (d:District {code: $district_code})
                    MERGE (d)-[:HAS_WARD]->(w)
                """,
                    code=ward["code"],
                    name=ward["name"],
                    codename=ward["codename"],
                    division_type=ward["division_type"],
                    district_code=district["code"],
                )

        print(f"  -> Đã import xong: {province['name']}")


def main():
    print("Đang tải dữ liệu Tỉnh/Huyện/Xã từ API...")
    response = requests.get(API_URL)
    if response.status_code != 200:
        print("Lỗi khi tải dữ liệu từ API!")
        return

    data = response.json()
    print("Tải thành công! Bắt đầu kết nối Neo4j...")

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        setup_constraints(session)
        import_data(session, data)

    driver.close()
    print("HOÀN THÀNH TOÀN BỘ QUÁ TRÌNH IMPORT!")


if __name__ == "__main__":
    main()
