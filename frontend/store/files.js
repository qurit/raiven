export const state = () => ({
  files: [
    {
      name: 'dicom store event 1',
      date: '09/09/2020',
      host: '68.89.31.226',
      port: '100'
    },
    {
      name: 'dicom store event 2',
      date: '09/12/2020',
      host: '70.10.13.289',
      port: '101'
    },
    {
      name: 'dicom store event 3',
      date: '09/15/2020',
      host: '11.10.50.199',
      port: '106'
    },
    {
      name: 'dicom store event 4',
      date: '09/18/2020',
      host: '36.23.90.869',
      port: '110'
    }
  ]
})

export const mutations = {
  get(state) {
    state.files
  }
}
