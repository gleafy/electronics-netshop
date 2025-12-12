from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    model = models.CharField(max_length=255, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    class NodeType(models.IntegerChoices):
        FACTORY = 0, "Завод"
        RETAIL = 1, "Розничная сеть"
        ENTREPRENEUR = 2, "Индивидуальный предприниматель"

    name = models.CharField(max_length=100, verbose_name="Название")
    
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=20, verbose_name="Номер дома")

    products = models.ManyToManyField(Product, verbose_name="Продукты", blank=True)

    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Поставщик",
        related_name="supplied_nodes",
    )

    node_type = models.IntegerField(
        choices=NodeType.choices, 
        default=NodeType.FACTORY, 
        verbose_name="Тип звена"
    )

    level = models.IntegerField(
        default=0, verbose_name="Уровень иерархии", editable=False
    )

    debt = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Задолженность"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_node_type_display()})"

    def save(self, *args, **kwargs):
        if not self.supplier:
            self.level = 0
        else:
            self.level = self.supplier.level + 1
        
        super().save(*args, **kwargs)