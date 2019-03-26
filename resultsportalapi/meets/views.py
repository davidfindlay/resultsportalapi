import datetime

from rest_framework.decorators import APIView
from rest_framework import viewsets
from django.http import JsonResponse

from resultsportalapi.scrape.results_portal_scrape import ResultsPortalScrape
from resultsportalapi.models.courses import Courses

# Create your views here.
class MeetListView(APIView):

    rp = ResultsPortalScrape()

    def get(self, request, format=None):

        now = datetime.datetime.now()
        year = now.year

        state_list = ['QLD', 'NSW', 'VIC', 'TAS', 'SA', 'NT', 'WA', '---']

        meet_list = []

        for state in state_list:

            meets = self.rp.get_events(year, state)

            for meet in meets:
                meet_list.append(meet.to_dict())

        return JsonResponse(meet_list, safe=False)


class MeetResultsView(APIView):

    rp = ResultsPortalScrape()

    def get(self, request, meet_id, format=None):

        results = self.rp.get_event_results(meet_id)

        result_list = []
        for result in results:
            result_list.append(result.to_list_item())

        return JsonResponse(result_list, safe=False)
