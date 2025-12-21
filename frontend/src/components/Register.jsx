import React, { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import './Login.css'

const Register = ({ onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    role: 'student'
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError('Mật khẩu xác nhận không khớp')
      return
    }

    if (formData.password.length < 6) {
      setError('Mật khẩu phải có ít nhất 6 ký tự')
      return
    }

    setLoading(true)

    const { confirmPassword, ...registerData } = formData
    const result = await register(registerData)
    setLoading(false)

    if (!result.success) {
      setError(result.error)
    } else {
      // Đăng ký thành công, chuyển sang màn hình đăng nhập
      alert('Đăng ký thành công! Vui lòng đăng nhập.')
      onSwitchToLogin()
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Đăng ký</h2>
        <form onSubmit={handleSubmit}>
          {error && <div className="error-message">{error}</div>}
          
          <div className="form-group">
            <label htmlFor="username">Tên đăng nhập</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              placeholder="Nhập tên đăng nhập"
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="Nhập email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="full_name">Họ và tên</label>
            <input
              type="text"
              id="full_name"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              placeholder="Nhập họ và tên (tùy chọn)"
            />
          </div>

          <div className="form-group">
            <label htmlFor="role">Vai trò</label>
            <select
              id="role"
              name="role"
              value={formData.role}
              onChange={handleChange}
              className="form-group input"
              style={{ padding: '12px', border: '2px solid #e0e0e0', borderRadius: '8px', width: '100%' }}
            >
              <option value="student">Học sinh</option>
              <option value="teacher">Giáo viên</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="password">Mật khẩu</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Nhập mật khẩu (tối thiểu 6 ký tự)"
              minLength={6}
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Xác nhận mật khẩu</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              placeholder="Nhập lại mật khẩu"
            />
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Đang đăng ký...' : 'Đăng ký'}
          </button>
        </form>

        <div className="auth-switch">
          <p>
            Đã có tài khoản?{' '}
            <button type="button" onClick={onSwitchToLogin} className="link-button">
              Đăng nhập ngay
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Register

