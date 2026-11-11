# CyberJob Radar VN — Source Validation

> **Dự án:** CyberJob Radar VN — MVP sản phẩm v1.0
> **Phiên bản tài liệu:** 0.2 — cập nhật kết quả smoke test Axon ngày 11/11/2026
> **Giai đoạn SDLC:** Phase 0 — Requirements Analysis & Feasibility / Source Validation  
> **Trạng thái:** `IN PROGRESS` — **chưa có nguồn cụ thể đạt `verified`**  
> **Phạm vi:** Công cụ cá nhân chạy cục bộ, tổng hợp tin tuyển dụng cybersecurity tại Việt Nam

## 1. Mục tiêu và nguyên tắc xác minh

Tìm **ít nhất một nguồn tuyển dụng thực tế** có thể dùng để kiểm chứng luồng **nguồn → collector → xử lý → SQLite → dashboard → link bài gốc**. Nguồn phải có ít nhất một tin liên quan cybersecurity tại Việt Nam và có cơ sở rõ ràng cho phương thức truy cập/lưu dữ liệu dự kiến. Phase 0 xác minh nguồn và chuẩn bị bằng chứng; luồng end-to-end được triển khai và kiểm thử trong Phase 1.

Phân biệt:

- **Provider:** công nghệ cung cấp bảng tuyển dụng hoặc API, ví dụ Greenhouse, Lever, Recruitee.
- **Source:** một board/site tuyển dụng **cụ thể của một doanh nghiệp**, ví dụ board Axon trên Greenhouse hay Amanotes trên Lever.
- **Job portal:** nền tảng tập hợp tin nhiều doanh nghiệp, ví dụ ITviec, TopCV.
- **Public API:** endpoint đọc được công bố; **không tự động cấp quyền** sao chép, lưu trữ, tái sử dụng hoặc tái xuất bản toàn bộ nội dung.
- **Tin đã quan sát:** bằng chứng rằng một trang tin được hiển thị tại thời điểm kiểm tra; **không phải** cam kết tin còn tuyển ở thời điểm sử dụng sau này.

MVP không tự khám phá nguồn mới, không đăng nhập tài khoản tuyển dụng, không vượt CAPTCHA, không scraping nơi bị cấm và không tự động ứng tuyển.

### Source Validation Status

Trạng thái xác minh áp dụng cho từng board/site cụ thể, không áp dụng cho provider.

| Trạng thái | Điều kiện sử dụng trong tài liệu |
|---|---|
| `candidate` | Đã tìm thấy nguồn/board đáng khảo sát, nhưng còn thiếu một hoặc nhiều bằng chứng bắt buộc. **Chưa bật trong cấu hình chạy định kỳ.** |
| `verified` | Đã kiểm tra quyền truy cập và phạm vi lưu dữ liệu; thực hiện API/HTTP smoke test hợp lệ; xác nhận phân trang/phạm vi; có ít nhất một tin cybersecurity tại Việt Nam với ID hoặc URL, địa điểm và liên kết gốc; có bằng chứng được ghi lại. |
| `blocked` | Điều khoản/quyền truy cập không cho phép phương thức dự kiến, hoặc cần token/chấp thuận chưa có. **Không tự động tích hợp.** Có thể đánh giá lại nếu được cấp phép. |

> **Lưu ý:** `verified` là trạng thái theo **từng source**, không theo provider. Một adapter Greenhouse chạy được với board A không chứng minh board B đã được xác minh.

### Integration Decision

Quyết định tích hợp được ghi riêng với trạng thái xác minh và không làm thay đổi trạng thái đó:

| Quyết định | Ý nghĩa |
|---|---|
| `evaluate` | Tiếp tục khảo sát; chưa bật tích hợp. |
| `enabled` | Nguồn đã `verified`, đáp ứng các điều kiện tích hợp cần thiết và được phép bật. |
| `disabled` | Không tích hợp bằng phương thức dự kiến. |
| `pending_permission` | Chờ xác minh hoặc được cấp quyền phù hợp; chưa bật tích hợp. |

Provider chỉ được đánh giá như công nghệ; không tự nhận trạng thái source hay được bật chỉ vì có API. Chỉ source `verified` đáp ứng các điều kiện tích hợp mới có thể được quyết định `enabled`; quyết định này không thay thế gate Phase 0.

## 2. Phương pháp và giới hạn của lần khảo sát này

- Đã đối chiếu **tài liệu API chính thức**, một số trang tuyển dụng công khai và **điều khoản sử dụng** bằng trình duyệt/tìm kiếm web.
- Đã tìm được ví dụ trang tin Security có địa điểm Việt Nam của **Axon (Greenhouse), Amanotes (Lever), Picus (Lever)**.
- Người dùng đã thực hiện smoke test HTTPX với Axon ngày **11/11/2026**, cung cấp báo cáo terminal: 1 GET, HTTP `200`, JSON hợp lệ và nhận 489 tin. Kết quả chi tiết tại mục 7.4; lượt cập nhật tài liệu này không chạy lại script hoặc gọi API.
- **Chưa có báo cáo smoke test Amanotes hoặc Picus** trong bằng chứng được cung cấp.
- **Chưa lưu response JSON nguồn làm fixture**. Axon trả `meta.total = 489`, khớp số tin nhận được; phân trang/phạm vi đầy đủ vẫn chưa xác nhận (`pagination_complete = null`).
- **Chưa xác nhận đầy đủ quyền lưu/tái sử dụng mô tả JD** cho ứng dụng aggregator cá nhân; API có thể được thiết kế cho website tuyển dụng của chính doanh nghiệp.
- **Chưa có nguồn được xác minh là đang có tin SOC/Blue Team Intern, Fresher hoặc Junior tại Việt Nam.** Các tin ví dụ chủ yếu yêu cầu kinh nghiệm.
- Số lượng tin đang có trên các portal hoặc board thay đổi liên tục. **Không sử dụng số lượng tìm thấy trong lượt tìm kiếm làm số liệu kiểm thử API.**

**Kết luận cập nhật ngày 11/11/2026:** `PARTIALLY VALIDATED`. Axon đã có bằng chứng truy cập và xử lý JSON thành công; chưa đạt điều kiện hoàn thành Phase 0 theo `intent.md`.

## 3. Kết quả khảo sát tổng quan

| Nguồn/nền tảng | Loại | Kết quả về dữ liệu | Cơ chế kỹ thuật | Source Validation Status | Integration Decision |
|---|---|---|---|---|---|
| Greenhouse | ATS provider | Có board Axon với tin Security tại TP.HCM | Job Board API, GET public theo `board_token` | Không áp dụng cho provider | `evaluate` — khảo sát từng board |
| Lever | ATS provider | Có board Amanotes và Picus với tin liên quan tại Việt Nam | Postings API, JSON theo `site`, hỗ trợ phân trang | Không áp dụng cho provider | `evaluate` — khảo sát từng board |
| Recruitee | ATS provider | Có khả năng phát hành tin tuyển dụng qua Careers Site API | Token theo tài khoản doanh nghiệp; hạn đưa token vào request là 10/02/2027 | Không áp dụng cho provider | `pending_permission` — chưa có quyền/token được xác minh |
| ITviec | Job portal | Có danh mục Information Security/Cybersecurity | Chưa xác minh API tìm việc dành cho aggregator; điều khoản hạn chế sao chép | `blocked` | `pending_permission` |
| TopCV | Job portal | Có các trang/tin tuyển dụng ATTT | API ứng viên/aggregator và quyền tự động thu thập chưa được xác minh | `candidate` | `pending_permission` |
| LinkedIn | Job portal | Có các danh mục việc làm Security tại Việt Nam | Chính sách cấm scraping/các bot không được phép | `blocked` | `disabled` |
| Glints | Job portal | Có nền tảng tuyển dụng tại Việt Nam | Điều khoản hạn chế screen scraping/robots khi thiếu chấp thuận bằng văn bản | `blocked` | `disabled` |
| CareerViet | Job portal | Có nền tảng tuyển dụng tại Việt Nam | Điều khoản hạn chế công cụ tự động điều hướng/tìm kiếm | `blocked` | `disabled` |

Các nhận xét về khả năng tích hợp chỉ là **kết quả đánh giá sơ bộ**, không phải phê duyệt pháp lý hoặc giấy phép sử dụng dữ liệu.

## 4. Hồ sơ nguồn ứng viên ưu tiên

### SRC-01 — Axon Careers (Greenhouse)

| Thuộc tính | Ghi nhận |
|---|---|
| `source_name` | Axon Careers |
| `company` | Axon |
| `provider` | Greenhouse |
| `external_key` | `axon` — endpoint dùng khóa này đã trả HTTP `200` trong báo cáo smoke test ngày 11/11/2026 |
| Board/website | https://job-boards.greenhouse.io/axon |
| API mẫu theo tài liệu | `GET https://boards-api.greenhouse.io/v1/boards/axon/jobs?content=true` |
| Endpoint đã smoke test | `GET https://boards-api.greenhouse.io/v1/boards/axon/jobs` — không có query parameter, không yêu cầu `content=true` |
| Trang tin quan sát | https://job-boards.greenhouse.io/axon/jobs/7823328003 |
| Ví dụ tin | Senior Security Operations Engineer I |
| Địa điểm quan sát | Ho Chi Minh City, Vietnam |
| Cấp bậc/mức phù hợp | Senior; phù hợp để kiểm thử nhận diện lĩnh vực, **không phải Intern/Junior** |
| Phân trang/phạm vi thực tế | Nhận 489 tin trong 1 response, khớp `meta.total = 489`; chưa xác nhận toàn bộ phạm vi board, `pagination_complete = null` |
| Dữ liệu API thực nhận | Báo cáo ghi JSON hợp lệ, 489 ID phân biệt; không phát hiện thiếu/sai `id`, `title`, `location.name`, `absolute_url` theo các kiểm tra hiện tại của script. `content`, `updated_at`, độ ổn định ID qua nhiều lần và nội dung bài gốc chưa được xác minh bởi báo cáo |
| Quyền lưu metadata/JD | **Chưa xác nhận** quyền sử dụng với aggregator bên thứ ba |
| Tần suất/rate-limit được phép | **Chưa xác nhận cho board này**; không suy đoán từ tài liệu của bên thứ ba |
| Response fixture được phép lưu | Chưa có |
| Source Validation Status | `candidate` |
| Integration Decision | `pending_permission` — đã có smoke test kỹ thuật; còn cần xác minh quyền sử dụng dữ liệu và phạm vi đầy đủ trước tích hợp |

**Bằng chứng:** [Trang tin Axon](https://job-boards.greenhouse.io/axon/jobs/7823328003); [Greenhouse Job Board API](https://docs.greenhouse.io/job-board); [Greenhouse API overview](https://support.greenhouse.io/hc/en-us/articles/10568627186203-Greenhouse-API-overview).

### SRC-02 — Amanotes Careers (Lever)

| Thuộc tính | Ghi nhận |
|---|---|
| `source_name` | Amanotes Careers |
| `company` | Amanotes |
| `provider` | Lever |
| `external_key` dự kiến | `amanotes` |
| Board/website | https://jobs.lever.co/amanotes |
| API mẫu theo tài liệu | `GET https://api.lever.co/v0/postings/amanotes?mode=json` |
| Trang tin quan sát | https://jobs.lever.co/amanotes/a3451dde-d684-43c0-81e7-d001d7f93e79 |
| Ví dụ tin | Site Reliability Engineer (GCP Experience), có nhiệm vụ Cloud Security |
| Địa điểm quan sát | Ho Chi Minh City, Vietnam |
| Cấp bậc/mức phù hợp | Tin yêu cầu 3+ năm; **không phải Intern/Junior**; chức danh không chứa từ `security` nhưng JD có nhiệm vụ bảo mật |
| Phân trang/phạm vi thực tế | **Chưa kiểm chứng**; Lever có `skip`/`limit` theo tài liệu |
| Dữ liệu API thực nhận | **Chưa kiểm chứng** |
| Quyền lưu metadata/JD | **Chưa xác nhận** |
| Tần suất/rate-limit được phép | Chưa xác nhận theo nguồn |
| Response fixture được phép lưu | Chưa có |
| Source Validation Status | `candidate` |
| Integration Decision | `pending_permission` — Ưu tiên cho phép thử bộ phân loại theo nội dung JD |

**Bằng chứng:** [Board Amanotes](https://jobs.lever.co/amanotes); [Trang tin SRE](https://jobs.lever.co/amanotes/a3451dde-d684-43c0-81e7-d001d7f93e79); [Lever Postings API](https://github.com/lever/postings-api).

### SRC-03 — Picus Careers (Lever)

| Thuộc tính | Ghi nhận |
|---|---|
| `source_name` | Picus Careers |
| `company` | Picus Security |
| `provider` | Lever |
| `external_key` dự kiến | `picus` |
| Board/website | https://jobs.lever.co/picus |
| API mẫu theo tài liệu | `GET https://api.lever.co/v0/postings/picus?mode=json` |
| Trang tin quan sát | https://jobs.lever.co/picus/3a2499d5-39e5-40c1-a0ff-3aa8d46bc73e |
| Ví dụ tin | Solution Architect - Vietnam |
| Địa điểm quan sát | Vietnam, remote |
| Cấp bậc/mức phù hợp | Kinh nghiệm 3–5 năm; **không phải Intern/Junior**, thuộc mảng giải pháp bảo mật |
| Phân trang/phạm vi thực tế | Chưa kiểm chứng |
| Dữ liệu API thực nhận | Chưa kiểm chứng |
| Quyền lưu metadata/JD | Chưa xác nhận |
| Tần suất/rate-limit được phép | Chưa xác nhận theo nguồn |
| Response fixture được phép lưu | Chưa có |
| Source Validation Status | `candidate` |
| Integration Decision | `pending_permission` — Nguồn ứng viên bổ sung để kiểm thử vị trí remote tại Việt Nam |

**Bằng chứng:** [Board Picus](https://jobs.lever.co/picus); [Trang tin Solution Architect](https://jobs.lever.co/picus/3a2499d5-39e5-40c1-a0ff-3aa8d46bc73e); [Lever Postings API](https://github.com/lever/postings-api).

## 5. Nguồn hiện chưa được phép đưa vào crawler

| Nền tảng | URL chính thức để đối chiếu | Lý do/giới hạn | Source Validation Status | Integration Decision |
|---|---|---|---|---|
| ITviec | https://itviec.com/blog/terms-conditions-vn/ | Mục 2.2 giới hạn việc lấy, hiển thị, sao chép, tải hoặc truyền nội dung khi chưa có đồng ý trước bằng văn bản, ngoài các ngoại lệ được nêu | `blocked` | `pending_permission` |
| TopCV | https://www.topcv.vn/terms-of-service | Điều khoản xác lập quyền đối với dữ liệu/nội dung; chưa xác minh quyền tự động thu thập và tái sử dụng tin; API đối tác tuyển dụng không phải API ứng viên công khai | `candidate` | `pending_permission` |
| LinkedIn | https://www.linkedin.com/help/linkedin/answer/a1341387/ | Chính sách nêu rõ không cho phép công cụ bên thứ ba tự động scraping hoặc thao tác trái phép | `blocked` | `disabled` |
| Glints | https://glints.com/vn/en/about/terms | Cấm screen scraping, data mining, robots để tái tạo dữ liệu trên website khác nếu thiếu văn bản đồng ý | `blocked` | `disabled` |
| CareerViet | https://careerviet.vn/en/jobseekers/use | Điều khoản hạn chế sử dụng công cụ tự động tìm kiếm/điều hướng ngoài công cụ được cung cấp | `blocked` | `disabled` |
| Recruitee Careers Site API | https://docs.recruitee.com/reference/authentication-1 | API của provider có tài liệu chính thức; dự án chưa có quyền/token được xác minh | Không áp dụng cho provider/API | `pending_permission` |

Tài liệu Recruitee mô tả xác thực qua header `X-Careers-Sites-Token`, với token theo từng tài khoản doanh nghiệp, và nêu hạn đưa token vào request là **10/02/2027**. Thông tin này không chứng minh mọi request đã bắt buộc token vào ngày khảo sát 08/11/2026. Dự án chưa xác minh được quyền hoặc token để tích hợp; không bật API dựa trên khả năng truy cập kỹ thuật.

Có thể tiếp tục **xem tin bằng trình duyệt như người dùng bình thường** theo điều khoản tương ứng. Điều đó không đồng nghĩa với việc được phép tạo crawler hoặc lưu lại nội dung hàng loạt.

## 6. Ma trận yêu cầu dữ liệu của Core MVP

| Trường chuẩn cần có | Greenhouse (tài liệu) | Lever (tài liệu) | Cần xác minh trên board thật |
|---|---|---|---|
| ID bài đăng ổn định | Có trường `id` | Có Posting ID | ID trả về, không nhầm ID job nội bộ với posting ID |
| Tiêu đề | Có `title` | Có `text`/chức danh | Không rỗng |
| Công ty | Có thể biết từ board đã xác minh | Có thể biết từ site đã xác minh | Ánh xạ đúng company, không suy từ provider |
| Địa điểm | Có trường location | Có trường categories/location | Chuẩn hóa Việt Nam, đa địa điểm, remote |
| Nội dung JD | Tùy chọn `content=true` | Có phần nội dung bài đăng | Được phép lưu `full`, `excerpt` hay `none` |
| Ngày đăng | Không mặc định có | Không mặc định có | Nếu thiếu: `posted_at=NULL`, không dùng ngày crawl thay thế |
| URL gốc | Có `absolute_url` | Có URL posting | URL HTTP(S) hợp lệ và trỏ về bài tuyển dụng |
| Phân trang/danh sách đầy đủ | Cần xác nhận theo endpoint | `skip`/`limit` | Đọc đủ phạm vi; không kết luận tin biến mất từ trang thiếu |

Bảng là **khả năng theo tài liệu provider**. Bằng chứng API thực nhận của Axon được ghi riêng tại mục 7.4; không suy rộng kết quả đó cho Amanotes hoặc Picus.

## 7. Kế hoạch và kết quả smoke test

### 7.1. Điều kiện trước khi gọi API

- [ ] Xác định từng board/site cụ thể và URL gốc.
- [ ] Kiểm tra điều khoản của provider **và** điều kiện sử dụng đối với board/doanh nghiệp (phương thức truy cập, lưu, hiển thị, tần suất); nếu chưa rõ, xin xác nhận hoặc hạn chế thử nghiệm trong phạm vi được phép.
- [ ] Chỉ sử dụng HTTP GET công khai hoặc phương thức đã được cấp quyền. Không cần và không thu thập cookie/credential ứng viên.
- [ ] Chọn số request nhỏ, có timeout; không tự động quét nhiều board.

### 7.2. Các bước kiểm tra cho mỗi source

1. Ghi URL, ngày/giờ, `provider`, `external_key`, điều kiện truy cập và căn cứ cho phép.
2. Gọi đúng endpoint đọc theo tài liệu bằng HTTPX hoặc `curl` trong một kiểm thử read-only được phép; ghi HTTP status, content type và lỗi, không ghi secret.
3. Kiểm tra cấu trúc JSON và các trường: source ID, title, company, location, URL gốc, mô tả (nếu được phép), ngày nguồn cung cấp (nếu có).
4. Kiểm tra danh sách rỗng hợp lệ và cách xử lý response sai cấu trúc, timeout, 403/429/5xx. Dùng mock/stub cho các tình huống lỗi hoặc ghi nhận nếu lỗi xảy ra tự nhiên; không chủ động gây lỗi trên API thật.
5. Xác nhận giới hạn phân trang/phạm vi. Với Lever, kiểm tra `skip`/`limit`; với Greenhouse, xác định endpoint trả về đúng toàn bộ board đang theo dõi.
6. Đếm riêng: **tổng tin đã đọc**, **tin cybersecurity ở Việt Nam**, **tin Intern/Fresher/Junior**, **tin mơ hồ**; lưu cách đếm và thời điểm chụp số liệu.
7. Ánh xạ URL bài đăng gốc của provider vào `apply_url` theo hợp đồng dữ liệu; mở thủ công ít nhất một URL thực tế để xác nhận đúng bài đăng. Với Lever, kiểm tra `hostedUrl` và `applyUrl` riêng vì trang tin và biểu mẫu ứng tuyển có thể khác nhau.
8. Chỉ lưu JSON response hoặc JD làm fixture khi phạm vi lưu dữ liệu đã được xác minh; nếu không, giữ số liệu/metadata tối thiểu được phép và ghi rõ phần không thể lưu.
9. Ghi Source Validation Status `candidate` / `verified` / `blocked` **theo source**, không suy rộng sang các board khác; ghi Integration Decision riêng.

### 7.3. Mẫu biên bản chạy thử

Sao chép và điền mẫu này **sau khi chạy**; các ô trống không được hiểu là kết quả đạt.

```yaml
validation_id: SRC-XX
checked_at_vietnam: null
provider: null
board_url: null
api_url: null
access_basis_url: null
storage_basis_or_permission: null
rate_limit_or_allowed_frequency: null
http_status: null
json_schema_valid: null
request_count: null
pages_read: null
pagination_complete: null
pagination_evidence: null
fetched_count: null
cybersecurity_vietnam_count: null
intern_fresher_junior_count: null
unknown_geography_count: null
sample_job_url: null
sample_response_storage_permitted: null
fixture_path: null
result: candidate
integration_decision: null
blockers: []
notes: null
```

`validation_id` là mã hồ sơ kiểm chứng (ví dụ `SRC-01`), không phải khóa chính `sources.id` trong SQLite. `result` ghi Source Validation Status; `integration_decision` ghi quyết định tích hợp riêng.

- `request_count`: Tổng số HTTP request đã thực hiện trong lần kiểm tra.
- `pages_read`: Số trang dữ liệu đã đọc.
- `pagination_complete`: Đã xác nhận đọc hết phạm vi nguồn hay chưa.
- `pagination_evidence`: Căn cứ xác định dữ liệu đã đầy đủ, bao gồm điều kiện kết thúc hoặc thông tin phạm vi.

### 7.4. Biên bản Axon — ngày 11/11/2026

**Nguồn bằng chứng:** hai báo cáo JSON terminal do người dùng cung cấp trong cuộc trao đổi ngày 11/11/2026, từ `scripts/smoke_test_public_apis.py`. Đây là ghi nhận báo cáo do người dùng chạy, không phải kết quả chạy lại trong lúc cập nhật tài liệu. Không lưu response API hoặc JD trong biên bản này.

| Lượt | Thời điểm UTC | Thời điểm Việt Nam (UTC+7) | Kết quả |
|---|---|---|---|
| 1 | `2026-11-11T13:41:20.077670+00:00` | `2026-11-11T20:41:20.077670+07:00` | `run_outcome = error`; thiếu HTTPX, `request_count = 0`, chưa có dữ liệu từ nguồn |
| 2 | `2026-11-11T13:43:14.498646+00:00` | `2026-11-11T20:43:14.498646+07:00` | `run_outcome = observations_require_review`; 1 GET thành công, `errors = []` |

Lệnh người dùng cung cấp cho lượt 2:

```powershell
python .\scripts\smoke_test_public_apis.py --confirm-access --confirm-report-permission
```

| Thuộc tính lượt 2 | Kết quả từ báo cáo |
|---|---|
| `validation_id` / source / provider | `SRC-01` / `axon` / `greenhouse` |
| Board | `https://job-boards.greenhouse.io/axon` |
| Endpoint / phương thức / query parameters | `https://boards-api.greenhouse.io/v1/boards/axon/jobs` / `GET` / `{}` |
| Căn cứ tham khảo truy cập | `https://docs.greenhouse.io/job-board` — tài liệu provider, chưa phải xác nhận quyền theo board |
| Căn cứ tần suất / trạng thái | `null` / `unverified` |
| Giới hạn request / khoảng cách cấu hình | 1 request / 5 giây; chỉ là cấu hình cục bộ, không chứng minh rate limit được phép; một request không đo được khoảng cách thực tế |
| HTTP status / content type / JSON | `200` / `application/json` / `json_valid = true` |
| Thời gian tới headers / tổng thời gian xử lý request | `371.3 ms` / `381.6 ms` theo script |
| Request thực hiện / trang đọc | 1 / 1 |
| `received_count` / `unique_identified_jobs` | 489 / 489 |
| Bản ghi không hợp lệ / ID trùng | 0 / 0 theo kiểm tra của script |
| Trường thiếu/sai | `id = 0`, `title = 0`, `location = 0`, `url = 0` theo kiểm tra của script |
| `possible_cybersecurity_vietnam_count` | 1 — dấu hiệu theo từ khóa, chưa kiểm tra thủ công |
| `possible_cybersecurity_vietnam_entry_level_count` | 0 — trong nhóm dấu hiệu trên, chưa thấy từ khóa cấp bậc đầu vào trong tiêu đề |
| `title_keyword_without_explicit_vietnam_count` | 2 — tiêu đề khớp từ khóa nhưng chuỗi địa điểm không có dấu hiệu Việt Nam được script nhận diện; không tương đương tổng tin `geography = unknown` |
| `pagination_complete` | `null` — chưa xác nhận |
| `pagination_evidence` | `Greenhouse meta.total=489; received=489. Equality alone does not prove complete board coverage.` |
| `errors` | `[]` |
| URL của tin được nhận diện trong lượt chạy | Chưa có trong báo cáo; không mặc định đó là trang tin quan sát trước đây tại mục 4 |
| Response fixture / JD được lưu | Chưa có fixture; báo cáo không kèm response nguồn hoặc JD |
| Source Validation Status / Integration Decision | Giữ `candidate` / `pending_permission` |

**Giới hạn diễn giải:** script chỉ xét tiêu đề và một chuỗi địa điểm, không xét JD. Kết quả bằng 0 ở nhóm đầu vào không chứng minh Axon không tuyển Intern/Fresher/Junior; số 1 ở nhóm cybersecurity tại Việt Nam chưa chứng minh một tin đã được xác nhận phù hợp. JSON parse được và các trường vượt kiểm tra cơ bản không đồng nghĩa toàn bộ schema, ID ổn định hoặc link bài gốc đã được xác minh.

**Các phần còn thiếu:** quyền truy cập theo board và phạm vi lưu/hiển thị metadata, JD, fixture; tần suất cho phép; xác nhận phân trang/phạm vi; nhận diện và mở thủ công tin phù hợp; response mẫu được phép lưu; mẫu gán nhãn và quyết định adapter đầu tiên. Các cờ xác nhận trong lệnh không thay thế bằng chứng về quyền sử dụng. Lượt 2 chứng minh truy cập và xử lý response hoạt động tại thời điểm chạy, chưa làm Phase 0 PASS hoặc source thành `verified`.

## 8. Các rủi ro và cách xử lý

| Rủi ro | Ảnh hưởng đến MVP | Quyết định |
|---|---|---|
| API công khai nhưng quyền tái sử dụng nội dung chưa rõ | Không thể xác nhận nguồn hợp lệ để lưu JD | Không bật tự động; làm rõ quyền trước |
| Nguồn ATS ít tin Intern/Junior tại Việt Nam | Website chạy đúng nhưng không hữu ích để tìm việc | Mở rộng danh sách **nguồn hợp lệ**, không thêm UI trước |
| Board thay đổi, tin bị xóa hoặc URL đổi | Tin trùng, link hỏng, trạng thái sai | Dùng ID nguồn khi đáng tin; không xem một lỗi là tin đóng |
| Phân trang không đầy đủ | Đánh nhầm `not_seen` | Chỉ đối chiếu tin vắng mặt sau lượt `success` đầy đủ |
| JD HTML không ổn định | `updated_count` tăng giả | Chuẩn hóa văn bản theo `intent.md` |
| Tin remote không ghi rõ quyền làm việc từ Việt Nam | Loại nhầm hoặc nhận nhầm địa lý | Gắn `geography=unknown` khi chưa đủ chứng cứ |
| Trang tuyển dụng thay đổi chính sách | Nguồn từng hợp lệ không còn hợp lệ | Kiểm tra lại điều khoản định kỳ và tắt nguồn khi cần |

## 9. Gate nghiệm thu Phase 0

Chỉ chuyển Phase 0 sang **PASS** khi đáp ứng tất cả điều kiện sau:

- [ ] Đã khảo sát tối thiểu **3 nguồn ứng viên cụ thể** và có hồ sơ/bằng chứng (nếu không tìm đủ thì nêu rõ, chưa tự coi đạt).
- [ ] Ít nhất **1 source** đạt `verified`, không chỉ provider có tài liệu API.
- [ ] Có căn cứ rõ ràng về quyền truy cập **và phạm vi dữ liệu được phép lưu/hiển thị**.
- [ ] Có smoke test hợp lệ với endpoint thật, JSON/HTML được phân tích, phân trang/phạm vi được kiểm tra.
- [ ] Có ít nhất một tin thực tế liên quan cybersecurity **tại Việt Nam** với URL gốc mở được.
- [ ] Đã ghi số tin quan sát, số tin cybersecurity tại Việt Nam, tin đầu vào và những trường dữ liệu thiếu.
- [ ] Có response mẫu từ nguồn thật được phép lưu để kiểm thử. Nếu chưa có, ghi rõ rào cản và **Phase 0 chưa PASS**; việc ghi rào cản không thay thế fixture.
- [ ] Chuẩn bị mẫu gán nhãn phục vụ đánh giá classifier theo `intent.md`; xác minh quyền lưu khi dùng dữ liệu từ nguồn thật và không coi mẫu giả lập là bằng chứng nguồn.
- [ ] Có quyết định chọn adapter đầu tiên dựa trên **source được xác minh**, không chọn chỉ vì API dễ sử dụng.

**Tình trạng checklist ngày 08/11/2026:** Chưa PASS; chưa thực hiện smoke test API và chưa xác minh đầy đủ phạm vi sử dụng dữ liệu của bất kỳ board nào.

**Cập nhật ngày 11/11/2026:** Axon đã có báo cáo GET thực tế thành công theo mục 7.4. Checklist vẫn **chưa PASS**: phần xác nhận phạm vi, quyền sử dụng, tin phù hợp có URL được kiểm tra, fixture và mẫu gán nhãn chưa đầy đủ. Các ô kết hợp nhiều điều kiện vẫn để trống vì chưa đạt trọn điều kiện; báo cáo số đếm heuristic chưa thay thế kết quả xác minh thủ công.

## 10. Đề xuất hành động tiếp theo

1. **Ưu tiên SRC-01 Axon**, SRC-02 Amanotes và SRC-03 Picus để xác minh điều kiện sử dụng dữ liệu, vì đã có URL board và trang tin công khai.
2. Tìm thêm các board doanh nghiệp **đang có vị trí SOC/Blue Team/Network Security Intern, Fresher hoặc Junior tại Việt Nam**. Các tin senior kể trên chỉ chứng minh sự hiện diện của chủ đề cybersecurity, chưa chứng minh giá trị tìm việc cho đối tượng mục tiêu.
3. Với **Axon**, tiếp tục từ kết quả mục 7.4: kiểm tra phạm vi API và xác định/mở thủ công tin có dấu hiệu phù hợp. Với **Amanotes/Picus**, sau khi quyền truy cập phù hợp được xác định, thực hiện smoke test read-only và ghi biên bản; không coi kết quả Axon là bằng chứng cho các nguồn này.
4. Chuẩn bị mẫu gán nhãn theo `intent.md`, tách biệt bằng chứng nguồn thật với dữ liệu giả lập.
5. Chỉ khi Phase 0 đạt các điều kiện, bao gồm một source `verified` và response mẫu được phép lưu, bắt đầu **Phase 1 — Core MVP**: xây adapter → chuẩn hóa/phân loại → SQLite → Streamlit → mở URL bài gốc.

Tin Intern/Fresher/Junior là ưu tiên tìm kiếm, không phải điều kiện bắt buộc để Phase 0 PASS. Đánh giá mức hữu ích của nguồn được báo cáo riêng sau khi dùng thử 7 ngày theo `intent.md`.

## 11. Tài liệu và bằng chứng tham khảo

**Tài liệu API chính thức:**

- [Greenhouse — Job Board API](https://docs.greenhouse.io/job-board)
- [Greenhouse — API overview](https://support.greenhouse.io/hc/en-us/articles/10568627186203-Greenhouse-API-overview)
- [Lever — Postings API](https://github.com/lever/postings-api)
- [Recruitee — API documentation](https://support.recruitee.com/en/articles/1066282-api-documentation)
- [Recruitee — Careers Site API authentication](https://docs.recruitee.com/reference/authentication-1)

**Bằng chứng board/tin:**

- [Axon — Senior Security Operations Engineer I](https://job-boards.greenhouse.io/axon/jobs/7823328003)
- [Amanotes — Site Reliability Engineer (GCP Experience)](https://jobs.lever.co/amanotes/a3451dde-d684-43c0-81e7-d001d7f93e79)
- [Picus — Solution Architect - Vietnam](https://jobs.lever.co/picus/3a2499d5-39e5-40c1-a0ff-3aa8d46bc73e)

**Điều khoản/chính sách nguồn khác:**

- [ITviec — Thỏa thuận sử dụng](https://itviec.com/blog/terms-conditions-vn/)
- [TopCV — Điều khoản dịch vụ](https://www.topcv.vn/terms-of-service)
- [LinkedIn — Prohibited software and extensions](https://www.linkedin.com/help/linkedin/answer/a1341387/)
- [Glints — Terms of Use](https://glints.com/vn/en/about/terms)
- [CareerViet — Agreement and Terms of Use](https://careerviet.vn/en/jobseekers/use)

---

**Quyết định cập nhật ngày 11/11/2026:** Giữ Phase 0 ở trạng thái `IN PROGRESS`. Axon đã có bằng chứng smoke test kỹ thuật nhưng vẫn là `candidate` / `pending_permission`. Không thêm bất kỳ source nào vào `sources.yaml` với `enabled: true` chỉ dựa trên bản khảo sát và số đếm này. Chỉ đổi sang `verified` sau khi các bằng chứng còn thiếu được hoàn tất.
