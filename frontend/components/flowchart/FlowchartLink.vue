<template>
  <v-hover v-slot:default="{ hover }">
    <g>
      <!-- Link Path -->
      <path :d="dAttr" :style="pathStyle" />

      <!-- Delete Icon -->
      <a v-if="hover" @click="deleteLink">
        <text
          text-anchor="middle"
          :transform="arrowTransform"
          font-size="20"
          color="red"
          bold
          >X</text
        >
      </a>
      <!-- Arrow -->
      <path
        v-else
        d="M -1 -1 L 0 1 L 1 -1 z"
        :style="arrowStyle"
        :transform="arrowTransform"
      />
    </g>
  </v-hover>
</template>

<script>
export default {
  name: 'FlowchartLink',
  props: {
    // start point position [x, y]
    start: {
      type: Array,
      default() {
        return [0, 0]
      }
    },
    // end point position [x, y]
    end: {
      type: Array,
      default() {
        return [0, 0]
      }
    },
    id: Number
  },
  data: () => ({
    show: {
      delete: false
    }
  }),
  methods: {
    caculateCenterPoint() {
      // caculate arrow position: the center point between start and end
      const dx = (this.end[0] - this.start[0]) / 2
      const dy = (this.end[1] - this.start[1]) / 2
      return [this.start[0] + dx, this.start[1] + dy]
    },
    caculateRotation() {
      // caculate arrow rotation
      const angle = -Math.atan2(
        this.end[0] - this.start[0],
        this.end[1] - this.start[1]
      )
      const degree = (angle * 180) / Math.PI
      return degree < 0 ? degree + 360 : degree
    },
    deleteLink() {
      this.$emit('deleteLink')
    }
  },
  computed: {
    pathStyle() {
      return {
        stroke: 'black',
        strokeWidth: 2.73205,
        fill: 'none'
      }
    },
    arrowStyle() {
      return {
        stroke: '#42b883',
        strokeWidth: 8,
        fill: 'none'
      }
    },
    arrowTransform() {
      const [arrowX, arrowY] = this.caculateCenterPoint()
      const degree = this.caculateRotation()
      return `translate(${arrowX}, ${arrowY}) rotate(${degree})`
    },
    dAttr() {
      let cx = this.start[0],
        cy = this.start[1],
        ex = this.end[0],
        ey = this.end[1]
      let x1 = cx,
        y1 = cy + 50,
        x2 = ex,
        y2 = ey - 50
      return `M ${cx}, ${cy} C ${x1}, ${y1}, ${x2}, ${y2}, ${ex}, ${ey}`
    }
  }
}
</script>

<style scoped lang="scss">
g {
  cursor: pointer;
}
</style>
