from django.shortcuts import render, redirect
from django.views.generic import View
import json
from django.core.serializers.json import DjangoJSONEncoder

from .forms import ClientForm
from .models import Conso_eur, Conso_watt


class ClientFormView(View):
    def get(self, request):
        return render(request, 'dashboard/accueil.html')

    def post(self, request):
        form = ClientForm(request.POST)

        if form.is_valid():
            client_id = form.cleaned_data['client']
            return redirect('dashboard:results', client_id=client_id)


def results(request, client_id):
    conso_euro = []
    conso_watt = []
    annual_costs = [0, 0]
    is_elec_heating = True
    dysfunction_detected = False
    conso_summer = 0
    conso_winter = 0
    year = 2017
    is_elec_max_ratio = 1.1
    conso_watt_per_year = []
    annual_watt = []
    dysfunction_detected_max_ratio = 1.1

    # Conso_eur from db
    conso_euro = Conso_eur.objects.filter(client_id=client_id).values_list('year', 'janvier', 'fevrier', 'mars', \
                                                                            'avril', 'mai', 'juin', 'juillet', 'aout', \
                                                                            'septembre', 'octobre', 'novembre',
                                                                            'decembre')
    conso_euro = json.dumps(list(conso_euro), cls=DjangoJSONEncoder)

    # Conso_watt from db
    conso_watt = Conso_watt.objects.filter(client_id=client_id).values_list('year', 'janvier', 'fevrier', 'mars', \
                                                                            'avril', 'mai', 'juin', 'juillet', 'aout', \
                                                                            'septembre', 'octobre', 'novembre',
                                                                            'decembre')
    conso_watt = json.dumps(list(conso_watt), cls=DjangoJSONEncoder)

    # is_elec_heating
    conso_summer = Conso_watt.objects.filter(client_id=client_id, year=year).values_list('juin', 'juillet', 'aout', \
                                                                            'septembre')
    conso_summer = json.dumps(list(conso_summer), cls=DjangoJSONEncoder)
    conso_summer = sum(map(float, conso_summer.translate(None, '[]').split(',')))

    conso_winter = Conso_watt.objects.filter(client_id=client_id, year=year).values_list('novembre', 'decembre', 'janvier', \
                                                                            'fevrier')
    conso_winter = json.dumps(list(conso_winter), cls=DjangoJSONEncoder)
    conso_winter = sum(map(float, conso_winter.translate(None, '[]').split(',')))

    if conso_winter/conso_summer > is_elec_max_ratio:
        is_elec_heating = True
    else:
        is_elec_heating = False

    # dysfunction_detected
    for conso_watt_per_year in Conso_watt.objects.filter(client_id=client_id).values_list('year', 'janvier', 'fevrier', 'mars', \
                                                                            'avril', 'mai', 'juin', 'juillet', 'aout', \
                                                                            'septembre', 'octobre', 'novembre',
                                                                            'decembre') :
        conso_watt_per_year = json.dumps(list(conso_watt_per_year), cls=DjangoJSONEncoder)
        conso_watt_per_year = map(float, conso_watt_per_year.translate(None, '[]').split(','))
        conso_watt_per_year.pop(0)
        conso_watt_per_year = sum(conso_watt_per_year)
        annual_watt.append(conso_watt_per_year)
    
    if annual_watt[1]/annual_watt[0] > dysfunction_detected_max_ratio:
        dysfunction_detected = True
    else:
        dysfunction_detected = False
    print(annual_watt[1]/annual_watt[0])

    context = {
        "conso_euro": conso_euro,
        "conso_watt": conso_watt,
        # "annual_costs": annual_costs,
        "is_elec_heating": is_elec_heating,
        "dysfunction_detected": dysfunction_detected
    }
    return render(request, 'dashboard/results.html', context)
