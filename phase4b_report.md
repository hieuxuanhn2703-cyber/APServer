# PHASE 4B — AUTHENTICATION & APPLICATION SHELL
## Báo Cáo Nghiệm Thu Hoàn Thiện Tầng Xác Thực & Khung Giao Diện React

---

## 1. Implementation Summary
Trong giai đoạn **Phase 4B**, hệ thống React Frontend đã được gia cố và hoàn thiện toàn bộ luồng xác thực (Authentication Flow) và khung ứng dụng (Application Shell) sẵn sàng cho môi trường production:
- **Xác thực toàn diện**: Xây dựng luồng đăng nhập chặt chẽ, kiểm tra hợp lệ đầu vào phía client, ngăn chặn gửi trùng request khi đang xử lý, và ánh xạ các lỗi xác thực từ backend (`400`, `401`, `403`, lỗi mạng) thành thông điệp tiếng Việt rõ ràng, dễ hiểu.
- **Client API & Quản lý Token**: Gia cố bộ client HTTP trung tâm (`src/api/client.js`) với cơ chế quản lý promise refresh token đồng thời (concurrency lock) nhằm chống race-condition khi có nhiều request đồng thời gặp 401; phân định rạch ròi giữa 401 (hết phiên) và 403 (không đủ quyền).
- **Khung ứng dụng linh hoạt (AppLayout & Shell)**: Hoàn thiện `Sidebar.jsx` và `Topbar.jsx` với khả năng thu gọn trên desktop, chuyển sang ngăn kéo drawer trên mobile/tablet, tích hợp xử lý khóa cuộn trang (`body overflow: hidden`) và phím `Escape` đóng drawer. Tiêu đề Topbar được cập nhật động theo từng trang đang xem.
- **Bảo toàn 100% Backend & Django Legacy**: Không thay đổi model, không thêm migration, không sửa code backend hay Django templates. Mọi màn hình nghiệp vụ (Inventory, Accounting, Working, Dashboard) tiếp tục được giữ dưới dạng placeholder chờ di chuyển theo từng giai đoạn sau.

---

## 2. Authentication Flow
Luồng xác thực hoàn chỉnh tuân thủ tuyệt đối chuẩn DRF JWT đã kiểm duyệt:
1. **Đăng nhập (`LoginPage.jsx`)**:
   - Thu thập và kiểm tra `account` (được `trim()`) và `password`.
   - Gửi yêu cầu `POST /api/v1/auth/token/` qua `apiClient` (với `skipAuth: true`).
   - Lưu trữ cặp khóa `{ access, refresh }` thông qua lớp trừu tượng `tokenStorage`.
   - Gửi yêu cầu `GET /api/v1/auth/me/` để lấy thông tin người dùng (`id`, `account`, `name`, `role`).
   - Cập nhật state người dùng trong `AuthContext` và chuyển hướng tới địa chỉ người dùng đang muốn truy cập (hoặc chuyển hướng thông minh theo vai trò).
2. **Ngăn chặn lỗi & trùng lặp**:
   - Submit button và các ô input tự động disabled khi `isSubmitting = true`.
   - Form có nhãn ngữ nghĩa, `aria-invalid`, `aria-describedby` và `aria-live` cho khối thông báo lỗi.

---

## 3. Token Management
- Toàn bộ thao tác đọc/ghi token đều tập trung duy nhất tại `src/utils/tokenStorage.js`.
- Cung cấp các phương thức an toàn: `getAccessToken()`, `getRefreshToken()`, `setTokens()`, `setAccessToken()`, `clearTokens()`, `hasAccessToken()`, `hasRefreshToken()`.
- **An ninh dữ liệu**:
  - Không bao giờ lưu mật khẩu ở bất cứ đâu (`localStorage`, `sessionStorage`, `state`).
  - Không bao giờ in token, Authorization header hay mật khẩu ra `console.log`.
  - Try-catch bọc quanh các thao tác localStorage để chống lỗi môi trường bảo mật cao.

---

## 4. API Client
Được triển khai trong `src/api/client.js` với các tính năng:
- **Tự động gắn JWT**: Kiểm tra và gắn `Authorization: Bearer <token>` vào request headers.
- **Tự động làm mới khi thiếu access token**: Nếu access token bị mất nhưng refresh token vẫn còn, client sẽ chủ động làm mới trước khi gửi yêu cầu.
- **Concurrency Guard**: Sử dụng `refreshTokenPromise` để đảm bảo khi nhiều request đồng thời nhận 401, chỉ có **duy nhất 1 request** gọi `POST /api/v1/auth/token/refresh/`. Các request còn lại cùng chờ và retry với token mới tạo.
- **Chống vòng lặp vô tận (Loop Prevention)**: Nếu sau khi làm mới token và retry mà vẫn nhận 401 (hoặc refresh token hết hạn), client xóa toàn bộ token và phát sự kiện `auth:session-expired` để đưa người dùng về trang đăng nhập.

---

## 5. Session Restoration
Khi người dùng tải lại trang (F5) hoặc mở tab mới:
1. `AuthProvider` khởi chạy effect `refreshUser()`.
2. Kiểm tra `hasAccessToken()` hoặc `hasRefreshToken()`. Nếu không có, đặt `user = null` và kết thúc loading.
3. Nếu có token, gọi `authApi.getMe()`:
   - Nếu access token hợp lệ -> nhận hồ sơ người dùng -> `user` được khôi phục, phiên làm việc tiếp tục.
   - Nếu access token hết hạn -> `apiClient` tự động kích hoạt refresh -> nhận token mới -> lấy hồ sơ thành công.
   - Nếu refresh thất bại -> xóa token, chuyển trạng thái unauthenticated -> điều hướng về `/login`.

---

## 6. Logout
Cơ chế đăng xuất an toàn:
- Gọi hàm `logout()` từ `AuthContext`.
- Xóa sạch `access` và `refresh` trong `tokenStorage`.
- Đặt `user = null` và xóa các thông báo lỗi.
- Đóng sidebar drawer nếu đang mở trên mobile.
- Lập tức chuyển hướng về trang `/login`. Các route được bảo vệ không thể truy cập sau khi đăng xuất.
- Tuyệt đối không gửi mật khẩu hay dữ liệu nhạy cảm trong quá trình đăng xuất.

---

## 7. Protected Routes
Được quản lý bởi `ProtectedRoute.jsx`:
- **Đang tải (`isLoading = true`)**: Hiển thị component `<LoadingSpinner />` đồng bộ giao diện.
- **Chưa đăng nhập (`!isAuthenticated`)**: Điều hướng về `<Navigate to="/login" state={{ from: location }} replace />` để giữ lại đường dẫn ban đầu cho lần đăng nhập tiếp theo.
- **Đã đăng nhập**: Render nội dung bên trong `<AppLayout />`.

---

## 8. Role-aware Navigation
Phân quyền hiển thị theo vai trò trên giao diện (`Sidebar.jsx` & `AppRoutes.jsx`):
- `PREMIUM`, `QUAN_LY`, `KE_TOAN`: Xem Báo Cáo Sản Xuất (`/dashboard`), Doanh Thu & Đơn Giá (`/accounting`), Kho Vật Tư (`/inventory`).
- `KHO`: Xem Quản Lý Kho (`/inventory`).
- `BASIC`, `NHA_CAT`, `KCS`, `HOAN_THIEN`: Xem Quy Trình Sản Xuất (`/working`).
- **Trang chủ (`/`)**: Điều hướng tự động dựa trên vai trò (`HomeRedirect`):
  - Nhóm Quản lý/Kế toán -> `/dashboard`
  - Nhóm Thủ kho -> `/inventory`
  - Nhóm Công nhân sản xuất -> `/working`
  - Vai trò chưa xác định -> fallback an toàn về `/dashboard`.
- **Nguyên tắc cốt lõi**: Phân quyền tại React thuần túy hỗ trợ trải nghiệm (UX). Các permission DRF trên backend (`IsAuthenticatedAppUser`, v.v.) nắm quyền kiểm soát an ninh tối cao.

---

## 9. Application Shell
Khung giao diện hoàn chỉnh gồm:
- **`AppLayout.jsx`**: Wrapper trung tâm kết nối `Sidebar`, `Topbar` và nội dung `<Outlet />`.
- **`Sidebar.jsx`**:
  - Logo và thương hiệu "MAY AN PHÁT".
  - Danh mục điều hướng nhóm theo phân hệ nghiệp vụ.
  - Hiển thị thông tin người dùng: Tên, avatar viết tắt, huy hiệu vai trò.
  - Nút đăng xuất nhanh.
- **`Topbar.jsx`**:
  - Nút bật/tắt menu sidebar với đầy đủ `aria-controls` và `aria-expanded`.
  - Tiêu đề trang cập nhật tự động theo đường dẫn route.
  - Lời chào và huy hiệu vai trò người dùng góc trên bên phải.

---

## 10. Responsive Behaviour
- **Desktop (>1024px)**:
  - Sidebar hiển thị cố định bên trái, hỗ trợ chế độ thu gọn (collapsed 70px) hoặc mở rộng (260px).
  - Trạng thái thu gọn được lưu giữ trong `localStorage` (`pm_sidebar_collapsed`).
- **Tablet / Mobile (<=1024px)**:
  - Sidebar chuyển thành dạng ngăn kéo (Drawer) trượt ngang từ bên trái (`transform: translateX(-100%)` -> `translateX(0)`).
  - Lớp phủ mờ nền (`sidebar-backdrop`) xuất hiện, bấm vào backdrop sẽ đóng drawer.
  - Bấm vào bất kỳ link điều hướng nào hoặc nút đăng xuất sẽ tự động đóng drawer.
  - Phím `Escape` đóng drawer ngay lập tức.
  - Khóa cuộn trang `document.body.style.overflow = 'hidden'` khi drawer mở, tránh lỗi tràn trang trên điện thoại.

---

## 11. Error / Loading / 401 / 403 Handling
- **Loading**: Sử dụng `<LoadingSpinner message="..." />` với hiệu ứng quay CSS nhẹ nhàng và `aria-live="polite"`.
- **Error**: Sử dụng `<ErrorState title="..." message="..." onRetry={...} />` hiển thị lỗi thân thiện kèm nút thử lại.
- **Phân định 401 vs 403**:
  - **401 Unauthorized**: Có nghĩa là token hết hạn hoặc chưa đăng nhập. Client thử refresh token 1 lần; nếu thất bại, đăng xuất an toàn và chuyển về `/login`.
  - **403 Forbidden**: Có nghĩa là người dùng đã đăng nhập nhưng không có quyền với tài nguyên cụ thể (hoặc tài khoản chưa duyệt). Client ném `ApiError(..., 403)`, giao diện hiển thị `<Unauthorized />` hoặc thông báo lỗi phù hợp. **Tuyệt đối không tự động đăng xuất người dùng hợp lệ khi gặp lỗi 403.**

---

## 12. Accessibility
- Các nút bấm icon có `aria-label` và `title` rõ ràng (nút toggle menu, nút đóng menu).
- Phím tắt `Escape` hỗ trợ đóng drawer trên thiết bị di động.
- Nút submit login hiển thị trạng thái `aria-busy` và vô hiệu hóa khi đang submit.
- Form inputs liên kết ngữ nghĩa với `<label htmlFor="...">`, hỗ trợ `aria-invalid` và `aria-describedby`.
- Thêm lớp CSS `:focus-visible` cho toàn bộ nút bấm, liên kết và ô nhập liệu để hỗ trợ người dùng duyệt bằng bàn phím.

---

## 13. Security Review
| Tiêu chí an ninh | Trạng thái | Ghi chú |
| :--- | :---: | :--- |
| Không lưu mật khẩu | ✅ ĐẠT | Mật khẩu chỉ gửi qua body đăng nhập, không lưu vào state/storage |
| Không log mật khẩu / token | ✅ ĐẠT | Không có lệnh `console.log` nào chứa credentials hay tokens |
| Không hardcode URL / secrets | ✅ ĐẠT | Toàn bộ URL cấu hình qua `VITE_API_BASE_URL` |
| Token đi qua abstraction | ✅ ĐẠT | Toàn bộ truy xuất qua `tokenStorage.js` |
| Backend giữ thẩm quyền bảo mật | ✅ ĐẠT | Phân quyền React chỉ phục vụ UX |
| Chống refresh token loop | ✅ ĐẠT | Giới hạn retry 1 lần, clear session nếu refresh thất bại |
| Khóa route khi chưa đăng nhập | ✅ ĐẠT | `ProtectedRoute` chặn và chuyển hướng về `/login` |

---

## 14. Django Compatibility
- Toàn bộ hệ thống URL backend truyền thống của Django (`/`, `/login/`, `/dashboard/`, `/working/`, `/inventory/`, `/accounting/`) tiếp tục vận hành bình thường.
- Không thay đổi bất kỳ file template, view hoặc URL configuration nào của Django.

---

## 15. Legacy Frontend Compatibility
- Giữ nguyên vẹn toàn bộ các file CSS cũ (`Working/static/working/css/premium.css`, `login.css`, `list.css`, `edit.css`).
- Giữ nguyên vẹn toàn bộ file JavaScript cũ (`Working/static/working/js/cascade_select.js`, `excel_filter.js`).
- Khung React kế thừa trung thực bảng màu gốc: `#0f172a`, `#1e293b`, `#94a3b8`, `#f1f5f9`, và dải màu đỏ may An Phát.

---

## 16. Database Safety
- Lệnh kiểm tra: `python manage.py makemigrations --check`
- Kết quả: **`No changes detected`**
- Xác nhận: 0 model thay đổi, 0 migration được tạo, schema database giữ nguyên 100%.

---

## 17. Backend Regression Tests
Đã thực thi toàn bộ test suite backend liên quan:
1. **Working API Tests**:
   - Lệnh: `python manage.py test Working.api.tests`
   - Kết quả: `Ran 7 tests in 0.275s — OK`
2. **Working Legacy Tests**:
   - Lệnh: `python manage.py test Working.tests`
   - Kết quả: `Ran 19 tests in 1.368s — OK`
3. **Inventory Tests**:
   - Lệnh: `python manage.py test Inventory`
   - Kết quả: `Ran 17 tests in 0.624s — OK`

---

## 18. React Verification
- **Lệnh đóng gói**: `cd frontend && npm run build`
- **Kết quả build**:
  ```text
  vite v5.4.21 building for production...
  transforming...
  ✓ 53 modules transformed.
  rendering chunks...
  computing gzip size...
  dist/index.html                   0.76 kB │ gzip:  0.46 kB
  dist/assets/index-DNFlk1jm.css    8.70 kB │ gzip:  2.49 kB
  dist/assets/index-DulSEBVz.js   185.11 kB │ gzip: 59.41 kB
  ✓ built in 807ms
  ```
- **Xác nhận chất lượng**: 0 lỗi (errors), 0 cảnh báo (warnings).

---

## 19. Files Changed
### Tệp tin đã chỉnh sửa (Modified):
1. `frontend/src/api/client.js`: Gia cố concurrent refresh, proactive token refresh, phân giải chi tiết field errors của DRF.
2. `frontend/src/utils/tokenStorage.js`: Bổ sung `hasRefreshToken()`.
3. `frontend/src/context/AuthContext.jsx`: Hỗ trợ khôi phục phiên dựa trên cả access và refresh token.
4. `frontend/src/pages/LoginPage.jsx`: Bổ sung validation, hiển thị lỗi tài khoản chưa duyệt, trạng thái disabled/spinner và thuộc tính trợ năng.
5. `frontend/src/components/layout/Sidebar.jsx`: Bổ sung lắng nghe phím Escape, đóng drawer khi logout, gắn `aria-label`.
6. `frontend/src/components/layout/Topbar.jsx`: Tiếp nhận `isSidebarOpen`, bổ sung `aria-controls` và `aria-expanded`.
7. `frontend/src/layouts/AppLayout.jsx`: Xử lý khóa cuộn body khi mở drawer trên mobile.
8. `frontend/src/index.css`: Thêm quy tắc `:focus-visible` hỗ trợ điều hướng bàn phím.
9. `frontend/src/routes/AppRoutes.jsx`: Cập nhật logic điều hướng thông minh theo vai trò (`HomeRedirect`).
10. `docs/frontend.md`: Cập nhật trạng thái Phase 4B.

---

## 20. Dependencies
Không thêm bất kỳ phụ thuộc nào mới. Giữ nguyên bộ dependencies tối giản:
- `react`: ^18.3.1
- `react-dom`: ^18.3.1
- `react-router-dom`: ^6.28.0
- `vite` & `@vitejs/plugin-react` (devDependencies)

---

## 21. Known Issues
- Kiểm thử phân trang fixture `Accounting.tests.AccountingTests.test_team_revenue_pagination_5_per_page`: Lỗi so khớp dữ liệu fixture cũ đã ghi nhận từ các phase trước. Giữ nguyên theo nguyên tắc không can thiệp code ngoài phạm vi.

---

## 22. Deferred Work
Các nội dung nghiệp vụ được bảo lưu chuyển sang các phase sau:
- Di chuyển các màn hình chức năng của Kho (`Inventory`).
- Di chuyển các màn hình chức năng Kế toán (`Accounting`).
- Di chuyển các màn hình chức năng Quy trình sản xuất (`Working`).
- Di chuyển bảng Dashboard và chuyển đổi `cascade_select.js` sang React component có kiểm soát trạng thái.

---

## 23. Final Verdict
# 👉 **PASS**

Hệ thống xác thực và khung giao diện React đã đạt độ ổn định cao, hoàn toàn tương thích với Django backend, bảo vệ trọn vẹn dữ liệu và sẵn sàng tiếp nhận các màn hình nghiệp vụ trong các phase di chuyển tiếp theo.

---

### STOP CONDITION (Chỉ thị Dừng)
> Tuân thủ Mục 42 của `phase4b.md`: **DỪNG LẠI TẠI ĐÂY**. Không tự ý bắt đầu Phase 4C hoặc di chuyển bất kỳ màn hình nghiệp vụ nào khi chưa có yêu cầu và phê duyệt chính thức từ người dùng.
