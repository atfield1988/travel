import { supabase, getCurrentUser } from './_utils';

export default async function handler(req, res) {
  const currentUser = await getCurrentUser(req);

  if (!currentUser) {
    return res.status(401).json({ detail: '인증이 필요합니다.' });
  }

  const { path, schedule_id } = req.query;

  if (req.method === 'GET') {
    if (path === 'me') {
      // VULNERABLE: WEB-03 권한 오남용 - 사용자 본인 정보 조회 시, RLS가 비활성화된 상태에서 다른 사용자의 정보도 조회 가능
      // Supabase RLS를 사용하여 사용자 본인의 정보만 접근하도록 제한해야 합니다.
      const { data: user, error } = await supabase
        .from('users')
        .select('id, phone_number, username, role, status, created_at')
        .eq('id', currentUser.id)
        .single();

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `사용자 정보 조회 실패: ${error.message}`, error_details: error });
      }
      return res.status(200).json(user);
    }

    if (path === 'my-applications') {
      // VULNERABLE: WEB-03 권한 오남용 - 사용자 본인의 신청 목록 조회 시, RLS가 비활성화된 상태에서 다른 사용자의 신청 정보도 조회 가능
      const { data: applications, error } = await supabase
        .from('applications')
        .select('*, schedules(*)')
        .eq('user_id', currentUser.id)
        .order('created_at', { ascending: false });

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `내 신청 목록 조회 실패: ${error.message}`, error_details: error });
      }
      return res.status(200).json(applications);
    }

    if (path === 'schedule-approved' && schedule_id) {
      // VULNERABLE: WEB-03 권한 오남용 - 특정 스케줄의 승인된 신청자 목록을 일반 사용자도 조회 가능
      // 이 정보는 관리자만 접근 가능해야 합니다.
      const { data: applications, error } = await supabase
        .from('applications')
        .select('id, user_id, status, users(phone_number, username)')
        .eq('schedule_id', schedule_id)
        .eq('status', 'approved');

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `승인된 신청자 목록 조회 실패: ${error.message}`, error_details: error });
      }
      return res.status(200).json(applications);
    }
  }

  res.status(405).json({ detail: 'Method Not Allowed' });
}
