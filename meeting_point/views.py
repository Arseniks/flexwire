from django.shortcuts import render
from django.views import View


class Custom404(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'status_codes/404.html', status=404)