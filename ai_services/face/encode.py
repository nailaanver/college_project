def encode_face(image_file):
    try:
        import face_recognition
    except ImportError:
        raise ValueError(
            "Face recognition library not installed. "
            "Contact admin."
        )

    image = face_recognition.load_image_file(image_file)
    encodings = face_recognition.face_encodings(image)

    if not encodings:
        raise ValueError("No face detected. Upload a clear image.")

    return encodings[0].tobytes()
