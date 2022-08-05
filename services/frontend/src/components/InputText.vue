<template>
  <div>
    <q-input
      color="accent"
      outlined
      style="min-width: 120px"
      v-model="input"
      :label="label"
      :hint="hint"
      :type="type"
      lazy-rules
      :rules="rules"
      :min="min"
      :max="max"
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
    min: Number,
    max: Number,
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