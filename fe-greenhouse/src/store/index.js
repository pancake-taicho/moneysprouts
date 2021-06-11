import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    // DO NOT MODIFY THESE!!!
    myTextColor: "blue",
    userName: "",
    user: {},
    isLoading: true,
    isAuthenticated: false,
    expensesList: [],
    ecoActionsList: [],
    ecoGoalsList: [],
    categoriesList: [],
    monthlyBudget: {},
    userMessage: { message: "", msgType: "" },
    showLogin: true,
    showBudgetVisualization: false,
    showExpenseInput: false,
    showBarChart: false,
    showBudgetInput: false,
    showSignUp: false,
  },
  mutations: {
    showSignUp(state) {
      state.showSignUp = true;
    },

    showBudgetInput(state) {
      state.showBudgetInput = true;
    },

    showBarChart(state) {
      state.showBarChart = true;
    },

    showExpenseInput(state) {
      state.showExpenseInput = true;
    },

    showBudgetVisualization(state) {
      state.showBudgetVisualization = true;
    },

    showLogin(state) {
      state.showLogin = true;
    },

    setShowsToFalse(state) {
      state.showLogin = false;
      state.showBudgetVisualization = false;
      state.showExpenseInput = false;
      state.showBarChart = false;
      state.showBudgetInput = false;
      state.showSignUp = false;
    },

    setUser(state, payload) {
      state.user = payload;
    },
    setUserName(state, payload) {
      state.userName = payload;
    },
    clearUserName(state) {
      state.userName = "";
      state.isLoading = true;
      state.user = {};
    },
    setLoadingStatus(state, payload) {
      if (typeof payload === "boolean") {
        state.isLoading = payload;
      } else {
        state.isLoading = payload.isLoading;
      }
    },
    setMyTextColor(state, payload) {
      state.myTextColor = payload;
    },
    setExpensesList(state, payload) {
      state.expensesList = [...payload.expensesList];
    },
    setEcoActionsList(state, payload) {
      state.ecoActionsList = payload.ecoActionsList;
    },
    setEcoGoalsList(state, payload) {
      state.ecoGoalsList = payload.ecoGoalsList;
    },
    setMonthlyBudget(state, payload) {
      state.monthlyBudget = payload.monthlyBudget;
    },
    setUserMessage(state, payload) {
      state.userMessage = payload;
    },
    setAuthenticated(state, payload) {
      state.isAuthenticated = payload;
    },
    setCategoriesList(state, payload) {
      state.categoriesList = payload.categoriesList;
    },
  }, // Use mutations to modify the state variables synchronously
  actions: {
    async verifyLogin({ commit, dispatch }, payload) {
      try {
        const res = await axios.post("/api/user/login", payload);
        if (res.data.error === -1) {
          commit("setUserMessage", {
            message: "Could not login",
            msgType: "error",
          });
        } else {
          commit("setUserName", res.data.username);
          commit("setUser", res.data);
          dispatch("receiveLoginSignal");
        }
      } catch (err) {
        console.error(err);
      }
    },

    async receiveLoginSignal({ commit, dispatch, state }) {
      // Need to download the data related to the current user
      commit("setLoadingStatus", true);
      try {
        const date = new Date();
        await dispatch("getBudgets");
        await dispatch("getExpenses", {
          year: date.getFullYear(),
          month: date.getMonth() + 1,
        });
        await dispatch("getEcoGoals");
        await dispatch("getEcoActions");
        await dispatch("getCategories");

        commit("setShowsToFalse");
        commit("showBudgetVisualization");

        commit("setLoadingStatus", false);
        commit("setAuthenticated", true);
      } catch (err) {
        console.error(`ERROR in the back-end API download! ${err}`);
      }
    },

    async createUser(store, payload) {
      try {
        await axios.post("/api/user/create", payload);
        store;
      } catch (err) {
        console.error(`ERROR in createUser! ${err}`);
      }
    },

    async createExpense({ dispatch, state }, payload) {
      try {
        await axios.post(`/api/user/${state.user.user_id}/expenses`, payload);
        const date = new Date();
        const newPayload = {
          year: date.getFullYear(),
          month: date.getMonth() + 1,
        }
        dispatch("getExpenses", newPayload);
      } catch (err) {
        console.error(`ERROR in createExpense! ${err}`);
      }
    },

    async updateExpense({ dispatch, state }, payload) {
      try {
        await axios.patch(`/api/user/${state.user.user_id}/expenses`, payload);
        dispatch("getExpenses");
      } catch (err) {
        console.error(`ERROR in updateExpense ${err}`);
      }
    },

    async getExpenses({ commit, state }, payload) {
      try {
        const res = await axios.get(
          `/api/user/${state.user.user_id}/expenses/${payload.year}/${payload.month}`
        );

        if (res === "Budget doesn't exist") {
          commit("setExpenseList", { expensesList: []})
        } else {
          commit("setExpensesList", { expensesList: res.data.expenses });
        }

      } catch (err) {
        console.error(`ERROR in getExpenses ${err}`);
      }
    },

    async updateBudget({ dispatch, state }, payload) {
      try {
        await axios.patch(
          `/api/user/${state.user.user_id}/user_budget`,
          payload
        );
        dispatch("getBudgets");
      } catch (err) {
        console.error(`ERROR in updateBudget ${err}`);
      }
    },

    async getBudgets({ commit, state }) {
      try {
        const res = await axios.get(
          `/api/user/${state.user.user_id}/user_budget`
        );
        commit("setMonthlyBudget", { monthlyBudget: res.data });
      } catch (err) {
        console.error(`ERROR in the getBudgets ${err}`);
      }
    },

    async getEcoGoals({ commit, state }) {
      try {
        const res = await axios.get(
          `/api/user/${state.user.user_id}/eco_goals`
        );
        if (res.data.eco_goals) {
          commit("setEcoGoalsList", { ecoGoalsList: res.data.eco_goals });
        }
      } catch (err) {
        console.error(`ERROR in the getEcoGoals ${err}`);
      }
    },

    async getEcoActions({ commit, state }) {
      try {
        const res = await axios.get(
          `/api/user/${state.user.user_id}/eco_actions`
        );
        if (res.data.eco_actions) {
          commit("setEcoActionsList", { ecoActionsList: res.data.eco_actions });
        }
      } catch (err) {
        console.error(`ERROR in the getEcoGoals ${err}`);
      }
    },

    async getCategories({ commit, state }) {
      try {
        const res = await axios.get(
          `/api/user/${state.user.user_id}/categories`
        );
        if (res.data.categories) {
          commit("setCategoriesList", { categoriesList: res.data.categories });
        }
      } catch (err) {
        console.error(`ERROR in the getCategories ${err}`);
      }
    },
  },
});
