from collections import defaultdict, Counter
from datetime import datetime
from json import JSONDecodeError

import requests
import pycountry
import os
from parent_parser import Parser
from row_objects import CostRow, RevenueRow


class MobifreakParser(Parser):
    """
    Парсер MobiFreak
    """
    required_auth_fields = ('api_key', )

    def _get_country_code(self, country_name):
        try:
            return pycountry.countries.get(name=country_name).alpha_2
        except KeyError:
            fix_pycountry = {
                "The Bahamas": "BS",
                "Bolivia": 'BO',
                "Brunei": "BN",
                "People's Republic of China": "CN",
                "Republic of China": "CN",
                "Cote d'Ivoire": "CI",
                "Falkland Islands": "FK",
                "The Gambia": "GM",
                "Iran": "IR",
                "North Korea": "KP",
                "South Korea": "KR",
                "Kosovo": "XK",
                "Laos": "LA",
                "Macau": "MO",
                "Macedonia": "MK",
                "Micronesia": "FM",
                "Moldova": "MD",
                "Nagorno-Karabakh": "AZ",
                "Netherlands Antilles": "AN",
                "Turkish Republic of Northern Cyprus": "CY",
                "Northern Mariana": "MP",
                "Palestine": "PS",
                "Pitcairn Islands": "PN",
                "Russia": "RU",
                "Saint Barthelemy": "BL",
                "Saint Helena": "SH",
                "Saint Martin": "MF",
                "Somaliland": "SO",
                "South Ossetia": "GE",
                "Svalbard": "SJ",
                "Syria": "SY",
                "Taiwan": "TW",
                "Tanzania": "TZ",
                "Transnistria Pridnestrovie": "MD",
                "Tristan da Cunha": "SH",
                "Vatican City": "VA",
                "Venezuela": "VE",
                "Vietnam": "VN",
                "British Virgin Islands": "VG",
                "US Virgin Islands": "VI",
                "Ivory Coast": "IC",
            }
            try:
                return fix_pycountry[country_name]
            except KeyError:
                return country_name

    def _make_request(self, **kwargs):
        """
        Сделать запрос к мобифрику, проверить на валидность, вернуть результат
        """
        _dict = defaultdict(lambda: {'clicks': 0, 'payout': 0})

        access_token = self.auth['api_key']
        kwargs['params'].update({
            'items': 100,
        })

        while kwargs['url'] is not None:
            res = requests.request(**kwargs, headers={'Authorization': access_token})
            try:
                response = res.json()
                for res in response['data']:
                    country = self._get_country_code(res['country'])
                    _dict[country]['clicks'] += int(res['clicks'])
                    _dict[country]['payout'] += float(res['payout'])
                kwargs['url'] = response['next_page_url']
            except JSONDecodeError:
                self._raise_error('Error')

        return _dict or []

    def revenue_countries(self, date, zone_id, zone_subid):
        data = self._make_request(
            url='https://publishersapi.mobifreak.org/v1/publisher/stats',
            params={
                'date_from': date.strftime('%Y-%m-%d'),
                'date_to': date.strftime('%Y-%m-%d'),
                'domain': zone_id,
            },
            method='GET'
        )

        rows = []
        for row in data:
            visits = int(data[row]['clicks'])
            country_code = row
            revenue = float(data[row]['payout'])
            rows.append(
                RevenueRow(
                    name=country_code,
                    date=date,
                    visits=visits,
                    revenue=revenue
                )
            )

        return rows


if __name__ == '__main__':

    parser = MobifreakParser(
        auth={
            'api_key': os.environ.get('MOBIFREAK_API_KEY'),
        },
    )

    data = parser.revenue_countries(
        date=datetime(2017, 8, 8).date(),
        zone_id=25966,
        zone_subid=None
    )

    for row in data:
        print(row)

    """
    Вызов revenue_countries для этих данных должен вернуть вот такие значения:
    
    name:MX,date:2017-08-08,visits:86,revenue:0.1046
    name:YE,date:2017-08-08,visits:6,revenue:0.0859
    name:CN,date:2017-08-08,visits:309,revenue:0.0227
    name:IL,date:2017-08-08,visits:48,revenue:0.0
    name:TW,date:2017-08-08,visits:2624,revenue:0.0
    name:IT,date:2017-08-08,visits:363,revenue:0.0
    name:GB,date:2017-08-08,visits:5385,revenue:0.0
    name:ES,date:2017-08-08,visits:1210,revenue:0.0
    name:BG,date:2017-08-08,visits:18,revenue:0.0
    name:ME,date:2017-08-08,visits:6,revenue:0.0
    name:FI,date:2017-08-08,visits:20,revenue:0.0
    name:PL,date:2017-08-08,visits:104,revenue:0.0
    name:AU,date:2017-08-08,visits:3108,revenue:0.0
    name:RS,date:2017-08-08,visits:12,revenue:0.0
    name:RU,date:2017-08-08,visits:1377,revenue:0.0
    name:FR,date:2017-08-08,visits:1345,revenue:0.0
    name:US,date:2017-08-08,visits:10211,revenue:0.0
    name:BE,date:2017-08-08,visits:99,revenue:0.0
    name:BR,date:2017-08-08,visits:126,revenue:0.0
    name:CA,date:2017-08-08,visits:13362,revenue:0.0
    name:VN,date:2017-08-08,visits:1334,revenue:0.0
    name:KR,date:2017-08-08,visits:740,revenue:0.0
    name:AT,date:2017-08-08,visits:17,revenue:0.0
    name:AR,date:2017-08-08,visits:44,revenue:0.0
    name:TH,date:2017-08-08,visits:1854,revenue:0.0
    name:EG,date:2017-08-08,visits:489,revenue:0.0
    name:RO,date:2017-08-08,visits:42,revenue:0.0
    name:PR,date:2017-08-08,visits:10,revenue:0.0
    name:NP,date:2017-08-08,visits:3,revenue:0.0
    name:PH,date:2017-08-08,visits:883,revenue:0.0
    name:PT,date:2017-08-08,visits:143,revenue:0.0
    name:SE,date:2017-08-08,visits:102,revenue:0.0
    name:NL,date:2017-08-08,visits:582,revenue:0.0
    name:MY,date:2017-08-08,visits:63,revenue:0.0
    name:JP,date:2017-08-08,visits:83,revenue:0.0
    name:SI,date:2017-08-08,visits:6,revenue:0.0
    name:SK,date:2017-08-08,visits:10,revenue:0.0
    name:HK,date:2017-08-08,visits:16,revenue:0.0
    name:ID,date:2017-08-08,visits:2,revenue:0.0
    name:DE,date:2017-08-08,visits:211,revenue:0.0
    name:AZ,date:2017-08-08,visits:18,revenue:0.0
    name:DZ,date:2017-08-08,visits:9,revenue:0.0
    name:PK,date:2017-08-08,visits:126,revenue:0.0
    name:CR,date:2017-08-08,visits:5,revenue:0.0
    name:BD,date:2017-08-08,visits:14,revenue:0.0
    name:HT,date:2017-08-08,visits:3,revenue:0.0
    name:SG,date:2017-08-08,visits:251,revenue:0.0
    name:IQ,date:2017-08-08,visits:18,revenue:0.0
    name:CO,date:2017-08-08,visits:45,revenue:0.0
    name:MM,date:2017-08-08,visits:12,revenue:0.0
    name:BA,date:2017-08-08,visits:3,revenue:0.0
    name:SV,date:2017-08-08,visits:1,revenue:0.0
    name:CL,date:2017-08-08,visits:247,revenue:0.0
    name:TR,date:2017-08-08,visits:4,revenue:0.0
    name:LY,date:2017-08-08,visits:4,revenue:0.0
    name:UA,date:2017-08-08,visits:54,revenue:0.0
    name:GE,date:2017-08-08,visits:21,revenue:0.0
    name:HN,date:2017-08-08,visits:10,revenue:0.0
    name:RE,date:2017-08-08,visits:22,revenue:0.0
    name:PE,date:2017-08-08,visits:23,revenue:0.0
    name:IR,date:2017-08-08,visits:5,revenue:0.0
    name:KH,date:2017-08-08,visits:124,revenue:0.0
    name:BS,date:2017-08-08,visits:6,revenue:0.0
    name:CZ,date:2017-08-08,visits:48,revenue:0.0
    name:HU,date:2017-08-08,visits:44,revenue:0.0
    name:LK,date:2017-08-08,visits:29,revenue:0.0
    name:MK,date:2017-08-08,visits:2,revenue:0.0
    name:DK,date:2017-08-08,visits:14,revenue:0.0
    name:OM,date:2017-08-08,visits:11,revenue:0.0
    name:AE,date:2017-08-08,visits:11,revenue:0.0
    name:GP,date:2017-08-08,visits:1,revenue:0.0
    name:IE,date:2017-08-08,visits:46,revenue:0.0
    name:CH,date:2017-08-08,visits:22,revenue:0.0
    name:QA,date:2017-08-08,visits:41,revenue:0.0
    name:GR,date:2017-08-08,visits:35,revenue:0.0
    name:ZA,date:2017-08-08,visits:27,revenue:0.0
    name:SA,date:2017-08-08,visits:54,revenue:0.0
    name:HR,date:2017-08-08,visits:16,revenue:0.0
    name:LV,date:2017-08-08,visits:7,revenue:0.0
    name:CD,date:2017-08-08,visits:2,revenue:0.0
    name:GF,date:2017-08-08,visits:2,revenue:0.0
    name:KW,date:2017-08-08,visits:9,revenue:0.0
    name:IN,date:2017-08-08,visits:3,revenue:0.0
    name:EE,date:2017-08-08,visits:2,revenue:0.0
    name:PA,date:2017-08-08,visits:1,revenue:0.0
    name:NG,date:2017-08-08,visits:1,revenue:0.0
    name:PY,date:2017-08-08,visits:1,revenue:0.0
    name:NO,date:2017-08-08,visits:1,revenue:0.0
    name:GT,date:2017-08-08,visits:5,revenue:0.0
    name:MA,date:2017-08-08,visits:9,revenue:0.0
    name:MD,date:2017-08-08,visits:1,revenue:0.0
    name:BY,date:2017-08-08,visits:5,revenue:0.0
    name:KE,date:2017-08-08,visits:4,revenue:0.0
    name:JO,date:2017-08-08,visits:5,revenue:0.0
    name:MQ,date:2017-08-08,visits:3,revenue:0.0
    """






