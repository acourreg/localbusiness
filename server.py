from flask import Flask
from flask import request
from pyspark.sql import SparkSession

app = Flask(__name__)
spark = SparkSession.builder.appName('localbusiness').getOrCreate()

company_table = spark.read.parquet('./output/company_table')
eco_table = spark.read.parquet('./output/eco_table')
sector_table = spark.read.parquet('./output/sector_table')
state_table = spark.read.parquet('./output/state_table').distinct()

@app.route('/')
def entry_point():

	currentStateId = request.args.get('state', default = 'US', type = str)
	currentSectorId = request.args.get('sector', default = 21, type = int)

	# Building Sector options
	sectorOptions = ''
	for index, sectorrow in sector_table.limit(20).collect():
		sectorOptions += '<option value="'+index+'">'+sectorrow+'</option>'

	stateOptions = ''
	for staterow in state_table.sort('population', ascending=False).limit(20).collect():
		stateOptions += '<option value="'+staterow['id']+'">'+staterow['name']+'</option>'

	# Requests
	state = state_table.where(state_table.id == currentStateId).first()
	sector = sector_table.where(sector_table.naics == currentSectorId).first()
	economics = eco_table.where(eco_table.naics == currentSectorId).where(eco_table.state_id == currentStateId).first()

	print(economics)

	return '''
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap-theme.min.css" integrity="sha384-6pzBo3FDv/PJ8r2KRkGHifhEocL+1X2rVCTTkUfGk7/0pbek5mMa1upzvWbrUbOZ" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>

<body class="p-3 mb-2 bg-primary text-white">
	<div class="container features bg-dark">
	  <div class="row">
	    <div class="col-lg-12 col-md-12 col-sm-12">
	      <h1 class="feature-title">Local businesses in United States</h1>
	      <p>
	      The purpose of this project is to gather small and mid size businesses data, along with population metrics in united states.
	      It can help entrepreneurs to explore some business opportunities in the town and sector they like, thanks to some metrics. 
	      <br><br>
	      A request builder is provided below <b>(limit 100 results)</b>. Source data have been removed to avoid any license issue,
	      but credits are included in Readme.
	      <hr><br><br>
			
			<form action='' method='GET'>
	      <div class="form-group">
		      <select class="form-control" onchange='this.form.submit()' name='state'>
		      '''+stateOptions+'''
		      </select>
		    </div>

		    <div class="form-group">
		      <select class="form-control" onchange='this.form.submit()' name='sector'>
		      '''+sectorOptions+'''
		      </select>
		    </div>
		    </form>

		    <hr>

		    <h2>Economic data for '''+sector[0]['name']+''' in '''+state[0]['name']+'''</h2>
		    <span class="badge badge-primary">Population: '''+state.population+'''</span>
			<span class="badge badge-secondary">Employees in this sector: (request not working for unknown reason)</span>

		    <h2>Example of company in this area</h2>
		    / (Not yet implemented)
	      </p>  
	    </div>
	  </div> 
	</div>
</body>
    '''


if __name__ == '__main__':
    app.run(debug=True)