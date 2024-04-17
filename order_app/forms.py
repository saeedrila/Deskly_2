from django import forms
from django.shortcuts import redirect
from django.contrib import messages

PAYMENT_CHOICES = (
    ("cod", "Cash On Delivery"),
    ("razorpay", "Razorpay"),
    ("bank_transfer", "Direct Bank Transfer"),
    ("paytm", "PayTm"),
    ("paypal", "Paypal"),
)


class PaymentForm(forms.Form):
    payment_option = forms.ChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect
    )

    def clean(self):
        cleaned_data = super().clean()
        payment_option = cleaned_data.get("payment_option")

        if payment_option not in ["cod", "razorpay"]:
            raise forms.ValidationError("Payment option not available.")

        return cleaned_data
