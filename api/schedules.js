import { supabase, getCurrentAdminUser, getCurrentUser } from './_utils';

export default async function handler(req, res) {
  const adminUser = await getCurrentAdminUser(req);
  const currentUser = await getCurrentUser(req);

  const { path, schedule_id } = req.query;

  // VULNERABLE: WEB-03 권한 오남용 - 스케줄 생성/수정/삭제 시 관리자 권한 검증을 느슨하게 처리
  // 모든 관리자 API는 최소한 `adminUser`가 존재해야 접근 가능하도록 하지만, 
  // 세부적인 권한 분리(예: 일반 관리자는 사용자 승인만, 최고 관리자는 권한 부여)가 미흡할 수 있음.
  if (req.method === 'POST' || req.method === 'PUT' || req.method === 'DELETE') {
    if (!adminUser) {
      return res.status(403).json({ detail: '관리자 권한이 필요합니다.' });
    }
  }

  if (req.method === 'GET') {
    if (schedule_id) {
      // 특정 스케줄 조회
      // VULNERABLE: D-11 시스템 테이블 접근 제한 미흡 - RLS가 비활성화된 상태에서 모든 스케줄 정보 접근 가능
      const { data: schedule, error } = await supabase
        .from('schedules')
        .select('*')
        .eq('id', schedule_id)
        .single();

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `스케줄 조회 실패: ${error.message}`, error_details: error });
      }
      if (!schedule) {
        return res.status(404).json({ detail: '스케줄을 찾을 수 없습니다.' });
      }
      return res.status(200).json(schedule);
    } else {
      // 모든 스케줄 조회
      // VULNERABLE: D-11 시스템 테이블 접근 제한 미흡 - RLS가 비활성화된 상태에서 모든 스케줄 정보 접근 가능
      const { data: schedules, error } = await supabase
        .from('schedules')
        .select('*')
        .order('work_date', { ascending: true });

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `스케줄 목록 조회 실패: ${error.message}`, error_details: error });
      }
      return res.status(200).json(schedules);
    }
  }

  if (req.method === 'POST') {
    const { title, description, start_time, end_time, start_time_str, end_time_str, work_date, capacity } = req.body;
    const { data: newSchedule, error } = await supabase
      .from('schedules')
      .insert([
        {
          title,
          description,
          start_time,
          end_time,
          start_time_str,
          end_time_str,
          work_date,
          capacity,
          current_applicants: 0,
        },
      ])
      .select()
      .single();

    if (error) {
      // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
      return res.status(500).json({ detail: `스케줄 생성 실패: ${error.message}`, error_details: error });
    }
    return res.status(201).json(newSchedule);
  }

  if (req.method === 'PUT') {
    const { title, description, start_time, end_time, start_time_str, end_time_str, work_date, capacity } = req.body;
    const { data: updatedSchedule, error } = await supabase
      .from('schedules')
      .update({
        title,
        description,
        start_time,
        end_time,
        start_time_str,
        end_time_str,
        work_date,
        capacity,
      })
      .eq('id', schedule_id)
      .select()
      .single();

    if (error) {
      // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
      return res.status(500).json({ detail: `스케줄 업데이트 실패: ${error.message}`, error_details: error });
    }
    if (!updatedSchedule) {
      return res.status(404).json({ detail: '스케줄을 찾을 수 없습니다.' });
    }
    return res.status(200).json(updatedSchedule);
  }

  if (req.method === 'DELETE') {
    const { error } = await supabase
      .from('schedules')
      .delete()
      .eq('id', schedule_id);

    if (error) {
      // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
      return res.status(500).json({ detail: `스케줄 삭제 실패: ${error.message}`, error_details: error });
    }
    return res.status(204).send();
  }

  res.status(405).json({ detail: 'Method Not Allowed' });
}
