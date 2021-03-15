import { generic_get } from '~/api'

export const send_c_echo = async ({$axios}, node) => {
  const URL = 'dicom/echo'
  await generic_get({$axios}, URL, node)
}



