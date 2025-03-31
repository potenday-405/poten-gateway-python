# 기록의 정원 Gateway

## 개요 
이 프로젝트에서는 MSA(Microservices Architecture) 구조를 도입하고, 서로 다른 언어(Python, Go)로 개발된 백엔드 서비스 간 통신을 원활하게 하기 위해 Gateway를 적용했습니다.

## 도입 배경
- 프로젝트 내에서 Go 언어로 개발된 서비스와 Python으로 개발된 서비스가 공존
- 각 서비스의 API 요청을 하나의 진입점에서 처리할 Gateway 필요
- 인증 및 라우팅 기능을 수행하는 중앙 관리 포인트 필요

## Gateway 역할
### 1. 인증 처리
- 사용자의 인증 정보를 검증하고, 각 서비스에 전달할 수 있도록 구성
- 인증이 필요한 요청과 불필요한 요청을 구분하여 관리
- ![인증방식](https://github.com/user-attachments/assets/2777741a-0760-4ccb-bd3b-bab0e591c11c)

### 2. 라우팅 기능
- Go 서비스로 전달해야 할 요청과 Python 서비스로 전달해야 할 요청을 구분
- 내부 서비스 간의 API 호출을 Gateway를 통해 일관되게 관리
###3. 확장성을 고려한 설계
- 서비스가 추가될 경우, Gateway를 통해 손쉽게 라우팅 확장 가능
- MSA 아키텍처 기반으로 마이크로서비스 간 결합도를 낮추고 독립적인 개발 가능

## 🛠 사용 기술
- Gateway: Nginx / API Gateway / Custom Gateway
- Backend: Go, Python
- Authentication: JWT 기반 인증
- Containerization: Docker

## 한계점 & 개선 방향
- 단일 데이터베이스를 공유하는 구조였기 때문에 완전한 MSA 구조를 이루지는 못함
- MSA 운영 시 데이터 일관성 유지, DB 동기화 문제에 대한 실질적인 경험 부족
- 향후 독립적인 데이터 저장소 구성 및 서비스 간 데이터 동기화 전략 학습 필요

