from django.db import models
from django.conf import settings

# Create your models here.

class Submission(models.Model):
    assignment = models.ForeignKey("assignments.Assignment", on_delete = models.CASCADE, related_name = "submissions")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    
    date_submitted = models.DateTimeField(auto_now_add = True)

    has_been_graded = models.BooleanField(default = False)

    points_received = models.DecimalField(max_digits = 4, decimal_places = 1, null=True, blank=True)

    filename = models.FilePathField(settings.MEDIA_ROOT, recursive=True, null=True)

    @property
    def is_on_time(self):
        return self.date_submitted <= self.assignment.due

    @property
    def points_possible(self):
        return self.assignment.points_possible

    @property
    def grade_percent(self):
        if self.points_received is None:
            return None
        return "{}%".format(self.points_received / self.points_possible * 100)

