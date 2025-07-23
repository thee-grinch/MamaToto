// src/utils/dates.js
export const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

export const formatDateTime = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

export const calculateAge = (birthDate) => {
  const today = new Date()
  const birth = new Date(birthDate)
  
  let years = today.getFullYear() - birth.getFullYear()
  let months = today.getMonth() - birth.getMonth()
  
  if (months < 0) {
    years--
    months += 12
  }
  
  if (years === 0) {
    return `${months} months`
  } else if (years === 1) {
    return months === 0 ? '1 year' : `1 year ${months} months`
  } else {
    return months === 0 ? `${years} years` : `${years} years ${months} months`
  }
}

export const calculatePregnancyWeeks = (dueDate) => {
  const due = new Date(dueDate)
  const today = new Date()
  const daysRemaining = Math.ceil((due - today) / (1000 * 60 * 60 * 24))
  const weeksRemaining = Math.max(0, Math.floor(daysRemaining / 7))
  const totalWeeks = 40
  const currentWeek = Math.max(1, totalWeeks - weeksRemaining)
  
  return {
    currentWeek: Math.min(42, currentWeek),
    weeksRemaining,
    daysRemaining: Math.max(0, daysRemaining)
  }
}

export const getTrimester = (week) => {
  if (week <= 12) return 1
  if (week <= 27) return 2
  return 3
}
