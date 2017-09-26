from django.db import models

class Phrase(models.Model):
    text = models.CharField(max_length=200)
    file = models.CharField(max_length=200)
    page = models.IntegerField()
    class Meta:
        indexes = [models.Index(fields=['text']),
                   models.Index(fields=['file']),
                   models.Index(fields=['page'])]
        # unique_together = ('text', 'file', 'page')
    def __str__(self):
        return 'Phrase({}, {}, {})'.format(self.text, self.file, self.page)

