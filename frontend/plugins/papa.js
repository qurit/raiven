import * as Papa from 'papaparse'

export default ({ app }, inject) => {
  inject('papa', Papa)
}
