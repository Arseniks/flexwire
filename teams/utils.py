def pull_out_list(request, name):
    technology_pks = request.POST.getlist(name)[0]
    if technology_pks:
        temp_dict = request.POST.copy()
        temp_dict.setlist(name, technology_pks.split(','))
        request.POST = temp_dict
