import cv2
from f3DDFA_V2.FaceBoxes.FaceBoxes_ONNX import FaceBoxes_ONNX
from deepface import DeepFace


def apply_blur(
    input_video_path="fb_data/inputs/input_video.mp4",
    ref_face_img_path="fb_data/inputs/ref_face_img.jpg",
    output_path="fb_data/outputs/result.avi",
):
    ref_img_face = cv2.imread(ref_face_img_path)
    face_boxes = FaceBoxes_ONNX()
    vid_capture = cv2.VideoCapture(input_video_path)

    if not vid_capture.isOpened():
        print("Error opening the video file")
    else:
        # Obtain frame size information using get() method
        frame_width = int(vid_capture.get(3))
        frame_height = int(vid_capture.get(4))
        frame_size = (frame_width, frame_height)
        print("Frame size: ", frame_size)

        # Get frame rate information
        # You can replace 5 with CAP_PROP_FPS as well, they are enumerations
        fps = vid_capture.get(5)
        print("Frames per second : ", fps, "FPS")

        # Get frame count
        # You can replace 7 with CAP_PROP_FRAME_COUNT as well, they are enumerations
        frame_count = vid_capture.get(7)
        print("Frame count : ", frame_count)

    # Initialize video writer object
    output = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc("M", "J", "P", "G"),
        fps,  # 45
        (frame_width, frame_height),
    )

    frame_no = 0
    while vid_capture.isOpened():
        ret, frame = vid_capture.read()
        frame_no = frame_no + 1
        print(f"processing frame number: {frame_no}")
        if ret:
            faces = face_boxes(frame)
            if len(faces):
                for face in faces:
                    x1, y1, x2, y2, _ = face
                    roi = frame[int(y1) : int(y2), int(x1) : int(x2)]

                    obj = DeepFace.verify(
                        roi,
                        ref_img_face,
                        model_name="Facenet",
                        distance_metric="euclidean",
                        enforce_detection=False,
                    )
                    if obj["verified"]:
                        cutFrame = cv2.medianBlur(roi, 21)
                        cutFrame = cv2.medianBlur(cutFrame, 21)
                        cutFrame = cv2.medianBlur(cutFrame, 21)
                        frame[int(y1) : int(y2), int(x1) : int(x2)] = cutFrame
                        # frame = cv2.rectangle(
                        #     frame,
                        #     (int(x1), int(y1)),
                        #     (int(x2), int(y2)),
                        #     (0, 255, 0),
                        #     2,
                        #     cv2.LINE_AA,
                        # )

            output.write(frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            print("Stream disconnected")
            break

    vid_capture.release()
    output.release()
    cv2.destroyAllWindows()
