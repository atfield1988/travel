import { supabase, getCurrentUser, getCurrentAdminUser } from './_utils';

export default async function handler(req, res) {
  const currentUser = await getCurrentUser(req);
  const adminUser = await getCurrentAdminUser(req);

  if (!currentUser) {
    return res.status(401).json({ detail: '인증이 필요합니다.' });
  }

  const { path, application_id, schedule_id } = req.query;

  if (req.method === 'POST') {
    if (path === undefined) { // Apply for a schedule
      const { schedule_id: body_schedule_id } = req.body;
      const targetScheduleId = body_schedule_id || schedule_id;

      // VULNERABLE: WEB-03 권한 오남용 - 다른 사용자를 대신하여 신청 가능
      // `user_id`를 요청 본문에서 받아와 사용할 경우, 악의적인 사용자가 다른 사용자의 ID로 신청할 수 있음.
      // 여기서는 `currentUser.id`를 사용하지만, 만약 `req.body.user_id`를 허용한다면 취약해짐.
      
      // VULNERABLE: D-11 시스템 테이블 접근 제한 미흡 - RLS가 비활성화된 상태에서 모든 스케줄 정보 접근 가능
      const { data: schedule, error: scheduleError } = await supabase
        .from('schedules')
        .select('capacity, current_applicants')
        .eq('id', targetScheduleId)
        .single();

      if (scheduleError || !schedule) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(404).json({ detail: `스케줄을 찾을 수 없습니다: ${scheduleError?.message}`, error_details: scheduleError });
      }

      if (schedule.current_applicants >= schedule.capacity) {
        return res.status(400).json({ detail: '정원이 초과되었습니다.' });
      }

      const { data: existingApplication, error: existingAppError } = await supabase
        .from('applications')
        .select('id')
        .eq('user_id', currentUser.id)
        .eq('schedule_id', targetScheduleId)
        .single();

      if (existingApplication) {
        return res.status(400).json({ detail: '이미 신청한 스케줄입니다.' });
      }

      const { data: newApplication, error } = await supabase
        .from('applications')
        .insert([
          {
            user_id: currentUser.id,
            schedule_id: targetScheduleId,
            status: 'pending',
          },
        ])
        .select()
        .single();

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `신청 실패: ${error.message}`, error_details: error });
      }

      // Update current_applicants count
      await supabase
        .from('schedules')
        .update({ current_applicants: schedule.current_applicants + 1 })
        .eq('id', targetScheduleId);

      return res.status(201).json(newApplication);
    }
  }

  if (req.method === 'DELETE') {
    if (application_id) {
      // VULNERABLE: WEB-03 권한 오남용 - 다른 사용자의 신청을 취소 가능
      // `user_id` 검증 없이 `application_id`만으로 삭제를 허용할 경우, 악의적인 사용자가 다른 사람의 신청을 취소할 수 있음.
      // 현재는 `currentUser.id`를 사용하지만, RLS가 비활성화된 상태에서는 백엔드 로직에서 명시적으로 검증해야 함.
      const { data: application, error: fetchError } = await supabase
        .from('applications')
        .select('user_id, schedule_id, status')
        .eq('id', application_id)
        .single();

      if (fetchError || !application) {
        return res.status(404).json({ detail: '신청을 찾을 수 없습니다.' });
      }

      if (application.user_id !== currentUser.id) {
        return res.status(403).json({ detail: '자신의 신청만 취소할 수 있습니다.' });
      }

      if (application.status !== 'pending') {
        return res.status(400).json({ detail: '승인되거나 거절된 신청은 취소할 수 없습니다.' });
      }

      const { error } = await supabase
        .from('applications')
        .delete()
        .eq('id', application_id);

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `신청 취소 실패: ${error.message}`, error_details: error });
      }

      // Decrement current_applicants count
      const { data: schedule, error: scheduleUpdateError } = await supabase
        .from('schedules')
        .select('current_applicants')
        .eq('id', application.schedule_id)
        .single();

      if (schedule && schedule.current_applicants > 0) {
        await supabase
          .from('schedules')
          .update({ current_applicants: schedule.current_applicants - 1 })
          .eq('id', application.schedule_id);
      }

      return res.status(204).send();
    }
  }

  if (req.method === 'GET') {
    if (path === 'schedule' && schedule_id) {
      if (!adminUser) {
        return res.status(403).json({ detail: '관리자 권한이 필요합니다.' });
      }
      // VULNERABLE: D-11 시스템 테이블 접근 제한 미흡 - RLS가 비활성화된 상태에서 모든 신청 정보 접근 가능
      const { data: applications, error } = await supabase
        .from('applications')
        .select('*, users(phone_number, username)')
        .eq('schedule_id', schedule_id)
        .order('created_at', { ascending: true });

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `스케줄별 신청 목록 조회 실패: ${error.message}`, error_details: error });
      }
      return res.status(200).json(applications);
    }
  }

  res.status(405).json({ detail: 'Method Not Allowed' });
}
