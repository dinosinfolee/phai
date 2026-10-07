# beaglecam

비글 수업용 USB 카메라 모듈입니다.

## 설치

```
pip install "https://github.com/dinosinfolee/phai/archive/main.zip#subdirectory=beagle"
```

## 업데이트

```
pip install -U --force-reinstall --no-deps "https://github.com/dinosinfolee/phai/archive/main.zip#subdirectory=beagle"
```

## 사용

카메라 화면 보기:

```
python -m beaglecam      # 외장 카메라 자동 탐색
python -m beaglecam 1    # 1번 카메라
```

조작: 0~9 카메라 전환, s 사진 저장, q 종료

코드에서 사용:

```python
from beaglecam import open_cam, save

cap = open_cam(1)        # 카메라 열기 (실패 시 None)
ok, frame = cap.read()   # 영상 한 장 읽기
save(frame)              # shots 폴더에 사진 저장
```
