<template>
  <div>
    <q-input
      color="accent"
      outlined
      v-model="input"
      :label="label"
      :hint="hint"
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