import { supabase, getCurrentUser, getCurrentAdminUser } from './_utils';

export default async function handler(req, res) {
  const currentUser = await getCurrentUser(req);
  const adminUser = await getCurrentAdminUser(req);

  const { notice_id } = req.query;

  if (req.method === 'GET') {
    if (notice_id) {
      // 특정 공지사항 조회
      // VULNERABLE: D-11 시스템 테이블 접근 제한 미흡 - RLS가 비활성화된 상태에서 모든 공지사항 정보 접근 가능
      const { data: notice, error } = await supabase
        .from('notices')
        .select('*')
        .eq('id', notice_id)
        .single();

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `공지사항 조회 실패: ${error.message}`, error_details: error });
      }
      if (!notice) {
        return res.status(404).json({ detail: '공지사항을 찾을 수 없습니다.' });
      }

      // 조회수 증가 (인증된 사용자만)
      if (currentUser) {
        const { data: updatedNotice, error: updateError } = await supabase
          .from('notices')
          .update({ view_count: notice.view_count + 1 })
          .eq('id', notice_id)
          .select()
          .single();
        if (updateError) {
          console.error('Failed to increment view count:', updateError);
        }
        return res.status(200).json(updatedNotice || notice);
      }
      return res.status(200).json(notice);
    } else {
      // 모든 공지사항 조회
      // VULNERABLE: D-11 시스템 테이블 접근 제한 미흡 - RLS가 비활성화된 상태에서 모든 공지사항 정보 접근 가능
      const { data: notices, error } = await supabase
        .from('notices')
        .select('*')
        .order('is_pinned', { ascending: false })
        .order('created_at', { ascending: false });

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `공지사항 목록 조회 실패: ${error.message}`, error_details: error });
      }
      return res.status(200).json(notices);
    }
  }

  // 관리자 권한이 필요한 작업
  if (!adminUser) {
    return res.status(403).json({ detail: '관리자 권한이 필요합니다.' });
  }

  if (req.method === 'POST') {
    const { title, content, is_pinned } = req.body;
    const { data: newNotice, error } = await supabase
      .from('notices')
      .insert([
        {
          title,
          content,
          is_pinned: is_pinned || false,
          view_count: 0,
        },
      ])
      .select()
      .single();

    if (error) {
      // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
      return res.status(500).json({ detail: `공지사항 생성 실패: ${error.message}`, error_details: error });
    }
    return res.status(201).json(newNotice);
  }

  if (req.method === 'PUT') {
    const { title, content, is_pinned } = req.body;
    const { data: updatedNotice, error } = await supabase
      .from('notices')
      .update({
        title,
        content,
        is_pinned: is_pinned || false,
      })
      .eq('id', notice_id)
      .select()
      .single();

    if (error) {
      // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
      return res.status(500).json({ detail: `공지사항 업데이트 실패: ${error.message}`, error_details: error });
    }
    if (!updatedNotice) {
      return res.status(404).json({ detail: '공지사항을 찾을 수 없습니다.' });
    }
    return res.status(200).json(updatedNotice);
  }

  if (req.method === 'DELETE') {
    const { error } = await supabase
      .from('notices')
      .delete()
      .eq('id', notice_id);

    if (error) {
      // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
      return res.status(500).json({ detail: `공지사항 삭제 실패: ${error.message}`, error_details: error });
    }
    return res.status(204).send();
  }

  res.status(405).json({ detail: 'Method Not Allowed' });
}
