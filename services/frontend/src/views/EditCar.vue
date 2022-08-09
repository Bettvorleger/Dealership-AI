<template>
  <section>
    <h5>Edit Car</h5>

    <q-form @submit="submit" class="q-gutter-sm q-ml-xs">
      <div class="q-gutter-md q-mb-md row">
        <SelectText v-model="car.make" label="Make" :rules="required" />

        <SelectText v-model="car.model" label="Model" :rules="required" />
      </div>
      <div class="q-gutter-md q-mb-md row">
        <InputText
          v-model="car.mileage"
          label="Mileage"
          :rules="required"
          type="number"
        />

        <InputText
          v-model="car.hp"
          label="HP"
          :rules="required"
          type="number"
        />

        <InputText
          v-model="car.year"
          label="Year"
          hint="First registration"
          :rules="required.concat(yearVal)"
          type="number"
        />
      </div>
      <div class="q-gutter-md row">
        <SelectText v-model="car.gear" label="Gear Type" :rules="required" />

        <SelectText v-model="car.fuel" label="Fuel Type" :rules="required" />

        <SelectText
          v-model="car.offer_type"
          label="Offer Type"
          :rules="required"
        />
      </div>
      <div class="q-gutter-md row">
        <q-input
          v-model="car.price"
          label="Price"
          type="number"
          outlined
          color="accent"
          prefix="€"
          lazy-rules
          :rules="required.concat(priceVal)"
        />
      </div>
      <q-btn flat color="accent" @click="$router.go(-1)" label="Cancel" />
      <q-btn type="submit" color="accent" label="Save" />
    </q-form>
  </section>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

import InputText from "../components/InputText.vue";
import SelectText from "../components/SelectText.vue";

export default {
  name: "editCar",
  props: ["id"],
  components: { InputText, SelectText },
  setup(props) {
    const store = useStore();
    const router = useRouter();

    // get car object from backend and load from store
    store.dispatch("getCar", props.id);
    const car = computed(() => store.getters.stateCar);

    // click action for car edit form, takes car object and entry id, push to backend
    const submit = () => {
      try {
        let data = {
          id: props.id,
          details: car.value,
        };
        store.dispatch("updateCar", data);
        router.push({ name: "dashboard" });
      } catch (error) {
        console.log(error);
      }
    };
    return {
      car,
      submit,
      required: [(val) => !!val || "Required"],
      yearVal: [
        (val) =>
          (val <= new Date().getFullYear() && val > 1900) ||
          "Year out of range",
      ],
      priceVal: [(val) => (val > 0 && !!val) || "Price cannot be negative"],
    };
  },
};
</script>