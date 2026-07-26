// ---------- Doughnut Chart ----------

const labels = categoryData.map(item => item[0]);
const values = categoryData.map(item => item[1]);

new Chart(document.getElementById("expenseChart"), {

    type: "doughnut",

    data: {

        labels: labels,

        datasets: [{

            data: values,

            backgroundColor: [

                "#4F46E5",
                "#22C55E",
                "#F59E0B",
                "#EF4444",
                "#14B8A6",
                "#EC4899",
                "#6366F1",
                "#8B5CF6"

            ],

            borderWidth: 0

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: true,

        cutout: "70%",

        plugins: {

            legend: {

                position: "bottom",

                labels: {

                    usePointStyle: true,

                    pointStyle: "circle",

                    padding: 20,

                    font: {

                        size: 13,

                        weight: "600"

                    }

                }

            }

        }

    }

});

// ---------- Daily Expense Chart ----------

new Chart(document.getElementById("dailyChart"), {

    type: "bar",

    data: {

        labels: dailyData.map(item => item[0]),

        datasets: [{

            label: "Expenses ($)",

            data: dailyData.map(item => item[1]),

            backgroundColor: "#4F46E5",

            borderRadius: 10,

            borderSkipped: false,

            maxBarThickness: 40

        }]

    },

    options: {

        responsive: true,

        scales: {

            y: {

                beginAtZero: true,

                grid: {

                    color: "#ececec"

                }

            },

            x: {

                grid: {

                    display: false

                }

            }

        },

        plugins: {

            legend: {

                display: false

            }

        }

    }

});