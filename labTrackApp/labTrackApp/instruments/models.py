from django.db import models

STATUS = [
    ('operational', 'Operational'),
    ('under_maintenance', 'Under Maintenance'),
    ('service', 'Validation'),
]
class Instrument(models.Model):
    brand = models.CharField(
        max_length=30,
        blank=True,
    )

    model = models.CharField(
        max_length=30,
    )

    serial_number = models.CharField(
        max_length=50,
        unique=True,
    )

    description = models.TextField(
        max_length = 150,
    )

    status = models.CharField(
        max_length=20,
        choices= STATUS,
        default='operational',
    )

    date_acquired = models.DateField(
        auto_now_add=True
        )


    def __str__(self):
        return self.model

class MaintenanceRecord(models.Model):

    instrument = models.ForeignKey(
        Instrument,
        on_delete=models.CASCADE,
        related_name='maintenance_history'
    )

    maintenance_date = models.DateField()

    description = models.TextField()

    cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        )
    
    performed_by = models.CharField(
        max_length=100, 
        verbose_name="Performed By (Internal/Vendor)",
        )
    
    # Optional field to track if it was routine calibration or repair
    record_type = models.CharField(
        max_length=10, 
        choices=[('CAL', 'Validation'), 
                 ('RPR', 'Repair'), 
                 ('SVC', 'Service'),
                 ]
    )

    def __str__(self):
        return f"Maintenance for {self.instrument.model} with {self.instrument.serial_number} on {self.maintenance_date}"

