<template>
  <div>
    <v-card elevation="6">
      <horizontal-bar
        v-if="loaded"
        :chart-data="datacollection"
        :options="options"
      ></horizontal-bar>
    </v-card>
  </div>
</template>

<script>
import HorizontalBar from './HorizontalBar.js'
import { generic_get } from '~/api'

export default {
  components: {
    HorizontalBar
  },
  data() {
    return {
      // this looks kinda ridiculous
      // modalities taken from: https://wiki.cancerimagingarchive.net/display/Public/DICOM+Modality+Abbreviations
      colors: {
        CR: '#7B241C',
        CT: '#943126',
        MR: '#633974',
        NM: '#5B2C6F',
        US: '#1A5276',
        OT: '#21618C',
        BI: '#117864',
        DG: '#0E6655',
        ES: '#196F3D',
        LS: '#1D8348',
        PT: '#9A7D0A',
        RG: '#9C640C',
        TG: '#935116',
        XA: '#873600',
        RF: '#979A9A',
        RTIMAGE: '#FFA07A',
        RTDOSE: '#F08080',
        RTSTRUCT: '#DC143C',
        RTPLAN: '#B22222',
        RTRECORD: '#8B0000',
        HC: '#FFD700',
        DX: '#FFA500',
        MG: '#FF8C00',
        IO: '#EEE8AA',
        PX: '#BDB76B',
        GM: '#7FFF00',
        SM: '#ADFF2F',
        PR: '#00FF7F',
        AU: '#98FB98',
        ECG: '#3CB371',
        EPS: '	#2E8B57',
        HD: '#808000',
        SR: '#556B2F',
        IVUS: '#6B8E23',
        OP: '#7FFFD4',
        SMR: '#AFEEEE	',
        AR: '#20B2AA',
        KER: '#5F9EA0',
        VA: '#008B8B',
        SRF: '#00BFFF',
        OCT: '#6495ED',
        LEN: '#4682B4',
        OPV: '#4169E1',
        OPM: '#7B68EE',
        OAM: '#483D8B',
        RESP: '#DDA0DD',
        KO: '#BA55D3',
        SEG: '#9370DB',
        REG: '#8A2BE2',
        OPT: '#9932CC',
        BDUS: '#FF69B4',
        BMD: '#DEB887',
        DOC: '#DAA520',
        FID: '#D2691E',
        PLAN: '#8B4513',
        IOL: '#A0522D',
        IVOCT: '#800000'
      },
      loaded: false,
      chartdata: null,
      datacollection: null,
      options: {
        legend: {
          labels: {
            fontColor: 'white'
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
                fontColor: 'white'
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
                fontColor: 'white'
              },
              ticks: {
                fontColor: 'white',
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
          backgroundColor: this.colors[modality[0]],
          data: [(modality[1] / modalitySum) * 100]
        })
      })
      this.fillData(modalityDatasets)
    },
    fillData(modalityDatasets) {
      this.datacollection = {
        labels: ['Modalities'],
        datasets: modalityDatasets
      }
      this.loaded = true
    }
  }
}
</script>
