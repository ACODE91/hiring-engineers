## Questions

Please provide screenshots and code snippets for all steps.

## Prerequisites - Setup the environment

I have used a Ubuntu v 16.04 on a vagrant VM as suggested in the README.

### Installing the Datadog Agent

1. Go to https://app.datadoghq.com/signup and fill the form

<img src="/img/SignUp.png" width="40%">

2. Informing about your stack is optional

<img src="/img/Stack.png" width="50%">

3. Inform your OS (Ubuntu) and copy the agent installation command

<img src="/img/Command.png" width="75%">

4. Paste the command in the shell and wait for the agent to inform back. We're ready to go!

<img src="/img/Running.png" width="75%">

## Collecting Metrics:

* Add tags in the Agent config file and show us a screenshot of your host and its tags on the Host Map page in Datadog.

  1. On your server navigate to `/etc/datadog-agent`

          cd /etc/datadog-agent

  2. Edit the `datadog.yaml` file to include the following line: "tags: purpose:hiring, role:solutionsengineer, location:spain"
  
          sudo vi datadog.yaml

<img src="/img/ConfigTags.png" width="45%">   
   
  3. Restart the datadog agent
  
          sudo service datadog-agent restart
      
  4. The host is now showing the defined tags
    
<img src="/img/HostWithTags.png" width="100%">
    
* Install a database on your machine (MongoDB, MySQL, or PostgreSQL) and then install the respective Datadog integration for that database.

  1. I have choosen to install MongoDB. Full step by step guide on [MongoDB Installation Guide](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
    
  2. The MongoDB integration is installed by default with the 6.x version of the agent. The only required configuration is to create a mongo.yaml file on `/etc/datadog-agent/conf.d/mongo.d/`

          cd /etc/datadog-agent/conf.d/mongo.d
          sudo vi mongo.yaml
  
    1. I have used the simplest possible version of the MongoDB yaml file.

<img src="/img/MongoYAML.png" width="30%">
    
   3. We need to change the file owner to dd-agent and then restart the agent.
    
     sudo chown dd-agent:dd-agent mongo.yaml
     sudo service datadog-agent restart
    
   4. In the agent status we can verify that the MongoDB integration is working
    
    sudo datadog-agent status
    
<img src="/img/MongoStatus.png" width="40%">
    
  5. In Datadog we navigate to Integration and activate the MongoDB Integration. First, selecting it from the list and then clicking on the **Install Integration** button

<img src="/img/Integrations.png" width="40%">

<img src="/img/MongoIntegration.png" width="80%">

  6. And we see some interesting metrics from the MongoDB Dashboard (available from the host, clicking on the _mongodb_ tag)
  
<img src="/img/MongoDashboard.png" width="100%">
    
* Create a custom Agent check that submits a metric named my_metric with a random value between 0 and 1000.

 1. Following instructions from [Datadog Documentation](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6) it's fairly straight forward to create the custom agent check.
    1. Create a file called `ruben.yaml` on the `/etc/datadog-agent/conf.d/` folder with the following code:
    
      instances: [{}]
    
    2. Create a file named `ruben.py` on the `/etc/datadog-agent/checks.d/` folder with the following code
    
            from datadog_checks.checks import AgentCheck
            from random import uniform
            __version__ = "1.0.0"
            class Ruben(AgentCheck):
              def check(self, instance):
                self.gauge('custom.ruben', uniform(0, 1000))
   3. We can verify that the check is correct using the agent's commands: `sudo datadog-agent check ruben`
    
<img src="/img/CustomCheck.png" width="70%">

   4. And see the gauge graph on Datadog
   
<img src="/img/CustomCheckGraph.png" width="50%">

* Change your check's collection interval so that it only submits the metric once every 45 seconds.

  1. As described in [the Collection Interval section](https://docs.datadoghq.com/developers/write_agent_check/?tab=agentv6#collection-interval), changing the collection interval is done by setting it on the `ruben.yaml`file on `/etc/datadog-agent/conf.d/`
    1. The check config file, `ruben.yaml`, needs to be updated in the following way:

<img src="/img/CheckInterval.png" width="40%">

   2. The check is now sending data every 45 seconds.
   
<img src="/img/CheckIntervalGraph.png" width="70%">
  
* **Bonus Question** Can you change the collection interval without modifying the Python check file you created?

It seems that this question is outdated, as the obvious answer following the documentation) doesn't require to modify the custom check's python file.
Just for the sake of the exercise, I can try to answer the reverse question. How to report every 45 seconds without chaging the config file?.
    
 1. Considering the default reporting inteval is 15 seconds, and the agent will report only if the previous execution of the custom check has finished, a simple answer will be to include a `time.sleep(35)`step just after the `self.gauge('custom.ruben', uniform(0, 1000))`step.
 2. This will inhibit the agent to report in the second and third slots (15 and 30 seconds), but will freed the check code long enough the third slot arrives (45 seconds).

## Visualizing Data:

Utilize the Datadog API to create a Timeboard that contains:

* Your custom metric scoped over your host.
* Any metric from the Integration on your Database with the anomaly function applied.
* Your custom metric with the rollup function applied to sum up all the points for the past hour into one bucket

Please be sure, when submitting your hiring challenge, to include the script that you've used to create this Timeboard.

As described in the [Datadog Documentation](https://docs.datadoghq.com/api/?lang=bash#create-a-timeboard) the first thing required to use the API is to have both and API and an APP Keys.
 1. Keys are created and managed from the Datadog UI. Navigate to Integrations/API:
<img src="/img/APIKeysAccess.png" width="30%">
 2. The API key is already present, but the APP key is not. Create it from the UI by writing a name and clicking the Create Application Key button:
<img src="/img/APIKeyCreation.png" width="100%">
 3. The CURL command to create the required timeboard is the following:
  
	    curl  -X POST -H "Content-type: application/json" \
	    -d '{
		      "graphs" : [{
		  "title": "My Custom Check",
		  "definition": {
		    "viz": "timeseries",
		    "requests": [{"q": "avg:custom.ruben{host:ubuntu-xenial}"}] 
		    }  	
		  },
		  {
		  "title": "WT Dirty Bytes (Anomalies)",
		  "definition": {
		    "viz": "timeseries",
		    "requests": [{"q":"anomalies(avg:mongodb.wiredtiger.cache.tracked_dirty_bytes_in_cache{server:mongodb://localhost:27017/admin}, \u0027basic\u0027, 2)"}] 
		    }
		  },
		  {
		  "title": "My Custom Check (1h Buckets)",
		  "definition": {
		    "viz": "timeseries",
		    "type":"bars",
		    "requests": [{"q": "avg:custom.ruben{host:ubuntu-xenial}.rollup(sum,3600)"}] 
		    }
		  }],
	      "title" : "My Custom Timeboard",
	      "description" : "Basic timeboard over my custom check and some MongoDB variables",
	      "read_only": "True"
	    }' \
	    "https://api.datadoghq.com/api/v1/dash?api_key=edb197c52****************47&application_key=f11497***************f6df5c"`

  4. There are a few parts of the call that are not evident:
   
   1. `"graphs" : [{` This is an array. Include as many sub documents as required, in our case, 3.
   2. `"requests": [{"q": "avg:custom.ruben{host:ubuntu-xenial}"}]` Between curly braces the tags that will be used for filtering
   3. `\u0027basic\u0027` The parameter of the anomalies function needs to be between single quotes. Theey need to be escaped using their unicode representation.
   4. `"type":"bars"` Bars are a better representaion for this type of graph.

Once this is created, access the Dashboard from your Dashboard List in the UI:

<img src="/img/Timeboard.png" width="100%">

* Set the Timeboard's timeframe to the past 5 minutes
  1. Click and drag on the graph to set the timeframe
  
<img src="/img/Timeboard5m.png" width="100%">

* Take a snapshot of this graph and use the @ notation to send it to yourself.
  1. Using the small _camera_ icon on any graph the annotations windows appears.
  2. Putting the _@_ simbol will show a list of recipients on the organisation. In this example, only one:
  
<img src="/img/Annotation.png" width="30%">

 3. After a few seconds an email with the notification is received (if checked on My Settings/Preferences )

<img src="/img/AnnotationMail.png" width="90%">
 
* **Bonus Question**: What is the Anomaly graph displaying?

The anomaly graph is showing the temporal serie together with a gray band, highlighting the points of the serie out of the band. As described, the _deviation_ parameter controls the width of the band.
There are three different algorithms to determine the range of acceptable values. The simplest one (basic) only takes in account the distribution of the data present in the graph, while the most advanced ones (agile and robust) consider historical data and factors in temporal patterns of the data.

## Monitoring Data

Since you’ve already caught your test metric going above 800 once, you don’t want to have to continually watch this dashboard to be alerted when it goes above 800 again. So let’s make life easier by creating a monitor.

Create a new Metric Monitor that watches the average of your custom metric (my_metric) and will alert if it’s above the following values over the past 5 minutes:

* Warning threshold of 500
* Alerting threshold of 800
* And also ensure that it will notify you if there is No Data for this query over the past 10m.

 1. Navigate to _Monitors/New Monitor_ in the UI

<img src="/img/NewMonitor.png" width="30%">

 2. Select the Monitor type to _Metric_

<img src="/img/MonitorType.png" width="60%">

 3. Configure the Monitor as described. It's needed select MultiAlert and include `host` in the list of variables to be able to notify as required in the next step.

<img src="/img/Monitor.png" width="80%">

Please configure the monitor’s message so that it will:

* Send you an email whenever the monitor triggers.
* Create different messages based on whether the monitor is in an Alert, Warning, or No Data state.
* Include the metric value that caused the monitor to trigger and host ip when the Monitor triggers an Alert state.

  4. In the __Say What's Happening__ section write your custom message
  
<img src="/img/MonitorNotification.png" width="60%">

Here you have a transcript of the message I have created

		{{#is_warning}} Ok, just a warning. Things can get worse, just saying, but for the moment you're safe.

		The current value is {{value}}, if it gets to {{threshold}} you'll get another notification. {{/is_warning}} {{host.ip}} {{#is_alert}} Booom!

		The {{host.name}} server is facing a crisis.

		The value of the variable is now on {{value}}.

		There's nothing you can do to control a completely random variable, but if you feel the impulse of doing something, SSH to {{host.ip}} and pray in front of your screen.{{/is_alert}}

		{{#is_no_data}} We have not received data for this variable in the last 10 minutes.

		Maybe it's ok, maybe not. You better check the host status on this dashboard:

		https://app.datadoghq.com/dash/integration/system_overview?tpl_var_scope=host:{{host.name}}

		Have a nice day!{{/is_no_data}}

		@elterce@gmail.com

  5. The last line also sets the __Notify Your Team__ section

* When this monitor sends you an email notification, take a screenshot of the email that it sends you.

<img src="/img/MonitorEmail.png" width="80%">

* **Bonus Question**: Since this monitor is going to alert pretty often, you don’t want to be alerted when you are out of the office. Set up two scheduled downtimes for this monitor:

  * One that silences it from 7pm to 9am daily on M-F,
  * And one that silences it all day on Sat-Sun.
  * Make sure that your email is notified when you schedule the downtime and take a screenshot of that notification.
   1. Navigate to _Notifications/Manage Downtime_ in the UI

<img src="/img/ManageDowntime.png" width="30%">

   2. Click on the yellow __Schedule Downtime__ button on the top right of the screen.
   3. Fill the required data on screen.
   	1. In this step we're setting the weekday downtime
   
<img src="/img/Downtime1.png" width="60%">

<img src="/img/Downtime1Email.png" width="60%"> 
   
   4. Repeat step 2 and 3 to fill the weekend downtime.
   	1. Note that we're only silencing notifications out of the bonds of the already created downtime
	
<img src="/img/Downtime2.png" width="60%">

<img src="/img/Downtime2Email.png" width="60%">
	
## Collecting APM Data:

Given the following Flask app (or any Python/Ruby/Go app of your choice) instrument this using Datadog’s APM solution:

```python
from flask import Flask
import logging
import sys

# Have flask use stdout as the logger
main_logger = logging.getLogger()
main_logger.setLevel(logging.DEBUG)
c = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c.setFormatter(formatter)
main_logger.addHandler(c)

app = Flask(__name__)

@app.route('/')
def api_entry():
    return 'Entrypoint to the Application'

@app.route('/api/apm')
def apm_endpoint():
    return 'Getting APM Started'

@app.route('/api/trace')
def trace_endpoint():
    return 'Posting Traces'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050')
```

* **Note**: Using both ddtrace-run and manually inserting the Middleware has been known to cause issues. Please only use one or the other.

 0. Install Dependencies. [Flask](http://flask.pocoo.org/docs/1.0/installation/#install-create-env) and ddtrace
 	1. Create a folder for the application
	
		mkdir my_app
		cd my_app		
	2. Define a Python virtual environment. This helps with dependencies when several Python projects share the same server.
	
		sudo apt-get install python-virtualenv
		virtualenv venv
	3. Run the venv:
	
		. venv/bin/activate
	4. Install `Flask`by running the following command on the venv shell:
 
 		pip install Flask
	5. Create the `my_app.py`file with the provided code.
	6. Install `ddtrace`, the Datadog tracing agent for Python. 
	
		pip install ddtrace
	
 1. Simple Solution
 	1. Datadog offers a a very straight forward way to trace Python applications. There is little control over the traces but provide basic instrumentation.
	2. Run the app using the `ddtrace run` wrapper. Define the `FLASK_APP` variable with your app filename. Set a port different from 5000 (already in use by the datadog agent, an unfortunately, the port by default in Flask)
	
		FLASK_APP=my_app.py DATADOG_ENV=APM_TEST ddtrace-run flask run --port 5050
		
	4. By calling some of the endpoints of the Service we generate traffic and traces that are sent to Datadog:
	
<img src="/img/AppRequests.png" width="60%">

<img src="/img/APMService.png" width="90%">
	5. Cliking on the Service provides a detailed view of the different calls to the resources and the response time fo each:
	
<img src="/img/APMTraces.png" width="100%">
	6. To generate a more interesting graphs you can use a shell script like [this example](/code/load.sh)

 2. Advance Solution
  1. It's possible to instrument the application in a much more detailed way adding decorators in the code itself. That method provides the ability to create a more granular tracing experience and customize the metadata.
  2. Modify the `my_app.py` file to include the following decorators:
	1. A resource name for each one of the resources ["Home", APM, "Traces"]
	2. Some extra metadata and a different service name on the APM resource
	3. Custom metadata and a subservice span on the "Home" resource.
  3. This [custom code](/code/my_app.py) provides an example of the updated function. Execute the file susing the following sentence to setup the service name to `rubensflaskapp`:
  
  		FLASK_APP=my_app.py DATADOG_ENV=APM_TEST DATADOG_SERVICE_NAME=RubensFlaskApp ddtrace-run flask run --port 5050
  
  4. The traces are much more rich now:
  
<img src="/img/APMTraces2.png" width="100%">

  5. And the Flame graph provides a detailes layer over layer information of the different stages for the call

<img src="/img/APMTraces2.png" width="100%"> 

You can access the [Dashboard](https://p.datadoghq.com/sb/af58179f4-d7b4e2b7492026ffb067565117e24883) directly

* **Bonus Question**: What is the difference between a Service and a Resource?

A "Service" is the name of a set of processes that work together to provide a feature set. A service is typically associated with an applciation that provides one or more pieces of functionality called resources.
A "Resource" is a particular call to one of the service functionalities.

## Final Question:

Datadog has been used in a lot of creative ways in the past. We’ve written some blog posts about using Datadog to monitor the NYC Subway System, Pokemon Go, and even office restroom availability!

Is there anything creative you would use Datadog for?

 * A monitoring system is a powerful tool to control with limited resources a large set of servers, processes and tools. The alerting system allows administrators to receive promt notification of metrics going out of usual ranges, and even to include custom instructions to investigate further ot correct the root cause of the problem.
 
In this point I'm seeing a potential new use case for Datadog. The ability to perform corrective actions automatically, releasing administrators of the tedious and repetitive workload.

In example: If the used space of a server disk is higher than 90%, the usual corrective action (specially in with shared storage on VM or in cloud environments) is to provide more storage until the used space goes down to 70%. This is a fairly trivial and repetitive task that could be automated.

In order to do that, the dd-agent should have higher privileges so it can execute the scripts. The corrective scripts will be stored, centralised, in datadog, and the agents will retrieve them when they connect to report new metrics if an alert has been fired. This makes easier the maintenace of the scrips and solves the problem of getting the agents notified (no inboud traffic required).
