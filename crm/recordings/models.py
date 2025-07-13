from django.db import models

class Recording(models.Model):
    title = models.CharField(max_length=200, blank=True)
    youtube_url = models.URLField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.youtube_url
    
    class Meta:
        verbose_name = "Recordings"
        verbose_name_plural = "Recordings"
        ordering = ['created_at']