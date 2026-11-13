# CyberJob Radar VN — Source Validation

> **Dự án:** CyberJob Radar VN — MVP sản phẩm v1.0
> **Phiên bản tài liệu:** 0.6 — mở rộng khảo sát 19 nguồn/site, làm rõ LinkedIn và nguồn doanh nghiệp ngày 13/11/2026; giữ MVP sản phẩm v1.0
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
- Ngày 12/11/2026 đã gửi email hỏi quyền sử dụng Axon; Gmail xác nhận nhãn `SENT`, chưa có bằng chứng được cấp quyền. Rà soát Amanotes phát hiện quy định hạn chế thu thập tự động và yêu cầu cho phép bằng văn bản; tạm `blocked` cho phương thức tự động dự kiến, xem mục 7.7.
- Ngày 13/11/2026 đã rà soát Picus: careers chính thức liên kết board Lever; bài gốc và board trả 403 qua công cụ duyệt web, trong khi kết quả tìm kiếm vẫn có bản lập chỉ mục. Điều khoản yêu cầu quyền bằng văn bản cho thu thập có hệ thống; tạm `blocked` cho phương thức tự động dự kiến, xem mục 7.8. Không gọi Postings API hoặc chạy smoke test mới.
- **Chưa lưu response JSON nguồn làm fixture**. Ngày 12/11/2026 đã đối chiếu tài liệu: endpoint List jobs trả toàn bộ bài đăng công khai của board, không mô tả phân trang cho endpoint này. Kết quả 489 tin khớp `meta.total` hỗ trợ tính đầy đủ của lượt 11/11; trường `pagination_complete = null` trong báo cáo gốc được giữ nguyên, đánh giá bổ sung tại mục 7.5.
- Ngày 12/11/2026 đã mở bài gốc Axon `7823328003`, xác nhận chức danh Security Operations, địa điểm TP.HCM và nội dung liên quan cybersecurity. Chưa có dữ liệu để chứng minh đây chính là tin được đếm trong lượt API ngày 11/11.
- **Chưa xác nhận đầy đủ quyền lưu/tái sử dụng mô tả JD** cho ứng dụng aggregator cá nhân; API có thể được thiết kế cho website tuyển dụng của chính doanh nghiệp.
- **Chưa có nguồn được xác minh là đang có tin SOC/Blue Team Intern, Fresher hoặc Junior tại Việt Nam.** Các tin ví dụ chủ yếu yêu cầu kinh nghiệm.
- Số lượng tin đang có trên các portal hoặc board thay đổi liên tục. **Không sử dụng số lượng tìm thấy trong lượt tìm kiếm làm số liệu kiểm thử API.**
- Mở rộng ngày **13/11/2026**: danh mục khảo sát gồm **10 portal và 9 nguồn doanh nghiệp**, tính cả ba nguồn trước đây; kết quả bổ sung tại mục 7.9. Độ sâu khác nhau: có nguồn đọc được bài gốc, có nguồn chỉ đọc được điều khoản/bản lập chỉ mục, có trang trả lỗi. Đây là phạm vi đã khảo sát, **không phải toàn bộ nguồn trên Internet hoặc 19 nguồn đã hoàn tất xác minh**. Không chạy smoke test mới, dò endpoint nội bộ, đăng nhập, gửi email mới hoặc lưu response/JD làm fixture.

**Kết luận cập nhật ngày 12/11/2026:** `PARTIALLY VALIDATED`. Axon có bằng chứng API thành công, bài gốc phù hợp và căn cứ về phạm vi endpoint; quyền sử dụng, tần suất và fixture/mẫu đánh giá vẫn chưa đầy đủ. Chưa đạt điều kiện hoàn thành Phase 0 theo `intent.md`.

## 3. Kết quả khảo sát tổng quan

| Nguồn/nền tảng | Loại | Kết quả về dữ liệu | Cơ chế kỹ thuật | Source Validation Status | Integration Decision |
|---|---|---|---|---|---|
| Greenhouse | ATS provider | Có board Axon với tin Security tại TP.HCM | Job Board API, GET public theo `board_token` | Không áp dụng cho provider | `evaluate` — khảo sát từng board |
| Lever | ATS provider | Có ghi nhận tin liên quan tại Việt Nam trước đây; Amanotes hiện có rào cản quyền sử dụng | Postings API, JSON theo `site`, hỗ trợ phân trang | Không áp dụng cho provider | `evaluate` — kết quả provider không cấp quyền cho board Amanotes |
| Recruitee | ATS provider | Có khả năng phát hành tin tuyển dụng qua Careers Site API | Token theo tài khoản doanh nghiệp; hạn đưa token vào request là 10/02/2027 | Không áp dụng cho provider | `pending_permission` — chưa có quyền/token được xác minh |
| SmartRecruiters | ATS provider | Có tin Bosch trên miền tuyển dụng của provider | Tài liệu public Posting API mô tả GET theo doanh nghiệp, `limit`/`offset`; chưa kiểm thử board Bosch hoặc xác minh quyền dùng | Không áp dụng cho provider | `evaluate` — không coi tài liệu API là giấy phép aggregator |
| Ashby | ATS provider | Có tài liệu Job Postings API; chưa xác định board có tin cybersecurity Việt Nam trong lượt này | GET theo tên board; tài liệu hướng tới careers của chính doanh nghiệp | Không áp dụng cho provider | `evaluate` — chưa có source cụ thể để tích hợp |
| ITviec | Job portal | Có danh mục Information Security/Cybersecurity | Chưa xác minh API tìm việc dành cho aggregator; điều khoản hạn chế sao chép | `blocked` | `pending_permission` |
| TopCV | Job portal | Có các trang/tin tuyển dụng ATTT | API ứng viên/aggregator và quyền tự động thu thập chưa được xác minh | `candidate` | `pending_permission` |
| LinkedIn | Job portal | Có các danh mục việc làm Security tại Việt Nam | Chính sách cấm scraping/các bot không được phép | `blocked` | `disabled` |
| Glints | Job portal | Có nền tảng tuyển dụng tại Việt Nam | Điều khoản hạn chế screen scraping/robots khi thiếu chấp thuận bằng văn bản | `blocked` | `disabled` |
| CareerViet | Job portal | Có nền tảng tuyển dụng tại Việt Nam | Điều khoản hạn chế công cụ tự động điều hướng/tìm kiếm | `blocked` | `disabled` |
| TopDev | Job portal | Đã đọc trang thỏa thuận; chưa xác minh một tin phù hợp cụ thể trong lượt này | Có giới hạn quyền nội dung và ngoại lệ sao chép nội bộ; chưa rõ quyền crawler/API cho dự án | `candidate` | `pending_permission` |
| JobsGO | Job portal | Đã đọc điều khoản ứng viên; chưa xác minh một tin phù hợp cụ thể trong lượt này | Điều khoản yêu cầu cho phép bằng văn bản khi dùng robot/spider hoặc thu thập để tái sử dụng | `blocked` cho phương thức dự kiến | `pending_permission` |
| Indeed | Job portal | Tìm kiếm có trang việc SOC tại Việt Nam; chưa đối chiếu từng tin gốc | Điều khoản có giới hạn bot/scraper và ngoại lệ có điều kiện; chưa xác minh ngoại lệ/quyền phù hợp cho dự án | `blocked` cho phương thức dự kiến | `pending_permission` |
| VietnamWorks | Job portal | Công cụ duyệt web báo 403 ở trang chủ; chưa kiểm tra được tin cụ thể | Chưa xác minh API đọc tin, điều khoản tái sử dụng hoặc giới hạn GET | `candidate` | `pending_permission` |
| Vieclam24h | Job portal | Công cụ duyệt web báo 403 ở trang chủ; chưa kiểm tra được tin cụ thể | Chưa xác minh API đọc tin, điều khoản tái sử dụng hoặc giới hạn GET | `candidate` | `pending_permission` |

Các nhận xét về khả năng tích hợp chỉ là **kết quả đánh giá sơ bộ**, không phải phê duyệt pháp lý hoặc giấy phép sử dụng dữ liệu.

Chín nguồn doanh nghiệp gồm Axon, Amanotes, Picus (hồ sơ mục 4) và OPSWAT, VNPT, VNG, CMC Global, Bosch, FPT IS (bảng khảo sát sơ bộ mục 7.9). Không cộng ATS provider vào số 19 nguồn/site. Lỗi 403/500 của công cụ duyệt web không phải kết quả kiểm thử API, không chứng minh tin đã đóng hoặc cho phép chuyển sang cách truy cập khác để vượt chặn.

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
| Trang tin đã mở và đối chiếu ngày 12/11/2026 | https://job-boards.greenhouse.io/axon/jobs/7823328003 — ID bài đăng từ URL: `7823328003` |
| Ví dụ tin | Senior Security Operations Engineer I |
| Địa điểm quan sát | Ho Chi Minh City, Ho Chi Minh City, Vietnam; nội dung xác nhận làm việc hybrid tại văn phòng TP.HCM |
| Cấp bậc/mức phù hợp | Senior; phù hợp để kiểm thử nhận diện lĩnh vực, **không phải Intern/Junior** |
| Phân trang/phạm vi | Tài liệu List jobs mô tả toàn bộ bài đăng của board, không nêu `page`/`skip`/`limit`; kết hợp báo cáo 489/489 để hỗ trợ tính đầy đủ tại lượt chạy. Báo cáo gốc vẫn giữ `pagination_complete = null`; không phải toàn bộ vị trí nội bộ hoặc toàn thị trường |
| Dữ liệu API thực nhận | Báo cáo ghi JSON hợp lệ, 489 ID phân biệt; không phát hiện thiếu/sai `id`, `title`, `location.name`, `absolute_url` theo các kiểm tra hiện tại của script. `content`, `updated_at`, độ ổn định ID qua nhiều lần và nội dung bài gốc chưa được xác minh bởi báo cáo |
| Quyền lưu metadata/JD | **Chưa xác nhận** cho aggregator cá nhân; đã rà soát tài liệu Greenhouse và điều khoản Axon, ghi nhận ranh giới áp dụng chưa rõ tại mục 7.6 |
| Tần suất/rate-limit được phép | **Chưa xác nhận cho board này**; không suy đoán từ tài liệu của bên thứ ba |
| Response fixture được phép lưu | Chưa có |
| Source Validation Status | `candidate` |
| Integration Decision | `pending_permission` — có bằng chứng kỹ thuật và bài gốc; chờ làm rõ quyền sử dụng dữ liệu và tần suất trước tích hợp |

**Bằng chứng:** [Trang tin Axon](https://job-boards.greenhouse.io/axon/jobs/7823328003); [Greenhouse Job Board API](https://docs.greenhouse.io/job-board); [Greenhouse API overview](https://support.greenhouse.io/hc/en-us/articles/10568627186203-Greenhouse-API-overview).

### SRC-02 — Amanotes Careers (Lever)

| Thuộc tính | Ghi nhận |
|---|---|
| `source_name` | Amanotes Careers |
| `company` | Amanotes |
| `provider` | Lever |
| `external_key` dự kiến | `amanotes` |
| Board/website | https://jobs.lever.co/amanotes |
| Careers chính thức hiện được liên kết | `https://www.careers.amanotes.com` — từ website Amanotes; chưa xác nhận backend/provider của trang này bằng kiểm thử |
| API mẫu theo tài liệu | `GET https://api.lever.co/v0/postings/amanotes?mode=json` |
| Trang tin quan sát | https://jobs.lever.co/amanotes/a3451dde-d684-43c0-81e7-d001d7f93e79 |
| Ví dụ tin | Site Reliability Engineer (GCP Experience), có nhiệm vụ Cloud Security |
| Địa điểm quan sát | Ho Chi Minh City, Vietnam |
| Cấp bậc/mức phù hợp | Tin yêu cầu 3+ năm; **không phải Intern/Junior**; chức danh không chứa từ `security` nhưng JD có nhiệm vụ bảo mật |
| Phân trang/phạm vi thực tế | **Chưa kiểm chứng**; Lever có `skip`/`limit` theo tài liệu |
| Dữ liệu API thực nhận | **Chưa kiểm chứng** |
| Quyền lưu metadata/JD | Chưa được cấp quyền; Community Guidelines yêu cầu cho phép bằng văn bản khi xây công cụ dùng dữ liệu/nội dung, có giới hạn thu thập tự động; xem mục 7.7 |
| Tần suất/rate-limit được phép | Chưa xác nhận theo nguồn |
| Response fixture được phép lưu | Chưa có |
| Source Validation Status | `blocked` cho phương thức thu thập tự động dự kiến — cập nhật 12/11/2026, có thể đánh giá lại khi có xác nhận phù hợp |
| Integration Decision | `pending_permission` — chưa được coi là nguồn thay thế sẵn sàng; chưa gọi Postings API hoặc bật lịch chạy |

**Bằng chứng:** [Board Amanotes](https://jobs.lever.co/amanotes); [Trang tin SRE](https://jobs.lever.co/amanotes/a3451dde-d684-43c0-81e7-d001d7f93e79); [Lever Postings API](https://github.com/lever/postings-api).

### SRC-03 — Picus Careers (Lever)

| Thuộc tính | Ghi nhận |
|---|---|
| `source_name` | Picus Careers |
| `company` | Picus Security |
| `provider` | Lever |
| `external_key` dự kiến | `picus` |
| Board/website | https://jobs.lever.co/picus |
| Liên kết từ doanh nghiệp | `https://www.picussecurity.com/careers-at-picus` → Join our team → `https://jobs.lever.co/picus`, đối chiếu 13/11/2026 |
| API mẫu theo tài liệu | `GET https://api.lever.co/v0/postings/picus?mode=json` |
| Trang tin quan sát | https://jobs.lever.co/picus/3a2499d5-39e5-40c1-a0ff-3aa8d46bc73e |
| Ví dụ tin | Solution Architect - Vietnam |
| Địa điểm quan sát | Vietnam, remote |
| Cấp bậc/mức phù hợp | Bản lập chỉ mục ghi kinh nghiệm 3–5 năm; **không phải Intern/Junior**, thuộc mảng giải pháp bảo mật/presales; chưa xác nhận nội dung live ngày 13/11/2026 |
| Phân trang/phạm vi thực tế | Chưa kiểm chứng |
| Dữ liệu API thực nhận | Chưa kiểm chứng |
| Quyền lưu metadata/JD | Chưa được cấp quyền; Terms of Use mục 5 yêu cầu cho phép bằng văn bản cho thu thập có hệ thống để tạo database; phạm vi riêng cho API Lever cần làm rõ |
| Tần suất/rate-limit được phép | Chưa xác nhận theo nguồn |
| Response fixture được phép lưu | Chưa có |
| Source Validation Status | `blocked` cho phương thức thu thập tự động dự kiến — cập nhật 13/11/2026; có thể đánh giá lại khi có quyền phù hợp |
| Integration Decision | `pending_permission` — chưa phải nguồn thay thế sẵn sàng, chưa có smoke test API |

**Bằng chứng:** [Board Picus](https://jobs.lever.co/picus); [Trang tin Solution Architect](https://jobs.lever.co/picus/3a2499d5-39e5-40c1-a0ff-3aa8d46bc73e); [Lever Postings API](https://github.com/lever/postings-api).

## 5. Nguồn hiện chưa được phép đưa vào crawler

| Nền tảng | URL chính thức để đối chiếu | Lý do/giới hạn | Source Validation Status | Integration Decision |
|---|---|---|---|---|
| ITviec | https://itviec.com/blog/terms-conditions-vn/ | Mục 2.2 giới hạn việc lấy, hiển thị, sao chép, tải hoặc truyền nội dung khi chưa có đồng ý trước bằng văn bản, ngoài các ngoại lệ được nêu | `blocked` | `pending_permission` |
| TopCV | https://www.topcv.vn/terms-of-service | Điều khoản xác lập quyền đối với dữ liệu/nội dung; chưa xác minh quyền tự động thu thập và tái sử dụng tin; API đối tác tuyển dụng không phải API ứng viên công khai | `candidate` | `pending_permission` |
| LinkedIn | https://www.linkedin.com/legal/user-agreement và https://www.linkedin.com/legal/crawling-terms | User Agreement mục 8.2 hạn chế scraping/bot; Crawling Terms yêu cầu được chấp thuận. Job Posting API phục vụ đăng tin của đối tác được phép, không chứng minh quyền đọc toàn bộ Jobs; xem mục 7.9 | `blocked` | `disabled` |
| Glints | https://glints.com/vn/en/about/terms | Cấm screen scraping, data mining, robots để tái tạo dữ liệu trên website khác nếu thiếu văn bản đồng ý | `blocked` | `disabled` |
| CareerViet | https://careerviet.vn/en/jobseekers/use | Điều khoản hạn chế sử dụng công cụ tự động tìm kiếm/điều hướng ngoài công cụ được cung cấp | `blocked` | `disabled` |
| TopDev | https://topdev.vn/term-of-services | Có ngoại lệ bản sao dùng nội bộ, nhưng chưa xác minh phạm vi tự động thu thập/tái sử dụng hoặc API phù hợp; không suy ra mọi dùng cá nhân đều bị cấm hoặc được phép | `candidate` | `pending_permission` |
| JobsGO | https://jobsgo.vn/media/pdf/dieu_khoan_su_dung_dich_vu_danh_cho_ung_vien_v2.0.pdf | PDF trang 9 (chỉ số trang 8) yêu cầu cho phép trước bằng văn bản khi dùng robot/spider hoặc thu thập để tái sử dụng | `blocked` cho phương thức dự kiến | `pending_permission` |
| Indeed | https://www.indeed.com/legal?hl=en và https://qa.indeed.com/legal?hl=en | Bản điều khoản khu vực đã đọc có giới hạn tự động truy cập, ngoại lệ crawling có điều kiện theo robots.txt. Chưa xác minh điều khoản áp dụng/ngoại lệ và quyền lưu, hiển thị cho nguồn Việt Nam; xem mục 7.9 | `blocked` cho phương thức dự kiến | `pending_permission` |
| VietnamWorks | https://www.vietnamworks.com/ | Trang chủ báo 403 qua công cụ duyệt web; điều khoản và API đọc tin chưa được xác minh. Không kết luận bị cấm pháp lý chỉ từ lỗi này | `candidate` | `pending_permission` |
| Vieclam24h | https://vieclam24h.vn/ | Trang chủ báo 403 qua công cụ duyệt web; điều khoản và API đọc tin chưa được xác minh. Không kết luận bị cấm pháp lý chỉ từ lỗi này | `candidate` | `pending_permission` |
| Recruitee Careers Site API | https://docs.recruitee.com/reference/authentication-1 | API của provider có tài liệu chính thức; dự án chưa có quyền/token được xác minh | Không áp dụng cho provider/API | `pending_permission` |
| Amanotes Careers | https://www.amanotes.com/community-guidelines | Mục về scraping/data mining hạn chế thu thập tự động, yêu cầu cho phép bằng văn bản khi dùng nội dung/dữ liệu để xây công cụ; phạm vi riêng cho board Lever cần được làm rõ | `blocked` cho phương thức dự kiến | `pending_permission` |
| Picus Careers | https://www.picussecurity.com/terms | Mục 5 yêu cầu quyền bằng văn bản cho thu thập có hệ thống để tạo collection/database; cần xác nhận phạm vi áp dụng riêng cho board/API Lever | `blocked` cho phương thức dự kiến | `pending_permission` |

Tài liệu Recruitee mô tả xác thực qua header `X-Careers-Sites-Token`, với token theo từng tài khoản doanh nghiệp, và nêu hạn đưa token vào request là **10/02/2027**. Thông tin này không chứng minh mọi request đã bắt buộc token vào ngày khảo sát 08/11/2026. Dự án chưa xác minh được quyền hoặc token để tích hợp; không bật API dựa trên khả năng truy cập kỹ thuật.

Có thể tiếp tục **xem tin bằng trình duyệt như người dùng bình thường** theo điều khoản tương ứng. Điều đó không đồng nghĩa với việc được phép tạo crawler hoặc lưu lại nội dung hàng loạt. Các nguồn doanh nghiệp mới tại mục 7.9 cũng chưa được phép bật crawler khi chưa xác minh đầy đủ.

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

Danh sách trên phản ánh trạng thái ngày 11/11/2026. Bằng chứng bổ sung ngày 12/11/2026 được đánh giá tại các mục sau, không sửa dữ liệu của lượt chạy gốc.

### 7.5. Đối chiếu bài gốc và phạm vi Axon — ngày 12/11/2026

Đã mở trang bài gốc và tài liệu chính thức bằng công cụ duyệt web; không gửi đơn, không chạy lại script và không tải response API mới. Mốc ghi nhận sau khi mở trang: `2026-11-12T08:17:58+00:00` / `2026-11-12T15:17:58+07:00`.

| Bằng chứng bài gốc | Ghi nhận |
|---|---|
| URL đã mở | [Bài đăng Axon](https://job-boards.greenhouse.io/axon/jobs/7823328003) |
| ID bài đăng | `7823328003`, lấy từ đường dẫn bài gốc; chưa đối chiếu với ID trong response gốc ngày 11/11 |
| Chức danh | Senior Security Operations Engineer I |
| Địa điểm hiển thị | Ho Chi Minh City, Ho Chi Minh City, Vietnam |
| Hình thức làm việc | Hybrid, có làm việc tại văn phòng TP.HCM; không diễn giải là remote toàn cầu |
| Nhãn đề xuất sau đọc trang | `relevance = related`, `geography = vietnam`, `seniority = other` (Senior), `work_mode = hybrid` |
| Căn cứ lĩnh vực (tóm tắt) | Nhiệm vụ liên quan công cụ bảo mật, quản lý lỗ hổng, kiểm tra an toàn trong CI/CD và xử lý sự cố |
| Trạng thái quan sát | Trang hiển thị JD và nút ứng tuyển tại thời điểm mở; không bảo đảm doanh nghiệp vẫn nhận hồ sơ sau đó |

Đây là xác nhận độc lập một tin phù hợp, không phải khôi phục danh tính của tin được script đếm ngày 11/11. Báo cáo khi đó không có ID/URL chi tiết nên chưa thể nối hai bằng chứng thành cùng một bản ghi.

**Phạm vi endpoint:** [Greenhouse Job Board API, mục List jobs](https://docs.greenhouse.io/job-board#list-jobs) mô tả endpoint `GET /v1/boards/{board_token}/jobs` trả danh sách tất cả bài đăng của board. Mục này chỉ liệt kê `content` là query parameter tùy chọn, không có cơ chế phân trang `page`/`skip`/`limit`; tham số phân trang ở các endpoint khác trong tài liệu không áp dụng mặc nhiên cho List jobs.

**Đánh giá:** đối chiếu tài liệu với báo cáo 1 response, 489 ID phân biệt và `meta.total = 489` cho phép ghi nhận phạm vi danh sách công khai đã được hỗ trợ bằng tài liệu và số liệu tổng hợp của lượt 11/11. Không còn yêu cầu thử thêm trang giả định. Tuy nhiên, không có response gốc để kiểm toán lại từng phần tử; không có bằng chứng snapshot bất biến, vị trí nội bộ hoặc mọi tin của doanh nghiệp ngoài board `axon`. Không thay `pagination_complete` trong báo cáo gốc thành kết quả mà script chưa xuất ra.

### 7.6. Quyền sử dụng, fixture và mẫu gán nhãn

Đã rà soát các nguồn chính thức ngày 12/11/2026:

| Nguồn | Phát hiện và giới hạn kết luận |
|---|---|
| [Greenhouse Job Board API](https://docs.greenhouse.io/job-board) | GET công khai không cần xác thực. Đây là căn cứ phương thức đọc, chưa xác nhận riêng quyền lưu lâu dài hoặc tái xuất bản nội dung Axon. |
| [Greenhouse API overview](https://support.greenhouse.io/hc/en-us/articles/10568627186203-Greenhouse-API-overview), mục Job Board API | Có thể áp dụng rate limit vì bảo mật/lưu lượng; không nêu hạn mức GET cụ thể cho board Axon. Không suy ra “không giới hạn” hoặc “mỗi 12 giờ đã được chấp thuận”. |
| [Axon Terms of Use](https://www.axon.com/terms-of-use), các mục Permitted Uses, Prohibited Uses và Links to Other Sites | Cho phép một số cách dùng cá nhân tạm thời, có giới hạn với sao chép/thu thập tự động, tải bất hợp lý và phân phối lại. Chưa xác định được cách áp dụng đầy đủ các điều khoản website Axon cho endpoint Greenhouse được công bố riêng; không kết luận mọi GET công khai bị cấm hoặc aggregator đã được cấp phép. |
| [Greenhouse Legal](https://www.greenhouse.com/legal) và [MSA](https://www.greenhouse.com/master-subscription-agreement), mục 2, 3(c), 4(d) | MSA điều chỉnh quan hệ thuê bao, nêu JD thuộc Customer Data và quyền cung cấp dịch vụ của Greenhouse. Không coi thỏa thuận dành cho khách hàng là giấy phép lưu/hiển thị nội dung cho dự án này. |

**Quyết định sử dụng dữ liệu:** chưa đủ căn cứ để xác nhận `full`, `excerpt` hoặc quyền lưu metadata tự động dài hạn. Chưa lưu JD/response thật làm fixture hoặc công bố dữ liệu nguồn vào Git. Các ghi nhận tối thiểu ở mục 7.5 phục vụ đối chiếu nguồn; không phải giấy phép cho lưu trữ hàng loạt. Giữ source `candidate`, quyết định `pending_permission` vì phạm vi áp dụng chưa rõ; chưa có căn cứ kết luận cấm riêng endpoint API để chuyển source thành `blocked`.

**Chuẩn bị fixture sau khi quyền được làm rõ:** dùng một response thật từ đúng endpoint đã được chấp thuận; ghi thời điểm nhận, endpoint/query, quyền cho phép, phần dữ liệu giữ lại và có được commit hay chỉ lưu cục bộ. Nếu chỉ cho phép trích metadata thì fixture phải ghi rõ đã rút gọn, không gắn nhãn raw response đầy đủ. Không tái tạo JSON từ trang HTML hoặc số liệu 489 rồi coi đó là response thật. Hiện chưa tạo fixture vì thiếu căn cứ lưu; điều kiện này chưa đạt.

**Chuẩn bị mẫu gán nhãn:** mục 7.5 là một ứng viên tham chiếu `related`/`vietnam`/`other`/`hybrid`; chưa xuất thành dữ liệu huấn luyện/kiểm thử và không đủ để đo precision/recall. Khi có quyền lưu, mỗi mẫu cần `source`, `job_id`, `url`, thời điểm quan sát, phạm vi nội dung được phép dùng, nhãn kỳ vọng và lý do; chia riêng bộ tinh chỉnh với bộ kiểm thử không trùng/gần trùng. Theo đặc tả, bộ kiểm thử cần ít nhất 40 tin có kết luận rõ (ít nhất 20 liên quan và 20 không liên quan), kèm mẫu mơ hồ riêng. Bộ dữ liệu có nội dung thực chưa được chuẩn bị đầy đủ; không dùng mẫu tổng hợp để thay bằng chứng nguồn thật.

**Yêu cầu làm rõ Axon (đã gửi):** [Axon Legal](https://www.axon.com/legal) công bố `ip@axon.com` cho câu hỏi sở hữu trí tuệ. Email đã gửi đến địa chỉ này qua Gmail ngày **12/11/2026**, yêu cầu chuyển tới đầu mối careers/API phù hợp. Gmail trả kết quả thành công với nhãn `SENT`; chưa xác nhận phát tới hộp thư đích hoặc có phản hồi cấp quyền. Mốc ghi nhận sau khi gửi: `2026-11-12T08:24:27+00:00` / `2026-11-12T15:24:27+07:00`. Nội dung cốt lõi đã gửi như dưới đây; thư có thêm lời chào, đề nghị chuyển đúng bộ phận và chữ ký cá nhân. Không lưu địa chỉ email cá nhân của người gửi vào tài liệu repository.

```text
Subject: Clarification on personal use of Axon's public Greenhouse job board API

I am building a local, single-user, non-commercial tool to track cybersecurity
job opportunities in Vietnam. I would like to use only public GET requests to:
https://boards-api.greenhouse.io/v1/boards/axon/jobs

Could you clarify whether I may:
1. Fetch the public listings once every 12 hours (proposed, not yet scheduled).
2. Retain job IDs, titles, locations and original posting URLs locally.
3. Display those fields in a private localhost dashboard linking to Axon's posts.
4. Save a small real API response sample for local automated tests, and whether
   that sample may be committed to a public repository or must remain private.
5. Retain any job description text, or whether it should be excluded entirely.

Please advise on applicable terms, request limits, attribution, retention/deletion
requirements and any separate permission needed from Greenhouse. I do not intend
to submit applications automatically or publish a public copy of the job board.
```

Đây là câu hỏi về phạm vi sử dụng cần được làm rõ, không phải xác nhận đã được cấp quyền. Chưa thay đổi cấu hình chạy định kỳ. Chờ phản hồi Axon; không gửi lặp yêu cầu này trong khi chưa có lý do theo dõi tiếp. Vấn đề kỹ thuật về hạn mức có thể cần Axon chuyển tiếp hoặc làm rõ thêm với Greenhouse.

### 7.7. Rà soát Amanotes như nguồn lựa chọn — ngày 12/11/2026

| Bằng chứng chính thức | Kết quả rà soát |
|---|---|
| [Amanotes homepage](https://www.amanotes.com/) | Liên kết Careers hiện trỏ tới `www.careers.amanotes.com`; không mặc định mọi tin hiện tại được cấp qua board Lever cũ. |
| [Amanotes Careers](https://careers.amanotes.com/) | Trang careers mở được bằng công cụ duyệt web và công bố `talents@amanotes.com`; đây là đầu mối tuyển dụng, chưa phải xác nhận quyền sử dụng API. |
| [Amanotes Terms of Service](https://www.amanotes.com/terms-and-conditions), mục 17 | Công bố `support@amanotes.com` cho câu hỏi về điều khoản; chưa có phản hồi hoặc giấy phép cho dự án. |
| [Community Guidelines](https://www.amanotes.com/community-guidelines), mục về scraping/data mining | Nêu hạn chế thu thập dữ liệu tự động từ website/dịch vụ và yêu cầu cho phép bằng văn bản khi xây công cụ dùng nội dung/dữ liệu Amanotes. Không tự suy ra ngoại lệ cho GET của board Lever; cần xác nhận riêng phạm vi và phương thức API dự kiến. |
| [Lever Postings API](https://github.com/lever/postings-api), Get a list of job postings | Có `skip`/`limit` và định dạng JSON. Tài liệu chỉ chứng minh cơ chế; giới hạn được nêu ở POST Application Rate Limit áp dụng cho nộp đơn, không phải căn cứ hạn mức GET. |
| Truy cập `https://jobs.lever.co/amanotes` qua công cụ duyệt web | Công cụ báo HTTP `403`; không thử vượt chặn hoặc truy cập lại bằng phương thức khác. Đây không phải smoke test HTTPX của endpoint `api.lever.co`, không chứng minh API bị đóng, tin đã hết hoặc không có việc phù hợp. |

**Kết luận vận hành:** chuyển SRC-02 từ `candidate` sang `blocked` cho phương thức thu thập tự động dự kiến, giữ Integration Decision `pending_permission`. Đây là quyết định tránh tích hợp khi thiếu chấp thuận theo chính sách đã đọc, không phải kết luận pháp lý rằng mọi truy cập bằng trình duyệt hoặc mọi GET Lever đều bị cấm. Chưa có bằng chứng quyền lưu metadata/JD, tần suất hoặc response fixture; không coi Amanotes là nguồn thay thế đã sẵn sàng.

**Để đánh giá lại:** cần xác nhận bằng văn bản từ Amanotes về việc đọc board/API cụ thể, dữ liệu được giữ, hiển thị cục bộ, tần suất và quyền lưu fixture. Đầu mối điều khoản là `support@amanotes.com`; có thể yêu cầu chuyển tới nhóm careers. Chưa gửi email cho Amanotes trong lần rà soát này. Chỉ kiểm thử API và tạo fixture sau khi phạm vi phù hợp được làm rõ.

### 7.8. Rà soát Picus như nguồn lựa chọn — ngày 13/11/2026

Mốc ghi nhận sau lượt đối chiếu trang và điều khoản: `2026-11-13T13:59:21+00:00` / `2026-11-13T20:59:21+07:00`. Chỉ dùng trình duyệt/tìm kiếm để đọc tài liệu và đối chiếu link; không gửi đơn, không gọi API và không tạo fixture.

| Bằng chứng | Ghi nhận |
|---|---|
| [Careers chính thức Picus](https://www.picussecurity.com/careers-at-picus) | Nút Join our team trỏ tới `https://jobs.lever.co/picus`, xác nhận mối liên hệ giữa doanh nghiệp và board. |
| [Bài Solution Architect - Vietnam](https://jobs.lever.co/picus/3a2499d5-39e5-40c1-a0ff-3aa8d46bc73e) | ID từ URL: `3a2499d5-39e5-40c1-a0ff-3aa8d46bc73e`. Kết quả tìm kiếm từ URL gốc có bản lập chỉ mục ghi Vietnam, Remote, Sales - Solutions Architecture – APAC, yêu cầu 3–5 năm kinh nghiệm. |
| Lần mở trực tiếp bài gốc và board | Công cụ duyệt web báo 403 cho cả hai. Không thử vượt chặn; không xem bản tìm kiếm là bằng chứng bài gốc đang nhận hồ sơ. Không suy ra API trả 403 hoặc tin đã đóng. |
| Đánh giá nội dung từ bản lập chỉ mục | Có dấu hiệu thuộc giải pháp cybersecurity/presales tại Việt Nam. Đây là ứng viên liên quan cần kiểm tra live sau, không phải vị trí SOC đầu vào; không nhận diện mọi việc bán hàng tại công ty bảo mật là cybersecurity. |
| [Lever Postings API](https://github.com/lever/postings-api) | Cơ chế GET theo site và `skip`/`limit` đã được mô tả; endpoint `https://api.lever.co/v0/postings/picus?mode=json` vẫn chỉ là ứng viên theo tài liệu. Chưa kiểm tra JSON, số tin hoặc phân trang thực tế của Picus. |
| [Picus Terms of Use](https://www.picussecurity.com/terms), mục 1, 2, 3, 5 | Có quyền dùng cá nhân giới hạn, đồng thời hạn chế tự động truy cập và yêu cầu cho phép bằng văn bản khi thu thập có hệ thống để tạo database. Không suy ra ngoại lệ cho board/API bên thứ ba; phạm vi áp dụng cho phương thức dự kiến cần được xác nhận. |
| [Contact Picus](https://www.picussecurity.com/contact-0) và footer careers | Công bố `info@picussecurity.com`; có thể hỏi và đề nghị chuyển tới người phụ trách quyền dữ liệu/careers. Chưa gửi email cho Picus. |

**Kết luận:** Picus có board chính thức và bằng chứng lập chỉ mục về việc cybersecurity tại Việt Nam, nhưng chưa chứng minh được quyền tự động thu thập/lưu/hiển thị hoặc tần suất GET. Chuyển SRC-03 sang `blocked` cho phương thức thu thập dự kiến, giữ Integration Decision `pending_permission`. Đây là quyết định vận hành của dự án khi thiếu quyền phù hợp, không phải kết luận rằng mọi GET công khai hoặc mọi lần đọc trang đều bị cấm.

**Phần còn thiếu:** phản hồi xác nhận quyền theo board/API, phạm vi metadata/JD, tần suất, fixture được phép lưu; sau đó mới thực hiện smoke test API và đối chiếu live bài gốc. Có thể dùng phạm vi câu hỏi mục 7.6 để hỏi Picus, thay endpoint và tên doanh nghiệp. Không tự gửi thư hoặc mở rộng script chỉ có Axon/Amanotes trong nhiệm vụ rà soát này. Chưa tìm được căn cứ đủ rõ để đưa Picus vào Core MVP.

### 7.9. Khảo sát mở rộng portal và doanh nghiệp — ngày 13/11/2026

Mốc ghi nhận trong lượt khảo sát: `2026-11-13T14:06:36+00:00` / `2026-11-13T21:06:36+07:00`. Đây là thời điểm khảo sát, không phải ngày đăng hoặc thời điểm chạy HTTPX. Chỉ ghi metadata và nhận xét tối thiểu để dẫn tới bằng chứng gốc; không tải toàn bộ board, tạo dataset JD hoặc thêm source vào cấu hình.

#### LinkedIn: đã kiểm tra chính sách và đường tích hợp chính thức

- [User Agreement, mục 8.2](https://www.linkedin.com/legal/user-agreement) hạn chế scraping/sao chép dữ liệu và bot không được phép. [Crawling Terms](https://www.linkedin.com/legal/crawling-terms) yêu cầu chấp thuận; có đầu mối `whitelist-crawl@linkedin.com`, nhưng việc công bố đầu mối không phải giấy phép cho dự án. Chưa gửi thư.
- [Job Posting API Overview](https://learn.microsoft.com/en-us/linkedin/talent/job-postings/api/overview) mô tả đối tác được phép **đăng tin thay khách hàng**. Không xác minh được API tìm kiếm/đọc toàn bộ LinkedIn Jobs dành cho aggregator cá nhân; không dùng API đăng tin làm căn cứ cho crawler đọc tin.
- Tìm kiếm có [bài tuyển dụng SOC Tier 1 mang tên Viettel Cyber Security Careers](https://vn.linkedin.com/posts/viettel-cyber-security-careers_viettelcybersecurity-vcscareers-careers-activity-7524307289227591681-tkfa). Đây chỉ là đầu mối khám phá: chưa đối chiếu bài tuyển dụng độc lập trên website doanh nghiệp, địa điểm đầy đủ, thời hạn hay mức kinh nghiệm. Không mặc định Tier 1 là Fresher hoặc coi tên tài khoản là bằng chứng xác thực doanh nghiệp. Chưa tính Viettel thành source độc lập thứ 20.
- **Quyết định:** giữ `blocked` / `disabled` cho crawler LinkedIn hiện tại. Có thể dùng tìm kiếm/thông báo do LinkedIn cung cấp theo điều khoản để tìm cơ hội; không tích hợp đọc email hoặc chức năng mới trong nhiệm vụ này. Không thử guest API không được công bố, cookie phiên đăng nhập hoặc công cụ vượt chống bot.

#### Các portal còn lại

Mười portal và trạng thái vận hành đã được ghi thống nhất tại mục 3 và 5. Bổ sung giới hạn bằng chứng:

| Portal | Phần đã đối chiếu | Phần chưa xác minh |
|---|---|---|
| ITviec | [Điều khoản mục 2.2](https://itviec.com/blog/terms-conditions-vn/) giới hạn lấy/tái sử dụng nội dung ngoài các ngoại lệ nêu trong đó | Chấp thuận cho crawler, phạm vi dữ liệu, rate limit và fixture |
| TopCV | [Danh mục ATTT](https://www.topcv.vn/tim-viec-lam-an-toan-thong-tin-kt1) và [điều khoản](https://www.topcv.vn/terms-of-service) | API đọc tin cho ứng dụng này và quyền thu thập/lưu; không lấy số kết quả tìm kiếm làm số tin API |
| Glints | [Terms of Use](https://glints.com/vn/en/about/terms), hạn chế screen scraping/robots nếu thiếu chấp thuận | Thỏa thuận hoặc cơ chế đọc tin được phép cho dự án |
| CareerViet | [Agreement and Terms of Use](https://careerviet.vn/en/jobseekers/use), hạn chế công cụ tự động tìm kiếm/điều hướng | Thỏa thuận hoặc cơ chế đọc tin được phép cho dự án |
| TopDev | [Thỏa thuận sử dụng](https://topdev.vn/term-of-services), có ngoại lệ bản sao nội bộ và yêu cầu ghi nguồn; trang hiện hiển thị thương hiệu Saramin | Không suy ra ngoại lệ này cho phép crawler định kỳ; API, điều khoản áp dụng sau thay đổi thương hiệu, một tin phù hợp và quyền fixture còn thiếu |
| JobsGO | [Điều khoản ứng viên, trang 9](https://jobsgo.vn/media/pdf/dieu_khoan_su_dung_dich_vu_danh_cho_ung_vien_v2.0.pdf), giới hạn thu thập để tái sử dụng khi thiếu văn bản cho phép | Chấp thuận, một tin phù hợp cụ thể, API đọc tin và rate limit |
| Indeed | [Điều khoản chung](https://www.indeed.com/legal?hl=en); [bản khu vực Qatar, Site Rules](https://qa.indeed.com/legal?hl=en) nêu giới hạn bot/scraper và ngoại lệ crawling có điều kiện; [trang SOC tại Việt Nam](https://jobs.vn.indeed.com/q-remote-soc-analyst-jobs.html) có kết quả lập chỉ mục | Bản khu vực không thay thế xác minh điều khoản áp dụng cho nguồn Việt Nam. Chưa xác minh ngoại lệ robots.txt/quyền phù hợp, API đọc tin, quyền lưu hoặc từng bài gốc; tạm chặn phương thức tự động dự kiến |
| VietnamWorks | [Trang chủ chính thức](https://www.vietnamworks.com/) trả 403 qua công cụ duyệt web | Tin phù hợp, điều khoản, API, quyền lưu và rate limit; không thử né 403 |
| Vieclam24h | [Trang chủ chính thức](https://vieclam24h.vn/) trả 403 qua công cụ duyệt web | Tin phù hợp, điều khoản, API, quyền lưu và rate limit; không thử né 403 |

#### Sáu nguồn doanh nghiệp bổ sung — hồ sơ sơ bộ

Các mã SRC-04–SRC-09 dưới đây chỉ định danh hồ sơ khảo sát, **không phải bản ghi database hoặc cấu hình đã bật**. Trạng thái tất cả sáu nguồn là `candidate`; Integration Decision là `pending_permission`. Chưa xác minh đủ căn cứ để gắn `blocked` theo điều khoản riêng hoặc `verified`.

| Mã / nguồn / board | Tin tham chiếu và ID hoặc URL | Địa lý, mức kinh nghiệm và độ chắc của bằng chứng | Cơ chế truy cập và phần còn thiếu |
|---|---|---|---|
| SRC-04 — [OPSWAT Open Positions](https://www.opswat.com/careers/open-positions) | [AI Security Engineer](https://www.opswat.com/jobs/4623181005); mã từ URL `4623181005` | Trang gốc đọc được, ghi Vietnam và Cybersecurity Operations. Chưa xác nhận cấp bậc hoặc đây là vị trí đầu vào; không coi mọi tin tại công ty bảo mật là cybersecurity | Trang HTML công khai. Chưa xác minh provider/board token, API đọc tin, điều khoản crawler và quyền lưu; không suy ra token Greenhouse từ mã URL |
| SRC-05 — [VNPT Tuyển dụng](https://tuyendung.vnpt.vn/) | [Kỹ sư chính sách An toàn thông tin](https://tuyendung.vnpt.vn/tim-viec-lam/ky-su-chinh-sach-an-toan-thong-tin-attt-jid5066.html); mã URL `5066` | Trang gốc đọc được: Hà Nội, yêu cầu 1 năm ATTT, hạn hiển thị 16/11/2026. Có nội dung GRC/tuân thủ; không gán nhãn SOC/Blue Team hoặc tự kết luận Junior | HTML; chưa xác minh public API/provider, quyền crawler/lưu và tần suất. Quy định dữ liệu cá nhân ứng viên không cấp quyền tái sử dụng tin tuyển dụng |
| SRC-06 — [VNG Careers](https://career.vng.com.vn/vi/tim-kiem-viec-lam) | [Security Engineer, Business Operations](https://career.vng.com.vn/tim-kiem-viec-lam/chi-tiet/6473-senior-security-engineer-vi); mã URL `6473`, mã tin hiển thị `26-IT-3443` | Bản lập chỉ mục từ miền chính thức ghi TP.HCM, nhiệm vụ IAM/endpoint/network security/incident management. Lần mở trực tiếp báo 500 qua công cụ; chưa xác nhận live hoặc cấp bậc từ nội dung. Không suy ra Senior từ slug | Chưa xác minh public API/provider, quyền crawler/lưu, rate limit hoặc độ ổn định ID; không coi bản lập chỉ mục là response thật |
| SRC-07 — [CMC Global Careers](https://cmcglobal.com.vn/career/) | [Cyber Security Engineer (SIEM/SOC)](https://cmcglobal.com.vn/career/cyber-security-engineer/); URL là định danh tham chiếu, chưa có ID API | Trang gốc đọc được: TP.HCM, nội dung SIEM/threat detection/incident response, yêu cầu kinh nghiệm. Trang hiển thị 31/10/2026 nhưng chưa xác minh ý nghĩa mốc này; không gán ngày đăng/hạn nộp | HTML; chưa xác minh public API, quyền crawler/lưu, tần suất và quy tắc phân trang. Hồ sơ này là CMC Global, không thay cho mọi đơn vị CMC |
| SRC-08 — [Bosch Việt Nam Careers](https://www.bosch.com.vn/careers/) | [Penetration Tester — AI Safety & Security](https://jobs.smartrecruiters.com/BoschGroup/744000150285289), mã URL `744000150285289`; thêm [Senior Embedded Security Engineer](https://jobs.smartrecruiters.com/oneclick-ui/company/BoschGroup/publication/891c4f2c-89a3-4ae3-be24-7c14fa9eebb8?dcr_ci=BoschGroup) | Tin Pentester đọc được nhưng phần trích xuất chưa có trường địa điểm rõ; không suy TP.HCM từ mô tả doanh nghiệp. Tin Embedded Security ghi địa chỉ Ho Chi Minh city, Vietnam và Senior, đủ làm ví dụ địa lý. Chưa xác minh từng tin còn nhận hồ sơ | Careers chính thức liên kết `jobs.bosch.com`; có trang BoschGroup trên SmartRecruiters và tài liệu GET Posting API. Chưa kiểm thử liên kết/phạm vi board API, quyền dùng dữ liệu, tần suất hoặc phân trang thực tế |
| SRC-09 — [FPT IS Tech Careers](https://techcareers.fis.com.vn/hotjob) | Mục **Pentester (Fresher/Junior/Senior)** trên trang tổng hợp; chưa có ID hoặc URL riêng cho từng tin | Trang đọc được, có nhiệm vụ pentest và các mục địa điểm FPT Tower, Hà Nội. Trang gộp nhiều công việc nên cần đối chiếu địa điểm/yêu cầu riêng từng mục; tiêu đề gộp không chứng minh mỗi vị trí đều nhận Fresher. Chưa xác nhận thời hạn hiện tại | HTML có form ứng tuyển: chỉ đọc, không gửi form/CV. Chưa xác minh API/provider, định danh từng tin, quyền crawler/lưu và tần suất; không coi trang tổng hợp là một job JSON |

**Số liệu của sáu nguồn mới:** tổng tin thực nhận qua API, số tin cybersecurity Việt Nam, số tin đầu vào và tỷ lệ thiếu trường đều **chưa đo**, không ghi `0`. Các URL trên là mẫu khảo sát chọn lọc; số dòng không phải độ phủ toàn board. Mã lấy từ URL chưa được chứng minh ổn định qua các lần thu thập. Không lưu JD đầy đủ hoặc tái dựng JSON từ HTML làm fixture.

**Đầu mối tin đầu vào cần kiểm tra tiếp:** [VNG System Intern (SRE & Security Platform), GreenNode](https://career.vng.com.vn/tim-kiem-viec-lam/chi-tiet/6752-system-intern-greennode-vi) có bản lập chỉ mục nêu OS hardening, nhưng mở trực tiếp bị timeout; địa điểm, mức liên quan của toàn vị trí và tình trạng tuyển hiện tại chưa được đối chiếu đầy đủ. Cùng mục Pentester của FPT IS, đây là đầu mối triển vọng, **chưa thay đổi kết luận chưa xác minh được nguồn có tin SOC/Blue Team Intern/Fresher/Junior đang mở tại Việt Nam**.

**Provider bổ sung:** [SmartRecruiters public Posting API](https://developers.smartrecruiters.com/docs/endpoints) mô tả GET danh sách theo công ty, có `limit`/`offset` và lọc `country`; chưa gọi endpoint Bosch. [Ashby Job Postings API](https://developers.ashbyhq.com/docs/public-job-posting-api) mô tả GET theo board để dựng careers của doanh nghiệp; chưa xác định board phù hợp tại Việt Nam. Đây là nghiên cứu cơ chế, không lựa chọn adapter, thêm công nghệ hoặc quyền sử dụng thay cho doanh nghiệp.

**Ưu tiên sau khảo sát:** tiếp tục chờ Axon vì đã có bằng chứng kỹ thuật; trong các nguồn mới, ưu tiên làm rõ quyền và dữ liệu của OPSWAT, VNPT, VNG, CMC Global, Bosch và FPT IS. FPT IS/VNG đáng chú ý về đầu mối vị trí đầu vào; Bosch đáng chú ý về tài liệu API. Chưa có cơ sở kết luận nguồn nào dễ được cấp quyền hoặc đủ điều kiện thay Axon. Với mỗi nguồn cần xác minh riêng endpoint/phương thức, metadata/JD được lưu và hiển thị, tần suất, phạm vi board/phân trang, fixture riêng tư/công khai; sau đó mới chuẩn bị smoke test tương ứng. Không gửi hàng loạt email hoặc gọi thử API trong lượt khảo sát này.

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

- [x] Đã khảo sát tối thiểu **3 nguồn ứng viên cụ thể** và có hồ sơ/bằng chứng: Axon, Amanotes, Picus tại mục 4. Đây là điều kiện khảo sát, không yêu cầu hoặc chứng minh cả ba đã smoke test/verified.
- [ ] Ít nhất **1 source** đạt `verified`, không chỉ provider có tài liệu API.
- [ ] Có căn cứ rõ ràng về quyền truy cập **và phạm vi dữ liệu được phép lưu/hiển thị**.
- [ ] Có smoke test hợp lệ với endpoint thật, JSON/HTML được phân tích, phân trang/phạm vi được kiểm tra. Axon đã đạt phần kỹ thuật và đối chiếu phạm vi tại mục 7.4–7.5; vẫn chờ làm rõ đầy đủ điều kiện sử dụng trước khi đánh dấu đạt trọn điều kiện.
- [x] Có ít nhất một tin thực tế liên quan cybersecurity **tại Việt Nam** với URL gốc mở được: Axon `7823328003`, đối chiếu ngày 12/11/2026 tại mục 7.5. Không xác nhận đây là chính tin script đếm ngày 11/11.
- [ ] Đã ghi số tin quan sát, số tin cybersecurity tại Việt Nam, tin đầu vào và những trường dữ liệu thiếu.
- [ ] Có response mẫu từ nguồn thật được phép lưu để kiểm thử. Nếu chưa có, ghi rõ rào cản và **Phase 0 chưa PASS**; việc ghi rào cản không thay thế fixture.
- [ ] Chuẩn bị mẫu gán nhãn phục vụ đánh giá classifier theo `intent.md`; xác minh quyền lưu khi dùng dữ liệu từ nguồn thật và không coi mẫu giả lập là bằng chứng nguồn.
- [ ] Có quyết định chọn adapter đầu tiên dựa trên **source được xác minh**, không chọn chỉ vì API dễ sử dụng.

**Tình trạng checklist ngày 08/11/2026:** Chưa PASS; chưa thực hiện smoke test API và chưa xác minh đầy đủ phạm vi sử dụng dữ liệu của bất kỳ board nào.

**Cập nhật ngày 11/11/2026:** Axon đã có báo cáo GET thực tế thành công theo mục 7.4. Checklist vẫn **chưa PASS**: phần xác nhận phạm vi, quyền sử dụng, tin phù hợp có URL được kiểm tra, fixture và mẫu gán nhãn chưa đầy đủ. Các ô kết hợp nhiều điều kiện vẫn để trống vì chưa đạt trọn điều kiện; báo cáo số đếm heuristic chưa thay thế kết quả xác minh thủ công.

**Cập nhật ngày 12/11/2026:** đã hoàn thành đối chiếu bài gốc và đánh giá phạm vi endpoint dựa trên tài liệu cùng báo cáo 11/11. Phase 0 tiếp tục **chưa PASS** do quyền lưu/hiển thị, tần suất, fixture được phép lưu, bộ mẫu gán nhãn và quyết định adapter còn thiếu. Greenhouse là phương án kỹ thuật ưu tiên có điều kiện cho Axon; chưa phải quyết định tích hợp được phê duyệt.

**Theo dõi tiếp ngày 12/11/2026:** email xin làm rõ Axon đã gửi qua Gmail; việc gửi không đồng nghĩa được cấp quyền. Amanotes được chuyển `blocked` / `pending_permission` cho phương thức tự động dự kiến sau rà soát chính sách; chưa có nguồn bổ sung đạt `verified`. Tiếp tục chờ bằng chứng trước khi tạo fixture hoặc chuyển sang Phase 1.

**Cập nhật ngày 13/11/2026:** đã rà soát Picus theo mục 7.8, chuyển sang `blocked` / `pending_permission` cho thu thập tự động dự kiến. Không bổ sung nguồn `verified`; Phase 0 tiếp tục `IN PROGRESS`. Bản tìm kiếm của tin Picus không thay thế điều kiện mở được URL gốc; điều kiện bài phù hợp trước đó vẫn dựa trên Axon tại mục 7.5.

**Khảo sát mở rộng ngày 13/11/2026:** mục 3, 5 và 7.9 ghi 19 nguồn/site ở các mức bằng chứng khác nhau. Sáu nguồn doanh nghiệp mới chỉ có hồ sơ sơ bộ, chưa smoke test hoặc có fixture/quyền lưu được xác minh. LinkedIn tiếp tục `blocked` / `disabled`; chưa có source mới `verified`, chưa chọn adapter và chưa PASS Phase 0.

## 10. Đề xuất hành động tiếp theo

1. **Tiếp tục ưu tiên SRC-01 Axon** về bằng chứng kỹ thuật; khảo sát quyền của các nguồn doanh nghiệp SRC-04–SRC-09 tại mục 7.9 để có lựa chọn bổ sung. Amanotes/Picus vẫn cần chấp thuận riêng, không phải nguồn thay thế sẵn sàng.
2. Đối chiếu tiếp đầu mối Pentester FPT IS và System Intern VNG, xác nhận địa điểm, yêu cầu kinh nghiệm và tình trạng tuyển. Tiếp tục tìm board **đang có vị trí SOC/Blue Team/Network Security Intern, Fresher hoặc Junior tại Việt Nam**; tiêu đề gộp hoặc bản lập chỉ mục chưa chứng minh đã đạt mục tiêu này.
3. Với **Axon**, theo dõi phản hồi thư đã gửi tại mục 7.6 và ghi đúng phạm vi được chấp thuận nếu có. Với **Amanotes/Picus**, cần làm rõ chấp thuận theo mục 7.7–7.8; chưa chạy API trong lúc thiếu quyền. Không coi kết quả Axon là bằng chứng cho các nguồn khác.
4. Sau khi có căn cứ lưu phù hợp, tạo fixture thật và bộ mẫu gán nhãn theo kế hoạch mục 7.6 và `docs/intent.md`, tách biệt bằng chứng nguồn thật với dữ liệu giả lập.
5. Chỉ khi Phase 0 đạt các điều kiện, bao gồm một source `verified` và response mẫu được phép lưu, bắt đầu **Phase 1 — Core MVP**: xây adapter → chuẩn hóa/phân loại → SQLite → Streamlit → mở URL bài gốc.

Tin Intern/Fresher/Junior là ưu tiên tìm kiếm, không phải điều kiện bắt buộc để Phase 0 PASS. Đánh giá mức hữu ích của nguồn được báo cáo riêng sau khi dùng thử 7 ngày theo `intent.md`.

## 11. Tài liệu và bằng chứng tham khảo

**Tài liệu API chính thức:**

- [Greenhouse — Job Board API](https://docs.greenhouse.io/job-board)
- [Greenhouse — API overview](https://support.greenhouse.io/hc/en-us/articles/10568627186203-Greenhouse-API-overview)
- [Greenhouse — Legal](https://www.greenhouse.com/legal)
- [Greenhouse — Master Subscription Agreement](https://www.greenhouse.com/master-subscription-agreement)
- [Lever — Postings API](https://github.com/lever/postings-api)
- [Recruitee — API documentation](https://support.recruitee.com/en/articles/1066282-api-documentation)
- [Recruitee — Careers Site API authentication](https://docs.recruitee.com/reference/authentication-1)

**Bằng chứng board/tin:**

- [Axon — Senior Security Operations Engineer I](https://job-boards.greenhouse.io/axon/jobs/7823328003)
- [Amanotes — Site Reliability Engineer (GCP Experience)](https://jobs.lever.co/amanotes/a3451dde-d684-43c0-81e7-d001d7f93e79)
- [Picus — Solution Architect - Vietnam](https://jobs.lever.co/picus/3a2499d5-39e5-40c1-a0ff-3aa8d46bc73e)

**Điều khoản/chính sách nguồn khác:**

- [Axon — Terms of Use](https://www.axon.com/terms-of-use)
- [Axon — Legal và đầu mối câu hỏi sở hữu trí tuệ](https://www.axon.com/legal)
- [Amanotes — Terms of Service](https://www.amanotes.com/terms-and-conditions)
- [Amanotes — Community Guidelines](https://www.amanotes.com/community-guidelines)
- [Amanotes — Careers chính thức](https://careers.amanotes.com/)
- [Picus — Careers chính thức](https://www.picussecurity.com/careers-at-picus)
- [Picus — Terms of Use](https://www.picussecurity.com/terms)
- [Picus — Contact](https://www.picussecurity.com/contact-0)
- [ITviec — Thỏa thuận sử dụng](https://itviec.com/blog/terms-conditions-vn/)
- [TopCV — Điều khoản dịch vụ](https://www.topcv.vn/terms-of-service)
- [LinkedIn — Prohibited software and extensions](https://www.linkedin.com/help/linkedin/answer/a1341387/)
- [Glints — Terms of Use](https://glints.com/vn/en/about/terms)
- [CareerViet — Agreement and Terms of Use](https://careerviet.vn/en/jobseekers/use)

---

**Quyết định cập nhật ngày 13/11/2026:** Giữ Phase 0 ở trạng thái `IN PROGRESS`. Axon có smoke test kỹ thuật, bài gốc phù hợp và căn cứ về phạm vi API, nhưng vẫn là `candidate` / `pending_permission` trong lúc chờ làm rõ quyền sử dụng. Amanotes và Picus là `blocked` / `pending_permission` cho phương thức tự động dự kiến theo mục 7.7–7.8. Khảo sát mở rộng 19 nguồn/site ở mục 7.9 chưa bổ sung source `verified`; LinkedIn vẫn `blocked` / `disabled`, sáu nguồn doanh nghiệp mới là `candidate` / `pending_permission`. Chưa tạo fixture nguồn thật khi quyền lưu chưa được xác minh. Không bật source hoặc chọn adapter chính thức trước khi các điều kiện còn thiếu hoàn tất. Phiên bản tài liệu tăng 0.5 → 0.6 cho lượt khảo sát mở rộng; phiên bản sản phẩm giữ MVP v1.0.
