<template>
  <div id="budget-input-container">
    <div id="budget-input-form">
      <h1>Update Budget</h1>
      <p>
        <span class="income">Monthly Income:</span>
        <span
          class="field-value"
          v-show="!showField('monthlyIncome')"
          @click="focusField('monthlyIncome')"
        >
          ¥{{ form.monthlyIncome }}
          <i class="fas fa-edit"></i>
        </span>
        <input
          v-model="form.monthlyIncome"
          v-show="showField('monthlyIncome')"
          id="monthly-income"
          type="text"
          class="field-value form-control"
          @focus="focusField('monthlyIncome')"
          @blur="blurField"
        />
      </p>
      <div id="budget-input-grid">
        <div></div>
        <div class="grid-col-header" id="currentHeader">Running Total</div>
        <div class="grid-col-header" id="allocHeader">Amount Allocated</div>
        <div class="grid-row-header" id="groceriesLbl">Groceries</div>
        <div class="grid-content" id="groceriesCurrent">
          ¥{{ runningGroceries }}
        </div>
        <div class="grid-content-2" id="groceriesAlloc">
          <span
            class="field-value"
            v-show="!showField('allocatedGroceries')"
            @click="focusField('allocatedGroceries')"
          >
            ¥{{ form.allocatedGroceries }}
            <i class="fas fa-edit"></i>
          </span>
          <input
            v-model="form.allocatedGroceries"
            v-show="showField('allocatedGroceries')"
            id="allocated-groceries"
            type="text"
            class="field-value form-control"
            @focus="focusField('allocatedGroceries')"
            @blur="blurField"
            maxlength="15"
          />
        </div>
        <div class="row-header" id="billsLbl">Bills</div>
        <div class="grid-content" id="billsCurrent">¥{{ runningBills }}</div>
        <div class="grid-content-2" id="billsAlloc">
          <span
            class="field-value"
            v-show="!showField('allocatedBills')"
            @click="focusField('allocatedBills')"
            >¥{{ form.allocatedBills }}
            <i class="fas fa-edit"></i>
          </span>
          <input
            v-model="form.allocatedBills"
            v-show="showField('allocatedBills')"
            id="allocated-bills"
            type="text"
            class="field-value form-control"
            @focus="focusField('allocatedBills')"
            @blur="blurField"
            maxlength="15"
          />
        </div>
        <div class="row-header" id="transportLbl">Transport</div>
        <div class="grid-content" id="transportCurrent">
          ¥{{ runningTransport }}
        </div>
        <div class="grid-content-2" id="transportAlloc">
          <span
            class="field-value"
            v-show="!showField('allocatedTransport')"
            @click="focusField('allocatedTransport')"
            >¥{{ form.allocatedTransport }}
            <i class="fas fa-edit"></i>
          </span>
          <input
            v-model="form.allocatedTransport"
            v-show="showField('allocatedTransport')"
            id="allocated-transport"
            type="text"
            class="field-value form-control"
            @focus="focusField('allocatedTransport')"
            @blur="blurField"
            maxlength="15"
          />
        </div>
        <div class="row-header" id="miscLbl">Misc</div>
        <div class="grid-content" id="miscCurrent">¥{{ runningMisc }}</div>
        <div class="grid-content-2" id="miscAlloc">
          <span
            class="field-value"
            v-show="!showField('allocatedMisc')"
            @click="focusField('allocatedMisc')"
            >¥{{ form.allocatedMisc }}
            <i class="fas fa-edit"></i>
          </span>
          <input
            v-model="form.allocatedMisc"
            v-show="showField('allocatedMisc')"
            id="allocated-misc"
            type="text"
            class="field-value form-control"
            @focus="focusField('allocatedMisc')"
            @blur="blurField"
            maxlength="15"
          />
        </div>
        <div class="row-header" id="savingsLabel">Savings Target</div>
        <div class="grid-content" id="savingsAlloc">
          <span
            class="field-value"
            v-show="!showField('savingsTarget')"
            @click="focusField('savingsTarget')"
            >¥{{ form.savingsTarget }}
            <i class="fas fa-edit"></i>
          </span>
          <input
            v-model="form.savingsTarget"
            v-show="showField('savingsTarget')"
            id="savings-target"
            type="text"
            class="field-value form-control"
            @focus="focusField('savingsTarget')"
            @blur="blurField"
            maxlength="15"
          />
        </div>
      </div>

      <p>
        <span class="savings"
          >Savings Leeway: ¥{{
            !isNaN(this.savingsLeeway) ? this.savingsLeeway : 0
          }}</span
        >
      </p>
      <div id="button-container">
        <button
          @click="patchUserBudgetInput"
          class="budget-submit-button"
          form="budget-input-form"
        >
          Update Budget
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BudgetInput",
  props: {},
  data() {
    return {
      warningNotice: null,
      userBudget: {},
      runningGroceries: "",
      runningBills: "",
      runningTransport: "",
      runningMisc: "",
      savingsLeeway: "",
      editField: "",
      allocatedTotal: "",
      monthlyBudget: "",
      form: {
        allocatedGroceries: this.$store.state.monthlyBudget.groceries_alloc,
        allocatedBills: this.$store.state.monthlyBudget.bills_alloc,
        allocatedTransport: this.$store.state.monthlyBudget.transport_alloc,
        allocatedMisc: this.$store.state.monthlyBudget.misc_alloc,
        savingsTarget: this.$store.state.monthlyBudget.savings_target,
        monthlyIncome: this.$store.state.monthlyBudget.monthly_income,
      },
    };
  },
  mounted() {
    const groceries_id = this.$store.state.categoriesList.filter(
      (categoryObj) => categoryObj.category_name === "Groceries"
    )[0].id;
    const transport_id = this.$store.state.categoriesList.filter(
      (categoryObj) => categoryObj.category_name === "Transport"
    )[0].id;
    const misc_id = this.$store.state.categoriesList.filter(
      (categoryObj) => categoryObj.category_name === "Misc"
    )[0].id;
    const bills_id = this.$store.state.categoriesList.filter(
      (categoryObj) => categoryObj.category_name === "Bills"
    )[0].id;
    this.monthlyIncome = 0;
    this.runningGroceries = !isNaN(this.getExpenseTotals(groceries_id))
      ? this.getExpenseTotals(groceries_id)
      : 0;
    this.allocatedGroceries = 0;
    this.runningBills = !isNaN(this.getExpenseTotals(bills_id))
      ? this.getExpenseTotals(bills_id)
      : 0;
    this.allocatedBills = 0;
    this.runningTransport = !isNaN(this.getExpenseTotals(transport_id))
      ? this.getExpenseTotals(transport_id)
      : 0;
    this.allocatedTransport = 0;
    this.runningMisc = !isNaN(this.getExpenseTotals(misc_id))
      ? this.getExpenseTotals(misc_id)
      : 0;
    this.allocatedMisc = 0;
    this.savingsTarget = 0;
    this.savingsLeeway =
      Number(this.form.monthlyIncome) -
      Number(this.form.savingsTarget) -
      (Number(this.form.allocatedGroceries) +
        Number(this.form.allocatedBills) +
        Number(this.form.allocatedTransport) +
        Number(this.form.allocatedMisc));
  },
  methods: {
    getExpenseTotals(categoryID) {
      return this.$store.state.expensesList
        .filter((element) => element.category_id == categoryID)
        .reduce(
          (accumulator, currentElement) => accumulator + currentElement.amount,
          0
        );
    },
    focusField(name) {
      this.editField = name;
    },
    showField(name) {
      // showField returns TRUE if UI has to show the field whose name is passed in parameter
      // Function used in conjunction with vue directive v-show
      // https://vuejs.org/v2/api/#v-show
      return this.form[name] == "" || this.editField == name;
    },
    blurField() {
      this.editField = "";
    },
    getSavingsLeeway() {
      return (
        Number(this.form.monthlyIncome) -
        Number(this.form.savingsTarget) -
        (Number(this.form.allocatedGroceries) +
          Number(this.form.allocatedBills) +
          Number(this.form.allocatedTransport) +
          Number(this.form.allocatedMisc))
      );
    },
    budgetValidator() {
      const budgetWarnings = {
        monthlyIncome: "Monthly Income",
        savingsTarget: "Savings Target",
        allocatedGroceries: "Groceries Allocation",
        allocatedBills: "Bills Allocation",
        allocatedTransport: "Transport Allocation",
        allocatedMisc: "Misc Allocation",
      };

      for (let budget in budgetWarnings) {
        if (isNaN(this.form[budget]) || this.form[budget] == "") {
          this.warningNotice = `Please input a valid amount at ${budgetWarnings[budget]}`;
          return false;
        }
      }

      return true;
    },
    patchUserBudgetInput() {
      if (this.budgetValidator()) {
        this.savingsLeeway = this.getSavingsLeeway();

        this.$store.dispatch("updateBudget", {
          user_id: this.$store.state.user.user_id,
          monthly_budget: this.form.monthlyIncome,
          groceries_alloc: this.form.allocatedGroceries,
          bills_alloc: this.form.allocatedBills,
          transport_alloc: this.form.allocatedTransport,
          misc_alloc: this.form.allocatedMisc,
          savings_target: this.form.savingsTarget,
          monthly_income: this.form.monthlyIncome,
        });
      } else {
        alert(this.warningNotice);
      }
    },
  },
};
</script>

<style scoped>

#monthly-income {
  font-weight: bold;
}
#savings-target {
  color: green;
  font-weight: bold;
}

#budget-input-container {
  display: flex;
  flex-direction: column;
  background-color: rgba(255, 255, 255, 0.5);
  align-content: center;
}

#budget-input-grid {
  display: grid;
  gap: 10px 0;
  grid-template-areas:
    ". currentHeader allocHeader"
    "groceriesLbl groceriesCurrent groceriesAlloc"
    "billsLbl billsCurrent billsAlloc"
    "transportLbl transportCurrent transportAlloc"
    "miscLbl miscCurrent miscAlloc"
    "savingsLabel savingsLabel savingsAlloc";
}

@media (min-width: 501px) {
  .grid-row-header,
  .row-header {
    width: 100px;
    text-align: left;
    padding: 2px;
    margin-left: 30px;
    font-weight: bold;
  }
}

@media (max-width: 500px) {
  #budget-input-grid {
    justify-items: center;
    align-items: center;
    grid-template-areas:
      "currentHeader allocHeader"
      "groceriesLbl groceriesLbl"
      "groceriesCurrent groceriesAlloc"
      "billsLbl billsLbl"
      "billsCurrent billsAlloc"
      "transportLbl transportLbl"
      "transportCurrent transportAlloc"
      "miscLbl miscLbl"
      "miscCurrent miscAlloc"
      "savingsLabel     savingsAlloc";
  }

  .two-columns {
    grid-column: 1fr;
  }

  .big-row {
    margin-top: auto;
    margin-left: auto;
    font-weight: bold;
  }

  .grid-row-header,
  .row-header {
    font-weight: bold;
    margin-top: 10px;
  }
}

#currentHeader {
  grid-area: currentHeader;
}
#allocHeader {
  grid-area: allocHeader;
}
#groceriesLbl {
  grid-area: groceriesLbl;
}
#groceriesCurrent {
  grid-area: groceriesCurrent;
}
#groceriesAlloc {
  grid-area: groceriesAlloc;
}
#billsLbl {
  grid-area: billsLbl;
}
#billsCurrent {
  grid-area: billsCurrent;
}
#billsAlloc {
  grid-area: billsAlloc;
}
#transportLbl {
  grid-area: transportLbl;
}
#transportCurrent {
  grid-area: transportCurrent;
}
#transportAlloc {
  grid-area: transportAlloc;
}
#miscLbl {
  grid-area: miscLbl;
}
#miscCurrent {
  grid-area: miscCurrent;
}
#miscAlloc {
  grid-area: miscAlloc;
}
#savingsLabel {
  grid-area: savingsLabel;
  margin-top: 35px;
  font-weight: bold;
}
#savingsAlloc {
  grid-area: savingsAlloc;
  margin-top: 35px;
  font-weight: bold;
}

.big-row {
  font-weight: bold;
}

.two-columns {
  grid-column: span 2 / auto;
}

#budget-input-grid > input {
  max-width: 40px;
  color: red;
}

.budget-submit-button {
  height: 2em;
  font-size: large;
  border-radius: 5px;
  background-color: #403d58;
  color: white;
  padding-left: 2em;
  padding-right: 2em;
}
.row-header {
  font-weight: bolder;
}

.grid-col-header,
.income,
.savings {
  font-weight: bold;
  padding: 10px;
  width: 100;
}

.grid-content {
  width: 150px;
  justify-content: center;
}

.fas {
  padding-left: 20px;
}
.savings {
  font-weight: bold;
}

button:active {
  background-color: rgb(111, 176, 42);
  transform: translateY(2px);
}
</style>
