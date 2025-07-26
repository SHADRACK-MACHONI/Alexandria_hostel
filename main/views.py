from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from .models import Room, ChatMessage
from .forms import BookingForm
from django.contrib import messages

def home(request):
    return render(request, 'main/home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login') # or 'home'

def chat_view(request):
    if request.method == 'POST':
        ChatMessage.objects.create(sender=request.user.username, content=request.POST['message'])
    messages = ChatMessage.objects.all().order_by('-timestamp')[:50]
    return render(request, 'chat.html', {'messages': messages})

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})

# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import date
from .models import Room, Booking

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if room.is_booked:
        messages.error(request, f"Room {room.number} is already booked. Please choose another room.")
        return redirect('rooms')  # Redirect back to the room listing

    # Optional: Prevent double bookings by same user
    existing_booking = Booking.objects.filter(user=request.user, room=room).first()
    if existing_booking:
        messages.warning(request, "You have already booked this room.")
        return redirect('rooms')

    # Create booking
    Booking.objects.create(
        user=request.user,
        room=room,
        check_in=date.today(),
        check_out=date.today(),  # Placeholder: ideally use form input
        payment_method='mpesa',  # Placeholder: use form input
    )

    room.is_booked = True
    room.save()

    messages.success(request, f"You have successfully booked Room {room.number}.")
    return redirect('rooms')


def rooms_view(request):
    rooms = Room.objects.all()
    return render(request, 'main/rooms.html', {'rooms': rooms})
# main/views.py
from django.shortcuts import render
from .models import Booking, Room, Payment  # Assuming you have these models
from django.contrib.auth.decorators import login_required

@login_required
def payments_view(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    payments = Payment.objects.filter(booking__in=bookings)

    context = {
        'payments': payments,
        'bookings': bookings,
    }
    return render(request, 'payments.html', context)
# main/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Booking, Payment, ChatMessage, Entertainment, Resource

@login_required
def dashboard(request):
    rooms = Room.objects.all()
    bookings = Booking.objects.all()
    payments = Payment.objects.all()
    chats = ChatMessage.objects.all()
    resources = Resource.objects.all()
    entertainment = Entertainment.objects.all()

    context = {
        'rooms': rooms,
        'bookings': bookings,
        'payments': payments,
        'chats': chats,
        'resources': resources,
        'entertainment': entertainment,
    }
    return render(request, 'main/dashboard.html', context)
from django.shortcuts import render
from .models import Resource
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def resource_list(request):
    resources = Resource.objects.all()
    return render(request, 'main/resources.html', {'resources': resources})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatMessage

from django.shortcuts import render, redirect, get_object_or_404
from .models import ChatMessage, ChatRoom
from django.contrib.auth.decorators import login_required

@login_required
def chat_view(request):
    # For simplicity, assume you have one room or pass room_id in GET or URL
    room = ChatRoom.objects.first()  # or use get_object_or_404(ChatRoom, id=some_id)

    if request.method == 'POST':
        content = request.POST.get('message')
        media = request.FILES.get('media')  # If handling file uploads

        if content or media:
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                content=content or '',
                media=media
            )
            return redirect('chat')  # or redirect back to the same room

    messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
    return render(request, 'main/chat.html', {'messages': messages, 'room': room})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Payment, Booking

@login_required
def payments_view(request):
    user = request.user

    # Filter payments by user through booking
    payments = Payment.objects.filter(booking__user=user).order_by('-timestamp')

    # Get all bookings by this user
    bookings = Booking.objects.filter(user=user)

    context = {
        'payments': payments,
        'bookings': bookings,
        'total_paid': sum(p.amount for p in payments if p.status == 'completed'),
        'total_pending': sum(p.amount for p in payments if p.status != 'completed'),
    }

    return render(request, 'payments.html', context)
from django.shortcuts import render

@login_required
def entertainment_view(request):
    entertainment_items = [
        {"title": "Movie Night", "type": "Movie", "date": "2025-07-28", "description": "Watch the latest movie in the lounge"},
        {"title": "Game Tournament", "type": "Gaming", "date": "2025-07-30", "description": "Compete in FIFA, Mortal Kombat, and more"},
        {"title": "Karaoke Night", "type": "Music", "date": "2025-08-01", "description": "Sing your heart out with friends"},
    ]
    return render(request, 'entertainment.html', {"entertainment_items": entertainment_items})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking
from django.contrib.auth.decorators import login_required

@login_required
def book_room_view(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.method == "POST":
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        user = request.user

        Booking.objects.create(
            user=user,
            room=room,
            check_in=check_in,
            check_out=check_out,
            email=user.email  # Optional if required in your model
        )
        return redirect('booking_success')  # Make sure this route exists

    return render(request, 'book_room.html', {'room': room})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Room, Booking
from .forms import BookingForm

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if room.is_booked:
        messages.error(request, "Sorry, this room is already booked.")
        return redirect('rooms')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.status = 'confirmed'
            booking.save()
            room.is_booked = True
            room.save()
            return redirect('booking_success')
    else:
        form = BookingForm()

    return render(request, 'main/book_room.html', {'room': room, 'form': form})

def booking_success(request):
    return render(request, 'main/booking_success.html')

