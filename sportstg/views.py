import requests
import datetime
from genderize import Genderize

from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import APIView
from rest_framework import status

from bs4 import BeautifulSoup


# Create your views here.
class CheckFinancial(APIView):

    def get(self, request, member_id="", format=None):

        s = requests.Session()

        portalURL = "https://console.sportstg.com/"
        imguser = request.META.get('HTTP_SPORTSTG_USER', '')
        imgpass = request.META.get('HTTP_SPORTSTG_PASSWORD', '')

        if imguser == '' or imgpass == '':
            return Response('SportsTG Username and Password must be set in header!',
                            status=status.HTTP_401_UNAUTHORIZED)

        if member_id != "":
            firstname = ""
            lastname = ""
            tech_number = ""
        else:

            firstname = request.query_params.get('firstname', '')
            lastname = request.query_params.get('lastname', '')
            tech_number = request.query_params.get('technumber', '')

        member_number = member_id

        print("Member Number %s" % member_id)

        if member_number == '' and firstname == '' and lastname == '' and tech_number == '':
            return Response('Member Number or Query Parameters must be provided!',
                            status=status.HTTP_400_BAD_REQUEST)

        login = s.post(portalURL + "login/index.cfm", data={'fuseaction': 'Process_Validate_Login',
                                                                     'Username': imguser,
                                                                     'Password': imgpass,
                                                                     'Login': 'Login'})

        if login.status_code != 200:
            return Response("Unable to login to SportsTG", status=status.HTTP_503_SERVICE_UNAVAILABLE)

        members_page = s.get(portalURL + "/level2members/index.cfm?fuseaction=display_landing")

        if members_page.status_code != 200:
            return Response("Unable to reach members section", status=status.HTTP_503_SERVICE_UNAVAILABLE)

        network_search_page = s.get(portalURL + "membersnetwork/index.cfm?fuseaction=display_search")

        if network_search_page.status_code != 200:
            return Response("Unable to reach network search page", status=status.HTTP_503_SERVICE_UNAVAILABLE)

        network_search_query = s.post(portalURL + "membersnetwork/index.cfm",
                                             data={
                                                 "fuseaction": "Process_Validate_Search",
                                                 "FirstName": firstname,
                                                 "LastName": lastname,
                                                 "MembershipNumber": member_number,
                                                 "CompetitionNumber": tech_number
                                             })

        soup = BeautifulSoup(network_search_query.text, 'html5lib')

        list_table = soup.find("table", {"class": "listing"})

        if list_table is None:
            return Response("Unable to get member details!", status=status.HTTP_503_SERVICE_UNAVAILABLE)

        list_table_body = list_table.find("tbody")

        if list_table_body is None:
            return Response("Unable to get member details!", status=status.HTTP_503_SERVICE_UNAVAILABLE)

        list_table_rows = list_table_body.find_all("tr")

        if list_table is None:
            return Response("Unable to find member based on these parameters!", status=status.HTTP_404_NOT_FOUND)

        member_list = []

        for row in list_table_rows:

            list_table_cells = row.find_all("td")
            member_name = list_table_cells[0].text
            club = list_table_cells[1].text
            dob = list_table_cells[2].text
            dob_obj = datetime.datetime.strptime(dob, '%d-%b-%Y')
            dob_out = dob_obj.strftime('%Y-%m-%d')
            number = list_table_cells[3].text
            membership_status = list_table_cells[5].text

            if club is not None and "\n" in club:
                split_data = club.split("\n")
                if len(split_data) >= 3:
                    club_name = split_data[1].strip()
                    branch_name = split_data[2].strip()
                else:
                    club_name = ""
                    branch_name = ""
            else:
                club_name = ""
                branch_name = ""

            if membership_status is not None:

                if "Yes" in membership_status:
                    financial = "Yes"
                elif "No" in membership_status:
                    financial = "No"
                else:
                    financial = "n/a"

                if "Active" in membership_status:
                    active = "Active"
                elif "Inactive" in membership_status:
                    active = "Inactive"
                else:
                    active = "n/a"

            else:
                financial = "n/a"
                active = "n/a"

            name_split = member_name.split(',')
            first_name = name_split[1].strip()
            surname = name_split[0].strip()

            genderize = Genderize(timeout=2)
            gender_data = genderize.get([first_name])

            gender = "n/a"
            if gender_data is not None and len(gender_data) > 0:
                gender = gender_data[0]['gender'].title()

            member = {
                "memberName": member_name,
                "firstName": first_name,
                "surname": surname,
                "membershipNumber": number,
                "club": club_name,
                "branch": branch_name,
                "dateOfBirth": dob_out,
                "gender": gender,
                "financialStatus": financial,
                "active": active
            }

            member_list.append(member)

        return JsonResponse(member_list, safe=False)
