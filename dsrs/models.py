from django.db import models


class Territory(models.Model):
    name = models.CharField(max_length=48)
    code_2 = models.CharField(max_length=2)
    code_3 = models.CharField(max_length=3)
    local_currency = models.ForeignKey(
        "Currency", related_name="territories", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "territory"
        verbose_name = "territory"
        verbose_name_plural = "territories"
        ordering = ("name",)


class Currency(models.Model):
    name = models.CharField(max_length=48)
    symbol = models.CharField(max_length=4)
    code = models.CharField(max_length=3)

    class Meta:
        db_table = "currency"
        verbose_name = "currency"
        verbose_name_plural = "currencies"


class DSR(models.Model):
    class Meta:
        db_table = "dsr"

    STATUS_ALL = (
        ("failed", "FAILED"),
        ("ingested", "INGESTED"),
    )

    path = models.CharField(max_length=256)
    period_start = models.DateField(null=False)
    period_end = models.DateField(null=False)

    status = models.CharField(
        choices=STATUS_ALL, default=STATUS_ALL[0][0], max_length=48
    )

    territory = models.ForeignKey(
        Territory, related_name="dsrs", on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        Currency, related_name="dsrs", on_delete=models.CASCADE
    )


class Resource(models.Model):
    class Meta:
        db_table = "resource"

    dsp_id = models.CharField(max_length=32)
    title = models.CharField(max_length=64)
    artists = models.CharField(max_length=64)
    isrc = models.CharField(max_length=16)
    usages = models.IntegerField()
    revenue = models.FloatField()
    dsrs = models.ManyToManyField("DSR", related_name="resources")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def dsr_list(self):
        return self.dsrs

    @dsr_list.setter
    def dsr_list(self, dsrs):
        self.dsrs.set(dsrs)
