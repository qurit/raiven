export const rules = [
  {
    type: 'combobox',
    multiple: true,
    tag: 'SeriesDescription',
    matchTypes: ['Any', 'All'],
    items: []
  },
  {
    type: 'select',
    multiple: true,
    tag: 'Modality',
    matchTypes: ['Any', 'All'],
    items: ['MR', 'CT', 'PT']
  },
]
