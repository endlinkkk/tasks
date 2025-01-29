from django.db import models


class Author(models.Model):
    firts_name = models.CharField(max_length=255, verbose_name="firts_name")
    last_name = models.CharField(max_length=255, verbose_name="last_name")

    def __str__(self):
        return f"{self.firts_name} | {self.last_name}"

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="title")
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books", verbose_name="author"
    )
    count = models.PositiveIntegerField(verbose_name="count books")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
