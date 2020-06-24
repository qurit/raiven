<template>

  <v-card max-width="300">
    <v-card-title style="position: absolute;">
        AE Status</v-card-title>
    <v-card-text style="max-height: 200px">
      <DougnutChart :chart-data="chartData" :options="chartOptions" />
    </v-card-text>
    <v-card-text class="text-center">
      <v-btn class="px-10" outlined v-text="'Refresh'" />
    </v-card-text>
  </v-card>
</template>

<script>
import DougnutChart from "../charts/DougnutChart";

export default {
  name: "StatusDoughnut",
  components: {DougnutChart},
  data: () => ({
    chartData: {
      datasets: [{
        data: [50, 20],
        backgroundColor: ["#1EB980", "#FF6859"],
        borderWidth: 0
      }],

      // These labels appear in the legend and in the tooltips when hovering different arcs
      labels: [
          'Up',
          'Down',
          'Unknown'
      ]
    },
    chartOptions: {
      rotation: Math.PI,
      circumference: Math.PI,
      responsive: true,
      legend: false,
    }
  })
}
</script>
