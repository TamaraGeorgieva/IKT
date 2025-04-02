from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TEACHER = 'teacher'
    STUDENT = 'student'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
        (ADMIN, 'Administrator'),
    ]

    role = (models.CharField
    (
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT
    ))

    def is_teacher(self):
        return self.role == self.TEACHER

    def is_student(self):
        return self.role == self.STUDENT

    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser
