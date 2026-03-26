import pytest
from labTrackApp.instruments.models import Instrument


@pytest.mark.django_db
def test_instrument_creation_simple():

    # arrange
    instrument = Instrument.objects.create(
        brand='Agilent',
        model='GC-MS 8000',
        serial_number='SN-LAB-12345',
        description='Gas Chromatograph Mass Spectrometer.',
    )

    assert instrument.pk is not None
    assert instrument.model == 'GC-MS 8000'

    assert str(instrument) == 'GC-MS 8000'