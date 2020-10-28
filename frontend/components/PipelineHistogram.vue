<template>
  <div class="small">
    <v-card elevation="6">
      <bar-chart
        v-if="loaded"
        :chart-data="datacollection"
        :options="options"
      ></bar-chart>
    </v-card>
  </div>
</template>

<script>
import BarChart from './BarChart.js'
import { generic_get } from '~/api'

export default {
  components: {
    BarChart
  },
  data() {
    return {
      loaded: false,
      chartdata: null,
      datacollection: null,
      maxYAxis: 0,
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
              gridLines: {
                display: false
              },
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
    const URL = '/pipeline/runs'
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
            label: 'Pipeline Runs per Day (7-day view)',
            data: Object.values(this.chartdata),
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            fillColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }
        ]
      }
    }
  }
}
</script>

<style>
.small {
  max-width: 600px;
  margin: 150px auto;
}
</style>
