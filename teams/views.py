import django.db.models
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
        query = teams.models.Team.objects.filter(
            is_published=True
        ).prefetch_related(
            teams.models.Team.technologies.field.name,
            teams.models.Team.languages.field.name,
        )

        return query


class TeamDetail(django.views.generic.DetailView):
    model = teams.models.Team
    template_name = 'teams/team_detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')

        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id or -1
        query = (
            teams.models.Team.objects.filter(
                django.db.models.Q(roleteams__members__user_id=user_id)
                | django.db.models.Q(is_published=True)
                | django.db.models.Q(creator_id=user_id)
            )
            .filter(pk=pk)
            .distinct()
        )

        team = django.shortcuts.get_object_or_404(query)

        query = query.prefetch_related(
            teams.models.Team.technologies.field.name,
            teams.models.Team.languages.field.name,
        ).first()

        members = teams.models.Member.objects.filter(
            role_team__team_id=team.id
        ).select_related('role_team__role_default')

        vacancies = teams.models.RoleTeam.objects.filter(
            team=team, members=None
        ).select_related('role_default')

        if user_id != -1:
            vacancies = vacancies.exclude(pendings__user_id=user_id)

        if user_id == team.creator_id:
            pendings = teams.models.Pending.objects.filter(
                role_team__team_id=team.id
            ).select_related('role_team__role_default')
            context['edit_form'] = teams.forms.EditTeamForm(instance=team)
            context['pendings'] = pendings

        context.update(
            {
                'team': query,
                'vacancies': vacancies,
                'members': members,
            }
        )

        return context

    def post(self, request, *args, **kwargs):
        team = teams.models.Team.objects.get(pk=kwargs.get('pk'))
        if request.user.id == team.creator_id:
            form = teams.forms.EditTeamForm(
                request.POST, request.FILES, instance=team
            )

            if form.is_valid():
                form.save()
            self.object = self.get_object()
            context = super(TeamDetail, self).get_context_data(**kwargs)
            context['edit_form'] = form
            return self.render_to_response(context=context)

        self.object = self.get_object()
        context = super(TeamDetail, self).get_context_data(**kwargs)
        return self.render_to_response(context=context)


class CreatePending(django.views.generic.View):
    def post(self, request, pk):
        role_team = django.shortcuts.get_object_or_404(
            teams.models.RoleTeam, pk=pk
        )
        if role_team.team.creator_id != self.request.user.id:
            teams.models.Pending.objects.create(
                role_team=role_team,
                user=self.request.user,
            )
            return django.shortcuts.redirect(
                'teams:team_detail', role_team.team_id
            )
        return


class RemoveMember(django.views.generic.View):
    def post(self, request, pk):
        member = django.shortcuts.get_object_or_404(teams.models.Member, pk=pk)
        if member.role_team.team.creator_id == self.request.user.id:
            member.delete()
            return django.shortcuts.redirect(
                'teams:team_detail', member.role_team.team_id
            )
        return


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
        return


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
        return
