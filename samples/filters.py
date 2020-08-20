import django_filters

from samples.models import Sample


class SampleFilter(django_filters.FilterSet):
    # lat = django_filters.NumberFilter()
    lat__lt = django_filters.NumberFilter(field_name='latitude', lookup_expr='lt')
    lat__gt = django_filters.NumberFilter(field_name='latitude', lookup_expr='gt')
    lon__lt = django_filters.NumberFilter(field_name='longitude', lookup_expr='lt')
    lon__gt = django_filters.NumberFilter(field_name='longitude', lookup_expr='gt')

    sample_no = django_filters.CharFilter(field_name="sample_no", lookup_expr='icontains')
    job_name = django_filters.AllValuesFilter(field_name="job_name")

    # Use the "filtering the queryset" method here https://django-filter.readthedocs.io/en/stable/guide/usage.html

    class Meta:
        model = Sample
        exclude = ["point"]
        fields = ["sample_no", "job__job_no", "job_name", "depth"]
