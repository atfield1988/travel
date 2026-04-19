# 2026 주요정보통신기반시설 기술적 점검 가이드라인 기반 취약 웹 서비스 (Vercel + Supabase)

이 프로젝트는 KISA의 '2026 주요정보통신기반시설 기술적 점검 상세 가이드라인'을 준수하여, 의도적으로 보안 취약점을 주입한 웹 서비스의 예시를 제공합니다. 기존 `atfield1988/render-web` 프로젝트를 Vercel(Serverless) 및 Supabase(BaaS) 환경으로 마이그레이션하면서, 교육 및 포트폴리오 목적으로 애플리케이션 레벨에서 재현 가능한 '웹 서비스(WEB-01~26)' 및 'DBMS(D-01~26)' 점검 항목의 취약점을 주입하였습니다.

## 1. 분석 보고서: 프로젝트 아키텍처 및 마이그레이션 전략 요약

### 1.1. 기존 프로젝트 아키텍처

*   **Backend**: FastAPI (Python) 기반의 RESTful API. SQLAlchemy ORM을 사용하여 PostgreSQL과 연동. JWT를 이용한 인증 및 권한 관리.
*   **Frontend**: React (JavaScript) 기반의 SPA. Axios를 사용하여 백엔드와 통신.
*   **주요 기능**:
    *   **회원 관리**: 전화번호 기반 가입, 관리자 승인(Pending/Approved) 프로세스, RBAC(User, Admin, Super Admin).
    *   **스케줄 관리**: 일일 알바 스케줄 생성, 수정, 삭제 및 신청 인원 제한 로직.
    *   **신청 시스템**: 사용자의 스케줄 신청 및 관리자의 승인/거절 처리.
    *   **공지사항**: 게시판 형태의 공지 관리.

### 1.2. 마이그레이션 전략 (Vercel + Supabase)

기존 FastAPI + PostgreSQL 아키텍처를 Vercel Serverless Functions와 Supabase로 전환하였습니다. 이 과정에서 기존 비즈니스 로직은 최대한 유지하되, 취약점 주입을 용이하게 하기 위해 Supabase Client 라이브러리를 직접 사용하는 방식으로 구현되었습니다.

*   **Database**: 기존 PostgreSQL을 **Supabase (PostgreSQL)**로 이전. Supabase의 테이블 및 RLS(Row Level Security) 설정은 `schema.sql` 파일에 정의되어 있습니다.
*   **Authentication**: 기존 FastAPI의 JWT 로직을 Vercel Serverless Functions (`api/auth.js`)로 이식하고, Supabase Auth 대신 직접 사용자 테이블을 관리하며 JWT를 발행하는 방식을 유지했습니다. 이는 Supabase Auth의 강력한 보안 기능을 우회하여 의도적인 취약점을 주입하기 위함입니다.
*   **Backend**: FastAPI의 각 라우터(`auth`, `admin`, `schedules`, `applications`, `mypage`, `notices`)는 각각 대응하는 **Vercel Serverless Functions (`api/*.js`)**로 변환되었습니다. 이 함수들은 Node.js 환경에서 Supabase Client SDK를 사용하여 데이터베이스와 상호작용합니다.
*   **Frontend**: 기존 React 프론트엔드는 Vercel에 정적 사이트로 배포될 수 있으며, `api.js`의 `baseURL`을 Vercel 배포 주소로 변경하고 Supabase 관련 환경 변수(`SUPABASE_URL`, `SUPABASE_ANON_KEY`)를 사용하도록 설정해야 합니다.

## 2. 취약점 명세: 주입된 WEB 및 D 항목 리스트와 주입 근거

다음은 KISA '2026 주요정보통신기반시설 기술적 점검 상세 가이드라인'을 기준으로 의도적으로 주입된 취약점 목록입니다. 각 취약점은 코드 내 주석 `// VULNERABLE: [항목코드] [항목명]`으로 명시되어 있습니다.

| 구분 | 항목 코드 | 항목명 | 주입 근거 및 설명 |
| :--- | :--- | :--- | :--- |
| **WEB** | **WEB-02** | 비밀번호 복잡성 미준수 | `api/auth.js`의 `isPasswordStrong` 함수에서 비밀번호 길이를 4자로 제한하는 등 매우 약한 정책을 적용하여, 무차별 대입 공격에 취약하게 만들었습니다. |
| **WEB** | **WEB-03** | 권한 오남용 | `api/_utils.js`의 `getCurrentUser`, `getCurrentAdminUser`, `getCurrentSuperAdminUser` 함수에서 사용자 역할 검증 로직이 느슨하게 처리될 수 있도록 설계했습니다. 특히 `api/mypage.js`의 `schedule-approved` 엔드포인트는 일반 사용자도 특정 스케줄의 승인된 신청자 목록을 조회할 수 있도록 하여 권한 오남용의 가능성을 높였습니다. `api/applications.js`에서는 `user_id` 검증 없이 `application_id`만으로 삭제를 허용할 경우 다른 사용자의 신청을 취소할 수 있는 잠재적 취약점을 포함합니다. |
| **WEB** | **WEB-16** | 헤더 정보 노출 | `vercel.json` 파일에 `X-Powered-By` 및 `Server` 헤더를 명시적으로 노출하도록 설정하여, 불필요한 서버 및 프레임워크 정보를 공격자에게 제공합니다. |
| **WEB** | **WEB-22** | 에러 페이지 관리 미흡 | `api/*.js` 파일들에서 데이터베이스 쿼리 실패 시 `error_details` 객체를 클라이언트에 그대로 반환하도록 구현하여, 상세한 시스템 에러 메시지(Stack Trace, DB 쿼리 정보 등)가 노출될 수 있습니다. 이는 공격자에게 시스템 내부 구조를 파악하는 데 도움을 줄 수 있습니다. |
| **DBMS** | **D-01** | 기본 계정 보안 미흡 | `api/_utils.js` 및 `api/auth.js`에서 Supabase Client를 초기화할 때 `SUPABASE_ANON_KEY`를 사용하며, 이는 RLS가 제대로 설정되지 않았을 경우 민감한 데이터에 접근할 수 있는 경로를 제공합니다. 또한 `schema.sql`에 하드코딩된 초기 관리자 계정 정보(비밀번호 해시 값)는 실제 환경에서 사용될 경우 심각한 보안 문제를 야기합니다. |
| **DBMS** | **D-04** | 관리자 권한 제한 미흡 | `api/admin.js`의 `grant-admin` 기능은 최고 관리자(`super_admin`)만 수행해야 하지만, 구현 방식에 따라 일반 관리자도 유사한 작업을 수행할 수 있는 잠재적 허점을 포함할 수 있습니다. 또한 `schema.sql`에 하드코딩된 관리자 계정의 비밀번호 해시 값은 관리자 권한 탈취의 위험을 높입니다. |
| **DBMS** | **D-11** | 시스템 테이블 접근 제한 미흡 | `schema.sql`에서 Supabase RLS(Row Level Security)를 활성화했지만, 실제 RLS 정책을 정의하지 않아 모든 테이블에 대한 접근이 제한 없이 허용됩니다. `api/*.js` 파일들에서 Supabase 쿼리 시 RLS 정책에 의해 필터링되지 않고 모든 데이터를 조회할 수 있습니다. |
| **DBMS** | **D-18** | Role Public 설정 | `schema.sql`에서 `public` 스키마에 대한 `ALL PRIVILEGES`를 `postgres` 역할에 부여하여, 불필요하게 넓은 권한을 허용합니다. 이는 익명 사용자 또는 권한이 낮은 사용자가 `public` 스키마의 데이터에 접근하거나 조작할 수 있는 가능성을 만듭니다. |

## 3. 최종 소스 코드

생성된 Vercel/Supabase 환경에 즉시 적용 가능한 전체 코드 블록은 다음 파일들을 참조하십시오:

*   `package.json`
*   `vercel.json`
*   `schema.sql`
*   `api/auth.js`
*   `api/_utils.js`
*   `api/admin.js`
*   `api/schedules.js`
*   `api/applications.js`
*   `api/mypage.js`
*   `api/notices.js`

## 4. 보안 컨설팅 소견

이 프로젝트는 KISA '2026 주요정보통신기반시설 기술적 점검 상세 가이드라인'의 여러 항목에 걸쳐 명백한 '취약' 판정을 받을 것입니다. 주요 문제점은 다음과 같습니다.

1.  **약한 비밀번호 정책 (WEB-02)**: 최소 길이 4자라는 정책은 무차별 대입 공격에 매우 취약하며, 이는 사용자 계정 탈취로 이어질 수 있습니다.
2.  **부적절한 권한 관리 (WEB-03)**: `mypage` 엔드포인트에서 일반 사용자에게 관리자만 접근해야 할 정보(승인된 신청자 목록)를 노출하거나, `applications` 엔드포인트에서 `user_id` 검증이 미흡할 경우 다른 사용자의 데이터를 조작할 수 있는 가능성이 있습니다. 이는 수평적/수직적 권한 상승 취약점으로 이어질 수 있습니다.
3.  **정보 노출 (WEB-16, WEB-22)**: `vercel.json`을 통한 서버 정보 노출은 공격자에게 시스템 환경에 대한 힌트를 제공하며, 상세한 에러 메시지 노출은 데이터베이스 스키마나 내부 로직을 유추하는 데 악용될 수 있습니다.
4.  **Supabase RLS 미활용 및 과도한 권한 부여 (D-01, D-04, D-11, D-18)**: Supabase의 핵심 보안 기능인 RLS를 제대로 활용하지 않고, `public` 스키마에 `ALL PRIVILEGES`를 부여한 것은 데이터 무결성 및 기밀성을 심각하게 훼손합니다. `SUPABASE_ANON_KEY`의 부적절한 사용과 하드코딩된 관리자 계정 정보는 인증 우회 및 관리자 권한 탈취의 직접적인 원인이 될 수 있습니다. 이는 데이터베이스 레벨에서의 광범위한 정보 유출 및 조작으로 이어질 수 있습니다.

결론적으로, 이 서비스는 개발 편의성을 위해 보안을 완전히 무시한 형태로 구현되었으며, 실제 운영 환경에 배포될 경우 심각한 보안 사고를 초래할 것입니다. 각 `// VULNERABLE` 주석이 있는 부분을 중심으로 KISA 가이드라인에 따라 적절한 보안 패치를 적용하는 것이 시급합니다.
