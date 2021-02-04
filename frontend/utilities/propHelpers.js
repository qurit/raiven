export function toPropFormat(stringsProps, value = true) {
  const obj = {}
  stringsProps.forEach(s => obj[s] = value)
  return obj
}
