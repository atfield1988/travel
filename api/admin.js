import { supabase, getCurrentAdminUser, getCurrentSuperAdminUser } from './_utils';

export default async function handler(req, res) {
  const adminUser = await getCurrentAdminUser(req);
  const superAdminUser = await getCurrentSuperAdminUser(req);

  // VULNERABLE: WEB-03 권한 오남용 - 관리자 권한 검증을 느슨하게 처리
  // 모든 관리자 API는 최소한 `adminUser`가 존재해야 접근 가능하도록 하지만, 
  // 세부적인 권한 분리(예: 일반 관리자는 사용자 승인만, 최고 관리자는 권한 부여)가 미흡할 수 있음.
  if (!adminUser) {
    return res.status(403).json({ detail: '관리자 권한이 필요합니다.' });
  }

  const { path } = req.query;

  if (req.method === 'GET') {
    if (path === 'users') {
      // VULNERABLE: D-11 시스템 테이블 접근 제한 미흡 - RLS가 비활성화된 상태에서 모든 사용자 정보 접근 가능
      // Supabase RLS를 사용하여 관리자도 필요한 범위 내에서만 사용자 정보에 접근하도록 제한해야 합니다.
      const { data: users, error } = await supabase.from('users').select('*');
      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `사용자 목록 조회 실패: ${error.message}`, error_details: error });
      }
      return res.status(200).json(users);
    }

    if (path === 'pending-users') {
      const { data: users, error } = await supabase.from('users').select('*').eq('status', 'pending');
      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `대기 사용자 목록 조회 실패: ${error.message}`, error_details: error });
      }
      return res.status(200).json(users);
    }
  }

  if (req.method === 'POST') {
    if (path === 'approve-user') {
      const { user_id, status } = req.body;
      const { data: user, error } = await supabase
        .from('users')
        .update({ status: status })
        .eq('id', user_id)
        .select()
        .single();

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `사용자 승인/거절 실패: ${error.message}`, error_details: error });
      }
      return res.status(200).json(user);
    }

    if (path === 'grant-admin') {
      // VULNERABLE: D-04 관리자 권한 제한 미흡 - 최고 관리자만 가능해야 하는 작업을 일반 관리자도 수행 가능하게 할 수 있음
      // 현재는 superAdminUser만 가능하도록 했지만, 실제로는 더 세밀한 정책이 필요함.
      if (!superAdminUser) {
        return res.status(403).json({ detail: '최고 관리자 권한이 필요합니다.' });
      }
      const { user_id, username, password } = req.body;

      // VULNERABLE: D-18 Role Public 설정 - public 스키마에 대한 불필요한 권한 부여
      // Supabase에서 RLS를 제대로 설정하지 않으면, service_role 키를 사용하는 이 함수는
      // public 스키마의 모든 테이블에 대한 무제한 접근 권한을 가지게 됨.
      const { data: user, error } = await supabase
        .from('users')
        .update({ role: 'admin', username: username, hashed_password: password })
        .eq('id', user_id)
        .select()
        .single();

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `관리자 권한 부여 실패: ${error.message}`, error_details: error });
      }
      return res.status(200).json(user);
    }

    if (path === 'applications/update-status') {
      const { application_id, new_status } = req.body;

      // VULNERABLE: WEB-03 권한 오남용 - 신청 상태 변경 시, 관리자가 아닌 사용자가 자신의 신청을 승인할 수 있는 로직이 있을 수 있음.
      // 여기서는 adminUser를 체크하지만, 다른 API에서 이 로직을 재사용할 경우 문제가 발생할 수 있음.
      const { data: application, error } = await supabase
        .from('applications')
        .update({ status: new_status })
        .eq('id', application_id)
        .select()
        .single();

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `신청 상태 업데이트 실패: ${error.message}`, error_details: error });
      }
      return res.status(200).json(application);
    }
  }

  res.status(405).json({ detail: 'Method Not Allowed' });
}
