from django.shortcuts import render
from os.path import join
from Items.models import Items
from Monsters.models import Monsters 
from Jobs.models import Jobs
from Skills.models import Skills
from Attributes.models import Attributes 
from Maps.models import Maps
from Dashboard.models import Version

# Create your views here.
APP_NAME = "Dashboard"

def index(request):

	FUNCT_NAME = 'index'
	if 'q' in request.GET:
		query = request.GET['q']
		data = {}
		data['item'] = list(Items.objects.filter(name__icontains = query))
		data['item_len'] = len(data['item'])
		data['item'] = data['item'] [:5]

		data['monster'] = list(Monsters.objects.filter(name__icontains = query))
		data['monster_len'] = len(data['monster'])
		data['monster'] = data['monster'] [:5]
		data['query'] = query

		data['maps'] = list(Maps.objects.filter(name__icontains=query))
		data['maps_len'] = len(data['maps'])
		data['maps'] = data['maps'][:5]

		data['jobs'] = list(Jobs.objects.filter(name__icontains=query))
		data['jobs_len'] = len(data['jobs'])
		data['jobs'] = data['jobs'][:5]

		att = list(Attributes.objects.filter(name__icontains=query))

		
		data['attributes_len'] = len(att)
		data['attributes'] = []
		for i in att[:5]:
			i.descriptions = i.descriptions.split("{nl}")
			data['attributes'].append(i)

		data['skills'] = list(Skills.objects.filter(name__icontains=query))
		data['skills_len'] = len(data['skills'])
		data['skills'] = data['skills'][:5]

		return render(request, join(APP_NAME,"search.html"), data)	
	else:
		ver = Version.objects.latest('created')
		context = {"version" : ver.version}
		return render(request, join(APP_NAME,"index.html"), context)
