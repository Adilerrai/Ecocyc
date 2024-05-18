from rest_framework import serializers, viewsets
from .models import TrashType, Trash, Ramassage, UserProfile, Balance

class TrashTypeSerializer(serializers.ModelSerializer):
    trash_type = serializers.SlugRelatedField(slug_field='type', queryset=TrashType.objects.all())




class TrashSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(
        queryset=TrashType.objects.all(),
        slug_field='type'  # or whatever field you want to display
    )

    class Meta:
        model = Trash
        fields = '__all__'  # or list the fields you want to include in the serialization

class TrashViewSet(viewsets.ModelViewSet):
    queryset = Trash.objects.all()
    serializer_class = TrashSerializer

class RamassageSerializer(serializers.ModelSerializer):
    trash = TrashSerializer(many=True)

    class Meta:
        model = Ramassage
        fields = ['id', 'date', 'heure', 'lieu', 'description', 'image', 'trash']

    def create(self, validated_data):
        trash_data = validated_data.pop('trash')
        ramassage = Ramassage.objects.create(**validated_data)
        for trash in trash_data:
            trash_type = TrashType.objects.get(type=trash.pop('type'))
            Trash.objects.create(ramassage=ramassage, type=trash_type, **trash)
        return ramassage
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['trash'] = TrashSerializer(instance.trash.all(), many=True).data
        return representation

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'

class RamassageViewSet(viewsets.ModelViewSet):
    queryset = Ramassage.objects.all()
    serializer_class = RamassageSerializer

    def perform_create(self, serializer):
        serializer.save()
        weight = serializer.validated_data.get('poids')
        if weight is not None:
            money = serializer.instance.calculate_money(weight)
            # This method is called when a new Ramassage is created
            # You can add your logic here to calculate the money and update the balance
            weight = calculate_total_weight(serializer.validated_data['trash'])
            if weight is not None:
                money = serializer.instance.calculate_money(weight)
                balance = Balance.objects.get(user=self.request.user)
                balance.add_money(money)
                balance.save()


class TrashTypeViewSet(viewsets.ModelViewSet):
    queryset = TrashType.objects.all()
    serializer_class = TrashTypeSerializer


class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer

    def get_queryset(self):
        # This method is called when the Balance is requested
        # You can add your logic here to filter the Balance based on the user
        return self.queryset.filter(user=self.request.user)

def calculate_total_weight(trash_list):
    total_weight = 0
    for trash in trash_list:
        total_weight += trash.poids
    return total_weight