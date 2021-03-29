from django.forms import ModelForm
from .models import ShippingAddress, FaceShape, Prescription

class ShippingForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ['user']


class ShippingUpdateForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        exclude = ['user']

class FaceShapeForm(ModelForm):
	class Meta: 
		model = FaceShape
		fields = ['name', 'image'] 


class PrescriptionAddForm(ModelForm):
    class Meta:
        model = Prescription
        fields = ('name', 'prescription', 'prescriptionImage', )