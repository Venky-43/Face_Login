# face_app/views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import RegisterForm
from .models import UserProfile
import cv2
import face_recognition
import os
import time
from django.conf import settings
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            user.save()

            messages.success(request, 'Registered successfully!')
            return redirect('success')  
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


import os
import time
import cv2
import face_recognition
from django.conf import settings
from django.shortcuts import render
from .models import UserProfile

def login_view(request):
    import numpy as np

    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  
    time.sleep(1)

    known_encodings = []
    known_users = []

    for user in UserProfile.objects.all():
        if not user.face_image:
            print(f"Warning: No face image set for user {user.username}")
            continue

        image_path = os.path.normpath(os.path.join(settings.MEDIA_ROOT, str(user.face_image)))
        print(f"Trying to load image: {image_path}")

        if not os.path.exists(image_path):
            print(f"Warning: Image file does not exist: {image_path}")
            continue

        try:
            bgr_image = cv2.imread(image_path)

            if bgr_image is None or bgr_image.ndim != 3 or bgr_image.shape[2] != 3:
                print(f"Warning: Invalid image format for {user.username}")
                continue

            rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_image)

            if encodings:
                known_encodings.append(encodings[0])
                known_users.append(user)
            else:
                print(f"Warning: No face found in image for user {user.username}")
        except Exception as e:
            print(f"Error processing image for {user.username}: {e}")
            continue

    authenticated_user = None

    while True:
        ret, frame = video.read()
        if not ret or frame is None:
            print("Warning: Could not read frame from camera.")
            break

        try:
            
            if frame.dtype != np.uint8 or frame.ndim != 3 or frame.shape[2] != 3:
                print(f"Skipping invalid frame: dtype={frame.dtype}, shape={frame.shape}")
                continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            
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

        except Exception as e:
            print(f"Error during frame processing: {e}")
            continue

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
def success(request):
    return render(request,'success.html')
