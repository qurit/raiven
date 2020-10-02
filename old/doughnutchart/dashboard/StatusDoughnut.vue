<template>
  <v-card max-width="300" max-height="300" loading>
    <v-row
      class="display-1 text-center mt-4"
      style="position: absolute; width: 100%"
      justify="center"
      v-text="title"
      no-gutters
    />
    <v-card-text>
      <DougnutChart :chart-data="chartData" :options="chartOptions" />
    </v-card-text>
    <v-card-actions style="position: absolute; bottom: 0; right: 0; left: 0;">
      <v-btn class="px-10 mx-auto" outlined v-text="'Refresh'" />
    </v-card-actions>
  </v-card>
</template>

<script>
import DougnutChart from "../charts/DougnutChart";

export default {
  name: "StatusDoughnut",
  components: {DougnutChart},
  data: () => ({
    title: 'AE Status',
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
      // legend: { position: 'bottom'},
      legend: false
    }
  })
}
</script>
