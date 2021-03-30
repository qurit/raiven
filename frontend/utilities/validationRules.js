export const validateNotEmpty = v => !!v || 'Field cannot be empty'
export const validateASCII = v => /^[\x00-\x7F]*$/.test(v)
export const validateLength = (v, length) => v.trim().length <= length
export const validateDomain = v =>
  /(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]/.test(
    v
  )
export const validateIP = v =>
  /\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\b/.test(
    v
  )
export const validatePort = v =>
  /^([1-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5])$/.test(
    v
  ) || 'Field is not a valid port'

export function validateAETitle(v) {
  if (!!v) {
    if (!validateASCII(v)) return 'Field must only contain ASCII characters'
    if (!validateLength(v, 12)) return 'Field must be less than 12 characters'
    return true
  } else return false
}

export function validateHostAddress(v) {
  if (!!v) {
    if (!validateDomain(v) && !validateIP(v))
      return 'Field is not a valid host address'
    return true
  }
  return validateNotEmpty(v)
}

export default {
  validateASCII,
  validateLength,
  validateNotEmpty,
  validateAETitle,
  validateHostAddress,
  validatePort
}
