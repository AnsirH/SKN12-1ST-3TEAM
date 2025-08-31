# 🚀 Hugging Face Spaces 배포 가이드

> **전국 차량 등록 현황 분석 대시보드를 Hugging Face Spaces에 배포하는 완벽한 가이드**

## 📋 **사전 준비사항**

### **필요한 계정**
- [ ] GitHub 계정
- [ ] Hugging Face 계정
- [ ] GitHub 저장소 (SKN12_First)

### **필요한 정보**
- [ ] Hugging Face 사용자명
- [ ] GitHub 저장소 URL
- [ ] 프로젝트 이름

## 🔧 **1단계: Hugging Face Space 생성**

### **1.1 Space 생성**
1. [Hugging Face](https://huggingface.co/)에 로그인
2. 우측 상단 "New Space" 버튼 클릭
3. Space 설정 입력:
   ```
   Owner: [your-username]
   Space name: vehicle-analysis-dashboard
   Space SDK: Streamlit
   License: MIT
   Hardware: CPU Basic
   ```

### **1.2 Space 설정 확인**
- Space가 생성되면 자동으로 GitHub 저장소와 연결 옵션이 제공됩니다
- "Repository" 섹션에서 GitHub 저장소 연결

## 🔑 **2단계: Hugging Face API 토큰 생성**

### **2.1 토큰 생성**
1. [Hugging Face Settings](https://huggingface.co/settings/tokens)로 이동
2. "New token" 버튼 클릭
3. 토큰 설정:
   ```
   Name: hf-spaces-deploy
   Role: Write
   ```
4. "Generate token" 클릭하여 토큰 생성
5. **생성된 토큰을 안전한 곳에 복사** (다시 볼 수 없음)

### **2.2 토큰 권한 확인**
- `write` 권한이 있어야 Space에 배포 가능
- 토큰은 절대 공개하지 마세요!

## 🔗 **3단계: GitHub 저장소 설정**

### **3.1 GitHub Secrets 설정**
1. GitHub 저장소로 이동
2. "Settings" → "Secrets and variables" → "Actions"
3. "New repository secret" 클릭하여 다음 시크릿 추가:

#### **HF_TOKEN**
```
Name: HF_TOKEN
Value: [생성된 Hugging Face API 토큰]
```

#### **HF_SPACE**
```
Name: HF_SPACE
Value: [username]/vehicle-analysis-dashboard
```

### **3.2 GitHub Actions 활성화**
1. "Actions" 탭으로 이동
2. "Deploy to Hugging Face Spaces" 워크플로우가 표시되는지 확인
3. 워크플로우가 비활성화되어 있다면 "Enable workflow" 클릭

## 📁 **4단계: 프로젝트 파일 구조 확인**

### **4.1 필수 파일 확인**
```
SKN12_First/
├── .github/
│   └── workflows/
│       └── deploy-to-huggingface.yml  ✅
├── app.py                              ✅
├── requirements.txt                     ✅
├── README.md                           ✅
├── my_pages/                           ✅
├── module/                             ✅
└── data/                               ✅
```

### **4.2 파일 수정 사항**
- [ ] `app.py`의 페이지 제목 및 아이콘 설정
- [ ] `requirements.txt`의 모든 의존성 포함
- [ ] `.gitignore`에 `.cursor/` 폴더 제외

## 🚀 **5단계: 배포 실행**

### **5.1 자동 배포**
1. `main` 브랜치에 코드 push:
   ```bash
   git add .
   git commit -m "Add Hugging Face Spaces deployment"
   git push origin main
   ```

2. GitHub Actions 자동 실행:
   - Actions 탭에서 워크플로우 실행 상태 확인
   - 각 단계별 실행 로그 확인

### **5.2 배포 상태 확인**
1. **GitHub Actions**: 워크플로우 실행 완료 확인
2. **Hugging Face**: Space 페이지에서 배포 상태 확인
3. **Space URL**: `https://huggingface.co/spaces/[username]/vehicle-analysis-dashboard`

## 🧪 **6단계: 배포 검증**

### **6.1 Space 실행 테스트**
1. Space 페이지 방문
2. "Run" 버튼 클릭
3. 애플리케이션 로딩 확인
4. 각 페이지 기능 테스트:
   - [ ] 홈페이지 표시
   - [ ] 차량 등록 현황 페이지
   - [ ] FAQ 페이지
   - [ ] 지도 시각화
   - [ ] 차트 분석

### **6.2 오류 확인**
1. **Space Logs**: 오류 메시지 확인
2. **GitHub Actions**: 배포 로그 확인
3. **의존성 문제**: 패키지 설치 오류 확인

## 🔄 **7단계: CI/CD 파이프라인 테스트**

### **7.1 자동 배포 테스트**
1. 코드 수정 후 `main` 브랜치에 push
2. GitHub Actions 자동 실행 확인
3. Hugging Face Spaces 자동 업데이트 확인

### **7.2 Pull Request 테스트**
1. 새로운 브랜치에서 기능 개발
2. Pull Request 생성
3. GitHub Actions 테스트 실행 확인

## 📊 **8단계: 모니터링 및 유지보수**

### **8.1 성능 모니터링**
- [ ] Space 사용량 확인
- [ ] 응답 시간 모니터링
- [ ] 사용자 접근 통계 확인

### **8.2 정기 업데이트**
- [ ] 의존성 패키지 버전 업데이트
- [ ] 보안 패치 적용
- [ ] 기능 개선 및 버그 수정

## 🐛 **문제 해결 가이드**

### **일반적인 문제들**

#### **1. 배포 실패**
```
Error: Failed to deploy to Hugging Face Spaces
```
**해결 방법:**
- GitHub Secrets 확인 (`HF_TOKEN`, `HF_SPACE`)
- Hugging Face API 토큰 권한 확인
- GitHub Actions 워크플로우 로그 확인

#### **2. 의존성 설치 실패**
```
Error: Package installation failed
```
**해결 방법:**
- `requirements.txt` 파일 형식 확인
- 패키지 버전 호환성 체크
- Python 버전 확인 (3.9+)

#### **3. 애플리케이션 실행 오류**
```
Error: Streamlit app failed to start
```
**해결 방법:**
- `app.py` 파일 문법 오류 체크
- 모듈 import 경로 확인
- 데이터 파일 경로 확인

### **로그 확인 방법**

#### **GitHub Actions 로그**
1. 저장소 → Actions 탭
2. 워크플로우 실행 기록 클릭
3. 실패한 단계의 로그 확인

#### **Hugging Face Space 로그**
1. Space 페이지 → Logs 탭
2. 실행 로그 및 오류 메시지 확인
3. 디버깅 정보 분석

## 📚 **추가 리소스**

### **공식 문서**
- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Streamlit Documentation](https://docs.streamlit.io/)

### **유용한 링크**
- [Hugging Face Spaces Examples](https://huggingface.co/spaces)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Streamlit Cloud](https://streamlit.io/cloud)

## 🎯 **성공 체크리스트**

### **배포 완료 확인**
- [ ] GitHub Actions 워크플로우 성공 실행
- [ ] Hugging Face Space 정상 생성
- [ ] 애플리케이션 정상 실행
- [ ] 모든 기능 정상 작동
- [ ] Space URL 공유 가능

### **CI/CD 파이프라인 확인**
- [ ] 코드 push 시 자동 배포
- [ ] Pull Request 시 테스트 실행
- [ ] 배포 상태 배지 표시
- [ ] 오류 시 자동 알림

---

## 🚀 **축하합니다!**

이제 전국 차량 등록 현황 분석 대시보드가 Hugging Face Spaces에 성공적으로 배포되었습니다!

**다음 단계:**
1. Space URL을 팀원들과 공유
2. 사용자 피드백 수집
3. 지속적인 기능 개선
4. 성능 최적화 및 모니터링

**문제가 발생하면:**
- 이 가이드의 문제 해결 섹션 참조
- GitHub Issues에 문제 등록
- 팀 내부 기술 지원 요청

**Happy Deploying! 🎉**
