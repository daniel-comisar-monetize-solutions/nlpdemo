from django.db import models

class Cause(models.Model):
    text = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return '{}'.format(self.text)

class DTC(models.Model):
    bmw_code = models.CharField(max_length=20)
    causes = models.ManyToManyField(Cause)
    code = models.CharField(max_length=20, primary_key=True)
    fault = models.CharField(max_length=200)
    fixes = models.ManyToManyField('Fix')
    name = models.CharField(max_length=200)
    def __str__(self):
        return '{}'.format(self.code)

class Fix(models.Model):
    text = models.CharField(max_length=400, unique=True)
    def __str__(self):
        return '{}'.format(self.text)

class Part(models.Model):
    image = models.CharField(max_length=20)
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return '{}'.format(self.name)

class PartLabel(models.Model):
    label = models.CharField(max_length=20)
    part = models.ForeignKey(Part)
    text = models.CharField(max_length=200)
    class Meta:
        unique_together = ('label', 'part', 'text')
    def __str__(self):
        return '{}'.format(self.text)

class Phrase(models.Model):
    count = models.IntegerField(db_index=True)
    sentences = models.ManyToManyField('Sentence', related_name='phrases')
    text = models.CharField(max_length=200, unique=True, db_index=True)
    def __str__(self):
        return '{}'.format(self.text)

class ReferenceFix(models.Model):
    code = models.CharField(max_length=40, primary_key=True)
    text = models.CharField(max_length=400)
    def __str__(self):
        return '{}'.format(self.text)

class Sentence(models.Model):
    filename = models.CharField(max_length=200, db_index=True)
    page = models.IntegerField(db_index=True)
    text = models.CharField(max_length=2000, db_index=True)
    class Meta:
        unique_together = (("filename", "page", "text"),)
    def __str__(self):
        return '{}'.format(self.text)
