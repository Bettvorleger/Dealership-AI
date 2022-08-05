<template>
  <q-select
    color="accent"
    outlined
    v-model="input"
    :hint="hint"
    use-input
    lazy-rules
    :rules="rules"
    input-debounce="0"
    :label="label"
    :options="options"
    @filter="filterFn"
  >
    <template v-slot:no-option>
      <q-item>
        <q-item-section class="text-grey"> No results </q-item-section>
      </q-item>
    </template>
  </q-select>
</template>

<script>
import { computed, ref } from "vue";

export default {
  name: "SelectText",
  props: {
    modelValue: String,
    label: String,
    hint: String,
    rules: Array,
    stringOptions: Array,
  },
  setup(props, { emit }) {
    const options = ref(props.stringOptions);
    const input = computed({
      get: () => props.modelValue,
      set: (value) => emit("update:modelValue", value),
    });
    const filterFn = (val, update) => {
      if (val === "") {
        update(() => {
          options.value = props.stringOptions;
        });
      } else {
        update(() => {
          const needle = val.toLowerCase();
          options.value = props.stringOptions.filter(
            (v) => v.toLowerCase().indexOf(needle) > -1
          );
        });
      }
    };
    return {
      input,
      filterFn,
      options,
    };
  },
};
</script>