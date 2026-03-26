from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin
from labTrackApp.instruments.forms import InstrumentAddForm, InstrumentDeleteForm, InstrumentEditForm, MaintenanceRecordForm
from labTrackApp.mixins import AdminRequiredMixin
from .models import Instrument
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Q

# for django rest framework
from rest_framework import viewsets
from .models import Instrument
from .serializers import InstrumentSerializer

# for djangofilter
from rest_framework import viewsets
from django_filters.rest_framework import FilterSet

class InstrumentAddView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Instrument
    form_class = InstrumentAddForm
    template_name = 'instruments/instrument-create.html'

    def form_valid(self, form):
        form.instance.recorded_by = self.request.user 
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('instruments-page', kwargs={'pk': self.object.pk})
    
    


class InstrumentListView(ListView):
    model = Instrument
    template_name = 'instruments/instruments-list.html'
    context_object_name = 'instruments'
    paginate_by = 6

    def get_queryset(self):
        # Base QuerySet: Start with the default model manager's queryset
        queryset = super().get_queryset()

        # Annotation: Calculate the total maintenance cost for each instrument
        # We use Sum to aggregate the 'cost' field from the related MaintenanceRecord model
        # The annotated field 'total_maintenance_cost' is now available on every Instrument object.
        qs = queryset.annotate(
            total_maintenance_cost=Sum('maintenance_history__cost')
        )
        

        # Filtering Logic (Filtering by 'status' via URL parameter)
        status_filter = self.request.GET.get('status')
        if status_filter:
            # Filters the queryset to only instruments matching the requested status
            queryset = queryset.filter(status=status_filter)

        # Search Logic (Complex OR lookup using Q objects)
        search_query = self.request.GET.get('q')
        if search_query:
            # Q objects allow building complex lookups like 'field A OR field B'
            qs = queryset.filter(
                Q(name__icontains=search_query) | # Case-insensitive partial match on instrument name
                Q(serial_number__icontains=search_query) # Case-insensitive partial match on serial number
            )
            
        # Final Ordering 
        # Order by the calculated annotated field (cost descending), then by name
        # Note: We can order by the annotated field 'total_maintenance_cost'
        return qs.order_by('-total_maintenance_cost', 'model')

    def get_context_data(self, **kwargs):
        # Passes extra data needed for the template's filter form
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', '') # Current selected status
        context['search_query'] = self.request.GET.get('q', '')     # Current search term
        context['status_choices'] = Instrument.status     # Pass choices for the filter dropdown
        return context

class InstrumentDetailView(LoginRequiredMixin, DetailView):
    model = Instrument
    template_name = 'instruments/instrument-details.html'
    context_object_name = 'instrument'


class InstrumentEditView():
    model = Instrument
    form_class = InstrumentEditForm
    template_name = ""
    context_object_name = ''

class InstrumentDeleteView():
    model = Instrument
    form_class = InstrumentDeleteForm
    template_name = ""
    context_object_name = ''


class InstrumentMaintenanceView(LoginRequiredMixin, FormMixin, DetailView):
    model = Instrument
    form_class = MaintenanceRecordForm
    template_name = 'instruments/instrument-maintenance.html'
    context_object_name = "instrument" 


    def get_success_url(self):
        return reverse('instrument-maintenance', kwargs={'pk': str(self.object.pk)})
    
    
    def form_valid(self, form):
        maintenance_record = form.save(commit=False)
        maintenance_record.instrument = self.object
        maintenance_record.recorded_by = self.request.user
        maintenance_record.save()
        return redirect(self.get_success_url())


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['maintenance_records'] = self.object.maintenance_history.all().order_by('-maintenance_date')
        return context



class InstrumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Instruments to be viewed or edited.
    Provides default CRUD operations (list, retrieve, create, update, destroy).
    """
    # queryset: define the data to be used
    queryset = Instrument.objects.all().order_by('model')

    # serializer: Define how to format the data
    serializer_class = InstrumentSerializer