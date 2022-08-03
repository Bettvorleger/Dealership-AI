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
            if (res.status == 200) {
                console.log(car)
                console.log(res.status)
            }
            console.log(res.data)
            return res.data
        }
        catch (err) {
            console.error(err);
        }
    },
    async getCars({ commit }) {
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