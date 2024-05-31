from django.db import models

# Create your models here.

class DomainLookup(models.Model):
    domain_id = models.BigAutoField(primary_key=True)
    domain_value = models.CharField(max_length=150, blank=False, null=False)
    domain_code = models.IntegerField(blank=False, null=False)
    domain_type = models.CharField(max_length=150, blank=False, null=False)
    domain_text = models.CharField(max_length=150, blank=True, null=True)
    domain_data_type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'domain_lookup'
