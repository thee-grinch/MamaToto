// src/utils/validation.js
export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

export const validatePassword = (password) => {
  return password.length >= 6
}

export const validatePhone = (phone) => {
  const re = /^[\+]?[0-9\s\-\(\)]{10,}$/
  return re.test(phone.replace(/\s/g, ''))
}

export const validateDate = (date) => {
  const d = new Date(date)
  return d instanceof Date && !isNaN(d)
}

export const validateWeight = (weight) => {
  const w = parseFloat(weight)
  return !isNaN(w) && w > 0 && w < 200 // kg
}

export const validateHeight = (height) => {
  const h = parseFloat(height)
  return !isNaN(h) && h > 0 && h < 300 // cm
}