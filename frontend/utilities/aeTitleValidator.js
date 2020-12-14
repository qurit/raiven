export function validateASCII(value) {
  if (!!value) {
    return /^[\x00-\x7F]*$/.test(value) || 'ASCII Characters only'
  }
}

export function validateLength(value) {
  if (!!value) {
    return (
      value.trim().length <= 16 || 'AE Title is too long, 16 characters max'
    )
  }
}

export default { validateASCII, validateLength }
