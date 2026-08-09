import json
import os
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
    ma_hang = forms.ChoiceField(label="Mã hàng")
    mau = forms.ChoiceField(label="Màu")
    co = forms.ChoiceField(label="Cỡ")
    to = forms.IntegerField(label="Tổ", required=True, min_value=1,
                            widget=forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS))

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

        all_colors, all_sizes = set(), set()
        for data in self.config.values():
            for color, sizes in data["colors"].items():
                all_colors.add(color)
                all_sizes.update(sizes)

        self.fields["mau"].choices = [("", "-- Chọn màu --")] + [(c, c) for c in sorted(all_colors)]
        self.fields["co"].choices = [("", "-- Chọn cỡ --")] + [(s, s) for s in sorted(all_sizes)]

    def clean(self):
        cleaned_data = super().clean()
        ma_hang = cleaned_data.get("ma_hang")
        mau = cleaned_data.get("mau")
        co = cleaned_data.get("co")

        if ma_hang and ma_hang not in self.config:
            self.add_error("ma_hang", "Mã hàng không hợp lệ.")
            return cleaned_data

        if ma_hang and mau:
            colors = self.config[ma_hang]["colors"]
            if mau not in colors:
                self.add_error("mau", f"Màu '{mau}' không thuộc mã hàng '{ma_hang}'.")
                return cleaned_data

            if co and co not in colors[mau]:
                self.add_error("co", f"Cỡ '{co}' không thuộc màu '{mau}' của mã hàng '{ma_hang}'.")

        return cleaned_data