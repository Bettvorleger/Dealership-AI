<template>
  <section>
    <div>
      <q-stepper
        v-model="step"
        vertical
        color="accent"
        animated
        flat
        active-icon="none"
        active-color="primary"
        done-icon="none"
        done-color="accent"
        inactive-icon="none"
      >
        <q-step :name="1" title="Start" prefix="1" :done="step > 1">
          <q-form class="q-ml-xl">
            <h5 class="q-mb-sm">Estimate the value of your car</h5>
            <p class="text-body2">
              Just input a few details regarding the car you want to sell, no
              personal information required.<br />
              Our AI is trained on thousands of car sales from the past years,
              even recent ones.
            </p>
            <p class="text-negative">
              Please note that this is an automatic estimate and may contain
              errors!
            </p>

            <q-stepper-navigation>
              <q-btn @click="step = 2" color="accent" label="Start" />
            </q-stepper-navigation>
          </q-form>
        </q-step>

        <q-step :name="2" title="Details" prefix="2" :done="step > 2">
          <q-form class="q-ml-xl" @submit="onSubmitCarDetails">
            <h5 class="q-mb-sm">Enter details of your car</h5>
            <p class="text-body2">
              Be sure to check the inputs as they are needed for the price
              prediction.
            </p>
            <div class="q-gutter-md q-mb-md row">
              <SelectText
                v-model="car.make"
                label="Make"
                :stringOptions="filter.make"
                :rules="required"
              />

              <SelectText
                v-model="car.model"
                label="Model"
                :stringOptions="filter.model[car.make]"
                :rules="required"
              />
            </div>
            <div class="q-gutter-md q-mb-md row">
              <InputText
                v-model="car.mileage"
                label="Mileage (km)"
                :rules="required"
                type="number"
                :min="0"
              />

              <InputText
                v-model="car.hp"
                label="HP"
                :rules="required"
                type="number"
                :min="1"
                :max="1000"
              />

              <InputText
                v-model="car.year"
                label="Year"
                hint="First registration"
                :rules="required.concat(yearVal)"
                :min="1900"
                :max="new Date().getFullYear()"
                type="number"
              />
            </div>
            <div class="q-gutter-md row">
              <SelectText
                v-model="car.gear"
                label="Gear Type"
                :rules="required"
                :stringOptions="['Manual', 'Automatic', 'Semi-automatic']"
              />

              <SelectText
                v-model="car.fuel"
                label="Fuel Type"
                :rules="required"
                :stringOptions="filter.fuel"
              />

              <SelectText
                v-model="car.offer_type"
                label="Offer Type"
                :rules="required"
                :stringOptions="[
                  'Used',
                  'Demonstration',
                  'Employee\'s car',
                  'Pre-registered',
                  'New',
                ]"
              />
            </div>

            <q-stepper-navigation>
              <q-btn flat @click="step = 1" color="accent" label="Back" />
              <q-btn
                color="accent"
                label="Continue"
                type="submit"
                class="q-ml-sm"
              />
            </q-stepper-navigation>
          </q-form>
        </q-step>

        <q-step :name="3" title="Review" prefix="3" :done="step > 3">
          <div v-if="!noListing" class="q-ml-xl">
            <h5 class="q-mb-sm">Review the predicted price</h5>
            <p class="text-body2">
              Check the predicted value of your car. You can also see the
              reasons for a potentially low or high price here.
            </p>
            <div class="row text-h6">
              Your cars predicted value: {{ car.price }}€
              <q-btn
                class="q-ml-md"
                flat
                no-caps
                color="accent"
                dense
                icon="report"
                @click="prompt = true"
              >
                <q-tooltip class="accent">Report an error</q-tooltip>
              </q-btn>
            </div>

            <div class="q-pa-md row items-stretch q-gutter-md">
              <q-card flat bordered class="col-md-5">
                <q-card-section>
                  <div class="text-h6">
                    Price Booster <q-icon color="positive" name="trending_up" />
                  </div>
                </q-card-section>
                <q-card-section class="q-pt-none">
                  Your car as a higher value because...
                  <q-list dense padding>
                    <q-item v-if="explain.mileage == 1">
                      - {{ car.mileage }}km mileage is relatively low
                    </q-item>
                    <q-item v-if="explain.hp == 1">
                      - {{ car.hp }} horsepower is relatively high
                    </q-item>
                    <q-item v-if="explain.year == 1">
                      - at {{ new Date().getFullYear() - car.year }} years the
                      car is relatively new
                    </q-item>
                    <q-item v-if="explain.make == 1">
                      - {{ car.make }} is generally high priced
                    </q-item>
                    <q-item v-if="explain.fuel == 1">
                      - {{ car.fuel }} fuel increases the value
                    </q-item>
                    <q-item v-if="explain.gear == 1">
                      - {{ car.gear }} gear increases the value
                    </q-item>
                    <q-item v-if="explain.offer_type == 1">
                      - {{ car.offer_type }} increases the value
                    </q-item>
                  </q-list>
                </q-card-section>
              </q-card>
              <q-card flat bordered class="col-md-5">
                <q-card-section>
                  <div class="text-h6">
                    Price Opposer
                    <q-icon color="negative" name="trending_down" />
                  </div>
                </q-card-section>
                <q-card-section class="q-pt-none">
                  Your car as a lower value because...
                  <q-list dense padding>
                    <q-item v-if="explain.mileage == -1">
                      - {{ car.mileage }} the mileage is relatively high
                    </q-item>
                    <q-item v-if="explain.hp == -1">
                      - {{ car.hp }} horsepower is relatively low
                    </q-item>
                    <q-item v-if="explain.year == -1">
                      - at {{ new Date().getFullYear() - car.year }} years the
                      car is relatively old
                    </q-item>
                    <q-item v-if="explain.make == -1">
                      - {{ car.make }} is generally low priced
                    </q-item>
                    <q-item v-if="explain.fuel == -1">
                      - {{ car.fuel }} fuel lowers the value
                    </q-item>
                    <q-item v-if="explain.gear == -1">
                      - {{ car.gear }} gear lowers the value
                    </q-item>
                    <q-item
                      v-if="
                        explain.offer_type == -1 && car.offer_type != 'Used'
                      "
                    >
                      - {{ car.offer_type }} lowers the value
                    </q-item>
                  </q-list>
                </q-card-section>
              </q-card>
            </div>

            <q-dialog v-model="prompt">
              <q-card style="max-width: 350px">
                <q-card-section>
                  <div class="text-body">
                    Please let us know, if the price seems hugely out of
                    proportion. Just click on the button below.
                  </div>
                </q-card-section>

                <q-card-actions align="right" class="text-primary">
                  <q-btn flat color="accent" label="Cancel" v-close-popup />
                  <q-btn
                    flat
                    color="accent"
                    label="Report error"
                    v-close-popup
                  />
                </q-card-actions>
              </q-card>
            </q-dialog>

            <q-stepper-navigation>
              <q-btn flat @click="step = 2" color="accent" label="Back" /><q-btn
                @click="step = 4"
                color="accent"
                label="Continue"
                class="q-ml-sm"
              />
            </q-stepper-navigation>
          </div>
          <div v-else>
            <div class="text-bold">
              Sorry, the value of your car cannot be predicted by our AI model.
              These reasons could apply:
            </div>
            <ul>
              <li>The car is too rare or not known to our AI</li>
              <li>The car details you provided are not correct</li>
              <li>The car has close to no value on the used car market</li>
            </ul>
            <q-stepper-navigation>
              <q-btn flat @click="step = 2" color="accent" label="Back" />
            </q-stepper-navigation>
          </div>
        </q-step>

        <q-step :name="4" title="Listing" prefix="4">
          <q-form class="q-ml-xl" @submit="onSubmitListing">
            <h5 class="q-mb-sm">Select an option for you car sale listing</h5>
            <p class="text-body2">
              Review the two options carefully, since the presented estimted
              price is automatically generated.
            </p>
            <div class="q-gutter-y-md q-mt-lg">
              <q-btn-toggle
                @onChange="show"
                class="toggle-listing"
                v-model="car.is_custom"
                spread
                no-caps
                rounded
                unelevated
                toggle-color="accent"
                color="white"
                text-color="black"
                :options="[
                  { value: false, slot: 'ai' },
                  { value: true, slot: 'custom' },
                ]"
              >
                <template v-slot:ai>
                  <div class="row items-center justify-center">
                    <div class="text-center text-h6 review-label">
                      Take Dealership AI’s sale adivce
                    </div>
                    <q-icon right name="task_alt" />
                  </div>
                  <ul dense class="row justify-center q-pl-xs q-mt-md q-mb-xs text-weight-regular">
                    <li class="col-md-5 text-left">
                      list your car for the <b>predicted price</b> of
                      {{ car.price }}€
                    </li>
                    <li class="col-md-5 text-left">
                      get <b>100€ cash back</b> for successful sale
                    </li>
                  </ul>
                </template>

                <template v-slot:custom>
                  <div class="row items-center wrap justify-center">
                    <div class="text-center text-h6 review-label">Select your own price</div>
                    <q-icon right name="tune" />
                  </div>
                  <ul dense class="row justify-center q-pl-xs q-mt-md q-mb-xs text-weight-regular">
                    <li class="col-md-5 text-left">
                      list your car for the <b>price you want</b>
                    </li>
                    <li class="col-md-5 text-left">
                      <b>no</b> cash back for successful sale
                    </li>
                  </ul>
                </template>
              </q-btn-toggle>
              <div class="row justify-end">
                <q-input
                  class="col-md-2 offset-2"
                  label="Custom Price"
                  v-if="car.is_custom"
                  outlined
                  v-model="customPrice"
                  type="number"
                  prefix="€"
                  lazy-rules
                  :rules="required.concat(priceVal)"
                />
                <div class="col-2"></div>
              </div>
            </div>

            <q-stepper-navigation>
              <q-btn flat @click="step = 3" color="accent" label="Back" />
              <q-btn
                color="accent"
                label="Create"
                type="submit"
                class="q-ml-sm"
              />
            </q-stepper-navigation>
          </q-form>
        </q-step>
      </q-stepper>
      <q-dialog
        v-model="successDialog"
        transition-show="scale"
        transition-hide="scale"
      >
        <q-card class="bg-primary text-black" style="width: 300px">
          <q-card-section>
            <div class="text-h6">You successfully submitted your car</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            Please use this code to check the status of the sale:
            {{ code }}
          </q-card-section>

          <q-card-actions align="right" class="bg-white text-accent">
            <q-btn
              flat
              label="OK"
              @click="$router.push({ name: 'status', params: { pCode: code } })"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </section>
</template>
<script>
import { ref, computed } from "vue";
import InputText from "../components/InputText.vue";
import SelectText from "../components/SelectText.vue";
import { useStore } from "vuex";

export default {
  name: "HomeView",
  components: { InputText, SelectText },
  setup() {
    const store = useStore();

    // init car object for inference/saving
    let car = ref({
      make: "",
      model: "",
      mileage: null,
      hp: null,
      year: null,
      fuel: "",
      gear: "",
      offer_type: "",
      is_custom: false,
      price: null,
    });
    const customPrice = ref(0);
    const step = ref(1);
    const successDialog = ref(false);
    const noListing = ref(false);
    const code = ref(null);

    // get filters and explainability coefficients from backend and load from store
    store.dispatch("getFilter");
    const filter = computed(() => store.getters["stateFilter"]);

    store.dispatch("getCoeff");
    const coeff = computed(() => store.getters["stateCoeff"]);
    const explain = ref({
      make: 0,
      mileage: 0,
      hp: 0,
      year: 0,
      fuel: 0,
      gear: 0,
      offer_type: 0,
    });

    // click action for car detail submit button (step 2)
    // inference via backend call with car object returns price, call explainability
    const onSubmitCarDetails = () => {
      store.dispatch("getPrice", car.value).then((resp) => {
        car.value.price = resp;
        createExplanability();
        if (resp <= 0) {
          noListing.value = true;
        } else {
          noListing.value = false;
        }
      });
      customPrice.value = car.value.price;
      step.value = 3;
    };

    // create explanability via coefficients from AI model
    // normalize each param with inference price, summing up all weights and output if over treshold (1/10 of sum)
    const createExplanability = () => {
      const impact = {
        mileage: (car.value.mileage * coeff.value.mileage) / car.value.price,
        hp: ((car.value.hp / 10) * coeff.value.hp) / car.value.price,
        year:
          (((car.value.year - new Date().getFullYear()) / 4) *
            coeff.value.year) /
          car.value.price,
        make: (coeff.value.make[car.value.make] ?? 0) / car.value.price,
        fuel: (coeff.value.fuel[car.value.fuel] ?? 0) / car.value.price,
        gear: (coeff.value.gear[car.value.gear] ?? 0) / car.value.price,
        offer_type:
          (coeff.value.offer_type[car.value.offer_type] ?? 0) / car.value.price,
      };

      let sum = 0;
      for (let key in impact) {
        sum += Math.abs(impact[key]);
      }

      let influence = (sum * 1) / 10;

      explain.value.mileage =
        Math.abs(impact.mileage) > influence
          ? 1 * Math.sign(impact.mileage)
          : 0;
      explain.value.hp =
        Math.abs(impact.hp) > influence ? 1 * Math.sign(impact.hp) : 0;
      explain.value.year =
        Math.abs(impact.year) > influence ? 1 * Math.sign(impact.year) : 0;
      explain.value.make =
        Math.abs(impact.make) > influence ? 1 * Math.sign(impact.make) : 0;
      explain.value.fuel =
        Math.abs(impact.fuel) > influence ? 1 * Math.sign(impact.fuel) : 0;
      explain.value.gear =
        Math.abs(impact.gear) > influence ? 1 * Math.sign(impact.gear) : 0;
      explain.value.offer_type =
        Math.abs(impact.hp) > influence ? 1 * Math.sign(impact.offer_type) : 0;
    };

    // click action for last submit step, creates entry in database 
    const onSubmitListing = () => {
      if (customPrice.value) {
        car.value.price = customPrice.value;
      }
      store.dispatch("createCar", car.value).then((resp) => {
        code.value = btoa(resp.id).replace("=", "");
        successDialog.value = true;
      });
    };
    return {
      car,
      filter,
      explain,
      customPrice,
      prompt: ref(false),
      successDialog,
      noListing,
      code,
      step,
      onSubmitCarDetails,
      onSubmitListing,
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