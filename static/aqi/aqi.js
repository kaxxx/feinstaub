function getData(days) {
    console.log("days:"+days);
    if (days == undefined){
        days=1;
    }
  fetch("/fs/api/v1.0/aqi/data/last/days/"+days).then(response => {
    response.json().then(data => {
      console.log(data);
      average(data);
      //updateHtml(data[data.length-1]);
    })
  }).catch(err => {
    console.log(err);
  })
}

function average (data){
    i=0;
    ppm10s=0;
    ppm25s=0;
    data.forEach(function (element, index, names){
        ppm10s+=element.ppm10;
        ppm25s+=element.ppm25;
        i++;
    });
    data.ppm10d = (ppm10s/i).toFixed(2);
    data.ppm25d = (ppm25s/i).toFixed(2);
    console.log("ppm10d:"+data.ppm10d);
    console.log("ppm15d:"+data.ppm25d);
    updateHtml(data);
}

function updateHtml(data) {
  let aqiPm25 = calcAQIpm25(data.ppm25d);
  let aqiPm10 = calcAQIpm10(data.ppm10d);

  //update HTML
  document.getElementById("time").innerHTML = "Durchnittliche Werte für den Zeitraum:"; // should be sorted before: +data[0].time +" - "+ data[data.length-1].time;
  document.getElementById("aqiPm25").innerHTML = aqiPm25;
  document.getElementById("aqiPm10").innerHTML = aqiPm10;
  document.getElementById("pm25").innerHTML = "(PM2.5: " + data.ppm25d + " µg/m³)";
  document.getElementById("pm10").innerHTML = "(PM10: " + data.ppm10d + " µg/m³)";

  //set colors
  colorsPm25 = getColor(aqiPm25);
  colorsPm10 = getColor(aqiPm10);
  document.getElementById("containerPm25").style.background = colorsPm25.bg;
  document.getElementById("containerPm25").style.color = colorsPm25.text
  document.getElementById("containerPm10").style.background = colorsPm10.bg;
  document.getElementById("containerPm10").style.color = colorsPm10.text
}

function getColor(aqi) {
  switch (true) {
    case (aqi >= 50 && aqi < 100):
      color = "yellow";
      break;
    case (aqi >= 100 && aqi < 150):
      color = "orange";
      break;
    case (aqi >= 150 && aqi < 200):
      color = "red";
      break;
    case (aqi >= 200 && aqi < 300):
      color = "purple";
      break;
    case (aqi >= 300):
      color = "brown";
      break;
    default:
      color = "Lime";
  }
  return {bg: color, text: (aqi > 200) ? "white" : "black"};
}

function calcAQIpm25(pm25) {
  let pm1 = 0;
	let pm2 = 12;
	let pm3 = 35.4;
	let pm4 = 55.4;
	let pm5 = 150.4;
	let pm6 = 250.4;
	let pm7 = 350.4;
	let pm8 = 500.4;

	let aqi1 = 0;
	let aqi2 = 50;
	let aqi3 = 100;
	let aqi4 = 150;
	let aqi5 = 200;
	let aqi6 = 300;
	let aqi7 = 400;
	let aqi8 = 500;

	let aqipm25 = 0;

	if (pm25 >= pm1 && pm25 <= pm2) {
		aqipm25 = ((aqi2 - aqi1) / (pm2 - pm1)) * (pm25 - pm1) + aqi1;
	} else if (pm25 >= pm2 && pm25 <= pm3) {
		aqipm25 = ((aqi3 - aqi2) / (pm3 - pm2)) * (pm25 - pm2) + aqi2;
	} else if (pm25 >= pm3 && pm25 <= pm4) {
		aqipm25 = ((aqi4 - aqi3) / (pm4 - pm3)) * (pm25 - pm3) + aqi3;
	} else if (pm25 >= pm4 && pm25 <= pm5) {
		aqipm25 = ((aqi5 - aqi4) / (pm5 - pm4)) * (pm25 - pm4) + aqi4;
	} else if (pm25 >= pm5 && pm25 <= pm6) {
		aqipm25 = ((aqi6 - aqi5) / (pm6 - pm5)) * (pm25 - pm5) + aqi5;
	} else if (pm25 >= pm6 && pm25 <= pm7) {
		aqipm25 = ((aqi7 - aqi6) / (pm7 - pm6)) * (pm25 - pm6) + aqi6;
	} else if (pm25 >= pm7 && pm25 <= pm8) {
		aqipm25 = ((aqi8 - aqi7) / (pm8 - pm7)) * (pm25 - pm7) + aqi7;
	}
	return aqipm25.toFixed(0);
}

function calcAQIpm10(pm10) {
	let pm1 = 0;
	let pm2 = 54;
	let pm3 = 154;
	let pm4 = 254;
	let pm5 = 354;
	let pm6 = 424;
	let pm7 = 504;
	let pm8 = 604;

	let aqi1 = 0;
	let aqi2 = 50;
	let aqi3 = 100;
	let aqi4 = 150;
	let aqi5 = 200;
	let aqi6 = 300;
	let aqi7 = 400;
	let aqi8 = 500;

	let aqipm10 = 0;

	if (pm10 >= pm1 && pm10 <= pm2) {
		aqipm10 = ((aqi2 - aqi1) / (pm2 - pm1)) * (pm10 - pm1) + aqi1;
	} else if (pm10 >= pm2 && pm10 <= pm3) {
		aqipm10 = ((aqi3 - aqi2) / (pm3 - pm2)) * (pm10 - pm2) + aqi2;
	} else if (pm10 >= pm3 && pm10 <= pm4) {
		aqipm10 = ((aqi4 - aqi3) / (pm4 - pm3)) * (pm10 - pm3) + aqi3;
	} else if (pm10 >= pm4 && pm10 <= pm5) {
		aqipm10 = ((aqi5 - aqi4) / (pm5 - pm4)) * (pm10 - pm4) + aqi4;
	} else if (pm10 >= pm5 && pm10 <= pm6) {
		aqipm10 = ((aqi6 - aqi5) / (pm6 - pm5)) * (pm10 - pm5) + aqi5;
	} else if (pm10 >= pm6 && pm10 <= pm7) {
		aqipm10 = ((aqi7 - aqi6) / (pm7 - pm6)) * (pm10 - pm6) + aqi6;
	} else if (pm10 >= pm7 && pm10 <= pm8) {
		aqipm10 = ((aqi8 - aqi7) / (pm8 - pm7)) * (pm10 - pm7) + aqi7;
	}
	return aqipm10.toFixed(0);
}