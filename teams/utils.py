def pull_out_technologies(request):
    technology_pks = request.POST.getlist('technologies')[0]
    if technology_pks:
        temp_dict = request.POST.copy()
        temp_dict.setlist('technologies', technology_pks.split(','))
        request.POST = temp_dict
