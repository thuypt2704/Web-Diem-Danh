import React, { createContext, useState, useContext, useEffect } from 'react'
import axios from 'axios'

const AuthContext = createContext()

const API_URL = 'http://localhost:8000'

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [loading, setLoading] = useState(true)

  // Cấu hình axios để tự động thêm token vào header
  axios.defaults.headers.common['Authorization'] = token ? `Bearer ${token}` : ''

  useEffect(() => {
    // Kiểm tra token khi component mount
    if (token) {
      fetchUserInfo()
    } else {
      setLoading(false)
    }
  }, [token])

  const fetchUserInfo = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/auth/me`)
      setUser(response.data)
    } catch (error) {
      console.error('Lỗi lấy thông tin user:', error)
      logout()
    } finally {
      setLoading(false)
    }
  }

  const login = async (username, password) => {
    try {
      const response = await axios.post(`${API_URL}/api/auth/login`, {
        username,
        password
      })
      const { access_token, user } = response.data
      setToken(access_token)
      setUser(user)
      localStorage.setItem('token', access_token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      return { success: true }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Đăng nhập thất bại'
      }
    }
  }

  const register = async (userData) => {
    try {
      const response = await axios.post(`${API_URL}/api/auth/register`, userData)
      return { success: true, data: response.data }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Đăng ký thất bại'
      }
    }
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
  }

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!token && !!user,
    isAdmin: user?.role === 'admin',
    isTeacher: user?.role === 'teacher',
    isStudent: user?.role === 'student'
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

