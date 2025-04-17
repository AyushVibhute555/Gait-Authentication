import cv2
import mediapipe as mp
import numpy as np

def extract_gait_features(video_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"[ERROR] Could not open video file: {video_path}")
        return None

    features = []
    frame_count = 0

    print("[INFO] Reading video frames... Press 'q' to exit preview.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 5 != 0:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        # Debug display
        cv2.imshow("Pose Detection Preview", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if results.pose_landmarks:
            frame_feats = []
            for lm in results.pose_landmarks.landmark:
                frame_feats.extend([lm.x, lm.y])
            features.append(frame_feats)
        else:
            print(f"[WARNING] No keypoints in frame {frame_count}")

    cap.release()
    cv2.destroyAllWindows()
    pose.close()

    if not features:
        print(f"[ERROR] No keypoints detected in video: {video_path}")
        return None

    features = np.array(features)
    avg_features = np.mean(features, axis=0)

    if np.any(np.isnan(avg_features)):
        print(f"[ERROR] NaN detected in features.")
        return None

    return avg_features
