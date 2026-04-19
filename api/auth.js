import { createClient } from '@supabase/supabase-js';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';

dotenv.config();

// VULNERABLE: D-01 기본 계정 보안 미흡 - service_role 키를 클라이언트 사이드에서 사용하거나 노출
// 실제 환경에서는 절대 이렇게 사용하면 안 됩니다. RLS가 활성화된 상태에서 사용자 권한으로만 접근해야 합니다.
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_ANON_KEY; // 또는 심지어 service_role 키를 여기에 사용
const supabase = createClient(supabaseUrl, supabaseKey);

const JWT_SECRET = process.env.JWT_SECRET || 'super-secret-jwt-key';
const ACCESS_TOKEN_EXPIRE_MINUTES = 60;

// VULNERABLE: WEB-02 비밀번호 복잡성 미준수 - 매우 약한 비밀번호 정책
// 실제로는 강력한 비밀번호 정책(길이, 특수문자, 숫자 포함 등)을 강제해야 합니다.
const isPasswordStrong = (password) => {
  return password.length >= 4; // 의도적으로 매우 약한 정책 적용
};

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { path } = req.query;

    if (path === 'register') {
      const { phone_number, password } = req.body;

      if (!isPasswordStrong(password)) {
        return res.status(400).json({ detail: '비밀번호가 너무 약합니다. (WEB-02)' });
      }

      const { data: existingUser, error: userError } = await supabase
        .from('users')
        .select('id')
        .eq('phone_number', phone_number)
        .single();

      if (existingUser) {
        return res.status(400).json({ detail: '이미 등록된 전화번호입니다.' });
      }

      const hashedPassword = await bcrypt.hash(password, 10);

      const { data: newUser, error } = await supabase
        .from('users')
        .insert([
          {
            phone_number,
            hashed_password: hashedPassword,
            status: 'pending',
            role: 'user',
          },
        ])
        .select()
        .single();

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `회원가입 실패: ${error.message}`, error_details: error });
      }

      return res.status(201).json(newUser);
    }

    if (path === 'login') {
      const { phone_number, password } = req.body;

      const { data: user, error } = await supabase
        .from('users')
        .select('*')
        .eq('phone_number', phone_number)
        .single();

      if (error || !user) {
        return res.status(404).json({ detail: '사용자를 찾을 수 없습니다.' });
      }

      const passwordMatch = await bcrypt.compare(password, user.hashed_password);

      if (!passwordMatch) {
        return res.status(400).json({ detail: '비밀번호가 일치하지 않습니다.' });
      }

      if (user.status !== 'approved') {
        return res.status(403).json({ detail: '관리자 승인이 필요합니다.' });
      }

      const token = jwt.sign({ id: user.id, role: user.role }, JWT_SECRET, { expiresIn: `${ACCESS_TOKEN_EXPIRE_MINUTES}m` });

      return res.status(200).json({ access_token: token, token_type: 'bearer' });
    }

    if (path === 'super-admin-login') {
      const { username, password } = req.body;

      const { data: user, error } = await supabase
        .from('users')
        .select('*')
        .eq('username', username)
        .in('role', ['admin', 'super_admin'])
        .single();

      if (error || !user) {
        return res.status(404).json({ detail: '관리자 계정을 찾을 수 없습니다.' });
      }

      const passwordMatch = await bcrypt.compare(password, user.hashed_password);

      if (!passwordMatch) {
        return res.status(400).json({ detail: '비밀번호가 일치하지 않습니다.' });
      }

      const token = jwt.sign({ id: user.id, role: user.role }, JWT_SECRET, { expiresIn: `${ACCESS_TOKEN_EXPIRE_MINUTES}m` });

      return res.status(200).json({ access_token: token, token_type: 'bearer' });
    }

    if (path === 'change-password') {
      const authHeader = req.headers.authorization;
      if (!authHeader) {
        return res.status(401).json({ detail: '인증 토큰이 필요합니다.' });
      }
      const token = authHeader.split(' ')[1];
      let decodedToken;
      try {
        decodedToken = jwt.verify(token, JWT_SECRET);
      } catch (e) {
        return res.status(401).json({ detail: '유효하지 않은 토큰입니다.' });
      }

      const { old_password, new_password } = req.body;

      const { data: currentUser, error: userError } = await supabase
        .from('users')
        .select('*')
        .eq('id', decodedToken.id)
        .single();

      if (userError || !currentUser) {
        return res.status(404).json({ detail: '사용자를 찾을 수 없습니다.' });
      }

      const oldPasswordMatch = await bcrypt.compare(old_password, currentUser.hashed_password);
      if (!oldPasswordMatch) {
        return res.status(400).json({ detail: '기존 비밀번호가 일치하지 않습니다.' });
      }

      if (!isPasswordStrong(new_password)) {
        return res.status(400).json({ detail: '새 비밀번호가 너무 약합니다. (WEB-02)' });
      }

      const newHashedPassword = await bcrypt.hash(new_password, 10);

      const { data, error } = await supabase
        .from('users')
        .update({ hashed_password: newHashedPassword })
        .eq('id', currentUser.id)
        .select()
        .single();

      if (error) {
        // VULNERABLE: WEB-22 에러 페이지 관리 미흡 - 상세 에러 메시지 노출
        return res.status(500).json({ detail: `비밀번호 변경 실패: ${error.message}`, error_details: error });
      }

      return res.status(200).json({ message: '비밀번호가 성공적으로 변경되었습니다.' });
    }
  }

  res.status(405).json({ detail: 'Method Not Allowed' });
}
