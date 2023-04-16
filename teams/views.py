import django.contrib.auth.mixins
import django.db.models
import django.http.request
import django.shortcuts
import django.views.generic

import teams.forms
import teams.models


class TeamsList(django.views.generic.ListView):
    model = teams.models.Team
    template_name = 'teams/teams_list.html'
    paginate_by = 3
    context_object_name = 'teams'

    def get_queryset(self):
        return teams.models.Team.objects.get_team_list(self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = teams.forms.SearchForm()
        return context

    def post(self, request):
        technologies = request.POST.getlist('technologies')
        languages = request.POST.getlist('language')
        search = request.POST.getlist('value')
        form = teams.forms.SearchForm(request.POST)

        query = super().get_queryset()

        if technologies:
            query = query.filter(technologies__id__in=technologies)

        if languages:
            query = query.filter(language_id__in=languages)

        if search:
            search = search[0]
            query = query.filter(
                django.db.models.Q(title__icontains=search)
                | django.db.models.Q(description__icontains=search)
            )
        self.object_list = query
        return super().render_to_response(
            {'teams': query.all(), 'form': form, 'value': search}
        )


class TeamDetail(django.views.generic.DetailView):
    model = teams.models.Team
    template_name = 'teams/team_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id or -1

        team = kwargs.get('team') or django.shortcuts.get_object_or_404(
            teams.models.Team.objects.get_team_by_pk(
                user_id, self.kwargs.get('pk')
            )
        )

        members = teams.models.Member.objects.get_members(team.id).all()
        vacancies = teams.models.RoleTeam.objects.get_vacancies(team.id)

        language = team.language
        technologies = team.technologies.all()

        if user_id != -1:
            vacancies = vacancies.exclude(pendings__user_id=user_id)

        if user_id == team.creator_id:
            pendings = teams.models.Pending.objects.get_pendings(team.id)
            context['pendings'] = pendings
            context['edit_form'] = teams.forms.TeamForm(
                instance=team,
            )

        context.update(
            {
                'team': team,
                'technologies': technologies,
                'language': language,
                'vacancies': vacancies,
                'members': members,
            }
        )

        return context

    def post(self, request, *args, **kwargs):
        team = django.shortcuts.get_object_or_404(
            teams.models.Team.objects.get_team_by_pk(
                self.request.user.id, self.kwargs.get('pk')
            )
        )
        if request.user.id == team.creator_id:
            form = teams.forms.TeamForm(
                request.POST, request.FILES, instance=team
            )

            if form.is_valid():
                form.save()
                return django.shortcuts.redirect(
                    'teams:team_detail', pk=team.id
                )

            self.object = self.get_object()
            context = super(TeamDetail, self).get_context_data(**kwargs)
            context['edit_form'] = form
            return super(TeamDetail, self).render_to_response(context=context)

        return django.shortcuts.redirect('teams:team_detail', pk=team.id)


class CreatePending(django.views.generic.View):
    def post(self, request, pk):
        role_team = django.shortcuts.get_object_or_404(
            teams.models.RoleTeam, pk=pk
        )
        is_exists = teams.models.Pending.objects.filter(
            user=self.request.user, role_team=role_team
        ).exists()

        if role_team.team.creator_id != self.request.user.id and not is_exists:
            teams.models.Pending.objects.create(
                role_team=role_team,
                user=self.request.user,
            )
        return django.shortcuts.redirect(
            'teams:team_detail', role_team.team_id
        )


class RemoveMember(django.views.generic.View):
    def post(self, request, pk):
        member = django.shortcuts.get_object_or_404(teams.models.Member, pk=pk)
        if member.role_team.team.creator_id == self.request.user.id:
            member.delete()
        return django.shortcuts.redirect(
            'teams:team_detail', member.role_team.team_id
        )


class AcceptPending(django.views.generic.View):
    def post(self, request, pk):
        pending = django.shortcuts.get_object_or_404(
            teams.models.Pending, pk=pk
        )
        if pending.role_team.team.creator_id == self.request.user.id:
            pending.delete()
            teams.models.Member.objects.create(
                role_team=pending.role_team, user=pending.user
            )
        return django.shortcuts.redirect(
            'teams:team_detail', pending.role_team.team_id
        )


class RejectPending(django.views.generic.View):
    def post(self, request, pk):
        pending = django.shortcuts.get_object_or_404(
            teams.models.Pending, pk=pk
        )
        if pending.role_team.team.creator_id == self.request.user.id:
            pending.delete()
        return django.shortcuts.redirect(
            'teams:team_detail', pending.role_team.team_id
        )


class CreateTeam(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.CreateView,
):
    model = teams.models.Team
    form_class = teams.forms.TeamForm
    template_name = 'teams/create_team.html'

    def form_valid(self, form, *args, **kwargs):
        form.instance.creator = self.request.user
        return super(CreateTeam, self).form_valid(form)
