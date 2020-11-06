<template>
  <div>
    <v-card elevation="6">
      <line-chart
        v-if="loaded"
        :chart-data="dataCollection"
        :options="options"
      ></line-chart>
    </v-card>
  </div>
</template>

<script>
import LineChart from './LineChart.js'
import colours from './colours.js'
import { generic_get } from '~/api'

export default {
  components: {
    LineChart
  },
  data() {
    return {
      dataCollection: null,
      loaded: false,
      chartData: null,
      options: {
        legend: {
          labels: {
            fontColor: colours.genericColours.labels
          }
        },
        layout: {
          padding: {
            top: 10
          }
        },
        scales: {
          yAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: 'DICOM Instances Received',
                fontColor: colours.genericColours.labels
              },
              ticks: {
                beginAtZero: true,
                stepSize: 1,
                fontColor: colours.genericColours.labels
              }
            }
          ],
          xAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: 'Date',
                fontColor: colours.genericColours.labels
              },
              ticks: {
                fontColor: colours.genericColours.labels
              }
            }
          ]
        }
      }
    }
  },
  async mounted() {
    const URL = '/dicom/received-series'
    try {
      this.loaded = false
      this.chartData = await generic_get(this, URL)
      this.fillData()
      this.loaded = true
    } catch (e) {
      console.log(e)
    }
  },
  methods: {
    fillData() {
      this.dataCollection = {
        labels: Object.keys(this.chartData),
        datasets: [
          {
            label: 'Dicom Instances Received',
            fill: false,
            borderColor: colours.genericColours.line,
            pointBackgroundColor: colours.genericColours.babyBlue,
            pointBorderColor: colours.genericColours.babyBlue,
            borderWidth: 1,
            lineTension: 0,
            borderWidth: 4,
            data: Object.values(this.chartData)
          }
        ]
      }
    }
  }
}
</script>
