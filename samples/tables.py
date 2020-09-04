import django_tables2 as tables
from .models import Sample


class SampleTable(tables.Table):
    # name = tables.LinkColumn('samples:detail', text='static text', args=[A('pk')])
    # sample_no = tables.Column(linkify=('samples:detail', {'pk': tables.A('pk')}))
    sample_no = tables.Column(linkify=True)
    # name = tables.Column(linkify=('samples:detail', {'name': tables.A('name'),'slug': tables.A('species')}))
    class Meta:
        model = Sample
        template_name = "django_tables2/bootstrap.html"
        fields = ("sample_no",
                  "job__job_no",
                  "job_name",
                  "latitude",
                  "longitude",
                  "depth",
                  "soil_type",
                  # "texture",
                  # "color",
                  "ph",
                  "redox_potential",
                  "conductivity",
                  # "chloride",
                  # "sulfate",
                  # "salinity",
                  "resistivity_as_collected",
                  "resistivity_saturated",
                  # "carbonate",
                  # "sulfide",
                  # "moisture_content",
                  # "comments",
                  "awwa",
                  "wssc",
                  )
