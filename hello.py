from flask import Flask
import requests
import json
import prettytable
app = Flask(__name__)

@app.route('/')
def index():
  return 'You\'ve hit the api for michaeldisabatino.tech'

@app.route('/hotspots')
def get_hotspots():
  return 'Florida, Texas, Arizona'

@app.route('/safetyRating/county/<fips>')
def get_safety_rating(fips):
  return 'Getting the safety rating for county with fips {}'.format(fips)

@app.route('/bls/stats')
def get_bls_stats():
  headers = {'Content-type': 'application/json'}
  with open('state_area_codes.txt', 'r') as f:
    codes = [line.strip().split()[0] for line in f]
  

  data = json.dumps({"seriesid": ['CUUR0000SA0','SUUR0000SA0'],"startyear":"2011", "endyear":"2014"})
  p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
  json_data = json.loads(p.text)
  for series in json_data['Results']['series']:
      x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
      seriesId = series['seriesID']
      for item in series['data']:
          year = item['year']
          period = item['period']
          value = item['value']
          footnotes=""
          for footnote in item['footnotes']:
              if footnote:
                  footnotes = footnotes + footnote['text'] + ','
          if 'M01' <= period <= 'M12':
              x.add_row([seriesId,year,period,value,footnotes[0:-1]])
      output = open(seriesId + '.txt','w')
      output.write (x.get_string())
      output.close()
  return "Finished getting data {}".format(', '.join(codes))