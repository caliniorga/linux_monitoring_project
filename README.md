This work is intended to be an anomaly detection project applied to a large volume of data, using the 
Python programming language. In this case, the detection algorithm is applied to a dataset collected 
during a calendar month, more precisely January 26 – March 24, which contains performance metrics of 
a Linux system. The objectives of the anomaly include:

  • Very high metric values, which may indicate over utilization of CPU, memory etc.
  
  • Significant increases in metric values in a very short time which may indicate as well over 
utilization of CPU, memory, etc.

  • Constant values over long time intervals or very low values that could represent system crashes 
or freezes.

It is important to define a method of approximating what could be an abnormality in the volume data 
because it is unknown what the database tables under investigation define as an anomaly. This issue is 
categorized as unsupervised from the standpoint of machine learning


The following brief descriptions can be made:

• PostgreSQL database - represents the database where the data to be used for defining the machine 
learning model are stored and extracted.

• dbconnector.py – this module manages the database connection, including functions for 
connecting and disconnecting to and from the database, as well for executing SQL queries needed 
to access and manipulate data.

• feature_extractor.py – this module is responsible for extracting relevant features from the 
collected data, transforming the raw data into feature sets to be used in the anomaly detection 
algorithm.

• train.py – handles the training of anomaly detection models, including all other modules above, 
optimizing hyperparameters to ensure high performance.

• notification.py – manages the notification system, sending alerts and email notifications in case 
of anomaly detection.

• deploy.py – is the module that combines all the other modules to bring the whole infrastructure 
to life.
