$(document).ready(function(){
    'use strict';

    Chart.defaults.global.defaultFontColor = '#75787c';

    var endpoint = 'api/test/data';
    var api_labels = api_data = [];

    $.ajax({
        method: 'GET',
        url: endpoint,
        success: function(data){
            api_labels = data.labels
            api_data =-data.data
            buildChart()
        },
        error: function(error_data){
            console.log("error")
        }
    })

    function buildChart(){
        var BARCHART1 = $('#barChartCustom1');
        var barChartHome = new Chart(BARCHART1, {
            type: 'bar',
            options:
            {
                scales:
                {
                    xAxes: [{
                        display: true,
                        barPercentage: 0.2
                    }],
                    yAxes: [{
                        ticks: {
                            max: 100,
                            min: 0
                        },
                        display: false
                    }],
                },
                legend: {
                    display: false
                }
            },
            data: {
                labels: api_labels,
                datasets: [
                    {
                        label: "Data Set 1",
                        backgroundColor: [
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99'
                        ],
                        borderColor: [
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99',
                            '#EF8C99'
                        ],
                        borderWidth: 0.3,
                        data: api_data
                    }
                ]
            }
        }
    })


})