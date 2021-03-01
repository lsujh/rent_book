from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Book(models.Model):
    title = models.CharField("Название", max_length=100, db_index=True)
    amount = models.SmallIntegerField("Количество")
    rental_cost = models.FloatField("Стоимость оренды за один день")

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title


class BookRent(models.Model):
    book = models.ForeignKey(
        Book,
        verbose_name="Название книги",
        related_name="book_rent",
        on_delete=models.CASCADE,
    )
    renter = models.CharField("Арендатор", max_length=150)
    amount = models.SmallIntegerField("Количество")
    term_rent = models.SmallIntegerField("Срок аренды")
    start_renting = models.DateTimeField("Начало аренды", auto_now_add=True)
    deposit = models.FloatField("Сумма залога")

    class Meta:
        ordering = ("-start_renting",)

    def __str__(self):
        return f"{self.renter}/{self.book.title}"


@receiver(post_save, sender=BookRent)
def update_amount(sender, instance, created, **kwargs):
    if created:
        Book.objects.filter(id=instance.book.id).update(
            amount=models.F("amount") - instance.amount
        )
