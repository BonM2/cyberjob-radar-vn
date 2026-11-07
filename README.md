# CyberJob Radar VN

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Mục tiêu](#mục-tiêu)
- [Kiến trúc dự kiến](#kiến-trúc-dự-kiến)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Công nghệ](#công-nghệ)
- [Cài đặt và chuẩn bị](#cài-đặt-và-chuẩn-bị)
- [Hướng phát triển](#hướng-phát-triển)

## Giới thiệu

CyberJob Radar VN được định hướng là công cụ cá nhân tổng hợp tin tuyển dụng An toàn thông tin và An ninh mạng tại Việt Nam. MVP v1.0 dành cho một người dùng và chạy cục bộ trên Windows.

Hệ thống dự kiến tự kiểm tra các nguồn tuyển dụng đã được cấu hình và xác minh; chuẩn hóa, phân loại, chống trùng và hiển thị tin trên dashboard. Người dùng có thể tìm kiếm, lọc, lưu tin, theo dõi quá trình ứng tuyển và mở bài tuyển dụng gốc để tự ứng tuyển. **Các chức năng này chưa được triển khai.**

## Mục tiêu

- Tự động kiểm tra những nguồn tuyển dụng đã cấu hình, giảm thời gian tìm việc trên nhiều trang.
- Ưu tiên cơ hội Intern, Fresher và Junior trong lĩnh vực cybersecurity tại Việt Nam.
- Tập trung thông tin việc làm và tiến trình ứng tuyển cá nhân tại một nơi.

## Kiến trúc dự kiến

Dự án được định hướng theo **Python modular monolith**:

```text
Nguồn tuyển dụng → Collectors → Processing → Repositories → SQLite
                                   ↑               ↑
                             Services ──────────────┘
                                ↑
                     Streamlit Dashboard / CLI
```

Collector thu thập dữ liệu nguồn; processing chuẩn hóa, xác thực, phân loại và chống trùng; repositories quản lý việc lưu và đọc SQLite. Services điều phối các chức năng, còn dashboard hiển thị thông tin và nhận thao tác người dùng. CLI dự kiến chạy collector theo lịch qua Windows Task Scheduler. Sơ đồ mô tả thiết kế, chưa phải luồng đang hoạt động.

## Cấu trúc dự án

Các đường dẫn dưới đây hiện có trong cây làm việc; các file source, cấu hình và test đều là placeholder rỗng.

```text
cyberjob-radar-vn/                   # Thư mục gốc dự án
├── config/                          # Cấu hình nguồn và từ khóa
│   ├── keywords.yaml                # Từ khóa phân loại dự kiến
│   └── sources.yaml                 # Nguồn tuyển dụng dự kiến
├── data/                            # Nơi lưu dữ liệu cục bộ dự kiến
│   └── .gitkeep                     # Giữ thư mục trong Git
├── docs/                            # Tài liệu dự án; hiện đang trống
├── src/                             # Mã nguồn dự án
│   └── cyberjob/                    # Package chính
│       ├── __init__.py              # Khởi tạo package
│       ├── cli.py                   # Điểm chạy CLI dự kiến
│       ├── config.py                # Quản lý cấu hình dự kiến
│       ├── collectors/              # Thu thập dữ liệu từ nguồn tuyển dụng
│       │   ├── __init__.py          # Khởi tạo package collectors
│       │   └── base.py              # Giao diện collector cơ sở dự kiến
│       ├── processing/              # Xử lý và phân loại dữ liệu
│       │   ├── __init__.py          # Khởi tạo package processing
│       │   ├── classifier.py        # Phân loại tin dự kiến
│       │   ├── deduplicator.py      # Chống trùng tin dự kiến
│       │   ├── normalizer.py        # Chuẩn hóa dữ liệu dự kiến
│       │   └── validator.py         # Xác thực dữ liệu dự kiến
│       ├── database/                # Quản lý lưu trữ SQLite
│       │   ├── __init__.py          # Khởi tạo package database
│       │   ├── connection.py        # Kết nối database dự kiến
│       │   ├── models.py            # Các model dữ liệu dự kiến
│       │   └── repositories.py      # Thao tác đọc/ghi dữ liệu dự kiến
│       ├── services/                # Điều phối nghiệp vụ
│       │   ├── __init__.py          # Khởi tạo package services
│       │   ├── collector_service.py # Điều phối thu thập dự kiến
│       │   ├── job_service.py       # Xử lý tin tuyển dụng dự kiến
│       │   └── tracking_service.py  # Theo dõi ứng tuyển dự kiến
│       └── dashboard/               # Giao diện Streamlit dự kiến
│           ├── __init__.py          # Khởi tạo package dashboard
│           ├── app.py               # Điểm chạy dashboard dự kiến
│           └── pages/               # Các trang giao diện dự kiến
│               ├── 1_Jobs.py        # Trang danh sách tin
│               ├── 2_Tracking.py    # Trang theo dõi ứng tuyển
│               └── 3_Collector.py   # Trang giám sát thu thập
├── tests/                           # Các bài kiểm thử dự kiến
│   ├── fixtures/                    # Dữ liệu mẫu cho kiểm thử
│   │   └── .gitkeep                 # Giữ thư mục trong Git
│   ├── test_classifier.py          # Kiểm thử phân loại dự kiến
│   ├── test_collector.py            # Kiểm thử collector dự kiến
│   ├── test_deduplicator.py         # Kiểm thử chống trùng dự kiến
│   └── test_tracking.py             # Kiểm thử theo dõi dự kiến
├── .env.example                     # Mẫu biến môi trường dự kiến
├── .gitignore                       # Quy tắc loại trừ Git dự kiến
├── AGENTS.md                        # Hướng dẫn làm việc cho AI Agent
├── CLAUDE.md                        # Tham chiếu đến AGENTS.md
├── pyproject.toml                   # Cấu hình Python và dependency dự kiến
└── README.md                        # Giới thiệu và hướng dẫn dự án
```

## Công nghệ
| Công nghệ | Vai trò |
|---|---|
| Python 3.11+ | Ngôn ngữ lập trình chính. |
| HTTPX | Gửi HTTP request để thu thập dữ liệu. |
| SQLAlchemy 2.x | ORM và thao tác database. |
| SQLite | Database cục bộ. |
| Streamlit | Dashboard trên trình duyệt. |
| pytest | Kiểm thử. |
| Windows Task Scheduler | Lên lịch chạy collector trên Windows. |

## Cài đặt và chuẩn bị

```powershell
git clone https://github.com/BonM2/cyberjob-radar-vn.git
```

## Hướng phát triển

- Xác minh và bổ sung các nguồn tuyển dụng hợp lệ.
- Xây dựng và cải thiện quy tắc phân loại tin.
- Hoàn thiện Job Tracking và dashboard.
- Tự động hóa việc thu thập sau khi collector hoạt động.
