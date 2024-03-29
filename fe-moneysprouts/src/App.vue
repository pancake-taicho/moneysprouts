<template>
  <div id="app">
    <div class="header">
      <h1 id="moneySproutsTitle">MoneySprouts</h1>
    </div>
    <div class="glass">
      <div v-bind:class="mainPanelClass">
        <!-- we display the LOGIN component if no user is currently active -->
        <user-message-display />
        <Login class="panel" v-if="this.$store.state.showLogin" />
        <BudgetVisualization
          class="panel"
          v-if="this.$store.state.showBudgetVisualization"
        />
        <BarChartScreen class="panel" v-if="this.$store.state.showBarChart" />
        <ExpenseInput class="panel" v-if="this.$store.state.showExpenseInput" />
        <SignUp class="panel" v-if="this.$store.state.showSignUp" />
        <BudgetInput class="panel" v-if="this.$store.state.showBudgetInput" />
      </div>
    </div>
    <div class="nav-bar">
      <div
        v-if="this.$store.state.userName !== ''"
        id="footer-button-container"
      >
        <button
          v-on:click="showBudgetVisualization"
          class="footer-button"
          name="profile"
          value="profile"
        >
          <i id="home-icon" class="fas fa-home"></i>
        </button>
        <button
          v-on:click="showExpenseInput"
          class="footer-button"
          name="expense-input"
          value="expense-input"
        >
          <i id="dollar-icon" class="fas fa-dollar-sign"></i>
        </button>
        <button
          v-on:click="showBudgetInput"
          class="footer-button"
          name="monthly-budget"
          value="monthly-budget"
        >
          <i id="calendar-icon" class="far fa-calendar-alt"></i>
        </button>
        <button
          v-on:click="showBarChart"
          class="footer-button"
          name="eco-action-chart"
          value="eco-action-chart"
        >
          <i id="chart-icon" class="fas fa-chart-bar"></i>
        </button>
        <button
          v-on:click="logout"
          class="footer-button"
          name="logout"
          value="logout"
        >
          <i id="signout-icon" class="fas fa-sign-out-alt"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Login from "./components/Login.vue";
import BudgetVisualization from "./components/BudgetVisualization.vue";
import ExpenseInput from "./components/ExpenseInput.vue";
import BudgetInput from "./components/BudgetInput.vue";
import UserMessageDisplay from "./components/UserMessageDisplay";
import BarChartScreen from "./components/BarChartScreen.vue";
import SignUp from "./components/SignUp.vue";

export default {
  name: "App",
  metaInfo: {
    title: "MoneySprouts",
    htmlAttrs: {
      lang: "en-US",
    },
    meta: [
      { charset: "utf-8" },
      {
        name: "description",
        content:
          "Expense tracking software which enables you to track your ecological footprint as well",
      },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
    ],
  },
  components: {
    Login,
    BudgetVisualization,
    ExpenseInput,
    BudgetInput,
    UserMessageDisplay,
    BarChartScreen,
    SignUp,
  },
  methods: {
    showBudgetVisualization() {
      this.$store.commit("setShowsToFalse");
      this.$store.commit("showBudgetVisualization");
    },
    showExpenseInput() {
      this.$store.commit("setShowsToFalse");
      this.$store.commit("showExpenseInput");
    },
    showBudgetInput() {
      this.$store.commit("setShowsToFalse");
      this.$store.commit("showBudgetInput");
    },
    showBarChart() {
      this.$store.commit("setShowsToFalse");
      this.$store.commit("showBarChart");
    },
    showSignUp() {
      this.$store.commit("setShowsToFalse");
      this.$store.commit("showSignUp");
    },
    logout() {
      this.$store.commit("clearUserName");
      this.$store.commit("setShowsToFalse");
      this.$store.commit("showLogin");
    },
  },
  mounted() {
    const externalScript = document.createElement("script");
    externalScript.setAttribute(
      "src",
      "https://kit.fontawesome.com/e3cbc00358.js"
    );
    externalScript.setAttribute("crossorigin", "anonymous");
    document.head.appendChild(externalScript);
  },
  computed: {
    mainPanelClass: function () {
      // Computed function to return the main Panel class dynamically
      // https://vuejs.org/v2/guide/class-and-style.html
      // Checking if the current component is included into the list of components
      // requiring the main Panel to be centered vertically
      const isCentered =
        this.$store.state.showLogin ||
        this.$store.state.showSignUp ||
        this.$store.state.showBarChart ||
        this.$store.state.showBudgetInput;
      return {
        "main-panel": true,
        contentCentered: isCentered,
      };
    },
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Carme&family=Lato&display=swap");
body {
  margin: 0;
  padding: 0;
}

h1 h2 {
  font-family: "Carme", sans-serif;
  color: #403d58;
}

button:active {
  background-color: rgb(111, 176, 42);
  transform: translateY(2px);
}

#app {
  --app-max-width: 800px;
  --header-color: #d7efbd;

  /* Variable calculation for positioning */
  --header-footer-height: max(10vh, 60px);

  max-width: var(--app-max-width);
  font-family: "Lato", sans-serif;

  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

  color: #2c3e50;
  min-height: 100vh;
  width: 100vw;

  background: url("assets/green-palmtree.jpg") top repeat-y;
  background-size: auto 100%;
}

#moneySproutsTitle {
  float: left !important;
  margin-left: 10px;
  font-size: 35px;
}

.main-panel {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  /* Height of the panel is the whole size - footer height */
  min-height: calc(100vh - 2 * var(--header-footer-height));
  /* The main panel has to be displayed from the bottom of the header, i.e
     header-content-height + 2* padding */
  margin-top: var(--header-footer-height);
  margin-bottom: var(--header-footer-height);
  text-align: center;
}

.contentCentered {
  justify-content: center;
}

.panel {
  padding: 5px;
  background-color: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(2px);
  min-width: 90%;
  border-radius: 5px;
  margin-top: 10px;
  margin-bottom: 40px;
}

.header {
  /* Header position: ABSOLUTE (to always stay on top) */
  position: fixed;
  top: 0;
  width: 100vw;
  max-width: var(--app-max-width);
  box-sizing: border-box;
  height: var(--header-footer-height);
  background-color: var(--header-color);
  display: flex; /* header has a flex display in order to center the title vertically */
  flex-direction: column;
  z-index: 5;
}

.header i {
  color: green;
}

.nav-bar {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 10px;
  box-sizing: border-box;
  position: fixed;
  bottom: 0;
  width: 100vw;
  max-width: var(--app-max-width);
  height: var(--header-footer-height);
  background: var(--header-color);
}

#footer-button-container {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  padding: 10px;
}

.footer-button {
  font-size: 2em;
  min-width: 60px;
  min-height: 60px;
  padding: 5px;
  text-align: center;
  border-radius: 12%;
  border: 3px solid #403d58;
  background-color: #403d58;
}

#home-icon,
#dollar-icon,
#calendar-icon,
#signout-icon,
#chart-icon {
  color: white;
}
</style>
