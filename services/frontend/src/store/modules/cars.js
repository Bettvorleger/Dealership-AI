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
        try {
            let res = await axios.post('cars', car);
            return res.data
        }
        catch (err) {
            console.error(err);
        }
    },
    async getCars({ commit }) {
        try {
            let { data } = await axios.get('cars');
            commit('setCars', data);
        } catch (err) {
            console.error(err);
        }
    },
    async getCar({ commit }, id) {
        try {
            let { data } = await axios.get(`car/${id}`);
            commit('setCar', data);
        } catch (err) {
            return -1
        }
    },
    // eslint-disable-next-line no-empty-pattern
    async updateCar({ }, car) {
        try {
            await axios.patch(`car/${car.id}`, car);
        } catch (e) {
            console.log(e)
        }
    },
    async deleteCar({ dispatch }, id) {
        await axios.delete(`car/${id}`);
        await dispatch('getCars');
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