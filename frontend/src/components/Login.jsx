import React, { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import './Login.css'

const Login = ({ onSwitchToRegister }) => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    const result = await login(username, password)
    setLoading(false)

    if (!result.success) {
      setError(result.error)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Đăng nhập</h2>
        <form onSubmit={handleSubmit}>
          {error && <div className="error-message">{error}</div>}
          
          <div className="form-group">
            <label htmlFor="username">Tên đăng nhập</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              placeholder="Nhập tên đăng nhập"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Mật khẩu</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Nhập mật khẩu"
            />
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Đang đăng nhập...' : 'Đăng nhập'}
          </button>
        </form>

        <div className="auth-switch">
          <p>
            Chưa có tài khoản?{' '}
            <button type="button" onClick={onSwitchToRegister} className="link-button">
              Đăng ký ngay
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Login

