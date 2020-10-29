<template>
  <div>
    <v-card elevation="6">
      <line-chart
        v-if="loaded"
        :chart-data="datacollection"
        :options="options"
      ></line-chart>
    </v-card>
  </div>
</template>

<script>
import LineChart from './LineChart.js'
import { generic_get } from '~/api'

export default {
  components: {
    LineChart
  },
  data() {
    return {
      datacollection: null,
      loaded: false,
      chartdata: null,
      options: {
        legend: {
          labels: {
            fontColor: 'white'
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
                fontColor: 'white'
              },
              ticks: {
                beginAtZero: true,
                stepSize: 1,
                fontColor: 'white'
              }
            }
          ],
          xAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: 'Date',
                fontColor: 'white'
              },
              ticks: {
                fontColor: 'white'
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
      this.chartdata = await generic_get(this, URL)
      this.fillData()
      this.loaded = true
    } catch (e) {
      console.log(e)
    }
  },
  methods: {
    fillData() {
      this.datacollection = {
        labels: Object.keys(this.chartdata),
        datasets: [
          {
            label: 'Dicom Instances',
            // maybe fill? not sure
            fill: false,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'grey',
            pointBackgroundColor: '#249EBF',
            pointBorderColor: '#249EBF',
            borderWidth: 1,
            // not sure if this looks too "rigid", but default tension looked kinda weird
            lineTension: 0,
            borderWidth: 4,
            data: Object.values(this.chartdata)
          }
        ]
      }
    }
  }
}
</script>
