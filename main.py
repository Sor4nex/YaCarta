import pygame
import requests
import sys
import os
import math


LAT_STEP = 0.008
LON_STEP = 0.002
coord_to_geo_x = 0.0000428
coord_to_geo_y = 0.0000428


def ll(x, y):
    return "{0},{1}".format(x, y)


class SearchResult(object):
    def __init__(self, point, address, postal_code=None):
        self.point = point
        self.address = address
        self.postal_code = postal_code

class MapParams(object):
    def __init__(self):
        self.lat = 55.729738
        self.lon = 37.664777
        self.zoom = 15
        self.type = "map"

        self.search_result = None
        self.use_postal_code = False


    def ll(self):
        return ll(self.lon, self.lat)

    
    def update(self, event):
        if event.key == pygame.K_PAGEUP  and self.zoom < 19:
            self.zoom += 1
        elif event.key == pygame.K_PAGEDOWN  and self.zoom > 2:
            self.zoom -= 1
        elif event.key == pygame.K_LEFT:
            self.lon -= LON_STEP * math.pow(2, 15 - self.zoom)
        elif event.key == pygame.K_RIGHT:
            self.lon += LON_STEP * math.pow(2, 15 - self.zoom)
        elif event.key == pygame.K_UP and self.lat < 85:
            self.lat += LAT_STEP * math.pow(2, 15 - self.zoom)
        elif event.key == pygame.K_DOWN and self.lat > -85:
            self.lat -= LAT_STEP * math.pow(2, 15 - self.zoom)
        elif event.key == pygame.K_1:
            self.type = "map"
        elif event.key == pygame.K_2:
            self.type = "sat"
        elif event.key == pygame.K_3:
            self.type = "sat,skl"
        elif event.key == pygame.K_DELETE:
            self.search_result = None
        elif event.key == pygame.K_INSERT:
            self.use_postal_code = not self.use_postal_code
        if self.lon > 180: self.lon -= 360
        if self.lon < -180: self.lon += 360
    def screen_to_geo(self, pos):
        dy = 225 - pos[1]
        dx = pos[0] - 300
        lx = self.lon + dx * coord_to_geo_x * math.pow(2, 15 - self.zoom)
        ly = self.lat + dy * coord_to_geo_y * math.cos(math.radians(self.lat)) * math.pow(2, 15 - self.zoom)
        return lx, ly
    def add_reverse_toponym_search(self, pos):
        point = self.screen_to_geo(pos)
        toponym = reverse_geocode(ll(point[0], point[1]))
        self.search_result = SearchResult(
            point,
            toponym["metaDataProperty"]["GeocoderMetaData"]["text"] if toponym else None,
            toponym["metaDataProperty"]["GeocoderMetaData"]["Address"].get(
                "postal_code") if toponym else None)
    def add_reverse_org_search(self, pos):
        self.search_result = None
        point = self.screen_to_geo(pos)
        org = find_business(ll(point[0], point[1]))
        if not org:
            return
        org_point = org["geometry"]["coordinates"]
        org_lon = float(org_point[0])
        org_lat = float(org_point[1])
        if lonlat_distance((org_lon, org_lat), point) <= 50:
            self.search_result = SearchResult(point, org["properties"]["CompanyMetaData"]["name"])


def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.zoom, type=mp.type)
    if mp.search_result:
        map_request += "&pt={0},{1},pm2grm".format(mp.search_result.point[0], mp.search_result.point[1])
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

    return map_file


def render_text(text):
    font = pygame.font.Font(None, 30)
    return font.render(text, 1, (100, 0, 100))


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mp = MapParams()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYUP:
            mp.update(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mp.add_reverse_toponym_search(event.pos)
            elif event.button == 3:
                mp.add_reverse_org_search(event.pos)
        else:
            continue
        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        if mp.search_result:
            if mp.use_postal_code and mp.search_result.postal_code:
                text = render_text(mp.search_result.postal_code + ", " + mp.search_result.address)
            else:
                text = render_text(mp.search_result.address)
            screen.blit(text, (20, 400))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)

def find_business(ll):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        "apikey": api_key,
        "lang": "ru_RU",
        "ll": ll,
        "spn": "0.001,0.001",
        "type": "biz",
        "text": ll,
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
                request=search_api_server, status=response.status_code, reason=response.reason))
    json_response = response.json()
    organizations = json_response["features"]
    return organizations[0] if organizations else None

def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return distance

def reverse_geocode(ll):
    geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={ll}&format=json"
    geocoder_request = geocoder_request_template.format(**locals())
    response = requests.get(geocoder_request)

    if not response:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
                request=geocoder_request, status=response.status_code, reason=response.reason))
    json_response = response.json()
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


if __name__ == "__main__":
    main()
