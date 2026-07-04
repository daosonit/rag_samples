import os
import argparse
from huggingface_hub import snapshot_download


def download_model(repo_id, local_dir):
    if not os.path.exists(local_dir) or not os.listdir(local_dir):
        print(f"Mô hình chưa có sẵn tại {local_dir}. Đang tiến hành tải về...")
        snapshot_download(repo_id=repo_id, local_dir=local_dir)
        print(f"✅ Đã tải xong mô hình: {repo_id}\n")
    else:
        print(f"✅ Đã tìm thấy mô hình tại {local_dir}. Bỏ qua thao tác tải.\n")


def main():
    parser = argparse.ArgumentParser(
        description="Tiện ích tải mô hình HuggingFace về máy (Offline)"
    )
    parser.add_argument(
        "--repo",
        type=str,
        help="Tên Repo (ví dụ: cross-encoder/ms-marco-MiniLM-L-6-v2)",
    )
    parser.add_argument(
        "--dir",
        type=str,
        help="Thư mục đích (ví dụ: ./local_models/ms-marco-MiniLM-L-6-v2)",
    )
    args = parser.parse_args()

    if args.repo and args.dir:
        # Nếu truyền tham số thì tải đúng model được yêu cầu
        download_model(args.repo, args.dir)
    else:
        # Nếu không truyền tham số, mặc định kiểm tra và tải các mô hình cốt lõi của khóa học
        print(
            "Không có tham số tùy chỉnh, tự động rà soát các mô hình cốt lõi của dự án RAG...\n"
        )

        # 1. Mô hình Embedding Vector (Dùng từ Bài 1 đến Bài 4.2)
        download_model(
            repo_id="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            local_dir="./local_models/paraphrase-multilingual-MiniLM-L12-v2",
        )

        # 2. Mô hình Re-ranking Cross Encoder (Dùng từ Bài 4.3)
        download_model(
            repo_id="cross-encoder/ms-marco-MiniLM-L-6-v2", 
            local_dir="./local_models/ms-marco-MiniLM-L-6-v2"
        )
        
        # 3. Siêu mô hình BGE-M3 1024 chiều (Dùng cho Module 6)
        download_model(
            repo_id="BAAI/bge-m3", 
            local_dir="./local_models/bge-m3"
        )

        # 3. Mô hình BAAI/bge-m3 (Dùng từ Bài 15)
        download_model(
            repo_id="BAAI/bge-m3",
            local_dir="./local_models/bge-m3",
        )


if __name__ == "__main__":
    main()
