from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .utils import make_room_name
from .models import Message

User = get_user_model()

@login_required
def chat_view(request, room_name):
    room_members_id = room_name.split('_')

    members_list = []

    for member_id in room_members_id:
        try:
            user = User.objects.get(id=int(member_id))

            if not user.id == request.user.id:
                members_list.append(user.username)            

        except User.DoesNotExist:
            return redirect('dashboard')
    
    members_name = " & ".join(members_list)

    messages = Message.objects.filter(room_name=room_name).order_by("timestamp")
        
    return render(request, 'chat.html', {
        'room_name': room_name,
        'room_member': members_name,
        'messages': messages,
    })


@login_required
def dashboard_view(request):
    current_user = request.user
    users = User.objects.exclude(id=request.user.id)

    user_rooms = [
        {
            "username": user.username,
            "room_name": make_room_name(current_user.id, user.id),
            # "room_member": f"{current_user.username} {user.username}"
        }
        for user in users
    ]

    return render(request, "dashboard.html", {
        "user_rooms": user_rooms
    })



def landing_page_view(request):
    return render(request, 'landing.html')