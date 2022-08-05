<template>
  <div>
    <section>
      <h4>Overview</h4>

      <div class="q-pa-md">
        <q-table
          dense
          flat
          bordered
          title="Cars"
          :rows="cars"
          :columns="columns"
          row-key="make"
          :filter="filter"
          :rows-per-page-options="[20,50,100]"
        >
          <template v-slot:top-right>
            <q-input
              borderless
              dense
              debounce="300"
              v-model="filter"
              placeholder="Search"
            >
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </template>

          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <q-btn
                dense
                round
                flat
                :disable="!props.row.is_sold ? false : true"
                color="grey"
                @click="editCar(props.row.id)"
                icon="edit"
              >
                <q-tooltip class="grey" :offset="[10, 10]">
                  Edit car entry
                </q-tooltip>
              </q-btn>
              <q-btn
                dense
                round
                flat
                color="grey"
                :disable="!props.row.is_sold ? false : true"
                @click="simulateSale(props.row)"
                icon="sell"
              >
                <q-tooltip class="grey" :offset="[10, 10]">
                  Simulate car sale
                </q-tooltip>
              </q-btn>
              <q-btn
                dense
                round
                flat
                color="grey"
                @click="deleteCar(props.row.id)"
                icon="delete"
              >
                <q-tooltip class="grey" :offset="[10, 10]">
                  Delete car entry
                </q-tooltip>
              </q-btn>
            </q-td>
          </template>
        </q-table>
      </div>
    </section>
  </div>
</template>

<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  name: "DashboardView",
  setup() {
    const store = useStore();
    const router = useRouter();

    store.dispatch("getCars");
    const cars = computed(() => store.getters["stateCars"]);

    const columns = [
      {
        name: "make",
        label: "Make",
        field: "make",
        sortable: true,
      },
      {
        name: "model",
        label: "Model",
        field: "model",
        sortable: true,
      },
      {
        name: "mileage",
        label: "Mileage",
        field: "mileage",
        sortable: true,
      },
      {
        name: "fuel",
        label: "Fuel Type",
        field: "fuel",
        sortable: true,
      },
      {
        name: "gear",
        label: "Gear Type",
        field: "gear",
        sortable: true,
      },
      {
        name: "offer_type",
        label: "Offer Type",
        field: "offer_type",
        sortable: true,
      },
      {
        name: "hp",
        label: "HP",
        field: "hp",
        sortable: true,
      },
      {
        name: "year",
        label: "Year",
        field: "year",
        sortable: true,
      },
      {
        name: "price",
        label: "Price (€)",
        field: "price",
        sortable: true,
      },
      {
        name: "is_sold",
        label: "Sale Status",
        field: "is_sold",
        sortable: true,
        format: (val) => (val ? "Sold" : "Not sold"),
      },
      {
        name: "is_custom",
        label: "Price Type",
        field: "is_custom",
        sortable: true,
        format: (val) => (val ? "Custom" : "AI"),
      },
      { name: "actions", label: "Actions", field: "", align: "center" },
    ];

    const editCar = (carId) => {
      try {
        router.push({ name: "editCar", params: { id: carId } });
      } catch (error) {
        console.log("Entry cannot be edited.", error);
      }
    };

    const deleteCar = (carId) => {
      try {
        store.dispatch("deleteCar", carId);
        router.push({ name: "dashboard" });
      } catch (error) {
        console.error(error);
      }
    };

    const simulateSale = (car) => {
      try {
        car.is_sold = true;
        store.dispatch("updateCar", car);
      } catch (error) {
        console.log(error);
      }
    };

    return {
      filter: ref(""),
      cars,
      columns,
      editCar,
      deleteCar,
      simulateSale,
    };
  },
};
</script>