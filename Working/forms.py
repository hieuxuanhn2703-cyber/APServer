import json
import os
import datetime
from django import forms
from django.conf import settings

CONFIG_PATH = os.path.join(settings.BASE_DIR, "Working", "config.json")

NUMERIC_FIELD_ATTRS = {"class": "numeric-input", "inputmode": "numeric"}


def load_config():
    try:
        from .models import Product
        config = {}
        for product in Product.objects.all():
            config[product.name] = {"colors": {}}
            for color in product.colors.all():
                config[product.name]["colors"][color.name] = ["N/A"]
        return config
    except Exception:
        # Fallback in case models are not ready during initial load
        return {}


class ProcessForm(forms.Form):
    ngay_lam_viec = forms.DateField(
        label="Ngày làm việc",
        initial=datetime.date.today,
        required=True,
        error_messages={'required': 'Vui lòng chọn ngày làm việc.'},
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    xuong = forms.IntegerField(
        label="Xưởng", required=True, min_value=1, initial=0,
        error_messages={'min_value': 'Vui lòng nhập số xưởng khác 0.', 'required': 'Vui lòng nhập số xưởng.'},
        widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS)
    )
    to = forms.IntegerField(
        label="Tổ", required=True, min_value=1, initial=0,
        error_messages={'min_value': 'Vui lòng nhập số tổ khác 0.', 'required': 'Vui lòng nhập số tổ.'},
        widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS)
    )
    ma_hang = forms.ChoiceField(label="Mã hàng")
    mau = forms.ChoiceField(label="Màu")
    co = forms.CharField(label="Cỡ", required=False, initial="N/A")

    nhan_btp = forms.IntegerField(label="Nhận BTP", required=False, min_value=0, initial=0,
                                   widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS))
    vao_chuyen = forms.IntegerField(label="Vào chuyền", required=False, min_value=0, initial=0,
                                     widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS))
    giua_chuyen = forms.IntegerField(label="Giữa chuyền", required=False, min_value=0, initial=0,
                                      widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS))
    ra_chuyen = forms.IntegerField(label="Ra chuyền", required=False, min_value=0, initial=0,
                                    widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS))
    thu_hoa = forms.IntegerField(label="Thu hóa", required=False, min_value=0, initial=0,
                                  widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS))
    la_thanh_pham = forms.IntegerField(label="Là thành phẩm", required=False, min_value=0, initial=0,
                                        widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS))
    kcs = forms.IntegerField(label="KCS", required=False, min_value=0, initial=0,
                              widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS))
    nhap_hoan_thien = forms.IntegerField(label="Nhập hoàn thiện", required=False, min_value=0, initial=0,
                                          widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS))

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

class FinishingForm(forms.Form):
    ngay_lam_viec = forms.DateField(
        label="Ngày làm việc",
        initial=datetime.date.today,
        required=True,
        error_messages={'required': 'Vui lòng chọn ngày làm việc.'},
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    ma_hang = forms.ChoiceField(label="Mã hàng")
    mau = forms.ChoiceField(label="Màu")

    nhan_hang_hoan_thien = forms.IntegerField(label="Nhận hàng hoàn thiện", required=False, min_value=0, initial=0, widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS))
    the_bai = forms.IntegerField(label="Thẻ bài", required=False, min_value=0, initial=0, widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS))
    gap_hang = forms.IntegerField(label="Gấp hàng", required=False, min_value=0, initial=0, widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS))
    treo_dong_thung = forms.IntegerField(label="Treo/Đóng thùng", required=False, min_value=0, initial=0, widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS))

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