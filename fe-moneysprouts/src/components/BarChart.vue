<script>
import { Bar } from "vue-chartjs";

export default {
  extends: Bar,
  props: {},
  name: "EcoActionsProgress",
  data: () => ({
    chartOptions: {},
  }),
  methods: {
    setChartData() {
      this.setChartData = {
        labels: [
          "Eco-bag/No bag",
          "No impulse purchase",
          "Eco-conscious transport",
        ],
        datasets: [
          {
            barPercentage: 1,
            barThickness: 50,
            data: [
              this.getEcoBagActionTotal(),
              this.getNoImpulseBuyActionTotal(),
              this.getTransportActionTotal(),
            ],
            backgroundColor: ["#004D48", "#00716A", "#00968C"],
            borderColor: ["rgb(0, 0, 0)"],
          },
        ],
      };
    },
  },
  mounted() {
    this.ecoActionsList = this.$store.state.ecoActionsList;
    (this.getEcoBagActionTotal = () => {
      let bagActionArray = this.ecoActionsList.filter(
        (element) =>
          element.eco_goal_id ==
          this.$store.state.ecoGoalsList.filter(
            (ecoGoalObj) => ecoGoalObj.goal_name === "Eco bag/no bag"
          )[0].id
      );
      return (bagActionArray.length / this.ecoActionsList.length) * 100;
    }),
      (this.getNoImpulseBuyActionTotal = () => {
        let noImpulseBuyActionArray = this.ecoActionsList.filter(
          (element) =>
            element.eco_goal_id ==
            this.$store.state.ecoGoalsList.filter(
              (ecoGoalObj) => ecoGoalObj.goal_name === "No impulse purchase"
            )[0].id
        );
        return (
          (noImpulseBuyActionArray.length / this.ecoActionsList.length) * 100
        );
      }),
      (this.getTransportActionTotal = () => {
        let transportActionArray = this.ecoActionsList.filter(
          (element) =>
            element.eco_goal_id ==
            this.$store.state.ecoGoalsList.filter(
              (ecoGoalObj) => ecoGoalObj.goal_name === "Eco conscious tranport"
            )[0].id
        );
        return (transportActionArray.length / this.ecoActionsList.length) * 100;
      }),
      this.setChartData();
    this.chartOptions = {
      legend: { display: false },
      scales: {
        yAxes: [
          {
            ticks: {
              min: 0,
              max: 100,
              beginAtZero: true,
              callback: function (value) {
                return ((value / 100) * 100).toFixed(0) + "%";
              },
            },
          },
        ],
        xAxes: [
          {
            ticks: {
              fontColor: "black",
            },
          },
        ],
      },
    };
    this.renderChart(this.setChartData, this.chartOptions);
  },
  watch: {
    savingsScore: function (newVal, oldVal) {
      this.setChartData(this.$props.savingsScore);
      newVal;
      oldVal;
      if (this.$data._chart) {
        this.$data._chart.destroy();
      }
      this.renderChart(this.setChartData, this.chartOptions);
    },
  },
};
</script>

<style scoped>
.chartContainer {
  width: 80%;
  max-width: 350px;
}
</style>
