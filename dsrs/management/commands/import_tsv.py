import os
import gzip
import csv
import dateutil.parser

from django.core.management.base import BaseCommand

from dsrs import models


class Command(BaseCommand):
    help = "Parse tsv statistic files"

    def add_arguments(self, parser):
        parser.add_argument("data_dir", type=str, help="Tickets for add to drills")

    def handle(self, *args, **options):
        for tsv in os.listdir(options["data_dir"]):
            dates = tsv.split("_")[-1].replace(".tsv.gz", "")
            period_start = dateutil.parser.parse(dates.split("-")[0])
            period_end = dateutil.parser.parse(dates.split("-")[1])
            currency = models.Currency.objects.get(code=tsv.split("_")[-2])
            territory = models.Territory.objects.get(code_2=tsv.split("_")[-3])
            dsr = models.DSR.objects.create(
                path=tsv,
                period_start=period_start,
                period_end=period_end,
                territory=territory,
                currency=currency,
            )
            with gzip.open(os.path.join(options["data_dir"], tsv), "rt") as f:
                d = csv.reader(f, delimiter="\t")
                fields = {
                    i: j
                    for i, j in enumerate(d.__next__())
                }
                try:
                    last_resource = models.Resource.objects.latest("id")
                except:
                    last_resource = None
                resourses = []
                for line in d:
                    model_fields = {
                        fields[j]: v
                        for j, v in enumerate(line)
                    }
                    model_fields["usages"] = int(model_fields["usages"]) if model_fields["usages"] else 0
                    model_fields["revenue"] = float(model_fields["revenue"]) if model_fields["revenue"] else 0.0
                    resourses.append(
                        models.Resource(
                            **model_fields
                        )
                    )
                models.Resource.objects.bulk_create(resourses)
                resourse_dsrs = []
                resource_for_update = models.Resource.objects.filter(pk__gt=last_resource.id) if last_resource else models.Resource.objects.all()
                for r in resource_for_update:
                    resourse_dsrs.append(
                        models.Resource.dsrs.through(resource_id=r.id, dsr_id=dsr.id)
                    )
                models.Resource.dsrs.through.objects.bulk_create(resourse_dsrs)
