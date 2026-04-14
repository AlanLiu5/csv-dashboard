

let chartInstance = null;

async function updateChart() {
    const group_by = document.getElementById("group_by").value;
    const metric = document.getElementById("metric").value;
    const field = document.getElementById("field").value;
    const city = document.getElementById("city").value;
    const k = document.getElementById("k").value;
    const errorBox = document.getElementById("error");
    const resultDiv = document.getElementById("result");

    if (k === "" || Number(k) <= 0) {
        errorBox.textContent = "k must be greater than 0";
        return;
    }

    errorBox.textContent = "";

    const url = `/analyze?group_by=${group_by}&metric=${metric}&field=${field}&city=${encodeURIComponent(city)}&k=${k}`;

    try {
        const res = await fetch(url);

        if (!res.ok) {
            throw new Error(`HTTP error: ${res.status}`);
        }

        const data = await res.json();

        if (data.error) {
            errorBox.textContent = data.error;
            return;
        }

        if (!data.results || data.results.length === 0) {
            resultDiv.innerHTML = "<p>No data found.</p>";

            if (chartInstance) {
                chartInstance.destroy();
                chartInstance = null;
            }
            return;
        }

        document.getElementById("params-box").innerHTML = `
            <div><b>group_by:</b> ${group_by}</div>
            <div><b>metric:</b> ${metric}</div>
            <div><b>field:</b> ${field}</div>
            <div><b>city:</b> ${city}</div>
            <div><b>k:</b> ${k}</div>
        `;

        let html = "";
        const labels = [];
        const values = [];
        let htmlplus="";

        htmlplus += `<h3>Summary</h3>`;
        htmlplus += `<p>total_rows: ${data.summary.total_rows}</p>`;
        htmlplus += `<p>after_filter: ${data.summary.after_filter}</p>`;
        htmlplus += `<p>group_by: ${data.summary.group_by}</p>`;
        htmlplus += `<p>metric: ${data.summary.metric}</p>`;
        htmlplus += `<p>field: ${data.summary.field}</p>`;
        htmlplus += `<p>city: ${data.summary.city}</p>`;
        htmlplus += `<p>k: ${data.summary.k}</p>`;


        htmlplus += `<h3>Insight</h3>`;
        data.insight.forEach(line => {
            htmlplus += `<p>${line}</p>`;
        });

        data.results.forEach(item => {
            html += `<p>${item.group}: ${item.value}</p>`;
            labels.push(item.group);
            values.push(item.value);
        });

        resultDiv.innerHTML = html+htmlplus;

        const ctx = document.getElementById("myChart");

        if (chartInstance) {
            chartInstance.destroy();
        }

        chartInstance = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: metric,
                        data: values
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true
                    }
                }
            }
        });
    } catch (err) {
        errorBox.textContent = "Failed to fetch data or draw chart.";
        console.log(err);
    }
}

updateChart();
