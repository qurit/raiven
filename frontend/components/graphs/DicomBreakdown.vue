<template>
  <div>
    <horizontal-bar
      v-if="loaded"
      :chart-data="dataCollection"
      :options="options"
      :height="70"
    ></horizontal-bar>
    {{ dicom_obj_type }}
  </div>
</template>

<script>
import HorizontalBar from './HorizontalBar.js'
import colours from './colours.js'
import { generic_get } from '~/api'

export default {
  props: ['dicom_obj_type', 'dicom_obj_id'],
  components: {
    HorizontalBar
  },
  data() {
    return {
      breakdownData: [],
      loaded: false,
      dataCollection: null,
      options: {
        layout: {
          padding: {
            left: -20
          }
        },
        maintainAspectRatio: false,
        responsive: true,
        legend: {
          labels: {
            fontColor: colours.genericColours.labels
          }
        },
        tooltips: {
          yAlign: 'center'
        },
        scales: {
          yAxes: [
            {
              gridLines: {
                display: false,
                drawBorder: false
              },
              maxBarThickness: 10,
              ticks: {
                display: false,
                fontColor: colours.genericColours.labels
              },
              stacked: true
            }
          ],
          xAxes: [
            {
              gridLines: {
                display: false,
                drawBorder: false
              },
              scaleLabel: {
                display: false,
                labelString: 'Percentage of all Modalities Received',
                fontColor: colours.genericColours.labels
              },
              ticks: {
                display: false,
                fontColor: colours.genericColours.labels
              },
              stacked: true
            }
          ]
        }
      }
    }
  },
  watch: {
    dicom_obj_id: {
      handler: function() {
        console.log('asfasdf')
        this.getData()
      }
    }
  },
  // async updated() {
  //   console.log(this.dicom_obj_id)
  //   console.log(this.dicom_obj_type)
  //   const URL = '/dicom/series-breakdown'
  //   try {
  //     this.loaded = false
  //     // const modalityData = await generic_get(this, URL)
  //     console.log(modalityData)
  //     // this.breakdownData = modalityData
  //     this.makeListData(modalityData)
  //     this.makeDatasets(modalityData)
  //   } catch (e) {
  //     console.log(e)
  //   }
  // },
  async created() {
    console.log('sdfsdf')
    const URL = `/dicom/series-breakdown/${this.dicom_obj_type}/${this.dicom_obj_id}`
    try {
      this.loaded = false
      const modalityData = await generic_get(this, URL)
      console.log(modalityData)
      this.breakdownData = modalityData
      this.makeListData(modalityData)
      this.makeDatasets(modalityData)
    } catch (e) {
      console.log(e)
    }
  },
  methods: {
    getData() {
      console.log(this.dicom_obj_id)
      console.log(this.dicom_obj_type)
    },
    makeListData(modalityData) {
      Object.entries(modalityData).forEach(data => {
        const dicomSeries = {
          modality: data[0],
          count: data[1]
        }
        // this.breakdownData.push(dicomSeries)
      })
      console.log(this.breakdownData)
    },
    makeDatasets(modalityData) {
      const modalityDatasets = []
      const entries = Object.entries(modalityData)
      entries.sort((a, b) => {
        return b[1] - a[1]
      })
      const modalitySum = Object.values(modalityData).reduce((a, b) => a + b, 0)
      entries.forEach(modality => {
        modalityDatasets.push({
          label: modality[0],
          backgroundColor: colours.dicomBreakdownColours[modality[0]],
          data: [Math.round((modality[1] / modalitySum) * 100)]
        })
      })
      this.fillData(modalityDatasets)
    },
    fillData(modalityDatasets) {
      this.dataCollection = {
        labels: ['Modalities'],
        datasets: modalityDatasets
      }
      this.loaded = true
    }
  }
}
</script>
