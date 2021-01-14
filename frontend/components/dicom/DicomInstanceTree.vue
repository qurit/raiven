<template>
  <v-treeview
      dense
      :items="nodes"
      item-text="id"
      :loadChildren="fetchTest"
      hoverable
  >
    <template v-slot:prepend="{ item }">
      <v-icon v-if="item.icon" v-text="item.icon"></v-icon>
    </template>

    <template slot="label" slot-scope="{ item }">
      <a v-if="item.hasOwnProperty('host')" @click="send">
        {{ item.title }}
        <span class="text-caption"
        >Host: {{ item.host }} Port: {{ item.port }}</span
        >
      </a>
      <a
          v-else-if="item.hasOwnProperty('patient_id')"
          @click="send"
      >
        {{ item.patient_id }}
      </a>
      <a
          v-else-if="item.hasOwnProperty('study_instance_uid')"
          @click="send"
      >
        {{ new Date(item.study_date).toLocaleDateString() }}
      </a>
      <a v-else @click="send">
        {{ item.series_description }}
      </a>
    </template>
  </v-treeview>
</template>

<script>
export default {
  name: 'DicomInstanceTree',
  props: ['nodes', 'send'],
  created() {
    console.log("NODES");
    console.log(this.nodes);
  }
}
</script>