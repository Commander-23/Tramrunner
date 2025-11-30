import requests

dvb_kuerzel_content_link = "http://efa.vvo-online.de:8080/std3/trias"

def get_dvb_kuerzel(url):
    try:
        response = requests.get(url) 
        if response.status_code == 200:
            return requests.get(url).text
        else:
            raise requests.HTTPError('HTTP Status: {}'.format(response.status_code))    
    except requests.RequestException as e:
        print(f"Failed to access DVB stop information. Request Exception", e)
        response = None

if __name__ == "__main__":
      
    output = get_dvb_kuerzel(dvb_kuerzel_content_link)

    print(output)