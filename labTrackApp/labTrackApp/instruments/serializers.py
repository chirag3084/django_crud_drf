from rest_framework import serializers
from .models import Instrument

# ModelSerializer automatically maps fields from the specified model

class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        # '__all__' includes every field; list can also be specified like:
        # fields = ('id', 'model', 'serial_number', 'brand', 'date_acquired')
        firlds = "__all__"
        read_only_fields = ('date_acquired',) 

        # A ModelSerializer automatically maps fields from the specified model

    class Meta:
        model = Instrument
        fields = '__all__'
        read_only_fields = ('date_acquired',) # protect fields that should not be updated via API

        

