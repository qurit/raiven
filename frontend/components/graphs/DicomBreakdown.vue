<template>
  <div>
    <v-card elevation="6">
      <horizontal-bar
        v-if="loaded"
        :chart-data="dataCollection"
        :options="options"
      ></horizontal-bar>
    </v-card>
  </div>
</template>

<script>
import HorizontalBar from './HorizontalBar.js'
import colours from './colours.js'
import { generic_get } from '~/api'

export default {
  components: {
    HorizontalBar
  },
  data() {
    return {
      loaded: false,
      dataCollection: null,
      options: {
        legend: {
          labels: {
            fontColor: colours.genericColours.labels
          }
        },
        layout: {
          padding: {
            right: 20
          }
        },
        scales: {
          yAxes: [
            {
              ticks: {
                fontColor: colours.genericColours.labels
              },
              stacked: true
            }
          ],
          xAxes: [
            {
              gridLines: {
                display: false
              },
              scaleLabel: {
                display: true,
                labelString: 'Percentage of all Modalities Received',
                fontColor: colours.genericColours.labels
              },
              ticks: {
                fontColor: colours.genericColours.labels,
                min: 0,
                max: 100,
                stepSize: 5
              },
              stacked: true
            }
          ]
        }
      }
    }
  },
  async mounted() {
    const URL = '/dicom/series-breakdown'
    try {
      this.loaded = false
      const modalityData = await generic_get(this, URL)
      this.makeDatasets(modalityData)
    } catch (e) {
      console.log(e)
    }
  },
  methods: {
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
          data: [(modality[1] / modalitySum) * 100]
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
