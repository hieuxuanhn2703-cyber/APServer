import datetime
from django import forms
from Working.forms import load_config, NUMERIC_FIELD_ATTRS, DATE_FIELD_ATTRS
from Working.models import ProductColor
from .models import ProductPrice, ExportReport


def load_price_map():
    """
    Trả về dictionary dạng { (ma_hang, mau): don_gia }
    và dạng string key { "ma_hang__mau": don_gia } phục vụ JSON Script cho JS.
    """
    price_map = {}
    for pc in ProductColor.objects.select_related('product', 'price').all():
        price_val = pc.price.don_gia if hasattr(pc, 'price') else 0
        price_map[f"{pc.product.name}__{pc.name}"] = price_val
    return price_map


class ExportReportForm(forms.Form):
    ngay_xuat = forms.DateField(
        label="Ngày xuất hàng",
        initial=datetime.date.today,
        required=True,
        error_messages={'required': 'Vui lòng chọn ngày xuất hàng.'},
        widget=forms.DateInput(attrs=DATE_FIELD_ATTRS)
    )
    ma_hang = forms.ChoiceField(label="Mã hàng", choices=[], required=True)
    mau = forms.ChoiceField(label="Màu sắc", choices=[], required=True)
    
    so_luong_xuat = forms.IntegerField(
        label="Số lượng xuất",
        required=True,
        min_value=1,
        initial=0,
        error_messages={'min_value': 'Số lượng xuất phải lớn hơn 0.', 'required': 'Vui lòng nhập số lượng xuất.'},
        widget=forms.NumberInput(attrs={**NUMERIC_FIELD_ATTRS, 'id': 'id_so_luong_xuat', 'oninput': 'calculateThanhTien()'})
    )
    
    ghi_chu = forms.CharField(
        label="Ghi chú",
        required=False,
        widget=forms.TextInput(attrs={'class': 'text-input', 'placeholder': 'Ghi chú (khách hàng, xe chở, số chứng từ...)'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = load_config()
        self.fields["ma_hang"].choices = [("", "-- Chọn mã hàng --")] + [
            (ma, ma) for ma in self.config.keys()
        ]
        all_colors = set()
        for data in self.config.values():
            for color in data["colors"].keys():
                all_colors.add(color)
        self.fields["mau"].choices = [("", "-- Chọn màu --")] + [(c, c) for c in sorted(all_colors)]

    def clean(self):
        cleaned_data = super().clean()
        ma_hang = cleaned_data.get("ma_hang")
        mau = cleaned_data.get("mau")

        if ma_hang and ma_hang not in self.config:
            self.add_error("ma_hang", "Mã hàng không hợp lệ.")
            return cleaned_data

        if ma_hang and mau:
            colors = self.config[ma_hang]["colors"]
            if mau not in colors:
                self.add_error("mau", f"Màu '{mau}' không thuộc mã hàng '{ma_hang}'.")
                return cleaned_data

        return cleaned_data


class PriceUpdateForm(forms.Form):
    product_color_id = forms.IntegerField(widget=forms.HiddenInput())
    don_gia = forms.IntegerField(
        label="Đơn giá (VNĐ)",
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'numeric-input', 'style': 'text-align: right;'})
    )
