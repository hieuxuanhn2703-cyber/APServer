from django import forms
from .models import MaterialReceipt, MaterialIssue, UNIT_CHOICES
from Working.models import AppUser
from Working.forms import NUMERIC_FIELD_ATTRS, DATE_FIELD_ATTRS, load_config

class MaterialReceiptForm(forms.ModelForm):
    ma_hang = forms.ChoiceField(label="Mã hàng", choices=[])
    mau = forms.ChoiceField(label="Màu sắc", choices=[])
    don_vi = forms.ChoiceField(
        label="Đơn vị",
        choices=UNIT_CHOICES,
        initial="m",
        widget=forms.Select(attrs={'class': 'entry-select', 'id': 'id_don_vi'})
    )

    class Meta:
        model = MaterialReceipt
        fields = ['ngay_nhap', 'ma_hang', 'mau', 'ten_vat_tu', 'so_luong_kien', 'don_vi', 'so_luong']
        widgets = {
            'ngay_nhap': forms.DateInput(attrs=DATE_FIELD_ATTRS),
            'ten_vat_tu': forms.TextInput(attrs={'class': 'entry-input', 'placeholder': 'Nhập tên vật tư'}),
            'so_luong_kien': forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS),
            'so_luong': forms.NumberInput(attrs={'class': 'entry-input numeric-input text-center', 'min': '0', 'step': '0.01', 'id': 'id_so_luong'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = load_config()

        self.fields["ma_hang"].choices = [("", "-- Chọn mã hàng --")] + [
            (ma, ma) for ma in self.config.keys()
        ]

        all_colors = set()
        for data in self.config.values():
            for color in data.get("colors", {}).keys():
                all_colors.add(color)

        self.fields["mau"].choices = [("", "-- Chọn màu --")] + [(c, c) for c in sorted(all_colors)]

    def clean(self):
        cleaned_data = super().clean()
        ma_hang = cleaned_data.get("ma_hang")
        mau = cleaned_data.get("mau")
        don_vi = cleaned_data.get("don_vi")
        so_luong = cleaned_data.get("so_luong")

        if ma_hang and ma_hang not in self.config:
            self.add_error("ma_hang", "Mã hàng không hợp lệ.")
            return cleaned_data

        if ma_hang and mau:
            colors = self.config.get(ma_hang, {}).get("colors", {})
            if mau not in colors:
                self.add_error("mau", f"Màu '{mau}' không thuộc mã hàng '{ma_hang}'.")
                return cleaned_data

        if don_vi == "chiếc":
            if so_luong is not None and (so_luong <= 0 or not float(so_luong).is_integer()):
                self.add_error("so_luong", "Khi đơn vị là 'chiếc', số lượng phải là số nguyên dương.")

        return cleaned_data


class MaterialIssueForm(forms.ModelForm):
    ma_hang = forms.ChoiceField(label="Mã hàng", choices=[])
    mau = forms.ChoiceField(label="Màu sắc", choices=[])
    don_vi = forms.ChoiceField(
        label="Đơn vị",
        choices=UNIT_CHOICES,
        initial="m",
        widget=forms.Select(attrs={'class': 'entry-select', 'id': 'id_don_vi'})
    )

    class Meta:
        model = MaterialIssue
        fields = ['ngay_xuat', 'ma_hang', 'mau', 'ten_vat_tu', 'so_luong_kien', 'don_vi', 'so_luong', 'nguoi_nhan']
        widgets = {
            'ngay_xuat': forms.DateInput(attrs=DATE_FIELD_ATTRS),
            'ten_vat_tu': forms.TextInput(attrs={'class': 'entry-input', 'placeholder': 'Nhập tên vật tư'}),
            'so_luong_kien': forms.NumberInput(attrs=NUMERIC_FIELD_ATTRS),
            'so_luong': forms.NumberInput(attrs={'class': 'entry-input numeric-input text-center', 'min': '0', 'step': '0.01', 'id': 'id_so_luong'}),
            'nguoi_nhan': forms.TextInput(attrs={'class': 'entry-input', 'placeholder': 'Ví dụ: Tổ Cắt, Anh Nam, Chị Hoa...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = load_config()

        self.fields["ma_hang"].choices = [("", "-- Chọn mã hàng --")] + [
            (ma, ma) for ma in self.config.keys()
        ]

        all_colors = set()
        for data in self.config.values():
            for color in data.get("colors", {}).keys():
                all_colors.add(color)

        self.fields["mau"].choices = [("", "-- Chọn màu --")] + [(c, c) for c in sorted(all_colors)]

    def clean(self):
        cleaned_data = super().clean()
        ma_hang = cleaned_data.get("ma_hang")
        mau = cleaned_data.get("mau")
        don_vi = cleaned_data.get("don_vi")
        so_luong = cleaned_data.get("so_luong")

        if ma_hang and ma_hang not in self.config:
            self.add_error("ma_hang", "Mã hàng không hợp lệ.")
            return cleaned_data

        if ma_hang and mau:
            colors = self.config.get(ma_hang, {}).get("colors", {})
            if mau not in colors:
                self.add_error("mau", f"Màu '{mau}' không thuộc mã hàng '{ma_hang}'.")
                return cleaned_data

        if don_vi == "chiếc":
            if so_luong is not None and (so_luong <= 0 or not float(so_luong).is_integer()):
                self.add_error("so_luong", "Khi đơn vị là 'chiếc', số lượng phải là số nguyên dương.")

        return cleaned_data
