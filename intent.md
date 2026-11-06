# CyberJob Radar VN — Product Intent v1.0

> **Trạng thái:** Đặc tả định hướng cho MVP, chưa phải mô tả tính năng đã triển khai  
> **Phiên bản tài liệu:** 1.0  
> **Sản phẩm:** CyberJob Radar VN  
> **Đối tượng sử dụng:** Cá nhân (một người dùng)  
> **Nền tảng:** Website chạy cục bộ trên máy Windows  
> **Ngôn ngữ tài liệu:** Tiếng Việt

## 1. Tầm nhìn (Vision)

CyberJob Radar VN là công cụ cá nhân giúp **tìm, tổng hợp và theo dõi tin tuyển dụng An toàn thông tin/An ninh mạng tại Việt Nam** từ những nguồn được phép truy xuất.

Thay vì phải mở nhiều website tuyển dụng mỗi ngày, người dùng có thể:

1. Xem danh sách tin tuyển dụng phù hợp trên một dashboard duy nhất.
2. Tìm kiếm và lọc vị trí theo từ khóa, nhóm công việc, cấp bậc và địa điểm.
3. Mở trực tiếp bài đăng gốc để đọc chi tiết và ứng tuyển.
4. Lưu các vị trí quan tâm, ghi chú và theo dõi tiến trình ứng tuyển.
5. Biết lần cập nhật gần nhất của từng nguồn, tránh nhầm dữ liệu cũ với tin mới.

**Tuyên bố giá trị:** *Một nơi để phát hiện cơ hội nghề nghiệp cybersecurity tại Việt Nam và quản lý hành trình ứng tuyển cá nhân.*

## 2. Vấn đề cần giải quyết

- Tin tuyển dụng ATTT phân tán trên nhiều trang và website doanh nghiệp.
- Cùng một tin có thể được đọc lại nhiều lần, khó nhận biết tin mới.
- Tìm kiếm bằng từ khóa chung như `security` dễ lẫn việc bảo vệ vật lý hoặc công việc không thuộc cybersecurity.
- Khó quản lý các tin đã quan tâm, đã ứng tuyển và tiến trình tuyển dụng nếu chỉ dùng bookmark trình duyệt.
- Một số trang không công bố đầy đủ ngày đăng hoặc hạn tuyển; hệ thống cần thể hiện rõ dữ liệu thiếu thay vì suy đoán.

## 3. Người dùng và kịch bản chính

**Người dùng duy nhất của v1:** Chủ sở hữu công cụ, đang theo dõi cơ hội thực tập và vị trí đầu vào trong ngành cybersecurity tại Việt Nam.

**Ưu tiên tìm kiếm:** SOC Analyst / Security Operations Center, Blue Team, Network Security, Information Security, Cybersecurity Intern, Fresher và Junior.

### User journey mong muốn

1. Máy chạy tác vụ thu thập theo lịch (mặc định mỗi 12 giờ khi máy có thể thực thi tác vụ).
2. Công cụ đọc các nguồn đã cấu hình, chuẩn hóa và lưu tin hợp lệ vào database.
3. Người dùng mở dashboard tại `http://localhost:8501`.
4. Người dùng lọc `Intern`, `SOC`, `TP. Hồ Chí Minh` (hoặc điều kiện khác).
5. Người dùng xem thông tin tóm tắt rồi mở `apply_url` đến tin gốc.
6. Người dùng đánh dấu đã lưu hoặc cập nhật trạng thái `Applied`, thêm ghi chú và ngày ứng tuyển.
7. Khi quay lại, thông tin theo dõi và lịch sử tin vẫn còn.

## 4. Phạm vi v1.0 (In scope)

### 4.1. Thu thập dữ liệu

- Có cơ chế **source adapter** để kết nối từng nguồn dữ liệu tuyển dụng.
- Trước mắt triển khai tối thiểu **một nguồn thực tế, được phép truy cập**, ưu tiên API công khai/được cấp phép theo từng doanh nghiệp (ví dụ Greenhouse hoặc Lever khi có board phù hợp).
- Có khả năng mở rộng để bổ sung nguồn thứ hai mà không sửa core processing.
- Cho phép bật/tắt nguồn bằng cấu hình.
- Thu thập bằng lệnh Python CLI; cấu hình chạy định kỳ với Windows Task Scheduler.
- Có timeout, giới hạn tốc độ hợp lý và cơ chế thử lại có kiểm soát khi nguồn tạm lỗi.
- Ghi nhật ký từng lần chạy và lỗi theo từng nguồn.

### 4.2. Xử lý dữ liệu

- Chuẩn hóa mỗi tin về một mô hình dữ liệu chung.
- Phân loại theo từ khóa/quy tắc: SOC, Network Security, General Security và nhóm liên quan.
- Nhận diện cấp bậc: `intern`, `fresher`, `junior`, `other` hoặc `unknown`.
- Ưu tiên vị trí tại Việt Nam; khi không đủ thông tin địa điểm, đánh dấu `unknown`, không tự đoán.
- Loại các chức danh không liên quan như `security guard` / `nhân viên bảo vệ`.
- Không tạo trùng tin từ cùng nguồn: định danh bằng `(source_id, external_id)`; fallback từ URL chuẩn hóa khi không có ID đáng tin cậy.
- Lưu `first_seen_at` và `last_seen_at` độc lập với `posted_at`.
- Không mặc định xem tin là đã đóng sau một lần không tìm thấy.

### 4.3. Dashboard

Website chạy cục bộ bằng **Streamlit**, gồm ba trang:

**A. Job Explorer**
- Danh sách tin tuyển dụng, sắp xếp theo lần phát hiện gần nhất hoặc ngày đăng nếu có.
- Tìm kiếm theo tiêu đề, công ty, mô tả/từ khóa.
- Bộ lọc tối thiểu: nhóm công việc, cấp bậc, địa điểm, nguồn.
- Mỗi tin hiển thị: chức danh, công ty, địa điểm, cấp bậc, nhóm công việc, nguồn, ngày đăng (nếu có), lần hệ thống phát hiện/cập nhật.
- Nút **Xem tin gốc / Ứng tuyển** mở đúng URL nguồn; không nộp hồ sơ trực tiếp trong CyberJob Radar VN.
- Nút **Lưu tin** để theo dõi sau.

**B. My Tracking**
- Xem danh sách tin đã lưu hoặc đã ứng tuyển.
- Cập nhật trạng thái: `not_applied`, `applied`, `interview`, `offer`, `rejected`, `withdrawn`.
- Nhập ghi chú cá nhân và ngày ứng tuyển (nếu có).
- Lưu bền vững vào database, không chỉ lưu ở Streamlit Session State.

**C. Collector Monitor**
- Hiển thị nguồn đang bật, thời điểm cập nhật thành công gần nhất.
- Hiển thị lịch sử chạy và số lượng tin lấy được, tin phù hợp, tin mới, tin cập nhật.
- Hiển thị lỗi/nguồn thất bại; phân biệt rõ **chưa có tin mới** với **thu thập thất bại**.

### 4.4. Vận hành và kiểm thử

- Chạy bằng môi trường Python `venv` và lệnh CLI.
- Database SQLite lưu trên máy cá nhân.
- Có `README.md` giải thích cài đặt, cấu hình nguồn, chạy collector, mở dashboard.
- Có `.env.example`, `.gitignore`, bộ test tối thiểu cho phân loại, chống trùng và theo dõi ứng tuyển.
- Không commit database cá nhân, secret, file `.env` hoặc log nhạy cảm lên GitHub.

## 5. Không thuộc phạm vi v1.0 (Out of scope)

- Đăng ký/đăng nhập và phân quyền nhiều người dùng.
- Đưa website công khai cho cộng đồng hoặc triển khai production 24/7.
- Nộp hồ sơ tự động, đăng nhập tài khoản tuyển dụng, thao tác ứng tuyển thay người dùng.
- AI/LLM để chấm điểm CV, phân tích JD hay gợi ý công việc nâng cao.
- Phân tích toàn bộ thị trường việc làm, bảo đảm bao phủ tất cả trang tuyển dụng Việt Nam.
- Tự động vượt CAPTCHA, proxy rotation né chặn, scraping trái điều khoản dịch vụ.
- Redis, Celery, Kafka, microservices, API backend FastAPI, frontend React.
- Thông báo Telegram/email, hệ thống theo dõi mức lương, lịch phỏng vấn tự động (để dành phiên bản tiếp theo).

## 6. Quyết định kiến trúc

**Kiểu kiến trúc:** Python modular monolith, chia lớp rõ ràng.

```text
Nguồn tuyển dụng được phép
         |
         v
Collectors (các source adapter)
         |
         v
Processing (normalize -> validate -> classify -> deduplicate)
         |
         v
Repositories <--> SQLite
         ^
         |
Services (jobs, tracking, collector orchestration)
         ^
         |
Streamlit Dashboard

Windows Task Scheduler --> Python CLI --> Collector Service
```

### Phân chia trách nhiệm

| Thành phần | Trách nhiệm |
|---|---|
| `collectors` | Gọi API/truy xuất dữ liệu nguồn và chuyển thành cấu trúc đầu vào thống nhất |
| `processing` | Chuẩn hóa, kiểm tra, phân loại, loại trùng |
| `database` | SQLAlchemy models, connection, repositories và transaction |
| `services` | Điều phối ca sử dụng, không phụ thuộc trực tiếp giao diện |
| `dashboard` | Hiển thị dữ liệu, nhận thao tác người dùng |
| `cli` | Điểm chạy tác vụ thu thập từ terminal hoặc Task Scheduler |
| `config` | Danh sách nguồn và bộ từ khóa |

**Nguyên tắc:** Dashboard không trực tiếp crawl; collector không chứa UI; giao diện và tác vụ thu thập dùng chung Service/Repository.

### Stack chính

- Python 3.11+ (chọn một phiên bản cụ thể khi khởi tạo dự án)
- HTTPX; BeautifulSoup khi nguồn trả nội dung HTML cần trích xuất
- SQLAlchemy 2.x + SQLite
- Streamlit
- PyYAML, python-dotenv
- pytest
- Windows Task Scheduler cho lịch chạy; chưa cần dịch vụ hàng đợi tác vụ

## 7. Cấu trúc thư mục dự kiến

```text
cyberjob-radar-vn/
├── config/
│   ├── sources.yaml
│   └── keywords.yaml
├── data/                         # Dữ liệu cục bộ (gitignored)
├── src/
│   └── cyberjob/
│       ├── __init__.py
│       ├── config.py
│       ├── cli.py
│       ├── collectors/
│       │   ├── base.py
│       │   ├── greenhouse.py
│       │   └── lever.py
│       ├── processing/
│       │   ├── normalizer.py
│       │   ├── validator.py
│       │   ├── classifier.py
│       │   └── deduplicator.py
│       ├── database/
│       │   ├── connection.py
│       │   ├── models.py
│       │   └── repositories.py
│       ├── services/
│       │   ├── collector_service.py
│       │   ├── job_service.py
│       │   └── tracking_service.py
│       └── dashboard/
│           ├── app.py
│           └── pages/
│               ├── 1_Jobs.py
│               ├── 2_Tracking.py
│               └── 3_Collector.py
├── tests/
│   ├── fixtures/
│   ├── test_collector.py
│   ├── test_classifier.py
│   ├── test_deduplicator.py
│   └── test_tracking.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── intent.md
```

## 8. Hợp đồng dữ liệu (Data contract)

Thiết kế v1 ưu tiên **4 bảng**. Thời gian trong DB lưu theo UTC, giao diện quy đổi sang múi giờ Việt Nam khi hiển thị; các trường không được nguồn cung cấp phải cho phép `NULL`.

### `sources`

| Cột | Kiểu/ý nghĩa |
|---|---|
| `id` | INTEGER PK |
| `name` | TEXT NOT NULL — tên nguồn/board |
| `provider` | TEXT NOT NULL — `greenhouse`, `lever`, ... |
| `external_key` | TEXT NOT NULL — định danh board/site |
| `is_active` | BOOLEAN NOT NULL DEFAULT TRUE |
| `last_success_at` | DATETIME NULL |

Ràng buộc đề xuất: `UNIQUE(provider, external_key)`.

### `jobs`

| Cột | Kiểu/ý nghĩa |
|---|---|
| `id` | INTEGER PK |
| `source_id` | INTEGER FK -> `sources.id` |
| `external_id` | TEXT NOT NULL — ID ổn định trong nguồn |
| `title` | TEXT NOT NULL |
| `company` | TEXT NOT NULL |
| `location_text` | TEXT NULL |
| `seniority` | TEXT NOT NULL DEFAULT `unknown` |
| `category` | TEXT NOT NULL DEFAULT `unknown` |
| `description_excerpt` | TEXT NULL |
| `apply_url` | TEXT NOT NULL |
| `posted_at` | DATETIME NULL |
| `deadline_at` | DATETIME NULL |
| `first_seen_at` | DATETIME NOT NULL |
| `last_seen_at` | DATETIME NOT NULL |
| `listing_status` | TEXT NOT NULL DEFAULT `listed` |

Ràng buộc bắt buộc: `UNIQUE(source_id, external_id)`; index cho `first_seen_at`, `seniority`, `category` và `source_id`. Ở v1 chỉ chống trùng **trong từng nguồn**; việc hợp nhất cùng một tin xuất hiện tại nhiều nguồn được hoãn lại.

`listing_status` có thể dùng `listed`, `not_seen`, `closed`; chỉ đổi trạng thái khi có chứng cứ đủ tin cậy. Không xóa tin đang theo dõi chỉ vì nguồn không còn trả về.

### `job_tracking`

| Cột | Kiểu/ý nghĩa |
|---|---|
| `job_id` | INTEGER PK, FK -> `jobs.id` (1 tin có tối đa 1 bản theo dõi cá nhân) |
| `is_saved` | BOOLEAN NOT NULL DEFAULT FALSE |
| `application_stage` | TEXT NOT NULL DEFAULT `not_applied` |
| `notes` | TEXT NULL |
| `applied_at` | DATETIME NULL |
| `updated_at` | DATETIME NOT NULL |

`application_stage`: `not_applied`, `applied`, `interview`, `offer`, `rejected`, `withdrawn`. `is_saved` độc lập với trạng thái ứng tuyển.

### `crawl_runs`

| Cột | Kiểu/ý nghĩa |
|---|---|
| `id` | INTEGER PK |
| `source_id` | INTEGER FK -> `sources.id` |
| `started_at` | DATETIME NOT NULL |
| `finished_at` | DATETIME NULL |
| `status` | TEXT NOT NULL — `running`, `success`, `partial`, `failed` |
| `fetched_count` | INTEGER NOT NULL DEFAULT 0 |
| `matched_count` | INTEGER NOT NULL DEFAULT 0 |
| `inserted_count` | INTEGER NOT NULL DEFAULT 0 |
| `updated_count` | INTEGER NOT NULL DEFAULT 0 |
| `error_message` | TEXT NULL |

## 9. Hành vi dữ liệu và độ tin cậy

1. **Không đoán ngày đăng:** `posted_at = NULL` khi không có dữ liệu; dùng `first_seen_at` để biểu diễn *ngày hệ thống phát hiện*.
2. **Không đoán tin còn tuyển:** cần nhãn/ghi chú rõ rằng tin đã được thấy tại lần kiểm tra nào; người dùng xác nhận tình trạng ở trang gốc.
3. **Không ghi trùng:** upsert theo `(source_id, external_id)`.
4. **Không mất dữ liệu theo dõi:** cập nhật job không được ghi đè `job_tracking`; dữ liệu ứng tuyển tồn tại qua lần thu thập mới.
5. **Không làm hỏng toàn bộ chu kỳ vì một nguồn lỗi:** xử lý và log theo từng nguồn.
6. **Không lưu bừa dữ liệu nhạy cảm:** chỉ lưu metadata việc làm, URL và ghi chú cá nhân; tránh ghi credentials, cookies, thông tin đăng nhập của bên thứ ba.
7. **Tôn trọng nguồn:** chỉ thu thập ở API/trang được phép, không né cơ chế bảo vệ hay vượt CAPTCHA, kiểm tra điều khoản sử dụng và giới hạn truy cập trước khi kích hoạt nguồn.
8. **Độ phủ có giới hạn:** một vài board trên Greenhouse/Lever không đại diện cho toàn bộ thị trường tuyển dụng cybersecurity tại Việt Nam.

## 10. Điều kiện nghiệm thu v1.0 (Definition of Done)

- [ ] Cài đặt và chạy được trên Windows theo hướng dẫn trong `README.md`.
- [ ] Có ít nhất **1 nguồn thật** được phép truy cập và có dữ liệu tuyển dụng phù hợp để kiểm thử end-to-end; nếu chưa có, trạng thái nguồn là blocker thay vì dùng dữ liệu giả và tuyên bố hoàn thành.
- [ ] Có thể chạy collector bằng CLI; kết quả được lưu vào SQLite.
- [ ] Chạy lại collector không tạo tin trùng từ cùng nguồn.
- [ ] Phân loại được các trường hợp cơ bản như `SOC Analyst Intern` và loại `Security Guard`.
- [ ] Dashboard hiển thị được dữ liệu, tìm kiếm và lọc theo cấp bậc/nhóm công việc/địa điểm/nguồn.
- [ ] Bấm `Xem tin gốc` mở đúng liên kết bài đăng của nguồn.
- [ ] Có thể lưu tin, sửa trạng thái và ghi chú ứng tuyển; dữ liệu tồn tại sau khi khởi động lại ứng dụng.
- [ ] Có lịch sử thu thập và thông báo lỗi nguồn rõ ràng.
- [ ] Cấu hình chạy mỗi 12 giờ, có hướng dẫn xử lý khi máy không hoạt động đúng lịch.
- [ ] Tests cơ bản pass; `.env` và database cá nhân không bị commit lên Git.

## 11. Thứ tự triển khai

| Giai đoạn | Phạm vi | Kết quả bàn giao |
|---|---|---|
| 0 — Source validation | Xác minh ít nhất 1 nguồn hợp lệ, dữ liệu có vị trí tại Việt Nam | Ví dụ response + quy tắc truy cập rõ ràng |
| 1 — Database | Models, SQLite, repositories, CRUD tests | Lưu/đọc được nguồn, job, tracking, crawl run |
| 2 — Collector | Adapter đầu tiên, normalizer, validator, classifier, deduplicator, CLI | Một lệnh thu thập thật, chống trùng |
| 3 — Dashboard | Job Explorer, My Tracking, Collector Monitor | Website localhost có thể sử dụng |
| 4 — Automation & hardening | Scheduler, retries, logging, tests, README | Tự cập nhật, vận hành cá nhân ổn định |

## 12. Các quyết định để dành cho v1.1+

- Thêm API adapter/nguồn tuyển dụng khác sau khi kiểm tra tính hợp lệ và chất lượng dữ liệu.
- Thông báo khi có công việc mới hợp tiêu chí qua Telegram/email.
- Chấm điểm mức phù hợp theo kỹ năng, địa điểm, kinh nghiệm.
- Dò tin giống nhau giữa các nguồn bằng quy tắc hoặc semantic matching.
- Lưu các phiên bản thay đổi của tin tuyển dụng và theo dõi khi JD thay đổi.
- Thêm FastAPI + React nếu xuất hiện nhu cầu tách frontend hoặc phục vụ nhiều người dùng.
- Chuyển SQLite sang PostgreSQL nếu quy mô hoặc truy cập đồng thời thực sự yêu cầu.

## 13. Nguyên tắc kiểm soát scope

> **Ưu tiên xây một công cụ hoạt động được với dữ liệu tuyển dụng thật, hơn một website đẹp nhưng chưa thu thập được gì.**

Mọi tính năng đề xuất cho v1.0 cần trả lời được ít nhất một câu hỏi:

- Nó có giúp **thu thập dữ liệu đúng và đáng tin cậy** hơn không?
- Nó có giúp **tìm việc và đi tới nguồn ứng tuyển** nhanh hơn không?
- Nó có giúp **theo dõi đơn ứng tuyển cá nhân** rõ ràng hơn không?
- Nó có giúp **phát hiện lỗi thu thập** và vận hành ổn định hơn không?

Nếu không, mặc định chuyển vào backlog v1.1+.
