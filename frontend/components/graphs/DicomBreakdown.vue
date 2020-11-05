<template>
  <div>
    <horizontal-bar
      id="breakdownBar"
      v-if="loaded"
      :chart-data="dataCollection"
      :options="options"
      :height="70"
    ></horizontal-bar>
    {{ dicom_obj_type }}

    <div id="chartjs-tooltip" style="position: absolute; z-index: 99999;">
      <table />
    </div>
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
      loaded: false,
      dataCollection: null,

      options: {
        tooltips: {
          // Disable the on-canvas tooltip
          enabled: false,

          custom: function(tooltipModel) {
            // Tooltip Element
            var tooltipEl = document.getElementById('chartjs-tooltip')

            // Create element on first render
            if (!tooltipEl) {
              tooltipEl = document.createElement('div')
              tooltipEl.id = 'chartjs-tooltip'
              tooltipEl.innerHTML = '<table></table>'
              document.body.appendChild(tooltipEl)
            }

            // Hide if no tooltip
            if (tooltipModel.opacity === 0) {
              tooltipEl.style.opacity = 0
              return
            }

            // Set caret Position
            tooltipEl.classList.remove('above', 'below', 'no-transform')
            if (tooltipModel.yAlign) {
              tooltipEl.classList.add(tooltipModel.yAlign)
            } else {
              tooltipEl.classList.add('no-transform')
            }

            function getBody(bodyItem) {
              return bodyItem.lines
            }
            console.log(tooltipModel)
            // Set Text
            if (tooltipModel.body) {
              var titleLines = tooltipModel.title || []
              var bodyLines = tooltipModel.body.map(getBody)

              var innerHtml = '<thead>'

              titleLines.forEach(function(title) {
                innerHtml += '<tr><th>' + title + '</th></tr>'
              })
              innerHtml += '</thead><tbody>'

              bodyLines.forEach(function(body, i) {
                var colors = 'white'
                var style = 'background:' + 'white'
                style += '; border-color:' + 'white'
                style += '; border-width: 2px'
                var span = '<span style="' + style + '"></span>'
                innerHtml += '<tr><td>' + span + body + '</td></tr>'
              })
              innerHtml += '</tbody>'

              var tableRoot = tooltipEl.querySelector('table')
              tooltipEl.style.opacity = 1
              console.log(tooltipEl)
              tableRoot.innerHTML = innerHtml
            }

            // `this` will be the overall tooltip
            let elem = document.getElementById('breakdownBar')
            console.log(elem)
            var position = elem.getBoundingClientRect()

            // Display, position, and set styles for font
            tooltipEl.style.opacity = 1
            tooltipEl.style.position = 'absolute'
            tooltipEl.style.left = position.left - 100 + 'px'
            console.log(position)
            tooltipEl.style.top = position.top + 'px'
            tooltipEl.style.fontFamily = tooltipModel._bodyFontFamily
            tooltipEl.style.fontSize = '50px'
            tooltipEl.style.fontStyle = tooltipModel._bodyFontStyle
            tooltipEl.style.pointerEvents = 'none'
          }
        },
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
        // tooltips: {
        //   yAlign: 'center'
        // },
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
  computed: {
    dicomNodeChange() {
      return [this.dicom_obj_id, this.dicom_obj_type].join()
    }
  },
  watch: {
    dicomNodeChange() {
      this.getData()
    }
  },
  async created() {
    if (this.dicom_obj_type && this.dicom_obj_id) {
      this.getData()
    }
  },
  methods: {
    async getData() {
      if (this.dicom_obj_type !== 'Series') {
        const URL = `/dicom/series-breakdown/${this.dicom_obj_type}/${this.dicom_obj_id}`
        try {
          this.loaded = false
          const modalityData = await generic_get(this, URL)
          this.makeDatasets(modalityData)
        } catch (e) {
          console.log(e)
        }
      }
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
