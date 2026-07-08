# 📱 Global Market Hub - 100% 무료 무비용 반응형 증시 대시보드

이 프로젝트는 매일 아침 글로벌 증시 주요 지표(S&P 500, Nasdaq, Dow, KOSPI, KOSDAQ, 환율)와 뉴스를 수집하고 AI(Gemini)로 분석하여 **모바일/태블릿/PC**에서 확인할 수 있도록 제공하는 프리미엄 다크모드 글래스모피즘 웹앱입니다.

개인 PC를 켜둘 필요가 없으며, 카드 정보 등록 없이 **GitHub Actions (데이터 수집 스케줄러)**와 **Vercel (무료 호스팅)**을 이용해 24시간 클라우드 상에서 완전 자동 배포됩니다.

---

## 🚀 무료 클라우드 자동 배포 구축 절차 (최초 1회)

구글 클라우드 결제 계정 가입 문제 없이, 100% 무료로 자동 배포 환경을 완성하는 단계별 절차입니다.

### 1단계. GitHub 저장소 생성 및 코드 업로드
1. 개인 [GitHub](https://github.com/) 계정에 로그인하고 새 저장소(New Repository)를 생성합니다. (Private, Public 모두 가능)
2. 내 로컬 프로젝트 폴더(`C:\Project\Test`)에서 터미널(cmd 또는 PowerShell)을 열고 코드를 업로드합니다:
   ```bash
   git init
   git branch -M main
   git remote add origin https://github.com/사용자아이디/레포지토리이름.git
   git add .
   git commit -m "feat: init market dashboard"
   git push -u origin main
   ```

### 2단계. GitHub Actions 쓰기 권한 허용 (필수)
자동 배포 봇이 매일 아침 수집한 데이터를 다시 저장소에 업데이트할 수 있도록 권한을 설정합니다.
1. 내 GitHub 저장소 페이지의 상단 메뉴에서 **[Settings]**로 이동합니다.
2. 좌측 메뉴에서 **[Actions] -> [General]**을 클릭합니다.
3. 페이지 가장 하단의 **[Workflow permissions]** 항목을 찾습니다.
4. **"Read and write permissions"**를 선택하고 **Save**를 누릅니다.

### 3단계. GitHub Secrets에 API 키 등록
1. 저장소 상단의 **[Settings]** 메뉴로 이동합니다.
2. 좌측 메뉴에서 **[Secrets and variables] -> [Actions]**를 클릭합니다.
3. **[New repository secret]** 버튼을 클릭합니다.
4. 아래 값을 입력하고 추가합니다:
   - **Name**: `GEMINI_API_KEY`
   - **Secret**: 본인의 구글 [Gemini API Key](https://aistudio.google.com/) 기입

### 4단계. Vercel에서 사이트 호스팅 연동 (카드 등록 없음)
1. [Vercel](https://vercel.com/) 사이트에 접속하여 **[Sign Up]**을 누르고, **Continue with GitHub**를 선택해 가입합니다.
2. 가입 완료 후 Vercel 대시보드 화면에서 우측 상단의 **[Add New...] -> [Project]**를 클릭합니다.
3. 내 GitHub 계정과 연동되면 방금 만든 저장소 이름이 리스트에 보입니다. 해당 저장소 우측의 **[Import]** 버튼을 클릭합니다.
4. 프레임워크 설정 등은 Vercel이 자동으로 Vite/React를 감지하므로, 변경할 필요 없이 하단의 **[Deploy]** 버튼을 누릅니다.
5. 1분 이내로 첫 빌드가 완료되며 무료 사이트 주소(예: `https://레포이름.vercel.app`)가 즉시 제공됩니다!

---

## ⏰ 작동 스케줄 안내
- **오전 8시 자동 갱신**: 매일 오전 8시(한국 시간)에 GitHub Actions가 자동으로 파이썬 데이터를 수집해 깃허브에 밀어 넣습니다.
- **실시간 웹앱 갱신**: Vercel이 코드가 밀려 들어온 것을 감지하여 약 10초 만에 사이트를 자동 재빌드하고 최신 화면으로 모바일/태블릿에 서비스해 줍니다.

---

## 💻 로컬에서 직접 실행해보기
1. 로컬 환경 변수 `.env` 파일에 `GEMINI_API_KEY`를 설정합니다.
2. 터미널에서 데이터를 수집하고 요약본을 생성합니다:
   ```bash
   python main.py
   ```
3. 로컬 웹 서버를 가동합니다:
   ```bash
   npm run dev
   ```
4. `http://localhost:5173/`에 접속하여 모바일 기기 레이아웃을 미리 테스트해 볼 수 있습니다.
