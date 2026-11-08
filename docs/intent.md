# CyberJob Radar VN — Product Intent v1.2 (MVP sản phẩm v1.0)

> **Trạng thái:** Đặc tả định hướng cho MVP, chưa phải mô tả tính năng đã triển khai
>
> **Phiên bản tài liệu:** 1.2 — cập nhật ngày 07/11/2026
>
> **Phiên bản sản phẩm mục tiêu:** MVP v1.0
>
> **Sản phẩm:** CyberJob Radar VN
>
> **Đối tượng sử dụng:** Cá nhân (một người dùng)
>
> **Nền tảng:** Website chạy cục bộ trên máy Windows
>
> **Ngôn ngữ tài liệu:** Tiếng Việt

## 1. Tầm nhìn (Vision)

CyberJob Radar VN là công cụ cá nhân giúp **tìm, tổng hợp và theo dõi tin tuyển dụng An toàn thông tin/An ninh mạng tại Việt Nam** từ những nguồn được phép truy xuất.

**Ý nghĩa của “tự tìm kiếm” trong MVP:** hệ thống tự kiểm tra các nguồn đã được người dùng cấu hình. Người dùng khảo sát và bổ sung nguồn; hệ thống chưa tự khám phá website hoặc doanh nghiệp mới trên Internet. Một `provider` là loại kết nối, còn một `source` là board/site cụ thể đã được xác minh.

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

Đây là ưu tiên hiển thị, không phải điều kiện bắt buộc để lưu tin. Tin cybersecurity ở cấp bậc khác hoặc chưa rõ cấp bậc vẫn được giữ nếu thuộc phạm vi địa lý. Các mặc định dưới đây là quyết định thiết kế cho MVP, cần được kiểm chứng trong giai đoạn khảo sát nguồn và dùng thử.

### User journey mong muốn

1. Máy chạy tác vụ thu thập theo lịch (mặc định mỗi 12 giờ khi máy có thể thực thi tác vụ).
2. Công cụ đọc các nguồn đã cấu hình, chuẩn hóa và lưu tin hợp lệ vào database.
3. Người dùng mở dashboard tại `http://localhost:8501`.
4. Người dùng lọc `Intern`, `SOC`, `TP. Hồ Chí Minh` (hoặc điều kiện khác).
5. Người dùng xem thông tin tóm tắt, đánh dấu đã xem và mở `apply_url` đến tin gốc.
6. Người dùng đánh dấu đã lưu hoặc cập nhật trạng thái `Applied`, thêm ghi chú và ngày ứng tuyển.
7. Khi quay lại, trạng thái đã xem, thông tin theo dõi, bản ghi tin và các mốc thời gian vẫn còn. V1 chưa lưu từng phiên bản nội dung JD hoặc lịch sử chuyển giai đoạn ứng tuyển.

## 4. Phạm vi v1.0 (In scope)

### Thứ tự hoàn thành và xác thực

Các nhóm sau chỉ dùng để phân chia thứ tự công việc; **MVP sản phẩm vẫn là v1.0 và Definition of Done tại mục 10 không thay đổi**:

- **Core MVP:** thu thập từ ít nhất một nguồn thực tế đã xác minh, chuẩn hóa/phân loại/lọc tin, lưu SQLite, hiển thị trên Streamlit, mở bài gốc và không tạo trùng khi chạy lại.
- **MVP Complete:** lưu tin và theo dõi ứng tuyển, các bộ lọc trong mục 4.3, vòng đời tin, Collector Monitor, lịch chạy, logging, xử lý lỗi và sao lưu.
- **Validation:** kiểm chứng nguồn trước, đánh giá classifier trên bộ kiểm thử độc lập và kiểm thử end-to-end; sau đó dùng thử thực tế 7 ngày để đánh giá giá trị tìm việc. Dùng thử được báo cáo riêng, không thay đổi checklist nghiệm thu kỹ thuật ở mục 10.

### 4.1. Thu thập dữ liệu

- Có cơ chế **source adapter** để kết nối từng nguồn dữ liệu tuyển dụng.
- Trước mắt triển khai tối thiểu **một nguồn thực tế, được phép truy cập và có tin phù hợp**. Chọn nguồn theo chất lượng dữ liệu trước, sau đó chọn adapter; Greenhouse hoặc Lever chỉ là ứng viên khi có board phù hợp.
- Có khả năng mở rộng để bổ sung nguồn thứ hai mà không sửa core processing.
- Cho phép bật/tắt nguồn bằng cấu hình.
- Thu thập bằng lệnh Python CLI; cấu hình chạy định kỳ với Windows Task Scheduler.
- Có timeout, giới hạn tốc độ hợp lý và cơ chế thử lại có kiểm soát khi nguồn tạm lỗi.
- Ghi nhật ký từng lần chạy và lỗi theo từng nguồn.

### 4.1.1. Kiểm chứng nguồn trước khi triển khai

- Khảo sát tối thiểu 3 nguồn ứng viên; không bắt buộc triển khai cả 3. Ghi kết quả trong `docs/source-validation.md` và ghi rõ nếu chưa tìm đủ ứng viên.
- Với mỗi nguồn, ghi: URL/board, doanh nghiệp, provider, phương thức truy cập, bằng chứng/đường dẫn quy tắc truy cập, phạm vi nội dung được lưu, giới hạn tần suất, ngày kiểm tra và trạng thái `candidate`, `verified` hoặc `blocked`.
- Ghi số tin quan sát được, số tin cybersecurity tại Việt Nam, số tin đầu vào, ví dụ URL thật và mức đầy đủ của ID/địa điểm/ngày đăng. Đây là số liệu tại thời điểm khảo sát, không phải cam kết nguồn luôn có tin.
- Xác minh phân trang và phạm vi dữ liệu: API trả toàn bộ board hay chỉ một truy vấn/trang; có lấy được mô tả và URL bài gốc hay không.
- Chỉ bật nguồn `verified`. Có response mẫu được phép lưu và ít nhất một tin cybersecurity tại Việt Nam để kiểm chứng luồng thật; nếu chưa có, giai đoạn này chưa đạt.
- API truy cập được không tự động chứng minh mọi hình thức lưu hoặc tái sử dụng nội dung đều được phép. Ghi căn cứ truy cập và lưu dữ liệu của từng nguồn, không suy diễn quyền từ tên provider.

**Trạng thái hiện tại:** chưa có nguồn cụ thể được xác minh trong tài liệu này. Không coi ví dụ Greenhouse/Lever là nguồn đã hoạt động.

### 4.2. Xử lý dữ liệu

- Chuẩn hóa mỗi tin về một mô hình dữ liệu chung.
- Tách ba quyết định: mức liên quan đến cybersecurity, nhóm công việc và cấp bậc; thực hiện theo từ khóa/quy tắc có thể kiểm thử.
- Mức liên quan: `related`, `uncertain`, `unrelated`. Tin `uncertain` được giữ trong nhóm cần xem xét; không tự khẳng định là tin phù hợp.
- Nhóm công việc chính: `soc`, `network_security`, `general_security`, `other_security`, `unknown`. Nếu khớp nhiều nhóm, dùng thứ tự ưu tiên được ghi trong `keywords.yaml`; lưu lý do phân loại ngắn để giải thích kết quả.
- Nhận diện cấp bậc: `intern`, `fresher`, `junior`, `other` hoặc `unknown`.
- Phạm vi địa lý: `vietnam` khi có địa điểm làm việc tại Việt Nam hoặc ghi rõ nhận ứng viên làm remote từ Việt Nam và thông tin không mâu thuẫn; `outside_vietnam` khi có bằng chứng giới hạn ngoài Việt Nam; còn lại là `unknown`. Từ “remote” đơn lẻ không đủ để kết luận.
- Với tin có nhiều địa điểm hoặc hình thức làm việc, xét toàn bộ thông tin tuyển dụng của tin: nếu có ít nhất một lựa chọn làm việc tại Việt Nam hoặc remote cho phép làm từ Việt Nam, phân loại `vietnam`, kể cả khi có địa điểm ở nước ngoài. Chỉ phân loại `outside_vietnam` khi có đủ bằng chứng tất cả lựa chọn đều giới hạn ngoài Việt Nam. Nếu không xác nhận được lựa chọn nào áp dụng tại Việt Nam và có ít nhất một lựa chọn chưa rõ phạm vi, phân loại `unknown`; thông tin nguồn mâu thuẫn cũng dùng `unknown` để người dùng kiểm tra.
- Ví dụ: `TP.HCM / Singapore` → `vietnam`; `Singapore / Tokyo`, nếu đều yêu cầu làm việc tại chỗ → `outside_vietnam`; `Singapore / remote` không ghi rõ phạm vi remote → `unknown`; `remote tại Việt Nam / Singapore` → `vietnam`. Không suy ra quyền làm remote từ Việt Nam chỉ vì tin có địa điểm nước ngoài hoặc vì doanh nghiệp có văn phòng tại Việt Nam.
- Lưu tin mới khi mức liên quan là `related`/`uncertain` và phạm vi địa lý là `vietnam`/`unknown`. Tin không chắc chắn phải có nhãn riêng; `outside_vietnam` và `unrelated` không được thêm mới vào danh sách.
- Giữ địa điểm gốc và chuẩn hóa danh sách địa điểm để lọc: ví dụ `HCMC`, `Ho Chi Minh City`, `TP.HCM` cùng một mã. Tin đa địa điểm khớp bộ lọc nếu có ít nhất một địa điểm phù hợp; không suy địa điểm từ trụ sở doanh nghiệp.
- Loại các chức danh không liên quan như `security guard` / `nhân viên bảo vệ` theo ngữ cảnh chức danh và nhiệm vụ. Không loại toàn bộ tin chỉ vì mô tả có một từ khóa loại trừ.
- Ưu tiên cấp bậc được ghi trực tiếp trong chức danh hoặc yêu cầu tuyển dụng; khi thiếu hoặc mâu thuẫn, dùng `unknown` và ghi lý do. Một tin ghi nhiều cấp bậc dùng cấp thấp nhất được chấp nhận rõ ràng theo thứ tự `intern`, `fresher`, `junior`, `other`.
- Không tạo trùng tin từ cùng nguồn: định danh bằng `(source_id, external_id)`; fallback từ URL chuẩn hóa khi không có ID đáng tin cậy.
- Lưu `first_seen_at` và `last_seen_at` độc lập với `posted_at`.
- Không mặc định xem tin là đã đóng sau một lần không tìm thấy.
- Tin đã có trong DB vẫn được ghi nhận hiện diện và cập nhật dù sau đó đổi nhãn hoặc không còn phù hợp; không xóa tracking. Quy tắc thêm tin mới không được dùng để kết luận tin cũ đã biến mất.

### 4.3. Dashboard

Website chạy cục bộ bằng **Streamlit**, gồm ba trang:

**A. Job Explorer**

- Khi chưa chọn bộ lọc địa điểm, mặc định hiển thị tin `related`, trạng thái `listed`, có `geography = vietnam` hoặc `geography = unknown`; không ẩn tin chưa rõ cấp bậc. Tin `unknown` phải có nhãn **Chưa xác minh địa điểm**, kèm địa điểm gốc nếu có, để người dùng kiểm tra bài gốc. Tin `uncertain` về mức liên quan vẫn ở nhóm cần xác minh; có lựa chọn riêng để xem tin cần xác minh, không thấy lại hoặc đã đóng.
- Mặc định sắp xếp `first_seen_at` giảm dần; nếu chọn sắp theo `posted_at`, đặt tin thiếu ngày đăng cuối danh sách. Không trộn ngày phát hiện vào nhãn ngày đăng.
- Tìm kiếm theo tiêu đề, công ty và phần văn bản mô tả đã lưu; giao diện ghi rõ khi chỉ có đoạn trích. Tìm kiếm không phân biệt hoa/thường và hỗ trợ tiếng Việt không dấu.
- Khi so khớp, chuẩn hóa cả truy vấn và văn bản bằng `casefold`, Unicode NFD, loại dấu kết hợp và ánh xạ `đ`/`Đ` thành `d`. Ví dụ `an toan thong tin` khớp `An toàn thông tin`, `da nang` khớp `Đà Nẵng`. Giữ nguyên văn bản gốc khi lưu/hiển thị; không dựa riêng vào `LIKE` mặc định của SQLite cho so khớp tiếng Việt. MVP có thể chuẩn hóa khi tìm trên tập dữ liệu cục bộ, chưa cần chỉ mục tìm kiếm chuyên biệt.
- Bộ lọc tối thiểu: nhóm công việc, cấp bậc, địa điểm chuẩn hóa, nguồn, trạng thái tin và chưa xem. Điều kiện giữa các bộ lọc kết hợp AND; nhiều lựa chọn trong cùng bộ lọc kết hợp OR.
- Khi chọn địa điểm cụ thể, chỉ khớp tin có địa điểm đó trong danh sách chuẩn hóa; không tự coi `unknown` là thuộc địa điểm đã chọn. Nếu một tin `unknown` có địa điểm cụ thể khớp trong danh sách, tin vẫn hiện kèm nhãn chưa xác minh. Nếu còn tin `unknown` bị bộ lọc địa điểm ẩn nhưng khớp các điều kiện lọc khác, hiển thị số lượng cùng nhắc nhở và cho phép chọn thêm **Chưa xác minh địa điểm** trong bộ lọc địa điểm để xem chúng theo quy tắc OR.
- Mỗi tin hiển thị: chức danh, công ty, địa điểm, cấp bậc, nhóm công việc, nguồn, ngày đăng (nếu có), lần đầu phát hiện, lần thấy gần nhất và lần thay đổi nội dung/trạng thái gần nhất.
- Nút **Xem tin gốc / Ứng tuyển** mở đúng URL nguồn; không nộp hồ sơ trực tiếp trong CyberJob Radar VN.
- Nút **Lưu tin** để theo dõi sau.
- Nút **Đánh dấu đã xem / chưa xem** lưu bền vững. Việc xuất hiện trên danh sách hoặc lưu tin không tự đánh dấu đã xem. V1 không suy ra người dùng đã đọc trang ngoài từ việc bấm liên kết.
- “Chưa xem” là trạng thái cá nhân; “Mới phát hiện” dựa trên `first_seen_at`. Crawl lại không biến tin cũ thành tin mới hoặc tự đặt lại trạng thái chưa xem.

**B. My Tracking**

- Xem danh sách tin đã lưu hoặc đã ứng tuyển.
- Cập nhật trạng thái: `not_applied`, `applied`, `interview`, `offer`, `rejected`, `withdrawn`.
- Nhập ghi chú cá nhân và ngày ứng tuyển (nếu có).
- Lưu bền vững vào database, không chỉ lưu ở Streamlit Session State.
- Danh sách gồm tin `is_saved = true` hoặc `application_stage != not_applied`, kể cả tin đã đóng/không còn phù hợp. Tin chỉ được đánh dấu đã xem không tự xuất hiện tại đây.
- Ngày ứng tuyển là ngày do người dùng nhập, có thể để trống. Không tự gán ngày hiện tại khi người dùng ghi lại một lần ứng tuyển trước đó; bỏ lưu không xóa giai đoạn, ngày hoặc ghi chú.

**C. Collector Monitor**

- Hiển thị nguồn đang bật, thời điểm cập nhật thành công gần nhất.
- Hiển thị lịch sử chạy và số lượng tin lấy được, tin phù hợp, tin mới, tin cập nhật.
- Hiển thị lỗi/nguồn thất bại; phân biệt rõ **chưa có tin mới** với **thu thập thất bại**.
- Hiển thị lượt chạy thiếu dữ liệu (`partial`), số tin không đổi, bị loại và không hợp lệ; cảnh báo khi nguồn đang bật chưa từng thành công hoặc quá 24 giờ chưa có lượt thu thập đầy đủ thành công.

### 4.4. Vận hành và kiểm thử

- Chạy bằng môi trường Python `venv` và lệnh CLI.
- Database SQLite lưu trên máy cá nhân.
- Có `README.md` giải thích cài đặt, cấu hình nguồn, chạy collector, mở dashboard.
- Có `.env.example`, `.gitignore`, bộ test tối thiểu cho phân loại, chống trùng và theo dõi ứng tuyển.
- Kiểm thử ràng buộc DB và tình huống dashboard lưu tracking khi collector ghi: hoặc hai thao tác đều được lưu, hoặc thao tác gặp khóa thất bại rõ ràng sau thời gian chờ; không mất tracking hay báo thành công giả.
- Không commit database cá nhân, secret, file `.env` hoặc log nhạy cảm lên GitHub.
- Collector chỉ có một tiến trình hoạt động tại một thời điểm, kể cả khi chạy thủ công trùng lịch; lần gọi bị trùng thoát với thông báo rõ và không bắt đầu ghi dữ liệu.
- Khi máy bỏ lỡ lịch, chạy bù một lượt khi có thể rồi tiếp tục lịch bình thường; không chạy dồn từng lượt đã bỏ lỡ. Dashboard không cần mở để collector chạy.
- Sau khi bảo đảm không còn collector cũ, lần chạy kế tiếp đánh dấu các lượt `running` bị bỏ dở là `failed` với lý do gián đoạn; không dùng chúng để suy ra tin biến mất.
- Có hướng dẫn sao lưu/khôi phục SQLite khi cả dashboard và collector đã dừng, lưu bản sao ngoài Git và kiểm chứng phục hồi tracking. V1 chưa yêu cầu dịch vụ sao lưu tự động.
- Dashboard chỉ lắng nghe trên loopback theo mặc định; dùng đường dẫn DB tuyệt đối theo cấu hình để CLI, Task Scheduler và dashboard mở cùng một database.

## 5. Không thuộc phạm vi v1.0 (Out of scope)

- Đăng ký/đăng nhập và phân quyền nhiều người dùng.
- Đưa website công khai cho cộng đồng hoặc triển khai production 24/7.
- Nộp hồ sơ tự động, đăng nhập tài khoản tuyển dụng, thao tác ứng tuyển thay người dùng.
- AI/LLM để chấm điểm CV, phân tích JD hay gợi ý công việc nâng cao.
- Phân tích toàn bộ thị trường việc làm, bảo đảm bao phủ tất cả trang tuyển dụng Việt Nam.
- Tự động khám phá website/board mới hoặc dùng công cụ tìm kiếm để mở rộng danh sách nguồn.
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

Adapter trả dữ liệu đầu vào cùng kết quả thực thi: đã đọc hết phạm vi nguồn hay chưa, ID/URL các tin quan sát được và lỗi. Orchestration chỉ đối chiếu tin vắng mặt sau khi xác nhận phạm vi thu thập đầy đủ. Ghi lượt `running` trước khi gọi nguồn; sau khi kết thúc đọc, ghi các tin hợp lệ, kết quả đối chiếu và kết quả lượt chạy trong một transaction theo nguồn. Không giữ transaction trong lúc chờ HTTP. Upsert phải cập nhật bản ghi hiện có, không xóa rồi tạo lại làm mất liên kết tracking.

`sources.yaml` là nơi quyết định cấu hình và bật/tắt nguồn; bảng `sources` lưu định danh bền vững cùng trạng thái vận hành. Đồng bộ cấu hình không xóa nguồn hoặc tin cũ, không đổi ID DB và không ghi đè `last_success_at`. Board bị bỏ khỏi cấu hình được vô hiệu hóa. Nếu thay đổi phạm vi truy vấn, phải đặt lại bộ đếm vắng mặt trước khi đối chiếu trong phạm vi mới.

SQLite dùng file trên ổ đĩa cục bộ, bật và kiểm tra `journal_mode=WAL`; thiết lập `foreign_keys=ON` và `busy_timeout` hữu hạn cho **mỗi kết nối** của collector và dashboard. WAL cho phép đọc đồng thời với ghi trong nhiều trường hợp nhưng vẫn chỉ có một writer và vẫn có thể gặp `SQLITE_BUSY`. Transaction ghi phải ngắn; nếu hết thời gian chờ, rollback toàn bộ transaction, ghi lỗi và báo cho người dùng/lượt crawl, không báo lưu thành công hoặc âm thầm ghi đè dữ liệu. Thao tác chỉnh tracking là transaction riêng, chỉ sửa `job_tracking`; collector chỉ cập nhật tin và dữ liệu vận hành, không ghi đè tracking. Không giữ transaction trong lúc chờ HTTP hoặc người dùng nhập liệu.

Trước sao lưu theo mục 4.4, dừng cả hai tiến trình, bảo đảm DB đã đóng và checkpoint WAL thành công; chỉ sao chép file DB khi xác nhận dữ liệu đã được hợp nhất. Nếu không thể xác nhận checkpoint, dùng SQLite Online Backup API để tạo bản sao nhất quán. Khôi phục trên bản sao riêng và kiểm tra trước khi thay DB đang sử dụng.

### Stack chính

- Python 3.11+ (chọn một phiên bản cụ thể khi khởi tạo dự án)
- HTTPX; BeautifulSoup khi nguồn trả nội dung HTML cần trích xuất
- SQLAlchemy 2.x + SQLite
- Streamlit
- PyYAML, python-dotenv
- pytest
- Windows Task Scheduler cho lịch chạy; chưa cần dịch vụ hàng đợi tác vụ

## 7. Cấu trúc thư mục dự kiến

Đây là cấu trúc dự kiến cho giai đoạn triển khai, không phải danh sách file đã tồn tại. `docs/source-validation.md` là kết quả cần tạo trong Phase 0, không thuộc phạm vi chỉnh sửa tài liệu hiện tại. Có thể tách thêm `docs/architecture.md`, `docs/database-design.md` và `docs/acceptance-tests.md` khi triển khai nếu tài liệu phát triển; `intent.md` vẫn là đặc tả sản phẩm chính.

```text
cyberjob-radar-vn/
├── docs/
│   └── source-validation.md      # Khảo sát nguồn và bằng chứng kiểm chứng
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
│       │   └── <provider>.py     # Chỉ triển khai adapter đã chọn ở giai đoạn 0
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
│   ├── fixtures/                 # Mẫu nguồn được phép lưu + bộ mẫu gán nhãn
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

Thiết kế v1 ưu tiên **4 bảng**. Các thời điểm hệ thống lưu theo UTC, giao diện quy đổi sang múi giờ Việt Nam. Ngày ứng tuyển do người dùng nhập là kiểu DATE. Nếu nguồn chỉ cho ngày đăng/hạn tuyển, giữ độ chính xác ở mức ngày; không trình bày giờ suy diễn như dữ liệu nguồn.

Trường tùy chọn thiếu dữ liệu dùng `NULL` hoặc nhãn `unknown` đã định nghĩa. Trường bắt buộc phải có dữ liệu nguồn hoặc giá trị xác định hợp lệ theo quy tắc dưới đây; bản ghi không đạt được đếm là không hợp lệ, không tự bịa dữ liệu. Các enum, khóa ngoại và ràng buộc duy nhất phải được kiểm tra khi ghi DB.

### `sources`

| Cột | Kiểu/ý nghĩa |
|---|---|
| `id` | INTEGER PK |
| `name` | TEXT NOT NULL — tên nguồn/board |
| `provider` | TEXT NOT NULL — `greenhouse`, `lever`, ... |
| `external_key` | TEXT NOT NULL — định danh board/site, gồm vùng API nếu provider phân vùng |
| `is_active` | BOOLEAN NOT NULL DEFAULT TRUE |
| `last_success_at` | DATETIME NULL — chỉ cập nhật sau lượt `success` đã ghi DB hoàn tất |

Ràng buộc bắt buộc: `UNIQUE(provider, external_key)`; `is_active` chỉ nhận `0` hoặc `1`.

### `jobs`

| Cột | Kiểu/ý nghĩa |
|---|---|
| `id` | INTEGER PK |
| `source_id` | INTEGER NOT NULL FK -> `sources.id` |
| `external_id` | TEXT NOT NULL — `id:<source ID>` hoặc `url:<SHA-256 của URL chuẩn hóa>` |
| `title` | TEXT NOT NULL |
| `company` | TEXT NULL — lấy từ tin hoặc cấu hình board đơn doanh nghiệp đã xác minh; không suy ra từ tên provider |
| `location_text` | TEXT NULL |
| `locations` | JSON NOT NULL DEFAULT `[]` — danh sách `{country_code, city_code}`; từng thành phần có thể null nếu chưa rõ |
| `geography` | TEXT NOT NULL DEFAULT `unknown` — `vietnam`, `outside_vietnam`, `unknown` |
| `work_mode` | TEXT NOT NULL DEFAULT `unknown` — `onsite`, `hybrid`, `remote`, `unknown` |
| `relevance` | TEXT NOT NULL DEFAULT `uncertain` — `related`, `uncertain`, `unrelated` |
| `seniority` | TEXT NOT NULL DEFAULT `unknown` |
| `category` | TEXT NOT NULL DEFAULT `unknown` |
| `classification_reason` | TEXT NULL — lý do/nhóm quy tắc dẫn tới nhãn hiện tại |
| `description_text` | TEXT NULL — văn bản đã làm sạch, lưu trong phạm vi nguồn cho phép |
| `description_scope` | TEXT NOT NULL DEFAULT `none` — `full`, `excerpt`, `none`; đoạn tóm tắt UI sinh từ phần văn bản đã lưu |
| `apply_url` | TEXT NOT NULL — URL HTTP(S) tới bài gốc của nguồn |
| `posted_at` | DATETIME NULL |
| `posted_precision` | TEXT NOT NULL DEFAULT `unknown` — `datetime`, `date`, `unknown` |
| `deadline_at` | DATETIME NULL |
| `deadline_precision` | TEXT NOT NULL DEFAULT `unknown` — `datetime`, `date`, `unknown` |
| `first_seen_at` | DATETIME NOT NULL |
| `last_seen_at` | DATETIME NOT NULL |
| `job_updated_at` | DATETIME NOT NULL — lần tạo hoặc đổi nội dung/nhãn/trạng thái tin; không đổi chỉ vì thấy lại |
| `listing_status` | TEXT NOT NULL DEFAULT `listed` |
| `consecutive_missing_runs` | INTEGER NOT NULL DEFAULT 0 — số lượt đầy đủ thành công liên tiếp không thấy tin |

Ràng buộc bắt buộc: `UNIQUE(source_id, external_id)`, `consecutive_missing_runs >= 0`, `last_seen_at >= first_seen_at` và `job_updated_at >= first_seen_at`. Index cho `first_seen_at`, `seniority`, `category`, `source_id`, `geography`, `relevance` và `listing_status`; lựa chọn index ghép khi triển khai theo truy vấn thực tế. `locations` lưu JSON nhiều địa điểm và được lọc ở lớp ứng dụng trong MVP, không khẳng định các index đơn hỗ trợ lọc theo thành phố. Ở v1 chỉ chống trùng **trong từng nguồn**; việc hợp nhất cùng một tin xuất hiện tại nhiều nguồn được hoãn lại.

`listing_status` dùng `listed`, `not_seen`, `closed` theo mục 9.1. `listed` chỉ nói rằng tin đã xuất hiện ở nguồn, không bảo đảm doanh nghiệp còn nhận hồ sơ. Không xóa tin đang theo dõi chỉ vì nguồn không còn trả về.

URL dùng để định danh chỉ bỏ thành phần đã được xác minh không tham gia định danh tin, ví dụ tham số theo dõi `utm_*`; giữ tham số định danh và fragment nếu nguồn dùng fragment để định tuyến bài đăng. Không tùy tiện bỏ toàn bộ query string hoặc đổi hoa/thường của path. Giữ URL bài gốc để mở liên kết. Với nguồn dùng fallback URL, URL đổi có thể tạo bản ghi mới; hạn chế này phải ghi trong hồ sơ nguồn. Nếu sau này chuyển sang source ID, phải ánh xạ bản ghi cũ trước khi đổi khóa để giữ tracking.

Ngày chỉ có độ chính xác `date` được mã hóa bằng ngày gốc tại 00:00 UTC làm mốc kỹ thuật; UI đọc phần ngày UTC, không chuyển múi giờ hoặc hiển thị giờ. Đây không phải giờ đăng thực tế và không được dùng để tự kết luận tin hết hạn. Với `datetime`, chỉ chuẩn hóa UTC khi xác định được múi giờ nguồn; nếu không, giữ phần ngày với precision `date`. `unknown` tương ứng với thời điểm `NULL`.

**Ý nghĩa bốn mốc:** `posted_at` là ngày/giờ do nguồn cung cấp, thiếu thì `NULL`; `first_seen_at` là lần hệ thống phát hiện tin và không đổi khi thu thập lại; `last_seen_at` là lần gần nhất hệ thống quan sát được tin; `job_updated_at` là lần tạo hoặc lần gần nhất nội dung, nhãn hay trạng thái tin thay đổi. Một lần quan sát nội dung không đổi chỉ cập nhật `last_seen_at`. Tin chuyển `not_seen` có thể có `job_updated_at` sau `last_seen_at`; đây là trạng thái hệ thống thay đổi, không phải thời điểm nguồn đăng lại tin.

**So sánh JD:** chuyển HTML được phép lưu thành văn bản có ranh giới đoạn, giải mã HTML entities, chuẩn hóa Unicode NFC và khoảng trắng trước khi so với `description_text` đã lưu cùng cách chuẩn hóa. Chỉ thay đổi thẻ trình bày, thứ tự thuộc tính HTML hoặc khoảng trắng không có nghĩa thì không tính cập nhật JD; thay đổi văn bản có nghĩa được tính. So sánh trực tiếp văn bản chuẩn hóa, không cần bảng lịch sử hoặc trường hash mới. Các metadata/nhãn/trạng thái khác vẫn được so sánh độc lập. Chỉ so sánh mô tả khi nguồn thực sự cung cấp nội dung có cùng phạm vi `full` hoặc `excerpt`; nếu request thiếu mô tả thì giữ dữ liệu cũ, không coi thiếu tạm thời là JD bị xóa. Khi phạm vi mô tả thay đổi hoặc nguồn xác nhận xóa mô tả, cập nhật dữ liệu/`description_scope` và coi là thay đổi dữ liệu, không khẳng định nội dung JD thực sự đã sửa.

### `job_tracking`

| Cột | Kiểu/ý nghĩa |
|---|---|
| `job_id` | INTEGER PK, FK -> `jobs.id` (1 tin có tối đa 1 bản theo dõi cá nhân) |
| `is_saved` | BOOLEAN NOT NULL DEFAULT FALSE |
| `viewed_at` | DATETIME NULL — null nghĩa là chưa xem; cập nhật qua thao tác đánh dấu của người dùng |
| `application_stage` | TEXT NOT NULL DEFAULT `not_applied` |
| `notes` | TEXT NULL |
| `applied_on` | DATE NULL — ngày ứng tuyển do người dùng nhập |
| `updated_at` | DATETIME NOT NULL |

`application_stage`: `not_applied`, `applied`, `interview`, `offer`, `rejected`, `withdrawn`. `is_saved`, `viewed_at` và giai đoạn ứng tuyển độc lập. Chưa có hàng tracking được hiểu là chưa xem/chưa lưu/chưa ứng tuyển. Cho phép sửa giai đoạn để hiệu chỉnh, không bắt buộc đi qua từng bước.

`job_id` vừa là khóa chính vừa là khóa ngoại tới `jobs.id`; `is_saved` chỉ nhận `0` hoặc `1`. Không xóa job để cập nhật; FK ngăn xóa tin đang được theo dõi.

### `crawl_runs`

| Cột | Kiểu/ý nghĩa |
|---|---|
| `id` | INTEGER PK |
| `source_id` | INTEGER NOT NULL FK -> `sources.id` |
| `started_at` | DATETIME NOT NULL |
| `finished_at` | DATETIME NULL |
| `status` | TEXT NOT NULL — `running`, `success`, `partial`, `failed` |
| `is_complete` | BOOLEAN NOT NULL DEFAULT FALSE — đã duyệt hết phạm vi nguồn và xác định được sự hiện diện của từng tin |
| `fetched_count` | INTEGER NOT NULL DEFAULT 0 |
| `matched_count` | INTEGER NOT NULL DEFAULT 0 |
| `inserted_count` | INTEGER NOT NULL DEFAULT 0 |
| `updated_count` | INTEGER NOT NULL DEFAULT 0 |
| `unchanged_count` | INTEGER NOT NULL DEFAULT 0 |
| `rejected_count` | INTEGER NOT NULL DEFAULT 0 |
| `invalid_count` | INTEGER NOT NULL DEFAULT 0 |
| `status_changed_count` | INTEGER NOT NULL DEFAULT 0 — tin vắng mặt được đổi trạng thái sau đối chiếu |
| `error_message` | TEXT NULL |

`fetched_count` là số bản ghi đã nhận và kiểm tra, gộp trùng theo định danh nếu xác định được. `matched_count` là tập con hợp lệ có `relevance = related` và `geography = vietnam`, không bao gồm tin cần xác minh. `rejected_count` đếm tin mới hợp lệ nhưng ngoài phạm vi lưu; `invalid_count` đếm bản ghi không hợp lệ. Các số này mô tả đầu vào đã xử lý, không khẳng định dữ liệu đã lưu.

`inserted_count`, `updated_count`, `unchanged_count` và `status_changed_count` chỉ ghi nhận sau commit thành công. Với lượt `success`/`partial` đã xử lý toàn bộ phần dữ liệu nhận được, mỗi bản ghi thuộc đúng một nhóm `inserted`, `updated`, `unchanged`, `rejected` hoặc `invalid`; tổng 5 nhóm bằng `fetched_count`. Nếu rollback, các bộ đếm kết quả DB bằng 0, giữ số đầu vào đã biết và ghi rõ lỗi; không áp dụng công thức tổng cho lượt `failed`.

`updated_count` chỉ đếm bản ghi đã tồn tại có thay đổi nội dung, nhãn hoặc trạng thái khi được quan sát lại. Chỉ tăng `last_seen_at`/đặt lại bộ đếm vắng mặt được tính `unchanged`. Tin mới không được tính thêm vào `updated_count`. Thay đổi trạng thái do tin vắng mặt dùng `status_changed_count`, nằm ngoài `fetched_count`.

### Ràng buộc chung và transaction

- Bốn bảng trên là toàn bộ schema MVP. `sources.id`, `jobs.id`, `crawl_runs.id` là PK; `jobs.source_id` và `crawl_runs.source_id` tham chiếu `sources.id`; `job_tracking.job_id` tham chiếu `jobs.id`. Dùng `ON DELETE RESTRICT` cho các FK; bật enforcement trên từng kết nối. Việc tắt nguồn không xóa dữ liệu.
- Dùng `CHECK` cho các giá trị enum đã liệt kê trong hợp đồng: `geography`, `work_mode`, `relevance`, `seniority`, `category`, `description_scope`, `posted_precision`, `deadline_precision`, `listing_status`, `application_stage` và `crawl_runs.status`. Các boolean `is_active`, `is_saved`, `is_complete` chỉ nhận `0`/`1`; các bộ đếm không âm.
- `posted_precision`/`deadline_precision` là `unknown` khi và chỉ khi thời điểm tương ứng `NULL`; `date` hoặc `datetime` yêu cầu thời điểm khác `NULL`. `description_scope = none` khi `description_text IS NULL`; `full`/`excerpt` yêu cầu văn bản khác `NULL`.
- `finished_at` là `NULL` khi `running`, khác `NULL` khi lượt kết thúc và không trước `started_at`; lượt `success` phải có `is_complete = true`. Mỗi thời điểm hệ thống dùng cùng cách biểu diễn UTC, nhất quán độ chính xác và định dạng để phép so sánh trong SQLite có nghĩa; không so sánh chuỗi thời gian khác múi giờ hoặc khác định dạng.
- Tạo/cập nhật job không sửa `job_tracking`; một transaction theo nguồn gắn các thay đổi tin với kết quả lượt chạy. Nếu transaction kết thúc thất bại, rollback và ghi `failed` bằng transaction riêng khi DB khả dụng; nếu không ghi được, lượt `running` được phục hồi theo mục 4.4. Không thực hiện so sánh vắng mặt từ kết quả chưa commit.

## 9. Hành vi dữ liệu và độ tin cậy

1. **Không đoán ngày đăng:** `posted_at = NULL` khi không có dữ liệu; dùng `first_seen_at` để biểu diễn *ngày hệ thống phát hiện*.
2. **Không đoán tin còn tuyển:** cần nhãn/ghi chú rõ rằng tin đã được thấy tại lần kiểm tra nào; người dùng xác nhận tình trạng ở trang gốc.
3. **Không ghi trùng:** upsert theo `(source_id, external_id)`.
4. **Không mất dữ liệu theo dõi:** cập nhật job không được ghi đè `job_tracking`; dữ liệu ứng tuyển tồn tại qua lần thu thập mới.
5. **Không làm hỏng toàn bộ chu kỳ vì một nguồn lỗi:** xử lý và log theo từng nguồn.
6. **Giới hạn dữ liệu lưu:** chỉ lưu metadata việc làm, phần mô tả được phép lưu, URL và dữ liệu theo dõi cá nhân; tránh ghi credentials, cookies, thông tin đăng nhập của bên thứ ba. Không ghi ghi chú cá nhân hoặc toàn bộ response vào log mặc định.
7. **Tôn trọng nguồn:** chỉ thu thập ở API/trang được phép, không né cơ chế bảo vệ hay vượt CAPTCHA, kiểm tra điều khoản sử dụng và giới hạn truy cập trước khi kích hoạt nguồn.
8. **Độ phủ có giới hạn:** một vài board trên Greenhouse/Lever không đại diện cho toàn bộ thị trường tuyển dụng cybersecurity tại Việt Nam.

### 9.1. Vòng đời tin tuyển dụng

| Sự kiện | Hành vi |
|---|---|
| Tin mới đạt điều kiện lưu | Tạo một bản ghi; đặt các mốc hệ thống theo lần quan sát; `listing_status = listed`, trừ khi nguồn xác nhận đã đóng |
| Tin cũ `listed`/`not_seen` xuất hiện lại và không có tín hiệu đóng | Cập nhật `last_seen_at`, đặt bộ đếm vắng mặt về 0, chuyển `listed`; giữ `first_seen_at` và tracking |
| Tin chưa `closed` vắng trong một lượt `success` đầy đủ, cùng phạm vi | Tăng bộ đếm; sau 2 lượt đủ điều kiện liên tiếp chuyển `not_seen`, không chuyển `closed` |
| Lượt `partial` hoặc phạm vi không đầy đủ | Không tăng bộ đếm vắng mặt, không đổi trạng thái các tin không quan sát được; có thể cập nhật tin đã quan sát hợp lệ khi commit thành công |
| Lượt `failed` | Không lưu thay đổi tin và không đối chiếu tin vắng mặt; lưu lỗi lượt chạy khi DB khả dụng |
| Nguồn cung cấp tín hiệu đóng rõ ràng | Chuyển `closed`; nếu tin được quan sát trong lượt hiện tại thì cập nhật `last_seen_at`. Ví dụ tín hiệu là trường trạng thái chính thức hoặc thông báo đã ngừng nhận hồ sơ của đúng bài đăng |
| HTTP 403/429/5xx, timeout hoặc 404 đơn lẻ | Ghi lỗi hoặc cần kiểm tra; không đủ để kết luận `closed` |
| Tin đã `closed` | Giữ `closed` khi vắng hoặc chỉ còn trang lưu trữ; khi nguồn xác nhận đăng lại/đang mở, chuyển `listed`, cập nhật `last_seen_at`, đặt bộ đếm về 0 và giữ định danh/tracking |

Ngưỡng 2 lượt là mặc định có thể cấu hình theo nguồn. “Liên tiếp” tính trên các lượt đầy đủ thành công; lượt lỗi không tăng hoặc đặt lại bộ đếm. Chỉ so sánh các tin thuộc cùng phạm vi dữ liệu đang theo dõi. Khi không chứng minh được phạm vi đầy đủ, giữ trạng thái hiện tại và hiển thị mốc lần thấy gần nhất.

### 9.2. Kết quả thu thập và lỗi

- `success`: đã đọc hết phạm vi, xử lý hợp lệ và commit thành công. Kết quả 0 tin vẫn có thể thành công nếu phản hồi hợp lệ và xác nhận được danh sách rỗng; response sai cấu trúc không được coi là rỗng.
- `partial`: giữ được một phần dữ liệu hợp lệ nhưng còn trang/request thất bại hoặc bản ghi không hợp lệ. Không cập nhật `last_success_at`, không đối chiếu tin vắng mặt.
- `failed`: không giữ được kết quả sử dụng được do lỗi truy cập, cấu trúc, transaction hoặc gián đoạn. Nguồn khác vẫn được thực thi.
- `is_complete` phản ánh độ đầy đủ của quá trình đọc và nhận diện tin; chỉ lượt vừa `success` vừa `is_complete = true` được đối chiếu tin vắng mặt.
- Có timeout và số lần retry hữu hạn; xử lý yêu cầu chờ của nguồn khi có, không lặp vô hạn. Lỗi định dạng dữ liệu cần được báo rõ, không giải quyết bằng retry liên tục.
- Đối chiếu trạng thái tin, cập nhật các bộ đếm cuối cùng và `last_success_at` phải nhất quán với dữ liệu đã commit. Không báo thành công trước khi commit.

### 9.3. Kiểm chứng chất lượng và giá trị sử dụng

- Tạo và gán nhãn bộ mẫu trước khi đánh giá, sau đó tách thành **bộ tinh chỉnh** keywords/quy tắc và **bộ kiểm thử độc lập**. Bộ kiểm thử có tối thiểu 40 tin có kết luận rõ, gồm ít nhất 20 liên quan và 20 không liên quan, bao phủ tiếng Việt/Anh và nhiều kiểu chức danh. Hai bộ không có cùng tin hoặc bản sao/biến thể gần giống; không dùng nhãn, kết quả hay lỗi của bộ kiểm thử để tinh chỉnh trực tiếp. Nếu đã dùng để tinh chỉnh, chuẩn bị bộ kiểm thử độc lập mới trước lần nghiệm thu tiếp theo.
- Thêm các trường hợp mơ hồ có nhãn mong đợi riêng để kiểm tra hành vi `uncertain`/`unknown`; không tính những trường hợp chưa thể gán nhãn nhị phân vào phép đo precision/recall.
- Mục tiêu trên **bộ kiểm thử độc lập**: precision và recall nhận diện cybersecurity đều đạt ít nhất 90%. Precision là tỷ lệ tin thực sự liên quan trong nhóm được nhận diện `related`; recall là tỷ lệ tin được nhận diện `related` trong toàn bộ tin liên quan đã gán nhãn. Tin liên quan bị xếp `uncertain` vẫn tính là bỏ sót trong phép đo recall này. Báo cáo số lượng mẫu và nhầm lẫn cùng tỷ lệ; nếu không đủ hai nhóm hoặc không có dự đoán `related`, báo không đủ căn cứ thay vì tính kết quả đạt.
- Bộ test phải bao gồm: `SOC Analyst Intern`, chức danh bảo vệ, `Security Analyst` thiếu cấp bậc, JD cybersecurity nhắc bảo vệ vật lý, tin không có từ “security” nhưng có nhiệm vụ ATTT rõ, nhiều cấp bậc, đa địa điểm, remote không rõ quốc gia và thiếu ngày đăng/địa điểm. Kiểm tra các trường hợp Việt Nam cùng nước ngoài, chỉ nước ngoài, nước ngoài cùng remote chưa rõ phạm vi và remote cho phép tại Việt Nam theo mục 4.2. Có ví dụ tiếng Việt có dấu/không dấu, tiếng Anh và chức danh mơ hồ.
- Ghi riêng kết quả cấp bậc/địa lý và các lỗi đã biết. Với tập nhỏ, chỉ vài mẫu thay đổi có thể làm tỷ lệ biến động mạnh; kết quả không đại diện toàn thị trường và không bảo đảm chất lượng thực tế. Không dùng synthetic data, một tin mẫu hoặc bộ test để khẳng định nguồn thực tế đã được kiểm chứng hay có độ phủ tốt.
- Sau khi chạy được luồng thật, dùng thử trong 7 ngày lịch, ghi số lượt chạy thực tế, tin mới phù hợp, tin đầu vào và tin nhận nhầm/bỏ sót qua kiểm tra thủ công. Không có tin mới trong tuần không tự động là lỗi collector; nếu nguồn hoạt động nhưng ít hữu ích, ưu tiên khảo sát thêm nguồn thay vì thêm tính năng giao diện.

## 10. Điều kiện nghiệm thu v1.0 (Definition of Done)

- [ ] Cài đặt và chạy được trên Windows theo hướng dẫn trong `README.md`.
- [ ] Có ít nhất **1 nguồn thật** được phép truy cập và có dữ liệu tuyển dụng phù hợp để kiểm thử end-to-end; nếu chưa có, trạng thái nguồn là blocker thay vì dùng dữ liệu giả và tuyên bố hoàn thành.
- [ ] Có `docs/source-validation.md` với kết quả khảo sát, căn cứ truy cập/lưu nội dung, độ đầy đủ phân trang và bằng chứng tin thật tại Việt Nam; nêu rõ nguồn chưa được xác minh.
- [ ] Có thể chạy collector bằng CLI; kết quả được lưu vào SQLite.
- [ ] Chạy lại collector không tạo tin trùng từ cùng nguồn.
- [ ] Đạt mục tiêu precision/recall trên bộ mẫu mục 9.3; kiểm thử các trường hợp mơ hồ, địa điểm và cấp bậc, không chỉ hai ví dụ chức danh.
- [ ] Dashboard hiển thị được dữ liệu, tìm kiếm và lọc theo cấp bậc/nhóm công việc/địa điểm/nguồn.
- [ ] Bấm `Xem tin gốc` mở đúng liên kết bài đăng của nguồn.
- [ ] Có thể lưu tin, sửa trạng thái và ghi chú ứng tuyển; dữ liệu tồn tại sau khi khởi động lại ứng dụng.
- [ ] Đánh dấu đã xem/chưa xem được lưu bền vững, độc lập với lưu tin/ứng tuyển; crawl lại không đặt lại các trạng thái cá nhân.
- [ ] Crawl lại dữ liệu không đổi: không thêm bản ghi, `updated_count = 0`, chỉ cập nhật lần thấy; thay đổi HTML trình bày/khoảng trắng vô nghĩa không làm tăng số cập nhật; sửa nội dung JD có nghĩa làm tăng số cập nhật và giữ `first_seen_at`/tracking.
- [ ] Thiếu ID dùng fallback URL không trùng; URL có tham số định danh không bị gộp nhầm. Tin thiếu dữ liệu tùy chọn vẫn hiển thị đúng nhãn thiếu thông tin.
- [ ] Hai lượt thành công đầy đủ không thấy tin chuyển `not_seen`; lỗi, thiếu trang và 404 đơn lẻ không chuyển `closed`. Tin mở lại giữ đúng bản ghi và tracking.
- [ ] Bộ lọc gom các biến thể tên TP.HCM, xử lý tin nhiều địa điểm theo mục 4.2, và tìm được tiếng Việt không dấu trong phạm vi văn bản đã lưu. Tin `related` có `geography = unknown` được hiển thị và gắn nhãn khi chưa lọc địa điểm; khi lọc địa điểm cụ thể, có nhắc nhở và cách xem các tin chưa xác minh bị ẩn theo mục 4.3.
- [ ] Có lịch sử thu thập và thông báo lỗi nguồn rõ ràng.
- [ ] Cấu hình chạy mỗi 12 giờ, có hướng dẫn xử lý khi máy không hoạt động đúng lịch.
- [ ] Chạy thủ công trùng lịch không tạo collector thứ hai; lượt bị gián đoạn được nhận diện, dashboard và collector cùng dùng đúng DB.
- [ ] Sao lưu và khôi phục thử trên bản DB riêng thành công, giữ nguyên ghi chú, trạng thái đã xem và tiến trình ứng tuyển.
- [ ] Tests cơ bản pass; `.env` và database cá nhân không bị commit lên Git.

Các mục trên nghiệm thu **MVP kỹ thuật**. Kết quả dùng thử 7 ngày ở mục 9.3 được báo cáo riêng để đánh giá giá trị sử dụng; chưa có báo cáo thì không tuyên bố đã chứng minh công cụ hữu ích hoặc có độ phủ đủ. Không đặt chỉ tiêu số tin mới bắt buộc vì còn phụ thuộc thực tế tuyển dụng và thời gian máy hoạt động.

## 11. Thứ tự triển khai

| Giai đoạn | Phạm vi | Kết quả bàn giao |
|---|---|---|
| 0 — Source validation | Khảo sát nguồn, xác minh ít nhất 1 nguồn có tin cybersecurity tại Việt Nam, chuẩn bị mẫu gán nhãn | `docs/source-validation.md`, response mẫu được phép lưu, quyết định adapter; chưa đạt thì chưa triển khai toàn bộ dashboard |
| 1 — Core MVP | Một adapter, chuẩn hóa/phân loại/lọc cơ bản, SQLite, CLI và một màn hình Streamlit có URL gốc | Thu thập tin thật → lưu DB → hiển thị → mở đúng bài gốc; chạy lại không trùng |
| 2 — MVP Complete: dữ liệu và tracking | Hoàn thiện mô hình, bộ phân loại, bộ lọc, địa điểm, vòng đời tin, đã xem/lưu/ứng tuyển | Đạt kiểm thử dữ liệu và ngưỡng chất lượng; giữ tracking qua cập nhật |
| 3 — MVP Complete: vận hành | Collector Monitor, scheduler, khóa chạy trùng, retry, logging, xử lý gián đoạn, sao lưu, README | Đạt checklist nghiệm thu kỹ thuật trên Windows |
| 4 — Validation: dùng thử | Theo dõi 7 ngày lịch, kiểm tra thủ công độ liên quan và mức hữu ích của nguồn | Báo cáo kết quả, giới hạn quan sát và danh sách nguồn/tính năng ưu tiên tiếp theo; không thay đổi checklist mục 10 |

## 12. Các quyết định để dành cho v1.1+

- Thêm API adapter/nguồn tuyển dụng khác sau khi kiểm tra tính hợp lệ và chất lượng dữ liệu.
- Tự khám phá nguồn mới, nếu danh sách cấu hình thủ công không còn đáp ứng nhu cầu.
- Thông báo khi có công việc mới hợp tiêu chí qua Telegram/email.
- Chấm điểm mức phù hợp theo kỹ năng, địa điểm, kinh nghiệm.
- Dò tin giống nhau giữa các nguồn bằng quy tắc hoặc semantic matching.
- Lưu các phiên bản JD và lịch sử chi tiết thay đổi; v1 chỉ ghi nhận thay đổi hiện tại qua `job_updated_at`, không lưu bản cũ.
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

## 14. Ghi nhận thay đổi tài liệu 1.1

- Giữ mục tiêu sản phẩm MVP v1.0; phiên bản 1.1 ở tiêu đề là phiên bản tài liệu.
- Làm rõ thu thập từ nguồn cấu hình sẵn, quy trình kiểm chứng và trạng thái chưa xác minh nguồn thực tế.
- Bổ sung tiêu chí liên quan/địa lý/cấp bậc, tin cần xác minh và bộ mẫu đo chất lượng.
- Đồng bộ tìm kiếm, lọc địa điểm, trạng thái đã xem và các mốc thời gian với hợp đồng dữ liệu.
- Quy định tin vắng mặt/đóng/mở lại, kết quả thu thập và ý nghĩa bộ đếm.
- Bổ sung chống chạy chồng, khôi phục sau gián đoạn, sao lưu và nghiệm thu tương ứng.
- Triển khai luồng dữ liệu thật xuyên suốt trước, tách nghiệm thu kỹ thuật khỏi đánh giá giá trị sau dùng thử.

**Tài liệu tham khảo về adapter ứng viên:** [Greenhouse Job Board API](https://docs.greenhouse.io/job-board) dùng định danh board; [Lever Postings API](https://github.com/lever/postings-api) dùng site theo doanh nghiệp. Các tài liệu này mô tả cơ chế API, không thay thế việc kiểm chứng từng nguồn ở giai đoạn 0.

## 15. Open Questions

Các câu hỏi này không ngăn bắt đầu Phase 0; không được xem khuyến nghị là kết quả đã xác minh.

1. **Nguồn đầu tiên là board nào?** Phương án: một board doanh nghiệp dùng Greenhouse/Lever hoặc nguồn khác có điều kiện truy cập phù hợp. Khuyến nghị: khảo sát theo mục 4.1.1 và chọn nguồn có tin phù hợp, có bằng chứng truy cập/lưu dữ liệu và định danh đáng tin cậy. Chưa có nguồn nào được xác minh trong tài liệu này.
2. **Lưu toàn bộ mô tả, đoạn trích hay không lưu mô tả cho từng nguồn?** Phương án: `full`, `excerpt` hoặc `none` theo điều kiện thực tế. Khuyến nghị: xác minh quyền và nhu cầu trong Phase 0, chọn phạm vi được phép; khả năng tìm kiếm bị giới hạn bởi phần được lưu.
3. **Mức độ nguồn hữu ích thế nào là đủ đối với người dùng?** Phương án: đánh giá thủ công sau 7 ngày hoặc đặt thêm ngưỡng số tin phù hợp sau khi có dữ liệu thực tế. Khuyến nghị: báo cáo số tin và chất lượng trong lần dùng thử đầu, rồi mới thống nhất ngưỡng; hiện chưa đủ bằng chứng để đặt chỉ tiêu số lượng.

## 16. Ghi nhận thay đổi tài liệu 1.2

- Phân chia Core MVP, MVP Complete và Validation theo thứ tự hoàn thành; giữ nguyên MVP sản phẩm v1.0 và checklist nghiệm thu kỹ thuật.
- Làm rõ so khớp tiếng Việt không dấu, bốn mốc thời gian và so sánh JD để tránh cập nhật giả do HTML.
- Rà soát khóa, enum, thời gian, chỉ mục, WAL, khóa ngoại, giao dịch đồng thời và sao lưu SQLite.
- Tách bộ tinh chỉnh và bộ kiểm thử classifier độc lập; duy trì mục tiêu precision/recall và nêu giới hạn tập mẫu nhỏ.
- Ghi các quyết định còn mở, phân biệt khảo sát nguồn thực tế với ví dụ provider và đánh giá giá trị sau dùng thử.

**Tham khảo kỹ thuật:** [SQLite WAL](https://www.sqlite.org/wal.html), [SQLite PRAGMA](https://www.sqlite.org/pragma.html), [SQLite Online Backup API](https://www.sqlite.org/backup.html), [Python Unicode HOWTO](https://docs.python.org/3/howto/unicode.html).