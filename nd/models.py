from django.db import models

class Cause(models.Model):
    text = models.CharField(max_length=200, primary_key=True)
    def __str__(self):
        return '{}'.format(self.text)

class DTC(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    causes = models.ManyToManyField(Cause)
    def __str__(self):
        return '{}'.format(self.code)

class Phrase(models.Model):
    text = models.CharField(max_length=200)
    file = models.CharField(max_length=200)
    page = models.IntegerField()
    class Meta:
        indexes = [models.Index(fields=['text']),
                   models.Index(fields=['file']),
                   models.Index(fields=['page'])]
    def __str__(self):
        return 'Phrase({}, {}, {})'.format(self.text, self.file, self.page)
