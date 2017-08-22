from __future__ import unicode_literals

from django.db import models

# Create your models here.

# Define scripts upload path
def upload_to_path(instance, filename):
    #upload_to = r'script4apps/%s/%s/%s' % (instance.author.username, instance.name, filename)
    upload_to = r'script4apps/%s/%s' % (instance.name, filename)
    #upload_to = r'script4apps/%s/%s' % (instance.author.username, filename)
    return upload_to


class cdap_model(models.Model):
    author = models.ForeignKey(User)
    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=64, null=True)
    owner = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    pub_date = models.DateTimeField('date published', null=True, auto_now=True)
    modelpath = models.FileField(upload_to=upload_to_path, null=True)
    modelcmd = models.TextField(null=True)
    hasoutput = models.BooleanField(default=True)

    type_class = (
        ('python', 'Python'),
        ('r', 'R'),
        ('knime', 'Knime'),
        ('spotfire', 'Spotfire'),
        ('excel', 'Excel'),
    )
    type = models.CharField(max_length=32, choices=type_class)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1

        while cdap_model.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(cdap_model, self).save()


class SeparatedValueField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(SeparatedValueField, self).__init__(*args, **kwargs)
    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([unicode(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class cdap_access(models.Model):
    model = models.ForeignKey(cdap_model, on_delete=models.CASCADE)
    modelname = models.CharField(max_length=255, blank=True)
    ShareUser = SeparatedValueField()
