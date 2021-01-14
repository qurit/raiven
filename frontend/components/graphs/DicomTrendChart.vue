<template>
  <v-card elevation="6">
    <line-chart :chart-data="dataCollection" :options="options"></line-chart>
  </v-card>
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
      chartData: {},
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
                labelString: 'DICOM Series Received',
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
      this.chartData = await generic_get(this, URL)
      this.fillData()
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
            label: 'Dicom Series Received',
            fill: false,
            borderColor: colours.genericColours.secondary,
            pointBackgroundColor: colours.genericColours.secondary,
            pointBorderColor: colours.genericColours.primary,
            borderWidth: 1,
            lineTension: 0,
            data: Object.values(this.chartData)
          }
        ]
      }
    }
  }
}
</script>
