import React from 'react'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import AuthPage from './components/AuthPage'
import Dashboard from './components/Dashboard'
import ProtectedRoute from './components/ProtectedRoute'
import './App.css'

const AppContent = () => {
  const { isAuthenticated, loading } = useAuth()

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        <div>Đang tải...</div>
      </div>
    )
  }

  return (
    <>
      {isAuthenticated ? (
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      ) : (
        <AuthPage />
      )}
    </>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App
