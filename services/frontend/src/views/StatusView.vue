<template>
  <div class="q-pa-md">
    <q-card flat class="form-card">
      <q-card-section>
        <h4 class="text-center q-mb-xs">Check car listing status</h4>
      </q-card-section>
      <q-card-section>
        <div class="text-body text-center">
          Please input the code you have been given to check the sale status of
          your car listing.
        </div>
      </q-card-section>
      <q-card-section class="row wrap justify-center items-center">
        <q-input
          outlined
          class="offset-sm-1 col-sm-4 col-8"
          color="black"
          type="text"
          label="Code"
          v-model="code"
          :error="!codeExists"
        >
          <template v-slot:error> No car for this code </template>
        </q-input>
        <q-btn
          class="q-ml-md"
          color="accent"
          label="Submit"
          align="center"
          @click="submit"
        />
      </q-card-section>
    </q-card>
    <div v-if="showCar" class="q-ma-lg">
      <div
        class="q-mt-xs q-gutter-md row items-start justify-center content-start"
      >
        <q-list bordered separator class="col-2">
          <q-item>
            <q-item-section>
              <q-item-label overline>Created on</q-item-label>
              <q-item-label>{{
                new Intl.DateTimeFormat("de").format(new Date(car.created_at))
              }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item>
            <q-item-section>
              <q-item-label overline>Make</q-item-label>
              <q-item-label>{{ car.make }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item>
            <q-item-section>
              <q-item-label overline>Model</q-item-label>
              <q-item-label>{{ car.model }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        <q-list bordered separator class="col-2">
          <q-item>
            <q-item-section>
              <q-item-label overline>Mileage</q-item-label>
              <q-item-label>{{ car.mileage }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item>
            <q-item-section>
              <q-item-label overline>HP</q-item-label>
              <q-item-label>{{ car.hp }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item>
            <q-item-section>
              <q-item-label overline>Year (first registration)</q-item-label>
              <q-item-label>{{ car.year }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        <q-list bordered separator class="col-2">
          <q-item>
            <q-item-section>
              <q-item-label overline>Fuel Type</q-item-label>
              <q-item-label>{{ car.fuel }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item>
            <q-item-section>
              <q-item-label overline>Gear Type</q-item-label>
              <q-item-label>{{ car.gear }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item>
            <q-item-section>
              <q-item-label overline>Offer Type</q-item-label>
              <q-item-label>{{ car.offer_type }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        <q-list bordered separator class="col-2">
          <q-item>
            <q-item-section>
              <q-item-label overline>Price</q-item-label>
              <q-item-label>{{ car.price }}€</q-item-label>
            </q-item-section>
          </q-item>
          <q-item>
            <q-item-section>
              <q-item-label overline>Price Type</q-item-label>
              <q-item-label>{{ car.is_custom ? "Custom" : "AI" }}</q-item-label>
            </q-item-section>
          </q-item>
          <q-item>
            <q-item-section>
              <q-item-label overline>Sale status</q-item-label>
              <q-item-label>{{
                car.is_sold ? "Sold" : "Not sold"
              }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
        <div class="text-center" v-if="car.is_sold">
          <div class="text-h6">
            Congratulaions, your car has been sold for {{ car.price }}€.
          </div>
          <div class="text-body-2">
            You are no eligable for a 100€ cash back! Please visit
            <a
              target="_blank"
              href="https://www.businessinsider.com/how-to-spend-money-and-be-happier-2013-7#youre-investing-too-much-in-yourself-and-not-enough-in-other-people-5"
              >here</a
            >
            to apply!
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";

export default {
  name: "StatusView",
  props: ["pCode"],
  setup(props) {
    const store = useStore();

    const car = computed(() => store.getters.stateCar);
    const showCar = ref(false);
    const code = ref(props.pCode);
    const codeExists = ref(true);

    const submit = () => {
      store.dispatch("getCar", atob(code.value)).then((resp) => {
        if (resp == -1) {
          codeExists.value = false;
          showCar.value = false;
        } else {
          codeExists.value = true;
          showCar.value = true;
        }
      });
    };

    if (props.pCode) {
      submit();
    }

    return {
      car,
      code,
      submit,
      codeExists,
      showCar,
    };
  },
};
</script>