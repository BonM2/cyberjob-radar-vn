# Hướng dẫn cho AI Agent

## Tổng quan dự án

CyberJob Radar VN là công cụ cá nhân tự động thu thập và theo dõi tin tuyển dụng an ninh mạng tại Việt Nam. Mục tiêu là MVP v1.0 cho một người dùng, chạy cục bộ trên Windows. Xem `intent.md` là đặc tả sản phẩm, không phải bằng chứng các tính năng đã được triển khai.

## Công nghệ và phạm vi

- Giữ kiến trúc Python modular monolith và các công nghệ đã thống nhất: Python 3.11+, HTTPX, SQLAlchemy 2.x, SQLite, Streamlit, pytest và Windows Task Scheduler.
- Không bổ sung hoặc thay thế công nghệ, hay cài thêm thư viện phụ thuộc khi chưa được người dùng cho phép.
- Không bổ sung FastAPI, React, Redis, Celery, Kafka, microservices, hỗ trợ nhiều người dùng hoặc phân loại bằng LLM/machine learning vào MVP v1.0, trừ khi người dùng yêu cầu hoặc phê duyệt rõ ràng.
- Chỉ thực hiện nhiệm vụ được yêu cầu; không thêm tính năng suy đoán hoặc tự động chuyển sang nhiệm vụ tiếp theo.

## Kiến trúc

- `collectors/` thu thập dữ liệu từ các nguồn tuyển dụng và chuyển về đầu vào chung; không truy cập database trực tiếp.
- `processing/` chuẩn hóa, xác thực, phân loại và loại bỏ dữ liệu trùng.
- `database/` quản lý kết nối, models, repositories và transactions.
- `services/` điều phối các trường hợp sử dụng và tương tác giữa các module.
- `dashboard/` hiển thị giao diện và nhận thao tác người dùng; không thu thập dữ liệu hoặc chứa logic nghiệp vụ.
- Đưa các thao tác database qua service và repository khi phù hợp. Tránh import vòng và các lớp trừu tượng không cần thiết.

## Chất lượng mã và tính toàn vẹn dữ liệu

- Viết mã Python dễ đọc, dễ bảo trì; đặt tên rõ nghĩa, chia hàm nhỏ theo trách nhiệm, dùng type hints khi phù hợp và xử lý exception rõ ràng. Không thêm mã không sử dụng hoặc ghi cứng thông tin bí mật.
- Sử dụng SQLAlchemy 2.x và SQLite. Bảo đảm các ràng buộc khóa chính, khóa ngoại và duy nhất; không thay đổi schema ngoài phạm vi nhiệm vụ.
- Chống trùng tin theo `(source_id, external_id)` và sử dụng transaction phù hợp với từng thao tác. Cập nhật tin phải giữ nguyên dữ liệu theo dõi ứng tuyển.
- Bảo vệ database cục bộ và dữ liệu cá nhân. Không thực hiện thao tác phá hủy dữ liệu khi chưa được cho phép.

## Thu thập dữ liệu

- Chỉ tích hợp nguồn đã xác minh, có bằng chứng về quyền truy cập và sử dụng nội dung. API truy cập được hoặc tên provider không đủ để xác minh nguồn.
- Tuân thủ điều khoản và giới hạn truy cập của nguồn; sử dụng timeout, giới hạn tốc độ và xử lý lỗi phù hợp. Một nguồn lỗi không được làm gián đoạn việc xử lý các nguồn khác.
- Không kết luận tin đã đóng nếu thiếu bằng chứng đáng tin cậy. Không tự tạo ngày đăng còn thiếu hoặc coi fixture giả lập là bằng chứng về nguồn thực tế.
- Có thể sử dụng fixtures và mocks trong kiểm thử, nhưng không dùng chúng thay thế dữ liệu tuyển dụng thật hoặc trình bày chúng như một nguồn đã xác minh.

## Bảo mật

- Không commit `.env`, thông tin đăng nhập, API keys hoặc database cá nhân. Không ghi thông tin bí mật hoặc dữ liệu cá nhân nhạy cảm vào log.
- Mặc định chỉ phục vụ dashboard trên giao diện mạng cục bộ; không mở cổng công khai khi chưa được cho phép rõ ràng.

## Kiểm thử và kiểm chứng

- Sử dụng pytest. Bổ sung unit test cho logic nghiệp vụ và integration test khi tích hợp các module, phù hợp với thay đổi.
- Không làm yếu test chỉ để mã vượt qua kiểm thử, che giấu lỗi hoặc giả mạo kết quả. Chỉ báo cáo các bước kiểm tra thực sự đã chạy và kết quả của chúng.

## Quy trình và tài liệu

1. Đọc nhiệm vụ của người dùng và chỉ kiểm tra các file, thành phần phụ thuộc liên quan. Xác định module bị ảnh hưởng; lập kế hoạch cho công việc nhiều bước khi hữu ích.
2. Chỉ thay đổi những gì nhiệm vụ yêu cầu. Giữ nguyên chức năng không liên quan và các thay đổi hiện có của người dùng; không thay đổi kiến trúc hoặc mở rộng phạm vi khi chưa được cho phép.
3. Rà soát các file đã thay đổi và chạy test phù hợp khi được yêu cầu hoặc khi có thể thực hiện an toàn. Báo cáo thay đổi, kết quả kiểm chứng và những phần chưa hoàn thành hoặc chưa được xác minh; không tuyên bố hoàn thành khi thiếu bằng chứng.

- Không chỉnh sửa `intent.md` trừ khi người dùng yêu cầu rõ ràng. Không tạo tài liệu khi chưa được yêu cầu hoặc viết lại toàn bộ tài liệu chỉ vì một thay đổi nhỏ.
- Giữ tài liệu phù hợp với trạng thái triển khai thực tế; không mô tả tính năng chưa hoàn thành như đã hoàn thành.
- Không tự đặt ra các yêu cầu nghiệp vụ còn thiếu. Nếu điểm chưa rõ hoặc mâu thuẫn quan trọng ngăn việc ra quyết định, hãy giải thích và hỏi người dùng, đồng thời tiếp tục những phần việc độc lập.
