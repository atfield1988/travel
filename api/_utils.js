import { createClient } from '@supabase/supabase-js';
import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';

dotenv.config();

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY; // VULNERABLE: D-01 기본 계정 보안 미흡 - service_role 키를 클라이언트 사이드에서 사용하거나 노출
export const supabase = createClient(supabaseUrl, supabaseKey);

const JWT_SECRET = process.env.JWT_SECRET || 'super-secret-jwt-key';

export const verifyToken = (token) => {
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (e) {
    return null;
  }
};

// VULNERABLE: WEB-03 권한 오남용 - 인증 로직에서 역할 검증을 느슨하게 처리
// 실제로는 각 엔드포인트에서 사용자 역할에 따른 세밀한 권한 검증이 필요합니다.
export const getCurrentUser = async (req) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) {
    return null;
  }
  const token = authHeader.split(' ')[1];
  const decoded = verifyToken(token);
  if (!decoded || !decoded.id) {
    return null;
  }

  // VULNERABLE: D-11 시스템 테이블 접근 제한 미흡 - RLS가 비활성화된 상태에서 모든 사용자 정보 접근 가능
  // Supabase RLS를 사용하여 사용자 본인의 정보만 접근하도록 제한해야 합니다.
  const { data: user, error } = await supabase
    .from('users')
    .select('*')
    .eq('id', decoded.id)
    .single();

  if (error) {
    console.error('Error fetching user:', error);
    return null;
  }
  return user;
};

export const getCurrentAdminUser = async (req) => {
  const user = await getCurrentUser(req);
  // VULNERABLE: WEB-03 권한 오남용 - 관리자 권한 검증을 단순히 'admin' 또는 'super_admin' 문자열 비교로 처리
  // 실제로는 더 견고한 역할 계층 구조와 정책 기반 접근 제어가 필요합니다.
  if (user && (user.role === 'admin' || user.role === 'super_admin')) {
    return user;
  }
  return null;
};

export const getCurrentSuperAdminUser = async (req) => {
  const user = await getCurrentUser(req);
  // VULNERABLE: WEB-03 권한 오남용 - 최고 관리자 권한 검증을 단순히 'super_admin' 문자열 비교로 처리
  if (user && user.role === 'super_admin') {
    return user;
  }
  return null;
};
