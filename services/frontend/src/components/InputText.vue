<template>
  <div>
    <q-input
      color="accent"
      outlined
      v-model="input"
      :label="label"
      :hint="hint"
      :type="type"
      lazy-rules
      :rules="rules"
    />
  </div>
</template>

<script>
import { computed } from "vue";

export default {
  name: "InputText",
  props: {
    modelValue: String,
    label: String,
    hint: String,
    rules: Array,
    type: String,
  },
  setup(props, { emit }) {
    const input = computed({
      get: () => props.modelValue,
      set: (value) => emit("update:modelValue", value),
    });
    return {
      input,
    };
  },
};
</script>