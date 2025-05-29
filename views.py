# face_app/views.py
from django.shortcuts import render, redirect
from .forms import RegisterForm
from .models import UserProfile
import cv2
import face_recognition
import os
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    # Use webcam to get frame
    video = cv2.VideoCapture(0)
    known_encodings = []
    known_users = []

    for user in UserProfile.objects.all():
        image_path = os.path.join(settings.MEDIA_ROOT, str(user.face_image))
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        known_encodings.append(encoding)
        known_users.append(user)

    authenticated_user = None
    while True:
        ret, frame = video.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            if True in matches:
                matched_index = matches.index(True)
                authenticated_user = known_users[matched_index]
                break
        if authenticated_user:
            break

        cv2.imshow("Login - Press Q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

    if authenticated_user:
        return render(request, 'home.html', {'user': authenticated_user})
    else:
        return render(request, 'login.html', {'error': 'Face not recognized. Try again.'})

def home(request):
    return render(request, 'home.html')
def landing(request):
    return render(request, 'landing.html')
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            user.generate_verification_code()
            user.save()

            send_mail(
                'Verify your Email',
                f'Your verification code is {user.verification_code}',
                'your_email@example.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('verify_email', user_id=user.id)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
def verify_email(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)

    if request.method == 'POST':
        code_entered = request.POST.get('verification_code')
        if code_entered == user.verification_code:
            user.is_verified = True
            user.save()
            return redirect('login')
        else:
            return render(request, 'verify_email.html', {'error': 'Invalid verification code', 'user_id': user_id})

    return render(request, 'verify_email.html', {'user_id': user_id})

