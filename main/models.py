from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# =============================
# Room Model
# =============================
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


from django.db import models

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('deluxe', 'Deluxe Room'),
    ]

    number = models.IntegerField(unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_booked = models.BooleanField(default=False)
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)  # ✅ Ensure this is in your model

    def _str_(self):
        return f"Room {self.number} ({self.get_room_type_display()})"

class Booking(models.Model):
    PAYMENT_METHODS = [
        ('mpesa', 'M-Pesa'),
        ('bank', 'Bank Transfer'),
        ('cash', 'Cash'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField('placeholder@example.com', default='Anonymous User')
    check_in = models.DateField()
    check_out = models.DateField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='mpesa')
    payment_number = models.CharField(max_length=20, help_text="Enter M-Pesa or Bank transaction number")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    booked_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.full_name} - Room {self.room.number} ({self.status})"

# =============================
# User Profile
# =============================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    joined = models.DateTimeField(auto_now_add=True)

    def _str_(self):  # ✅ fix typo
        return self.user.username

# =============================
# Payment Model
# =============================
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Booking

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('mpesa', 'M-Pesa'),
        ('bank', 'Bank Transfer'),
        ('cash', 'Cash'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default='mpesa')
    transaction_id = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"{self.booking.user.username} | {self.transaction_id} | {self.status}"

# =============================
# Entertainment Model
# =============================
class Entertainment(models.Model):
    CATEGORY_CHOICES = [
        ('movie', 'Movie'),
        ('music', 'Music'),
        ('event', 'Event'),
        ('announcement', 'Announcement'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']
        verbose_name = "Entertainment"
        verbose_name_plural = "Entertainment"

    def __str__(self):
        return f"{self.title} ({self.category})"

# =============================
# Resource Model
# =============================
class Resource(models.Model):
    title = models.CharField(max_length=200, help_text="Title of the resource (e.g., Hostel Rules, Exam Timetable)")
    description = models.TextField(blank=True, help_text="Brief description of the resource")
    file = models.FileField(upload_to='resources/', help_text="Upload the resource file here (PDF, DOCX, etc.)")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_resources')

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Hostel Resource"
        verbose_name_plural = "Hostel Resources"

    def _str_(self):
        return self.title

# =============================
# ChatRoom and ChatMessage
# =============================
class ChatRoom(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the chatroom (e.g., General, Admins, Tenants)")
    is_group = models.BooleanField(default=True, help_text="Whether this is a group chat")
    members = models.ManyToManyField(User, related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(blank=True, help_text="Text content of the message")
    media = models.FileField(upload_to='chat_media/', blank=True, null=True, help_text="Optional media or image file")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def _str_(self):
        return f"{self.sender.username} in {self.room.name}: {self.content[:30]}"
    