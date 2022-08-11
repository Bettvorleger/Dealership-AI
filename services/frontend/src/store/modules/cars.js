import axios from 'axios';

const state = {
    cars: null,
    car: null,
    filter: null,
    coeff: null,
};

const getters = {
    stateCars: state => state.cars,
    stateCar: state => state.car,
    stateFilter: state => state.filter,
    stateCoeff: state => state.coeff,
};

const actions = {
    // eslint-disable-next-line no-empty-pattern
    async createCar({ }, car) {
        try {
            let res = await axios.post('cars', car, {
                withCredentials: false,
            });
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
            let { data } = await axios.get(`car/${id}`, {
                withCredentials: false,
            });
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
    // eslint-disable-next-line no-empty-pattern
    async getPrice({ }, car) {
        try {
            let res = await axios.post('price', car, {
                withCredentials: false,
            });
            return res.data
        }
        catch (err) {
            console.error(err);
        }
    },
    async getFilter({ commit }) {
        try {
            let { data } = await axios.get('filter', {
                withCredentials: false,
            });
            commit('setFilter', data);
        }
        catch (err) {
            console.error(err);
        }
    },
    async getCoeff({ commit }) {
        try {
            let { data } = await axios.get('coefficients', {
                withCredentials: false,
            });
            commit('setCoeff', data);
        }
        catch (err) {
            console.error(err);
        }
    },
};

const mutations = {
    setCars(state, cars) {
        state.cars = cars;
    },
    setCar(state, car) {
        state.car = car;
    },
    setFilter(state, filter) {
        state.filter = filter;
    },
    setCoeff(state, coeff) {
        state.coeff = coeff;
    },
};

export default {
    state,
    getters,
    actions,
    mutations
};