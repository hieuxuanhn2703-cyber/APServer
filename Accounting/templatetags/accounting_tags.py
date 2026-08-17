from django import template

register = template.Library()


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
