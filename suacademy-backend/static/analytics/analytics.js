const barCtx = document.getElementById("barChart");
const pieCtx = document.getElementById("pieChart");

let barChart, pieChart;

function loadData(nationality="") {
  fetch(`/admin/analytics/api/vocabulary/?nationality=${nationality}`)
    .then(res => res.json())
    .then(data => {
      if (barChart) barChart.destroy();
      if (pieChart) pieChart.destroy();

      barChart = new Chart(barCtx, {
        type: "bar",
        data: {
          labels: ["Topics", "Words"],
          datasets: [{
            label: "Vocabulary",
            data: [data.topics, data.words],
            backgroundColor: ["#4e73df", "#e74a3b"]
          }]
        }
      });

      pieChart = new Chart(pieCtx, {
        type: "pie",
        data: {
          labels: ["Topics", "Words"],
          datasets: [{
            data: [data.topics, data.words],
            backgroundColor: ["#36b9cc", "#f6c23e"]
          }]
        }
      });
    });
}

document.getElementById("nationality").addEventListener("change", e => {
  loadData(e.target.value);
});

loadData();
