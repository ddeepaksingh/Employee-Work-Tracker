"""
Employees app models: Department, Designation, EmployeeProfile.
"""
import logging
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

logger = logging.getLogger(__name__)
User = get_user_model()


class Department(models.Model):
    """Organisational department."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('employees:department_detail', kwargs={'pk': self.pk})

    @property
    def employee_count(self) -> int:
        return self.employee_profiles.filter(is_active=True).count()


class Designation(models.Model):
    """Job designation within a department."""

    name = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='designations',
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = [('name', 'department')]
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'

    def __str__(self) -> str:
        return f"{self.name} ({self.department.name})"


class EmployeeProfile(models.Model):
    """Extended profile linked one-to-one with Django's User model."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employee_profile',
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employee_profiles',
    )
    designation = models.ForeignKey(
        Designation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employee_profiles',
    )
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        verbose_name = 'Employee Profile'
        verbose_name_plural = 'Employee Profiles'

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return self.user.get_full_name() or self.user.username

    @property
    def email(self) -> str:
        return self.user.email

    def get_absolute_url(self) -> str:
        return reverse('employees:employee_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs) -> None:
        if not self.employee_id:
            last = EmployeeProfile.objects.order_by('-id').first()
            next_num = (last.id + 1) if last else 1
            self.employee_id = f"EMP{next_num:04d}"
        super().save(*args, **kwargs)
