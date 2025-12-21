import React from 'react'
import './ButtonGroup.css'

const ButtonGroup = ({ onTableSelect, activeTable }) => {
  const tables = [
    { name: 'teachers', label: '👨‍🏫 Giáo viên', endpoint: '/api/teachers' },
    { name: 'classes', label: '📚 Lớp học', endpoint: '/api/classes' },
    { name: 'students', label: '👨‍🎓 Học sinh', endpoint: '/api/students' },
  ]

  return (
    <div className="button-group">
      <h2>Chọn bảng để xem</h2>
      <div className="buttons-grid">
        {tables.map((table) => (
          <button
            key={table.name}
            className={`table-button ${activeTable === table.name ? 'active' : ''}`}
            onClick={() => onTableSelect(table.name)}
          >
            {table.label}
          </button>
        ))}
      </div>
    </div>
  )
}

export default ButtonGroup

