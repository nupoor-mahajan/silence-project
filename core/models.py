from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    population = models.IntegerField()
    current_complaints = models.IntegerField()
    historical_avg = models.IntegerField(help_text="Historical trend for early warning")
    
    # Computed fields logic handled in analytics pipeline
    
    def __str__(self):
        return self.name