from rest_framework import serializers
from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class NetworkNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = "__all__"
        read_only_fields = ("debt", "created_at", "level")

    def validate(self, data):
        """
        Проверка корректности выбора поставщика.
        """
        supplier = data.get("supplier")
        
        if self.instance:
            if supplier and supplier.id == self.instance.id:
                raise serializers.ValidationError({"supplier": "Звено не может быть своим поставщиком."})

        if supplier:
            if supplier.level >= 2:
                raise serializers.ValidationError(
                    {"supplier": "Выбранный поставщик находится на низшем уровне иерархии и не может иметь подчиненных."}
                )

        return data