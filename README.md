# Mystic Harmony

동양과 서양의 점성술을 결합한 운세 서비스 웹 애플리케이션입니다.

## 기능

- **운세 분석**: 사용자의 생년월일과 태어난 시간을 기반으로 운세를 분석합니다.
- **간단 모드와 고급 모드**: 기본적인 운세부터 심도 있는 분석까지 선택할 수 있습니다.
- **파트너 매칭**: 사용자와 가장 잘 맞는 파트너의 특성을 제시합니다.
- **시각화**: 파트너의 얼굴을 시각적으로 생성합니다.

## 설치 방법

1. 저장소를 클론합니다:
```
git clone https://github.com/eoh9/mystic-harmony.git
cd mystic-harmony
```

2. 필요한 패키지를 설치합니다:
```
pip install -r requirements.txt
```

3. `.env` 파일에 OpenAI API 키를 설정합니다:
```
OPENAI_API_KEY=your_api_key_here
```

## 실행 방법

다음 명령어로 앱을 실행합니다:
```
streamlit run app.py
```

브라우저에서 http://localhost:8501 으로 접속하여 앱을 사용할 수 있습니다.

## 프로젝트 구조

- `app.py`: 메인 Streamlit 애플리케이션
- `fortune_engine.py`: 운세 분석 엔진
- `partner_matcher.py`: 파트너 매칭 시스템
- `face_generator.py`: 파트너 얼굴 생성기
- `gpt_enhancer.py`: GPT를 활용한 텍스트 강화 모듈

## 개발 환경

- Python 3.9+
- Streamlit
- OpenAI API
- Pandas, NumPy
- ephem (천문학 계산)
- PIL (이미지 처리)

## 라이센스

MIT 라이센스를 따릅니다.
