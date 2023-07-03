import xml.etree.ElementTree as ET
from datetime import datetime
import argparse
import traceback

argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument(
    '--input',
    dest='input',
    required=True,
    type=str,
    help='Input file in GPX xml-format',
)
argparser.add_argument(
    '--output',
    dest='output',
    required=True,
    type=str,
    help='Output file in Nemea.GPS format',
)

def convert_lat(lat):
    """
    >>> convert_lat('60.157365901399999')
    '6009.44'
    """
    deg_1, deg_2 = lat.split('.')
    return deg_1 + str(round(float("0." + deg_2) * 60, 2)).zfill(5)

def convert_lon(lon):
    """
    >>> convert_lon('24.780305307399999')
    '02446.82'
    """
    deg_1, deg_2 = lon.split('.')
    return deg_1.zfill(3) + str(round(float("0." + deg_2) * 60, 2))

def convert_time(time_str):
    """
    >>> convert_time("2023-05-16T15:41:11Z")
    '154111'
    """
    datetime_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
    return datetime_obj.strftime("%H%M%S")

def create_nemea_line(t, lat, lon):
    """
    >>> len(create_nemea_line('154111', '6009.44', '02446.82'))
    110
    """
    lines = [
        f'$GPGGA,{t},{lat},N,{lon},E,2,6,001.0,034.3,M,-032.3,M,001,0400',
        '$GPVTG,000.0,T,,,000.6,N,001.1,K',
        'res=2\n'
    ]
    return '\n'.join(lines)

def convert_file(file_name):
    root = ET.parse(file_name)
    namespace = {'default': 'http://www.topografix.com/GPX/1/1'}
    result_str = ''
    for trkpt in root.findall('.//default:trkpt', namespace):
        lat = trkpt.get('lat')
        lon = trkpt.get('lon')
        time = trkpt.find('default:time', namespace).text
        print(f'Latitude: {lat}, Longitude: {lon}, Time: {time}')

        c_lat = convert_lat(lat)
        c_lon = convert_lon(lon)
        c_time = convert_time(time)
        print(f'Converted: {c_lat}, Longitude: {c_lon}, Time: {c_time}')
        result_str += create_nemea_line(c_time, c_lat, c_lon)

    result_str += '$GPVTG,000.0,T,,,000.6,N,001.1,K\n'
    return result_str

def write_output(file_name, result_str):
    with open(file_name, 'w+') as file:
        file.write(result_str)


if __name__ == "__main__":
    try:
        print("Starting script")
        args = argparser.parse_args()
        result_str = convert_file(args.input)
        write_output(args.output, result_str)
        print("Data has been converted.")
    except Exception:
        print(traceback.format_exc())

