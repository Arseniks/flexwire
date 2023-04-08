import django.views.generic
import django.db.models

import teams.models


class TeamsList(django.views.generic.ListView):
    model = teams.models.Team
    template_name = 'teams/teams_list.html'
    context_object_name = 'teams'

    def get_queryset(self):
        queryset = teams.models.Team.objects.filter(
            is_published=True
        ).prefetch_related(
            teams.models.Team.technologies.field.name,
            teams.models.Team.languages.field.name,
        )
        # .prefetch_related(
        #     django.db.models.Prefetch(
        #         'ro',
        #         queryset=teams.models.Member.objects.all(
        #         ).select_related('user')
        #     ),
        #     ).select_related('creator').prefetch_related(
        #         'technologies', 'languages'
        #     )

        return queryset
