import axios from 'axios';

const state = {
    cars: null,
    car: null,
};

const getters = {
    stateCars: state => state.cars,
    stateCar: state => state.car,
};

const actions = {
    // eslint-disable-next-line no-empty-pattern
    async createCar({ }, car) {
        await axios.post('cars', car);
    },
    async getCars({ commit }) {

        console.log("TEST")
        let { data } = await axios.get('cars');
        commit('setCars', data);
    },
    async getCar({ commit }, id) {
        let { data } = await axios.get(`car/${id}`);
        commit('setCar', data);
    },
    // eslint-disable-next-line no-empty-pattern
    async updateCar({ }, car) {
        await axios.patch(`car/${car.id}`, car.details);
    },
    // eslint-disable-next-line no-empty-pattern
    async deleteCar({ }, id) {
        await axios.delete(`car/${id}`);
    },
};

const mutations = {
    setCars(state, cars) {
        state.cars = cars;
    },
    setCar(state, car) {
        state.car = car;
    },
};

export default {
    state,
    getters,
    actions,
    mutations
};