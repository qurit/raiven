import Vue from 'vue'
import * as components from '../components/global'

for (const key in components.default) {
  Vue.component(key, components.default[key])
}


