// Conso per year
conso_euro = (JSON.parse(conso_euro));
conso_euro.forEach(function(element) {
  year = element[0];
  element.shift();
  sum = 0;
  $.each(element,function(){sum+=parseFloat(this) || 0;});
  sum = Math.round(sum);
  $( ".annual_costs" ).append( "<p>Année : "+year+", dépense : "+sum+"€</p>" );
});

// Plot conso for 2017
conso_watt = (JSON.parse(conso_watt));
var options = {
    series: {
        lines: { show: true },
        points: { show: true }
    },
    xaxes: [ {min: 1, max: 12 } ],
};

data = [[1, conso_watt[1][1]], [2, conso_watt[1][2]],[3, conso_watt[1][3]],[4, conso_watt[1][4]],[5, conso_watt[1][5]],
[6, conso_watt[1][6]],[7, conso_watt[1][7]],[8, conso_watt[1][8]],[9, conso_watt[1][9]],[10, conso_watt[1][10]],
[11, conso_watt[1][11]],[12, conso_watt[1][12]]];
var dataset = [{label: "2017",data: data}];

$(document).ready(function () {$.plot($("#flot-placeholder"),dataset, options);});

//Is elec heating ?
if (is_elec_heating == "True") {$( ".is_elec_heating" ).append( "<p>Oui</p>" );
}else if (is_elec_heating == "False")  {
    $( ".is_elec_heating" ).append( "<p>Non</p>" );
}

//Dysfunction_detected ?
console.log(dysfunction_detected)
if (dysfunction_detected == "True") {$( ".dysfunction_detected" ).append( "<p>Oui</p>" );
}else if (dysfunction_detected == "False")  {
    $( ".dysfunction_detected" ).append( "<p>Non</p>" );
}
