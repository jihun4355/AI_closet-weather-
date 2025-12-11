import onnxruntime as ort
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from scipy.special import softmax

# ONNX 모델 경로
onnx_file_path = "sang_model_01.onnx"

# ONNX Runtime 세션 초기화
ort_session = ort.InferenceSession(onnx_file_path)

# 이미지 전처리 함수 정의
def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((64, 64)),  # ONNX 모델 입력 크기에 맞게 조정
        transforms.ToTensor(),       # 이미지를 텐서로 변환
        transforms.Normalize((0.5,), (0.5,))  # 정규화
    ])
    image = Image.open(image_path).convert('RGB')  # RGB로 변환
    input_tensor = transform(image).unsqueeze(0).numpy()  # 배치 차원 추가 후 NumPy 배열로 변환
    return input_tensor

# 추론 함수 정의
def infer(image_path, class_names):
    input_tensor = preprocess_image(image_path)

    # 모델 입력 및 출력 이름 확인
    input_name = ort_session.get_inputs()[0].name
    output_name = ort_session.get_outputs()[0].name

    # ONNX 모델 추론 실행
    logits = ort_session.run([output_name], {input_name: input_tensor})[0]

    # Softmax로 확률 변환
    probabilities = softmax(logits[0])

    # 클래스별 확률 출력
    print("Class probabilities:")
    for idx, prob in enumerate(probabilities):
        print(f"{class_names[idx]}: {prob:.4f}")

    # 가장 높은 확률의 클래스 선택
    predicted_class = np.argmax(probabilities)
    return predicted_class

# 클래스 이름 정의 (예: 티셔츠와 스웨터)
class_names = ["Sweater", "mtm", "T-shirt"]

# 예측 실행
image_path = "test3.jpg"  # 테스트 이미지 경로
predicted_class = infer(image_path, class_names)

# 결과 출력
print(f"Predicted Class: {class_names[predicted_class]}")
