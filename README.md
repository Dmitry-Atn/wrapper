# flask_wrapper_task


Wrap a neural network model with Flask  
what you will do?
- get an image as an input
- run a neural network on it
- return the results
- wrap the app with docker with all relevant environment variables
  the production start script should be named "serve"
- except a /predict API call, add also /health API
- eventually we want to call `docker run -p 8080:8080 image_name serve` and it will run the server

Things to take into consideration:
 - logging
 - virtualenv
 - error codes on failure
 - tests
 - project folder structure
 - use python3.6
