// src/utils/constants.js
export const GENDER_OPTIONS = [
  { value: 'male', label: 'Male' },
  { value: 'female', label: 'Female' },
  { value: 'other', label: 'Other' }
]

export const LANGUAGE_OPTIONS = [
  { value: 'en', label: 'English' },
  { value: 'sw', label: 'Kiswahili' }
]

export const APPOINTMENT_TYPES = [
  { value: 'anc', label: 'Antenatal Care' },
  { value: 'ultrasound', label: 'Ultrasound' },
  { value: 'specialist', label: 'Specialist' },
  { value: 'lab', label: 'Laboratory Test' },
  { value: 'checkup', label: 'General Checkup' }
]

export const HEALTH_RECORD_TYPES = [
  { value: 'symptom', label: 'Symptom' },
  { value: 'medication', label: 'Medication' },
  { value: 'test_result', label: 'Test Result' },
  { value: 'general', label: 'General Note' }
]

export const SEVERITY_LEVELS = [
  { value: 'low', label: 'Low', color: 'green' },
  { value: 'medium', label: 'Medium', color: 'yellow' },
  { value: 'high', label: 'High', color: 'orange' },
  { value: 'critical', label: 'Critical', color: 'red' }
]

export const VACCINATION_STATUS = [
  { value: 'pending', label: 'Pending', color: 'gray' },
  { value: 'due', label: 'Due', color: 'yellow' },
  { value: 'overdue', label: 'Overdue', color: 'red' },
  { value: 'completed', label: 'Completed', color: 'green' },
  { value: 'skipped', label: 'Skipped', color: 'orange' }
]