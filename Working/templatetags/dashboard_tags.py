from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Tạo query string mới dựa trên request.GET hiện tại,
    thay thế hoặc thêm các tham số được truyền vào (ví dụ p1=2, cut_filter_ma_hang='AT01').
    Bảo toàn toàn bộ các bộ lọc cột và bộ lọc ngày của tất cả các bảng.
    """
    request = context.get('request')
    if not request:
        return ""

    query = request.GET.copy()
    for key, value in kwargs.items():
        if value is None or value == "":
            query.pop(key, None)
        else:
            query[key] = str(value)

    return '?' + query.urlencode()


@register.filter(name='comma_num')
def comma_num(value):
    """
    Định dạng số nguyên/tiền tệ với dấu phẩy ngăn cách hàng nghìn (ví dụ: 150,000).
    Nếu giá trị rỗng hoặc không hợp lệ, trả về '0'.
    """
    if value is None or value == "":
        return "0"
    try:
        clean = str(value).replace(".", "").replace(",", "").replace(" ", "").replace("đ", "").replace("VNĐ", "").strip()
        num = int(float(clean))
        return f"{num:,}"
    except (ValueError, TypeError):
        return str(value)
