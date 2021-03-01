from django import forms
from django.core.exceptions import ValidationError

from .models import BookRent, Book


class BookRentForm(forms.ModelForm):
    class Meta:
        model = BookRent
        fields = (
            "book",
            "renter",
            "amount",
            "term_rent",
            "deposit",
        )

    def clean(self):
        cd = self.cleaned_data
        query = Book.objects.filter(id=cd["book"].id).values("rental_cost", "amount")[0]
        amount = cd["amount"]
        if amount > query["amount"]:
            BookRentForm.add_error(
                self,
                field="amount",
                error=ValidationError(f'В наличии {query["amount"]} шт.'),
            )
        else:
            min_deposit = (amount * cd["term_rent"] * query["rental_cost"]) * 0.3
            if min_deposit > cd["deposit"]:
                BookRentForm.add_error(
                    self,
                    field="deposit",
                    error=ValidationError(
                        f"Сумма залога не может быть меньше чем 30% ({min_deposit}) от стоимости аренды."
                    ),
                )
