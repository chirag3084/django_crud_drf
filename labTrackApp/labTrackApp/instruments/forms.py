from django import forms
from .models import Instrument
from django import forms
from .models import Instrument, MaintenanceRecord

class InstrumentBaseForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = ['brand', 'model', 'serial_number', 'description', "status"]


class InstrumentAddForm(InstrumentBaseForm):
    pass

class InstrumentEditForm(InstrumentBaseForm):
    class Meta(InstrumentBaseForm.Meta):
        field = ["status", 'maintenance_date', "cost", "performed_by", "record_type"]

class InstrumentDeleteForm(InstrumentBaseForm):
    pass


class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ['maintenance_date', 'record_type', 'description', 'cost', 'performed_by']
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
        }
