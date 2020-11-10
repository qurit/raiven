<template>
  <div>
    <v-card elevation="6">
      <bar-chart
        v-if="loaded"
        :chart-data="dataCollection"
        :options="options"
      ></bar-chart>
    </v-card>
  </div>
</template>

<script>
import BarChart from './BarChart.js'
import colours from './colours.js'
import { generic_get } from '~/api'

export default {
  components: {
    BarChart
  },
  data() {
    return {
      loaded: false,
      chartData: null,
      dataCollection: null,
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
              gridLines: {
                display: false
              },
              scaleLabel: {
                display: true,
                labelString: 'Pipeline Runs',
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
              gridLines: {
                display: false
              },
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
    const URL = '/pipeline/runs'
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
            label: 'Pipeline Runs per Day (7-day view)',
            data: Object.values(this.chartData),
            backgroundColor: colours.genericColours.secondary,
            borderColor: colours.genericColours.primary,
            borderWidth: 2
          }
        ]
      }
    }
  }
}
</script>
