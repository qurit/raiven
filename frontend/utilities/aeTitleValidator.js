export const validateEmpty = v => !!v
export const validateASCII = v => /^[\x00-\x7F]*$/.test(v)
export const validateLength = (v, length) => v.trim().length <= length

export function validateAETitle(v) {
  if (!validateEmpty(v)) return 'Field Cannot be Empty'
  if (!validateASCII(v)) return 'Field Must Only Contain ASCII Characters'
  if (!validateLength(v, 16)) return 'Field must be less then 16 characters'

  return true
}

export default { validateASCII, validateLength, validateEmpty, validateAETitle }
