import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './DataViewer.css'

const DataViewer = ({ tableName, onClose }) => {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedItem, setSelectedItem] = useState(null)

  const API_URL = 'http://localhost:8000'
  
  const endpoints = {
    teachers: '/api/teachers',
    classes: '/api/classes',
    students: '/api/students',
  }

  useEffect(() => {
    fetchData()
  }, [tableName])

  const fetchData = async () => {
    setLoading(true)
    setError(null)
    try {
      const endpoint = endpoints[tableName]
      if (!endpoint) {
        setError('Bảng không hợp lệ')
        setLoading(false)
        return
      }
      const response = await axios.get(`${API_URL}${endpoint}`)
      setData(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Lỗi khi tải dữ liệu')
      console.error('Error fetching data:', err)
    } finally {
      setLoading(false)
    }
  }

  const formatValue = (value) => {
    if (value === null || value === undefined) return '-'
    if (typeof value === 'boolean') return value ? 'Có' : 'Không'
    if (value instanceof Date || (typeof value === 'string' && value.includes('T'))) {
      return new Date(value).toLocaleString('vi-VN')
    }
    if (typeof value === 'object') return JSON.stringify(value, null, 2)
    return String(value)
  }

  const getTableHeaders = () => {
    if (data.length === 0) return []
    return Object.keys(data[0])
  }

  if (loading) {
    return (
      <div className="data-viewer">
        <div className="loading">Đang tải dữ liệu...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="data-viewer">
        <div className="error">
          <p>❌ Lỗi: {error}</p>
          <button onClick={fetchData}>Thử lại</button>
        </div>
      </div>
    )
  }

  const headers = getTableHeaders()

  return (
    <div className="data-viewer">
      <div className="viewer-header">
        <h2>
          {tableName === 'teachers' && '👨‍🏫 Giáo viên'}
          {tableName === 'classes' && '📚 Lớp học'}
          {tableName === 'students' && '👨‍🎓 Học sinh'}
        </h2>
        <div className="header-actions">
          <span className="count">Tổng: {data.length} bản ghi</span>
          <button onClick={fetchData} className="refresh-btn">🔄 Làm mới</button>
          <button onClick={onClose} className="close-btn">✕ Đóng</button>
        </div>
      </div>

      {data.length === 0 ? (
        <div className="empty-state">
          <p>Không có dữ liệu</p>
        </div>
      ) : (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                {headers.map((header) => (
                  <th key={header}>{header}</th>
                ))}
                <th>Thao tác</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row, index) => (
                <tr key={index}>
                  {headers.map((header) => (
                    <td key={header} className={header.includes('id') ? 'id-cell' : ''}>
                      {formatValue(row[header])}
                    </td>
                  ))}
                  <td>
                    <button
                      className="detail-btn"
                      onClick={() => setSelectedItem(row)}
                    >
                      Chi tiết
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedItem && (
        <div className="modal-overlay" onClick={() => setSelectedItem(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Chi tiết</h3>
              <button onClick={() => setSelectedItem(null)} className="modal-close">✕</button>
            </div>
            <div className="modal-body">
              {Object.entries(selectedItem).map(([key, value]) => (
                <div key={key} className="detail-row">
                  <strong>{key}:</strong>
                  <span>{formatValue(value)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default DataViewer

