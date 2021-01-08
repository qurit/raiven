export const validateNotEmpty = v => !!v || 'Field cannot be empty'
export const validateASCII = v => /^[\x00-\x7F]*$/.test(v)
export const validateLength = (v, length) => v.trim().length <= length

export function validateAETitle(v) {
  if (!!v) {
    if (!validateASCII(v)) return 'Field must only contain ASCII characters'
    if (!validateLength(v, 12)) return 'Field must be less than 12 characters'
    return true
  }
}

export default {
  validateASCII,
  validateLength,
  validateNotEmpty,
  validateAETitle
}
