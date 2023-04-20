const RAPIDAPI_API_URL = 'http://localhost:5055/get_data/';
//const RAPIDAPI_API_URL = 'http://localhost:5013/get_data/';
//const RAPIDAPI_API_URL = 'http://192.168.0.2:5013/get_data/';
const RAPIDAPI_REQUEST_HEADERS = {
          'X-RapidAPI-Host': 'arjunkomath-jaas-json-as-a-service-v1.p.rapidapi.com'
          , 'X-RapidAPI-Key': '7xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
          , 'Content-Type': 'application/json'
        };

function get_draw_ok_nok(period, type_info){
    console.log('Hola: ' + period + "  --- " + type_info);
    axios.get(`${RAPIDAPI_API_URL}`+period+'/'+type_info, { headers: RAPIDAPI_REQUEST_HEADERS }).then(response => {
    console.log(response.data['date_end']);
    // before updating, check if the data has changed ... 
    if (response.data['tot_ok'] != window.metrics2['tot_ok'] ||  response.data['tot_nok'] != window.metrics2['tot_nok']){
        window.metrics2 = response.data;
        document.getElementById("info_metrics").innerHTML = "Total of OK parts: " + window.metrics2['tot_ok'] + 
          " &emsp;&emsp; Total of NOK parts:" + window.metrics2['tot_nok'];
          console.log("  ok: " + response.data['tot_ok'] + "  nok: " + response.data['tot_nok']);
      chart_draw();
    }
    
  }).catch(error => console.error('On get student error', error))
  }

function get_draw_working_time(period, type_info){
    console.log('Hola: ' + period + "  --- " + type_info);
    axios.get(`${RAPIDAPI_API_URL}`+period+'/'+type_info, { headers: RAPIDAPI_REQUEST_HEADERS }).then(response => {
    console.log(response.data['date_end']);
    // before updating, check if the data has changed ... 
    if (response.data['tot_ok'] != window.metrics2['tot_ok'] ||  response.data['tot_nok'] != window.metrics2['tot_nok']){
        window.metrics2 = response.data;
        document.getElementById("info_metrics").innerHTML = "Avg: " + window.metrics2['avg'].toFixed(3) + 
        "&emsp; Std: " + window.metrics2['std'].toFixed(3) + 
        "&emsp; Min: " + window.metrics2['min'] + 
        "&emsp; Max: " + window.metrics2['max'];
        console.log("  ok: " + response.data['tot_ok'] + "  nok: " + response.data['tot_nok']);
        chart_working_time_draw();
    }
    
  }).catch(error => console.error('On get student error', error))
  }

function chart_working_time_draw(){
    data_labels = [];
    for(let i = 0; i < window.metrics2.data['id'].length; i++){
        data_labels.push(i);
    }
    console.log(data_labels);
    data_ = []
    for(let i = 0; i < window.metrics2.data['working_time'].length; i++){
        data_.push(window.metrics2.data['working_time'][i]);
    }
    console.log(data_);

    new Chart(document.getElementById("myCanvasTime"), {
        type: 'line',
        data: {
          labels: data_labels,
          datasets: [{
              data: data_,
              label: "Parts",
              borderColor: "#3e95cd",
              fill: true
            }, 
          ]
        },
        options: {
          title: {
            display: true,
            text: 'Working time of OK parts period: '+ window.metrics2['date_start'] + ' - ' + window.metrics2['date_end'],
            maintainAspectRatio: false,
            responsive: true,
          },
          hover: {
           mode: 'index',
           intersect: true
          },
        }
      });

}

  function chart_draw(){
    console.log(" chart_draw:::   ok: " + window.metrics2['tot_ok'] + "  nok: " + window.metrics2['tot_nok']);
    //data__ = [parseInt(window.metrics2['tot_ok']), parseInt(window.metrics2['tot_nok'])];
    //data__ = [10, 10];
    //console.log(data__[0] * 2)
    // Bar chart
new Chart(document.getElementById("myCanvas"), {
  type: 'bar',
  data: {
    labels: ['Tot. OK', 'Tot. NOK'],
    datasets: [
      {
        label: "Parts information",
        backgroundColor: ["#00aa00", "#aa0000"],
        //data: [{{metrics['tot_ok']}}, {{metrics['tot_nok']}}]
        //data: data__ 
        data: [window.metrics2['tot_ok'], window.metrics2['tot_nok']]
      }
    ]
  },
  options: {
    legend: { display: false },
    title: {
      display: true,
      text: 'Total of parts in the period: '+ window.metrics2['date_start'] + ' - ' + window.metrics2['date_end'],
        maintainAspectRatio: false,
        responsive: true,
    },
    scales: {
      yAxes: [{
          display: true,
          stacked: true,
          ticks: {
              min: 0, // minimum value
              max: Math.max(window.metrics2['tot_ok'], window.metrics2['tot_nok']) // maximum value
          }
      }]
  }
  }
});
}

function openserverurl(url){
  window.location.href=url
}