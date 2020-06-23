import { helpers } from 'vuelidate/lib/validators'
export const finite = (value) => !helpers.req(value) || isFinite(value)

export default ({ app }, inject) => {
  inject('validator', {
    getErrors(field, $v) {
      console.log(field, $v)
      return errorMsg($v[field])
    },
  })
}

// export function handleErrors(field, $v) {
//   return errorMsg($v[field])
// }

function errorMsg(f) {
  const errors = []
  if (!f.$dirty) return errors
  if ('required' in f && !f.required) errors.push('Required.')
  if ('integer' in f && !f.integer) errors.push('Not an integer.')
  if ('alpha' in f && !f.alpha) errors.push('Not a String')
  if ('decimal' in f && !f.decimal) errors.push('Not a number.')
  if ('finite' in f && !f.finite) errors.push('Not a number.')
  if ('maxLength' in f && !f.maxLength) errors.push('Exceeds Max Length.')
  if ('minValue' in f && !f.minValue) errors.push('Too Small')
  if ('ipAddress' in f && !f.ipAddress) errors.push('Not a IP Address')
  return errors
}
