"""USB 카메라 보기 (경량판)

    py -m beaglecam        외장 USB 카메라를 자동으로 찾아 연다 (가장 뒤 번호부터 탐색)
    py -m beaglecam 1      1번 카메라를 연다

조작:  0~9 카메라 전환   s 사진 저장   q/ESC 종료
다른 코드에서:  from beaglecam import open_cam
"""
import os
import sys
import time

import cv2

# 윈도우에서는 DSHOW 백엔드가 더 빠르게 열린다
BACKEND = cv2.CAP_DSHOW if os.name == "nt" else cv2.CAP_ANY
SHOT_DIR = os.path.join(os.getcwd(), "shots")  # 실행한 폴더에 저장


def open_cam(i, wait=2.0):
    """i번 카메라를 열어 반환한다. 실패하면 None.
    ESP32 계열 카메라는 첫 프레임이 늦게 나오므로 최대 wait초 대기한다."""
    cap = cv2.VideoCapture(i, BACKEND)
    end = time.time() + wait
    while cap.isOpened() and time.time() < end:
        if cap.read()[0]:
            return cap
        time.sleep(0.05)
    cap.release()
    return None


def find_cam(max_id=5):
    """뒤 번호부터 시도한다. 내장 캠이 0번이므로 외장 카메라는 대개 뒤 번호이다."""
    for i in reversed(range(max_id)):
        cap = open_cam(i)
        if cap:
            return i, cap
    return None, None


def save(frame):
    """한글 경로에서도 저장되도록 imwrite 대신 imencode 를 사용한다."""
    os.makedirs(SHOT_DIR, exist_ok=True)
    path = os.path.join(SHOT_DIR, time.strftime("%Y%m%d_%H%M%S.png"))
    cv2.imencode(".png", frame)[1].tofile(path)
    print("[저장]", path)


def main():
    if len(sys.argv) > 1:
        idx = int(sys.argv[1])
        cap = open_cam(idx)
    else:
        idx, cap = find_cam()
    if cap is None:
        print("카메라를 열 수 없습니다. 연결 상태와 다른 프로그램의 사용 여부를 확인하십시오.")
        return

    win = "camera"
    print(f"{idx}번 카메라 연결 완료")
    while True:
        ok, frame = cap.read()
        if not ok:
            print("영상을 수신하지 못했습니다.")
            break
        cv2.imshow(win, frame)
        cv2.setWindowTitle(win, f"camera {idx}  |  0-9: switch  s: save  q: quit")

        key = cv2.waitKey(1) & 0xFF
        if key in (ord("q"), 27):
            break
        elif key == ord("s"):
            save(frame)
        elif ord("0") <= key <= ord("9"):
            new = open_cam(key - ord("0"))
            if new:
                cap.release()
                cap, idx = new, key - ord("0")
                print(f"{idx}번 카메라로 전환")
            else:
                print(f"{key - ord('0')}번 카메라를 열 수 없습니다.")
        if cv2.getWindowProperty(win, cv2.WND_PROP_VISIBLE) < 1:
            break  # 창의 X 버튼으로 닫은 경우

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
