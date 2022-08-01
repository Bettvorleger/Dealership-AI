<template>
  <section>
    <div class="q-pa-md">
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
        <q-step
          :name="1"
          title="Image"
          caption="Optional"
          prefix="1"
          :done="step > 1"
          optional
        >
          <q-form class="q-ml-xl">
            <h5 class="q-mb-sm">Upload an image of your car</h5>
            <p class="text-body2">
              This is optional. Also, more images can be uploaded after the
              successful listing.
            </p>
            <div class="fit row wrap justify-start content-start">
              <q-file
                color="accent"
                outlined
                class="col-3"
                v-model="image"
                accept=".jpg, image/*"
                label="Pick image"
                @update:model-value="handleUpload()"
              >
                <template v-slot:prepend>
                  <q-icon name="attach_file" />
                </template>
              </q-file>
              <q-card v-if="imageUrl" flat bordered class="col-5 offset-1">
                <q-item>
                  <q-item-section>
                    <div class="text-h7 q-mb-sm">Preview:</div>
                  </q-item-section>
                </q-item>

                <q-img
                  :src="imageUrl"
                  spinner-color="black"
                  fit="contain"
                  style="max-height: 250px"
                ></q-img>
              </q-card>
            </div>

            <q-stepper-navigation>
              <q-btn @click="step = 2" color="accent" label="Continue" />
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
              <SelectText v-model="car.brand" label="Brand" :rules="required" />

              <SelectText v-model="car.model" label="Model" :rules="required" />
            </div>
            <div class="q-gutter-md q-mb-md row">
              <InputText
                v-model="car.mileage"
                label="Mileage"
                :rules="required"
              />

              <InputText v-model="car.hp" label="HP" :rules="required" />

              <InputText
                v-model="car.year"
                label="Year"
                hint="First registration"
                :rules="required.concat(yearVal)"
              />
            </div>
            <div class="q-gutter-md row">
              <SelectText
                v-model="car.gearType"
                label="Gear Type"
                :rules="required"
              />

              <SelectText
                v-model="car.fuelType"
                label="Fuel Type"
                :rules="required"
              />

              <SelectText
                v-model="car.offerType"
                label="Offer Type"
                :rules="required"
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

        <q-step :name="3" title="Review" prefix="3" :done="step > 2">
          <div class="q-ml-xl">
            <h5 class="q-mb-sm">Review the predicted price</h5>
            <p class="text-body2">
              Check the predicted value of your car. You can also see the
              reasons for a potentially low or high price here.
            </p>
            <div class="row text-h6">
              Your cars predicted value: {{ price }}€
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

            <div class="q-pa-md row items-start q-gutter-md">
              <q-card flat bordered class="col-5">
                <q-card-section>
                  <div class="text-h6">Price Booster</div>
                </q-card-section>

                <q-card-section class="q-pt-none">
                  Your car as a higher value because of the...
                </q-card-section>
              </q-card>
              <q-card flat bordered class="col-5">
                <q-card-section>
                  <div class="text-h6">Price Opposer</div>
                </q-card-section>

                <q-card-section class="q-pt-none">
                  Your car as a lower value because of the...
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
        </q-step>

        <q-step :name="4" title="Listing" prefix="4">
          <q-form class="q-ml-xl">
            <h5 class="q-mb-sm">Select an option for you car sale listing</h5>
            <p class="text-body2">
              Review the two options carefully, since the presented estimted
              price is automatically generated.
            </p>
            <q-form class="q-gutter-y-md q-mt-lg" @submit="onSubmitListing">
              <q-btn-toggle
                @onChange="show"
                class="toggle-listing"
                v-model="listing_ai"
                spread
                no-caps
                rounded
                unelevated
                toggle-color="accent"
                color="white"
                text-color="black"
                :options="[
                  { value: true, slot: 'ai' },
                  { value: false, slot: 'custom' },
                ]"
              >
                <template v-slot:ai>
                  <div class="row items-center no-wrap">
                    <div class="text-center text-h6">
                      Take Dealership AI’s sale adivce
                    </div>
                    <q-icon right name="task_alt" />
                  </div>
                  <ul dense class="row q-mt-md q-mb-xs text-weight-regular">
                    <li class="col-5 text-left">
                      list your car for the <b>predicted price</b> of
                      {{ price }}€
                    </li>
                    <li class="col-5 offset-1 stext-left">
                      get <b>100€ cash back</b> for successful sale
                    </li>
                  </ul>
                </template>

                <template v-slot:custom>
                  <div class="row items-center no-wrap">
                    <div class="text-center text-h6">Select your own price</div>
                    <q-icon right name="tune" />
                  </div>
                  <ul dense class="row q-mt-md q-mb-xs text-weight-regular">
                    <li class="col-5 text-left">
                      list your car for the <b>price you want</b>
                    </li>
                    <li class="col-5 offset-1 text-left">
                      <b>no</b> cash back for successful sale
                    </li>
                  </ul>
                </template>
              </q-btn-toggle>
              <div class="row justify-end">
                <q-input
                  class="col-2 offset-2"
                  label="Custom Price"
                  v-if="!listing_ai"
                  outlined
                  v-model="customPrice"
                  type="number"
                  prefix="€"
                  lazy-rules
                  :rules="required.concat(priceVal)"
                />
                <div class="col-2"></div>
              </div>
            </q-form>

            <q-stepper-navigation>
              <q-btn flat @click="step = 3" color="accent" label="Back" />
              <q-btn color="accent" label="Create" class="q-ml-sm" />
            </q-stepper-navigation>
          </q-form>
        </q-step>
      </q-stepper>
    </div>
  </section>
</template>
<script>
import { ref } from "vue";
import InputText from "../components/InputText.vue";
import SelectText from "../components/SelectText.vue";

export default {
  name: "HomeView",
  components: { InputText, SelectText },
  setup() {
    let car = ref({
      brand: "",
      model: "",
      mileage: null,
      hp: null,
      year: null,
      fuelType: "",
      gearType: "",
      offerType: "",
    });
    const price = ref(0);
    const customPrice = ref(null);
    const listing_ai = ref(true);
    const step = ref(3);
    const image = ref(null);
    const imageUrl = ref("");
    const handleUpload = () => {
      if (image.value) {
        imageUrl.value = URL.createObjectURL(image.value);
      }
    };
    const onSubmitCarDetails = () => {
      console.log("Succces");
      console.log(car.value);
      step.value = 3;
    };
    return {
      car,
      price,
      customPrice,
      listing_ai,
      prompt: ref(false),
      step,
      image,
      imageUrl,
      handleUpload,
      onSubmitCarDetails,
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