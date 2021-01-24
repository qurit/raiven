<template>
  <v-treeview
    dense
    :items="nodes"
    item-text="id"
    :loadChildren="loadChildren"
    hoverable
  >
    <template v-slot:prepend="{ item }">
      <v-icon v-if="item.icon" v-text="item.icon"></v-icon>
    </template>

    <template slot="label" slot-scope="{ item }">
      <a v-if="item.hasOwnProperty('host')" @click="sendSelectEvent('Node', item.id)">
        {{ item.title }}
        <span class="text-caption"
          >Host: {{ item.host }} Port: {{ item.port }}</span
        >
      </a>
      <a
        v-else-if="item.hasOwnProperty('patient_id')"
        @click="sendSelectEvent('Patient', item.id)"
      >
        {{ item.patient_id }}
      </a>
      <a
        v-else-if="item.hasOwnProperty('study_instance_uid')"
        @click="sendSelectEvent('Study', item.id)"
      >
        {{ new Date(item.study_date).toLocaleDateString() }}
      </a>
      <a v-else @click="sendSelectEvent('Series', item.id)">
        {{ item.series_description }}
      </a>
    </template>
  </v-treeview>
</template>

<script>
export default {
  name: 'DicomInstanceTree',
  props: ['nodes', 'loadChildren'],
  methods: {
    sendSelectEvent (name, id) {
      this.$emit('select', name, id)
    }
  }
}
</script>
