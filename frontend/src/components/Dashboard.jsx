import React from 'react'
import { useAuth } from '../contexts/AuthContext'
import DataViewer from './DataViewer'
import ButtonGroup from './ButtonGroup'
import './Dashboard.css'

const Dashboard = () => {
  const [activeTable, setActiveTable] = React.useState(null)
  const { user, logout, isAdmin, isTeacher } = useAuth()

  const handleTableSelect = (tableName) => {
    setActiveTable(tableName)
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <div>
            <h1>📊 Hệ thống Quản lý Điểm danh</h1>
            <p>Xin chào, <strong>{user?.full_name || user?.username}</strong> ({user?.role})</p>
          </div>
          <button onClick={logout} className="btn-logout">
            Đăng xuất
          </button>
        </div>
      </header>

      <main className="dashboard-main">
        <ButtonGroup 
          onTableSelect={handleTableSelect}
          activeTable={activeTable}
        />
        
        {activeTable && (
          <DataViewer 
            tableName={activeTable}
            onClose={() => setActiveTable(null)}
          />
        )}
      </main>
    </div>
  )
}

export default Dashboard

