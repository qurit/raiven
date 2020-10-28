<template>
  <div class="small">
    <v-card color="white">
      <bar-chart :chart-data="datacollection" :options="options"></bar-chart>
      <button @click="fillData()">Randomize</button>
      <v-btn @click="test"> test</v-btn>
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
      options: {
        scales: {
          yAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: 'Pipeline Runs'
              },
              ticks: {
                beginAtZero: true
              }
            }
          ],
          xAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: 'Date'
              }
            }
          ]
        }
      }
    }
  },
  async mounted() {
    this.fillData()
    this.loaded = false
    const URL = '/pipeline/runs'
    try {
      const test = await generic_get(this, URL)
      this.chartdata = test
      this.loaded = true
    } catch (e) {
      console.log(e)
    }
  },
  methods: {
    test() {
      console.log(this.chartdata)
    },
    fillData() {
      this.datacollection = {
        labels: [
          '2020-09-21',
          '2020-09-22',
          '2020-09-23',
          '2020-09-24',
          '2020-09-25',
          '2020-09-26'
        ],
        datasets: [
          {
            label: 'Pipeline Runs per Day',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            fillColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }
        ]
      }
    },
    getRandomInt() {
      return Math.floor(Math.random() * (50 - 5 + 1)) + 5
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
